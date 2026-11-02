"""Reproducible, deliberately bounded mathematics proof pipeline.

Run from this directory: python pipeline.py --bank ../proofs_derivations_core_json/mathematics_core.json
The formalizations file contains problem inputs, never solution sequences.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import time
from collections import Counter
from pathlib import Path

import sympy as s

from automatic_trig_solver import A, C, S, denominator_factors, domain_safe, exact_equal, solve
from newclid_probe import FIGURE_ID, JGEX_INPUT, QUESTION_ID, main as run_newclid_probe

HERE = Path(__file__).resolve().parent
X = s.Symbol("x", real=True)
FUNCTIONS = {"sin": s.sin, "cos": s.cos, "tan": s.tan,
             "cot": s.cot, "sec": s.sec, "csc": s.csc}
SYMBOLS = {"A": A, "x": X}
STATUSES = {"SOLVED_AND_TRACE_CHECKED", "COUNTEREXAMPLE", "INCONCLUSIVE",
            "UNSUPPORTED", "INPUT_AMBIGUOUS", "SOURCE_NEEDS_CORRECTION"}


def parse_math(source: str) -> s.Expr:
    """Parse a small arithmetic grammar; never call sympify on bank text."""
    def walk(node: ast.AST) -> s.Expr:
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return s.Integer(node.value)
        if isinstance(node, ast.Name) and node.id in SYMBOLS:
            return SYMBOLS[node.id]
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in FUNCTIONS and len(node.args) == 1 and not node.keywords:
                return FUNCTIONS[node.func.id](walk(node.args[0]))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -walk(node.operand)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.UAdd):
            return walk(node.operand)
        if isinstance(node, ast.BinOp):
            left, right = walk(node.left), walk(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                return left / right
            if isinstance(node.op, ast.Pow) and right.is_Integer and abs(right) <= 8:
                return left ** right
        raise ValueError(f"Unsupported expression syntax: {ast.dump(node)}")

    return walk(ast.parse(source, mode="eval").body)


def source_domain_factors(source: str) -> tuple[s.Expr, ...]:
    """Collect original poles from syntax before SymPy can cancel them."""
    found = set()
    tree = ast.parse(source, mode="eval")
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in ("tan", "sec"):
                found.add(C)
            elif node.func.id in ("cot", "csc"):
                found.add(S)
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            base = parse_math(ast.unparse(node.right))
            found.update(denominator_factors(s.Pow(base, -1, evaluate=False)))
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Pow):
            exponent = parse_math(ast.unparse(node.right))
            if exponent.is_Integer and exponent < 0:
                base = parse_math(ast.unparse(node.left))
                found.update(denominator_factors(s.Pow(base, exponent, evaluate=False)))
    return tuple(sorted(found, key=str))


def trace_step(before: s.Expr | str, after: s.Expr | str, rule: str,
               reason: str, *, relation: str = "equality", premises: list[str] | None = None,
               conditions: list[str] | None = None, origin: str = "code_search",
               verified: bool = False, checker: str = "exact_sympy_rule_replay") -> dict:
    def show(value: s.Expr | str) -> str:
        return str(value)
    return {"input": show(before), "output": show(after), "rule_id": rule,
            "supporting_premises": premises or [], "relation": relation,
            "required_assumptions": conditions or [],
            "verification": {"passed": bool(verified), "checker": checker},
            "origin": origin, "reason": reason,
            "input_latex": s.latex(before) if isinstance(before, s.Basic) else None,
            "output_latex": s.latex(after) if isinstance(after, s.Basic) else None}


def common_fields(q: dict) -> dict:
    return {"id": q["id"], "topic": q["topic"], "class": q["class"],
            "task_kind": q["task_kind"],
            "question_text_original": q["question_text_original"],
            "question_text_cleaned": q["question_text_cleaned"],
            "stated_assumptions": q["stated_assumptions"],
            "inferred_assumptions": q["inferred_assumptions"],
            "proposed_corrections": [],
            "provenance": {"source_question_id": q["source_question_id"],
                           "source_id": q["source"]["source_id"],
                           "paper": q["source"]["paper"],
                           "pdf_pages": q["source"]["pdf_pages"],
                           "board_status": q["board_status"]},
            "figure_required": q["context_requirements"]["given_diagram_required"],
            "trace": [], "method_approval": "draft_unverified",
            "presentation_review": "not_reviewed",
            "formalization_review": "draft_manual_transcription"}


def trig(q: dict, spec: dict) -> dict:
    lhs, rhs = parse_math(spec["lhs"]), parse_math(spec["rhs"])
    original_domain = tuple(sorted(set(source_domain_factors(spec["lhs"]) +
                                       source_domain_factors(spec["rhs"])), key=str))
    discovered = solve(lhs, rhs, seconds=20, extra_domain=original_domain)
    status = {"SOLVED": "SOLVED_AND_TRACE_CHECKED",
              "NOT_VERIFIED": "INCONCLUSIVE"}.get(discovered["status"], discovered["status"])
    result = {**common_fields(q), "status": status, "method": spec["method"],
              "formalized_input": {"lhs": spec["lhs"], "rhs": spec["rhs"],
                                   "normalization_note": spec["input_note"]},
              "domain_conditions": discovered.get("original_domain_factors_nonzero", []),
              "diagnostics": {k: v for k, v in discovered.items() if k not in
                              {"steps", "status", "original_domain_factors_nonzero"}}}
    if status == "SOLVED_AND_TRACE_CHECKED":
        domain = tuple(sorted(set(denominator_factors(lhs) + denominator_factors(rhs) + original_domain), key=str))
        for edge in discovered["steps"]:
            before, after = parse_math(edge["before"]), parse_math(edge["after"])
            # The search engine has already replayed the exact rule on its original
            # SymPy objects. Reparsed strings may lose an unevaluated substitution,
            # so independently check equality and domain on the serialized trace.
            passed = bool(discovered["trace_replayed"] and exact_equal(before, after)
                          and domain_safe(after, domain))
            result["trace"].append(trace_step(before, after, edge["rule"], edge["reason"],
                         premises=["trig identity" if "pythagorean" in edge["rule"] else "original expression"],
                         conditions=[f"{f} != 0" for f in domain], verified=passed))
        if not all(step["verification"]["passed"] for step in result["trace"]):
            result["status"] = "INCONCLUSIVE"
            result["diagnostics"]["reason"] = "Independent trace replay failed."
        result["presentation_review"] = "needs_review_for_algebraic_jumps"
    return result


def factor_theorem(q: dict, spec: dict) -> dict:
    p, factor = parse_math(spec["polynomial"]), parse_math(spec["factor"])
    polynomial, divisor = s.Poly(p, X), s.Poly(factor, X)
    if divisor.degree() != 1 or polynomial.degree() < 1:
        return {**common_fields(q), "status": "UNSUPPORTED", "reason": "Requires a linear proposed factor."}
    root = s.solve(factor, X)[0]
    quotient, remainder = polynomial.div(divisor)
    qexpr = quotient.as_expr()
    factored_q = s.factor(qexpr)
    fully = s.factor(p)
    checks = [s.simplify(p.subs(X, root) - remainder.as_expr()) == 0,
              s.expand(p - factor*qexpr - remainder.as_expr()) == 0,
              s.expand(qexpr - factored_q) == 0,
              s.expand(p - fully) == 0]
    steps = [trace_step(p.subs(X, root), remainder.as_expr(), "factor_theorem_remainder",
                        "Substitute the root of the proposed linear factor.",
                        premises=[f"{factor} = 0 at x = {root}"], origin="method_template", verified=checks[0]),
             trace_step(p, factor*qexpr + remainder.as_expr(), "polynomial_division",
                        "Divide the polynomial by the proposed factor.", origin="method_template", verified=checks[1]),
             trace_step(qexpr, factored_q, "factor_quotient",
                        "Factor the quotient.", origin="method_template", verified=checks[2]),
             trace_step(p, fully, "multiply_back",
                        "Combine the factors and check by expansion.", origin="method_template", verified=checks[3])]
    return {**common_fields(q), "status": "SOLVED_AND_TRACE_CHECKED" if all(checks) and remainder.is_zero else "INCONCLUSIVE",
            "method": spec["method"], "formalized_input": spec,
            "domain_conditions": [], "trace": steps, "diagnostics": {"root": str(root), "remainder": str(remainder.as_expr())},
            "presentation_review": "template_rendered_unreviewed"}


def completing_square(q: dict, spec: dict) -> dict:
    p = parse_math(spec["polynomial"])
    poly = s.Poly(p, X)
    if poly.degree() != 2 or poly.LC() <= 0:
        return {**common_fields(q), "status": "UNSUPPORTED", "reason": "Requires a positive-leading real quadratic."}
    a, b, c = poly.all_coeffs()
    h = -b/(2*a)
    k = s.simplify(c - b*b/(4*a))
    square = a*(X-h)**2+k
    equal = s.expand(p-square) == 0
    positive = bool(a > 0 and k > 0)
    steps = [trace_step(p, square, "complete_square", "Complete the square.",
                        conditions=["x is real"], origin="method_template", verified=equal),
             trace_step(str(square), f">= {k} > 0 for every real x", "square_nonnegative",
                        "A real square is nonnegative; the constant is positive.",
                        relation="implication", conditions=["x is real"], origin="method_template", verified=positive)]
    return {**common_fields(q), "status": "SOLVED_AND_TRACE_CHECKED" if equal and positive else "INCONCLUSIVE",
            "method": spec["method"], "formalized_input": spec,
            "domain_conditions": ["x is real"], "trace": steps,
            "diagnostics": {"leading_coefficient": str(a), "minimum": str(k)},
            "presentation_review": "template_rendered_unreviewed"}


def ap_term_relation(q: dict, spec: dict) -> dict:
    a, d = s.symbols("a d", real=True)
    zero_index = int(spec["zero_term_index"])
    target_index = int(spec["target_term_index"])
    compare_index = int(spec["comparison_term_index"])
    multiplier = s.Integer(spec["multiplier"])
    if min(zero_index, target_index, compare_index) < 1:
        return {**common_fields(q), "status": "INPUT_AMBIGUOUS", "reason": "AP term indices must be positive."}
    term = lambda index: a + (index-1)*d
    a_from_zero = -(zero_index-1)*d
    left = s.expand(term(target_index).subs(a, a_from_zero))
    right = s.expand((multiplier*term(compare_index)).subs(a, a_from_zero))
    checks = [s.simplify(term(zero_index).subs(a, a_from_zero)) == 0,
              s.simplify(term(target_index).subs(a, a_from_zero)-left) == 0,
              s.simplify((multiplier*term(compare_index)).subs(a, a_from_zero)-right) == 0,
              s.simplify(left-right) == 0]
    steps = [trace_step(s.Eq(term(zero_index), 0), s.Eq(a, a_from_zero), "ap_zero_term",
                        "Use the given zero term to find the first term in terms of the common difference.",
                        premises=[f"T_{zero_index}=0", "T_k=a+(k-1)d"], origin="method_template", verified=checks[0]),
             trace_step(term(target_index), left, "ap_term_substitute",
                        "Substitute the first-term relation into the target term.",
                        premises=[f"a={a_from_zero}"], origin="method_template", verified=checks[1]),
             trace_step(multiplier*term(compare_index), right, "ap_term_substitute",
                        "Substitute the same relation into the comparison term.",
                        premises=[f"a={a_from_zero}"], origin="method_template", verified=checks[2]),
             trace_step(left, right, "ap_compare", "Both sides are equal.",
                        premises=["previous two terms"], origin="method_template", verified=checks[3])]
    return {**common_fields(q), "status": "SOLVED_AND_TRACE_CHECKED" if all(checks) else "INCONCLUSIVE",
            "method": spec["method"], "formalized_input": spec, "domain_conditions": ["term indices are positive integers"],
            "trace": steps, "diagnostics": {}, "presentation_review": "template_rendered_unreviewed"}


def ap_sum_relation(q: dict, spec: dict) -> dict:
    n = s.Symbol("n", integer=True, positive=True)
    first = s.Integer(spec["first_term"])
    differences = [s.Integer(value) for value in spec["common_differences"]]
    coefficients = [s.Integer(value) for value in spec["claim_coefficients"]]
    if len(differences) != len(coefficients) or not differences:
        return {**common_fields(q), "status": "INPUT_AMBIGUOUS", "reason": "AP sum lists must have the same nonzero length."}
    formula = lambda difference: n*(2*first+(n-1)*difference)/2
    sums = [formula(difference) for difference in differences]
    combined = s.expand(sum(c*value for c, value in zip(coefficients, sums)))
    checks = [s.simplify(s.summation(first+(s.Symbol("k", integer=True)-1)*diff,
                                      (s.Symbol("k", integer=True), 1, n))-value) == 0
              for diff, value in zip(differences, sums)]
    checks.append(combined == 0)
    steps = [trace_step(f"AP {i}: a={first}, d={diff}", value, "ap_sum_formula",
                        "Use S_n=n[2a+(n-1)d]/2.", premises=["n is a positive integer"],
                        origin="method_template", verified=checks[i-1])
             for i, (diff, value) in enumerate(zip(differences, sums), 1)]
    steps.append(trace_step("claimed linear combination of the sums", combined,
                            "ap_sum_combine", "Substitute the three formulas and simplify.",
                            premises=["previous sum formulas"], origin="method_template", verified=checks[-1]))
    return {**common_fields(q), "status": "SOLVED_AND_TRACE_CHECKED" if all(checks) else "INCONCLUSIVE",
            "method": spec["method"], "formalized_input": spec,
            "domain_conditions": ["n is a positive integer"], "trace": steps,
            "diagnostics": {"claim_coefficients": [int(c) for c in coefficients]},
            "presentation_review": "template_rendered_unreviewed"}


def isosceles_midpoint_geometry(q: dict, spec: dict) -> dict:
    if q["id"] != QUESTION_ID or spec.get("figure_asset_id") != FIGURE_ID or spec.get("jgex_input") != JGEX_INPUT:
        return {**common_fields(q), "status": "INPUT_AMBIGUOUS", "reason": "Geometry input is not the figure-reviewed formulation."}
    probe = run_newclid_probe()  # Fresh engine run; no cached proof can promote the result.
    if not probe["proof_accepted_by_pipeline"]:
        return {**common_fields(q), "status": "UNSUPPORTED", "reason": "Newclid proof or independent symbolic replay did not pass.",
                "diagnostics": {"probe_status": probe["status"]}}
    checks = probe["independent_replay"]["checks"]
    common = {"origin": "newclid_proof_plus_independent_replay", "checker": "exact_symbolic_coordinate_replay"}
    trace = [
        trace_step("S is midpoint of PQ", "PS² = PQ²/4", "midpoint_S",
                   "S lies halfway from P to Q.", premises=["S is midpoint of PQ"],
                   verified=checks["PS_squared_is_PQ_squared_over_4"], **common),
        trace_step("T is midpoint of PR", "PT² = PR²/4", "midpoint_T",
                   "T lies halfway from P to R.", premises=["T is midpoint of PR"],
                   verified=checks["PT_squared_is_PR_squared_over_4"], **common),
        trace_step("RS² - QT²", "3(PR² - PQ²)/4", "midpoint_distance_identity",
                   "Expand both squared distances using the midpoint coordinates.",
                   premises=["S is midpoint of PQ", "T is midpoint of PR"],
                   verified=checks["RS_QT_squared_difference_follows_equal_sides"], **common),
        trace_step("PR = PQ", "RS = QT", "equal_sides_nonnegative_lengths",
                   "Equal original sides make the squared-distance difference zero; both lengths are nonnegative.",
                   premises=["PR = PQ", "RS² - QT² = 3(PR² - PQ²)/4"],
                   verified=bool(probe["solver_goal_checked"] and probe["independent_replay"]["passed"]), **common),
    ]
    return {**common_fields(q), "status": "SOLVED_AND_TRACE_CHECKED" if all(t["verification"]["passed"] for t in trace) else "INCONCLUSIVE",
            "method": spec["method"], "formalized_input": spec, "trace": trace,
            "domain_conditions": ["P, Q, R form the nondegenerate triangle shown in the figure"],
            "diagnostics": {"figure_id": FIGURE_ID, "figure_sha256_verified": probe["figure_sha256_verified"],
                            "newclid_status": probe["status"], "independent_replay": probe["independent_replay"]},
            "presentation_review": "needs_teacher_review"}


def classify_unsolved(q: dict) -> dict:
    result = common_fields(q)
    if q["id"] == "PD-MATH-XII-030":
        result.update(status="SOURCE_NEEDS_CORRECTION", reason="Displayed plane equation needs a x b != 0; otherwise it does not specify a unique plane.",
                      proposed_corrections=["Qualify the conclusion with a x b != 0, or state the degenerate case separately."])
    elif q["id"] == "PD-MATH-XII-036":
        result.update(status="SOURCE_NEEDS_CORRECTION", reason="Printed logarithmic family omits y=0 and real sign branches; completeness is not established.",
                      proposed_corrections=["Include the zero solution and the signed nonzero branches on intervals where sin(2x) has fixed sign."])
    else:
        reason = ("The supplied figure has no verified symbolic geometry encoding or Newclid replay."
                  if result["figure_required"] else
                  "No audited formalization and reusable derivation route is implemented for this question.")
        result.update(status="UNSUPPORTED", reason=reason)
    return result


def render_answer(result: dict) -> str:
    if result["status"] != "SOLVED_AND_TRACE_CHECKED":
        return ""
    lines = [f"## {result['id']}", "", result["question_text_original"], "", "**Solution**", ""]
    method = result["method"]
    if method == "rational_trig_identity":
        side = result["diagnostics"]["starting_side"]
        start_text = result["formalized_input"]["lhs" if side == "LHS" else "rhs"]
        lines += [f"Starting with the {side}:", "", f"$${s.latex(parse_math(start_text))}$$", ""]
        for step in result["trace"]:
            lines += [f"$$= {step['output_latex']}$$", "", step["reason"], ""]
        lines.append("Hence the identity holds wherever both original sides are defined.")
    elif method == "factor_theorem":
        root = result["diagnostics"]["root"]
        root_latex = s.latex(s.Rational(root))
        polynomial_latex = result["trace"][1]["input_latex"]
        substitution_latex = polynomial_latex.replace("x", rf"\left({root_latex}\right)")
        lines += [f"Let $P(x)={polynomial_latex}$. The proposed linear factor is zero at $x={root_latex}$.", "",
                  f"$$P\\left({root_latex}\\right)={substitution_latex}=0$$", "",
                  "By the factor theorem, the proposed factor divides $P(x)$.", ""]
        for step in result["trace"][1:]:
            lines += [step["reason"], "", f"$${step['input_latex']}={step['output_latex']}$$", ""]
        lines.append("The zero remainder confirms the proposed factor; the last line is the complete factorisation.")
    elif method == "ap_term_relation":
        lines += ["Let the first term be $a$ and the common difference be $d$. Then $T_k=a+(k-1)d$.", ""]
        first = result["trace"][0]
        lines += [first["reason"], "", f"$${first['input_latex']}\\implies {first['output_latex']}$$", ""]
        for step in result["trace"][1:-1]:
            lines += [step["reason"], "", f"$${step['input_latex']}={step['output_latex']}$$", ""]
        spec = result["formalized_input"]
        lines.append(f"Thus $T_{{{spec['target_term_index']}}}={result['trace'][1]['output_latex']}={spec['multiplier']}T_{{{spec['comparison_term_index']}}}$.")
    elif method == "ap_sum_relation":
        lines += ["For an AP with first term $a$ and common difference $d$, $S_n=\\frac{n}{2}[2a+(n-1)d]$.", ""]
        for index, step in enumerate(result["trace"][:-1], 1):
            lines += [f"For progression {index}, $S_{index}={step['output_latex']}$.", ""]
        n = s.Symbol("n", integer=True, positive=True)
        spec = result["formalized_input"]
        terms = [s.Mul(s.Integer(c), n*(2*s.Integer(spec["first_term"])+(n-1)*s.Integer(d))/2)
                 for c, d in zip(spec["claim_coefficients"], spec["common_differences"])]
        symbolic = s.Add(*[s.Mul(s.Integer(c), s.Symbol(f"S_{i}"))
                           for i, c in enumerate(spec["claim_coefficients"], 1)], evaluate=False)
        lines += ["Substitute and collect the terms:", "",
                  f"$${s.latex(symbolic, order='none')}={s.latex(s.Add(*terms, evaluate=False), order='none')}=0$$", "",
                  "Hence the sum relation holds for every positive integer $n$."]
    elif method == "isosceles_midpoint_geometry":
        lines += ["Since $S$ and $T$ are midpoints, $PS=\\tfrac12 PQ$ and $PT=\\tfrac12 PR$. The isosceles condition $PQ=PR$ therefore gives $PS=PT$.", "",
                  "Also, $\\angle RPS=\\angle QPT$: both are the angle at $P$ between $PQ$ and $PR$.", "",
                  "Thus $\\triangle PRS\\cong\\triangle PQT$ by SAS, with $PR=PQ$, $PS=PT$, and equal included angles. Corresponding sides give $RS=QT$."]
    else:
        first = result["trace"][0]
        lines += ["Complete the square:", "", f"$${first['input_latex']}={first['output_latex']}$$", "",
                  "Since a square of a real number is nonnegative, this expression is strictly positive.", "",
                  "Therefore the equation has no real root."]
    return "\n".join(lines) + "\n"


def run(bank_path: Path, output_dir: Path) -> dict:
    start = time.monotonic()
    bank_bytes = bank_path.read_bytes()
    bank = json.loads(bank_bytes)
    specs = json.loads((HERE/"formalizations.json").read_text(encoding="utf-8"))
    results = []
    for q in bank["questions"]:
        spec = specs.get(q["id"])
        if not spec:
            result = classify_unsolved(q)
        else:
            try:
                route = {"rational_trig_identity": trig, "factor_theorem": factor_theorem,
                         "completing_square_no_real_root": completing_square,
                         "ap_term_relation": ap_term_relation, "ap_sum_relation": ap_sum_relation,
                         "isosceles_midpoint_geometry": isosceles_midpoint_geometry}[spec["method"]]
                result = route(q, spec)
            except (ValueError, TypeError, KeyError, s.PolynomialError) as exc:
                result = {**common_fields(q), "status": "INPUT_AMBIGUOUS", "reason": f"Formalization failed: {exc}"}
        if result["status"] not in STATUSES:
            raise AssertionError(result["status"])
        results.append(result)
    output_dir.mkdir(parents=True, exist_ok=True)
    counts = Counter(x["status"] for x in results)
    report = {"bank_sha256": hashlib.sha256(bank_bytes).hexdigest(),
              "bank_question_count": len(bank["questions"]),
              "questions_attempted": len(results), "status_counts": dict(counts),
              "automatically_solved": counts["SOLVED_AND_TRACE_CHECKED"],
              "trace_verification_success": sum(all(st["verification"]["passed"] for st in x["trace"])
                                                for x in results if x["status"] == "SOLVED_AND_TRACE_CHECKED"),
              "domain_or_source_issues": [x["id"] for x in results if x["status"] in ("SOURCE_NEEDS_CORRECTION", "INPUT_AMBIGUOUS")],
              "method_approved": 0, "presentation_human_reviewed": 0,
              "complete_answer_accuracy_observed": None,
              "accuracy_uncertainty": "Not estimable: no independent marking or expert-reviewed random sample.",
              "figure_required_questions": sum(x["figure_required"] for x in results),
              "llm_calls": 0, "llm_tokens": 0, "runtime_seconds": round(time.monotonic()-start, 3),
              "sympy_version": s.__version__, "newclid_available": importlib.util.find_spec("newclid") is not None,
              "newclid_available_meaning": "Python module found only; solver execution is checked separately.",
              "newclid_geometry_solved": sum(x["status"] == "SOLVED_AND_TRACE_CHECKED" and
                                             x.get("method") == "isosceles_midpoint_geometry" for x in results),
              "failure_count": sum(x["status"] == "INCONCLUSIVE" for x in results)}
    (output_dir/"per_question_results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir/"metrics.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    answers = "# Rendered sample answers\n\nThese are machine generated and still require presentation review.\n\n"
    answers += "\n".join(render_answer(x) for x in results if x["status"] == "SOLVED_AND_TRACE_CHECKED")
    (output_dir/"sample_answers.md").write_text(answers, encoding="utf-8")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bank", type=Path, default=HERE.parent/"proofs_derivations_core_json"/"mathematics_core.json")
    parser.add_argument("--output", type=Path, default=HERE/"results")
    args = parser.parse_args()
    print(json.dumps(run(args.bank, args.output), indent=2))

"""Step 2: check a spec before solving. This is the defence against a misread question:
a misread claim is usually false, and a false claim is caught here with a counterexample."""
from __future__ import annotations

import sympy as s

from .problem import Problem, build
from .sampling import admissible_points, numerically_equal
from .spec import Spec, hypothesis_kind

VALIDATION = {"VALID", "FALSE_CLAIM", "INCONSISTENT", "AMBIGUOUS"}


def validate(spec: Spec) -> dict:
    try:
        problem = build(spec)
    except (ValueError, KeyError, TypeError) as exc:
        return {"status": "AMBIGUOUS", "reason": f"Spec does not parse: {exc}", "problem": None}
    result = {"status": "VALID", "reason": "", "problem": problem, "english": english(problem),
              "conditions": [str(c) for c in problem.conditions]}
    used = set().union(*(e.free_symbols for e in problem.exprs.values() if isinstance(e, s.Basic)), set())
    for l, r in problem.hypotheses:
        used |= l.free_symbols | r.free_symbols
    declared = {name for name, assumptions in spec.variables.items() if assumptions}
    declared |= {d for function in spec.functions.values() for d in function.get("derivatives", [])}
    vague = sorted(v.name for v in used if v.name not in declared and v not in problem.introduced)
    if vague:
        return {**result, "status": "AMBIGUOUS", "reason": f"No domain declared for {vague}"}
    check = {"prove_identity": _equality, "prove_from_hypotheses": _equality,
             "factor_theorem": _factor, "show_no_real_roots": _no_real_roots}.get(problem.kind)
    if check is None:
        return {**result, "reason": "Not numerically checkable here; the route's own checker is used."}
    return {**result, **check(problem)}


def relation_zeros(problem: Problem) -> list:
    """The givens, plus their derivatives when y is a function of x, so that sampled values of
    y1, y2 are the true derivatives rather than free numbers."""
    zeros = problem.hypothesis_zeros()
    if not problem.ctx.chain:
        return zeros
    from .rules.calculus import total_derivative
    chain = tuple(problem.ctx.chain.items())
    extra = []
    for zero in zeros:
        current = zero
        for _ in range(len(chain)):
            current = total_derivative(current, problem.ctx.variable, chain)
            extra.append(current)
    return zeros + extra


def _equality(problem: Problem) -> dict:
    points = admissible_points(problem.symbols, relation_zeros(problem), problem.conditions, count=16,
                               prefer=problem.solve_order, intervals=problem.intervals)
    if len(points) < 4:
        return {"status": "INCONSISTENT",
                "reason": (f"Found only {len(points)} values satisfying the givens and the domain; "
                           "the givens may be contradictory, or the spec may be misread.")}
    lhs, rhs = (problem.theory.expand_definitions(problem.exprs[k]) for k in ("lhs", "rhs"))
    warnings = []
    complex_symbols = [v for v in problem.symbols if v.is_real is None]
    if complex_symbols and problem.hypotheses:
        real = [s.Symbol(v.name, real=True) for v in complex_symbols]
        swap = dict(zip(complex_symbols, real))
        real_points = admissible_points([swap.get(v, v) for v in problem.symbols],
                                        [h.xreplace(swap) for h in problem.hypothesis_zeros()], [], count=2)
        if not real_points:
            warnings.append("No real values satisfy the givens; the result is proved as an algebraic identity.")
    def at(e, point):  # subs keeps an integral's own variable bound
        return e.subs(point) if e.has(s.Integral) else e.xreplace(point)

    if problem.spec.figure:
        from .figure import check
        ok, reason = check(problem.spec, problem)
        if not ok:
            return {"status": "AMBIGUOUS", "reason": reason}
    for point in points:
        if not numerically_equal(lhs, rhs, [point]):
            return {"status": "FALSE_CLAIM", "reason": "The two sides differ at an admissible point.",
                    "counterexample": {str(k): str(v) for k, v in point.items()} |
                                      {"lhs": str(s.N(at(lhs, point), 15)), "rhs": str(s.N(at(rhs, point), 15))}}
    return {"sample_points_checked": len(points), "warnings": warnings}


def _factor(problem: Problem) -> dict:
    x, p, f = problem.exprs["variable"], problem.exprs["polynomial"], problem.exprs["factor"]
    if s.Poly(f, x).degree() != 1:
        return {"status": "AMBIGUOUS", "reason": "The factor theorem route needs a linear factor."}
    remainder = s.Poly(p, x).rem(s.Poly(f, x)).as_expr()
    if remainder != 0:
        return {"status": "FALSE_CLAIM", "reason": f"Dividing leaves remainder {remainder}."}
    return {}


def _no_real_roots(problem: Problem) -> dict:
    x, p = problem.exprs["variable"], problem.exprs["polynomial"]
    roots = s.Poly(p, x).real_roots()
    if roots:
        return {"status": "FALSE_CLAIM", "reason": f"Real root {roots[0]} exists."}
    return {}


def english(problem: Problem) -> str:
    """Plain-words restatement for comparison with the source question."""
    spec, parts = problem.spec, []
    if spec.points:
        from .figure import words
        parts.append("Points: " + "; ".join(f"{n} = ({x}, {y})" for n, (x, y) in spec.points.items()) + ".")
        if spec.figure:
            parts.append("Figure: " + "; ".join(words(f) for f in spec.figure) + ".")
    if spec.variables:
        parts.append("Variables: " + "; ".join(f"{n} ({', '.join(a)})" for n, a in spec.variables.items()) + ".")
    for name, seq in spec.sequences.items():
        step = f"common difference {seq['difference']}" if seq["type"] == "ap" else f"common ratio {seq['ratio']}"
        parts.append(f"{name} is an {seq['type'].upper()} with first term {seq['first']} and {step}.")
    for h in spec.hypotheses:
        parts.append({
            "equation": lambda: f"Given {h['lhs']} = {h['rhs']}.",
            "in_ap": lambda: f"Given {', '.join(h['terms'])} are in AP.",
            "in_gp": lambda: f"Given {', '.join(h['terms'])} are in GP.",
            "equal_ratios": lambda: "Given " + " = ".join(f"({n})/({d})" for n, d in h["ratios"]) + ".",
            "equal_roots": lambda: f"Given {h['polynomial']} = 0 has equal roots in {h['variable']}.",
        }[hypothesis_kind(h)]())
    goal = spec.goal

    def claim(g: dict) -> str:
        if "in_ap" in g or "in_gp" in g:
            form = "in_ap" if "in_ap" in g else "in_gp"
            return f"{', '.join(g[form])} are in {form[3:].upper()}"
        return f"{g.get('lhs')} = {g.get('rhs')}"

    parts.append({
        "prove_identity": lambda: "Prove " + "; ".join(claim(p) for p in goal.get("parts", [goal])) + ".",
        "prove_from_hypotheses": lambda: "Prove " + "; ".join(claim(p) for p in goal.get("parts", [goal])) + ".",
        "factor_theorem": lambda: f"Show {goal.get('factor')} is a factor of {goal.get('polynomial')}, then factorise it.",
        "show_no_real_roots": lambda: f"Show {goal.get('polynomial')} = 0 has no real solution.",
        "solve_equation": lambda: (f"Solve {goal['lhs']} = {goal['rhs']} for {goal['low']} <= {goal['variable']} "
                                   f"{'<' if goal.get('high_open') else '<='} {goal['high']}."),
        "evaluate": lambda: f"Find {goal.get('name') or 'the value of'} {goal['expr']}.",
        "one_real_roots": lambda: f"Show at least one of {', '.join(p + ' = 0' for p in goal['polynomials'])} has real roots in {goal['variable']}.",
        "only_solution": lambda: f"Show the only real solution of {goal['lhs']} = {goal['rhs']} is {goal['variable']} = {goal['value']}.",
        "general_solution": lambda: f"Find the general solution of {goal['lhs']} = {goal['rhs']} in {goal['variable']}.",
        "first_principles": lambda: f"Find the derivative of {goal['function']} with respect to {goal['variable']} from first principles.",
        "monotonic": lambda: f"Show {goal['function']} is {goal['direction']} in {goal['variable']}.",
        "extremum": lambda: f"Find the {goal['type']}imum of {goal['objective']} over {goal['variable']}.",
        "find_value": lambda: (f"Find {goal['variable']} with {goal['lhs']} = {goal['rhs']}"
                               + (f", {goal['low']} <= {goal['variable']} <= {goal['high']}" if "low" in goal else "") + "."),
        "geometry_jgex": lambda: f"Geometry (JGEX): {goal.get('jgex')}.",
    }[problem.kind]())
    if spec.prescribed_method:
        parts.append(f"Method required: {spec.prescribed_method.replace('_', ' ')}.")
    return " ".join(parts)

"""Step 6: independent verification of a finished trace.

Does not call the search (engine.py imports only the Step record). Each step is checked
by replaying its named rule from the registry and by a mathematical check that suits
its relation:
- equality:    exact (ideal or saturated radical membership) and 50-digit numeric at
               fresh admissible points; every new denominator needs a certificate
- implication: the derived equation follows from the givens (exact and numeric)
- equivalence: both equations have the same difference of sides
- solution:    the value satisfies the original equation and the stated constraints
Then the trace must prove exactly the spec's goal, using only justified substitutions.
"""
from __future__ import annotations

import sympy as s

from .engine import Step
from .equality import Z, _numerator, domain_safe, exact_equal, finish_holds, hypothesis_ideal, in_radical, normal
from .problem import Problem
from .rules import REGISTRY, build
from .sampling import admissible_points, numerically_equal

SEED = 20261112  # independent of the validation sample
PROPERTY_RULES = ("average_with_reflection",)  # rules that quote a property of definite integrals


def _implied(eq: s.Eq, problem: Problem, extra_nonzero: s.Expr = s.Integer(1), theory=None) -> bool:
    theory = theory or problem.theory  # the givens plus the premises already established
    if extra_nonzero == 1:
        return exact_equal(eq.lhs, eq.rhs, theory)
    target = _numerator(normal(theory.expand_definitions(eq.lhs - eq.rhs)))
    return in_radical(target, list(hypothesis_ideal(theory)), s.prod(theory.domain)*extra_nonzero)


def verify(problem: Problem, found: dict) -> dict:
    theory = problem.theory
    expand = theory.expand_definitions
    from .validate import relation_zeros
    points = admissible_points(problem.symbols, relation_zeros(problem), problem.conditions, count=10, seed=SEED,
                               prefer=problem.solve_order)
    checks = []

    def replay(step: Step) -> bool:
        if step.rule in ("algebra_finish", "reciprocal_quotient_finish"):
            return finish_holds(step.rule, step.before, step.after)
        if step.rule == "exponentiate":
            return True  # checked as the goal's conclusion below
        if step.rule not in REGISTRY:
            return False
        try:
            rule = build(step.rule, theory, {k: v for k, v in step.params.items() if k != "roots"})
            return rule.apply(step.after) == step.before if step.reverse else rule.apply(step.before) == step.after
        except Exception:
            return False

    parts = [("premise", st) for st in found.get("premises", [])] + [("step", st) for st in found.get("steps", [])]
    if found.get("conclusion"):
        parts.append(("conclusion", found["conclusion"]))
    base = theory
    # Each premise is judged against the givens and the premises before it; later steps may use
    # every premise's conclusion. This is sound because a failed premise fails the whole trace.
    established = list(problem.hypotheses) + list(problem.facts)
    derived = [(p.after.lhs, p.after.rhs) for p in found.get("premises", []) if isinstance(p.after, s.Eq)]
    # Every derived fact follows from the givens (and, for y(x), from their derivatives), so the
    # points that satisfy those satisfy every fact as well.
    here = points
    for part, step in parts:
        if part == "premise":
            theory = base.with_facts(established[len(problem.hypotheses):])
        else:
            theory = base.with_facts(derived)
        check = {"part": part, "rule": step.rule, "relation": step.relation}
        if step.relation == "geometry":
            check["passed"] = _geometry(step)
        elif step.relation == "transformation":
            # A rule applied to an equation already established (differentiate both sides, take logs).
            check["replayed"] = replay(step)
            check["from_established"] = (step.before.lhs, step.before.rhs) in established
            check["passed"] = check["replayed"] and check["from_established"]
        elif step.relation == "evaluation":
            check["replayed"] = replay(step)
            check["numeric"] = bool(s.N(step.before.doit() - step.after, 50) == 0)
            check["passed"] = check["replayed"] and check["numeric"]
        elif step.relation == "implication" and isinstance(step.after, s.Eq) and step.rule not in ("exponentiate", "numerator_zero"):
            extra = s.Integer(1)
            if step.rule == "positive_root":  # both sides positive, so their sum is nonzero
                extra = step.after.lhs + step.after.rhs
                check["positive"] = bool(extra.is_positive) or _positive_root(step.after)
            check["replayed"] = replay(step)
            check["exact"] = _implied(step.after, problem, extra, theory)
            check["numeric"] = numerically_equal(expand(step.after.lhs), expand(step.after.rhs), here)
            check["passed"] = all(v for k, v in check.items() if k in ("replayed", "exact", "numeric", "positive"))
        elif step.rule == "limit_step":
            from .rules.calculus import limits_equal
            h = step.params["h"]
            if isinstance(step.before, s.Derivative):  # the definition of the derivative
                check["passed"] = (isinstance(step.after, s.Limit) and limits_equal(
                    step.after, s.diff(step.before.args[0], step.before.args[1][0]), h))
            else:
                check["replayed"] = replay(step)
                check["numeric"] = _limit_numeric(step.before, step.after, h, points)
                check["passed"] = check["replayed"] and check["numeric"]
        elif step.rule == "sign_on_domain":
            check["replayed"] = replay(step)
            sign = 1 if isinstance(step.after, s.StrictGreaterThan) else -1
            values = [complex(s.N(step.before.xreplace(p), 30)) for p in points]
            check["numeric"] = bool(values) and all(sign*v.real > 0 and abs(v.imag) < 1e-20 for v in values)
            check["passed"] = check["replayed"] and check["numeric"]
        elif step.relation == "implication" and step.rule != "exponentiate":
            check["passed"] = check["replayed"] = replay(step)
        elif step.rule == "exponentiate":
            check["passed"] = bool(step.after.lhs.is_positive and step.after.rhs.is_positive)
        elif step.relation == "equivalence":
            check["replayed"] = replay(step)
            check["exact"] = exact_equal(step.before.lhs - step.before.rhs, step.after.lhs - step.after.rhs, theory)
            check["passed"] = check["replayed"] and check["exact"]
        elif step.relation == "solution":
            check["passed"] = _solution(problem, step)
        elif step.relation == "implication" and step.rule == "numerator_zero":
            check["replayed"] = replay(step)
            difference = step.before.lhs - step.before.rhs
            check["exact"] = exact_equal(step.after.lhs, difference*s.fraction(s.together(difference))[1], theory)
            check["passed"] = check["replayed"] and check["exact"]
        elif step.relation == "critical_point":
            from .strategies.calculus import critical_points
            v = problem.exprs["variable"]
            roots, point = critical_points(step.before.lhs, v)
            check["passed"] = point is not None and s.simplify(point - step.after.rhs) == 0 \
                and s.simplify(step.before.lhs.xreplace({v: point})) == 0
        elif step.relation == "second_derivative":
            v, function, point = problem.exprs["variable"], step.params["function"], step.params["point"]
            value = s.simplify(s.diff(function, v, 2).xreplace({v: point}))
            wanted = problem.spec.goal["type"]
            check["passed"] = s.simplify(value - step.after) == 0 and bool(
                value.is_negative if wanted == "max" else value.is_positive)
        elif step.relation == "claim":
            check["passed"] = exact_equal(step.after.lhs, step.after.rhs, base)
        elif step.relation == "roots":
            check["passed"] = _roots(problem, step)
        elif step.relation == "solution_set":
            check["passed"] = _solution_set(problem, found, step)
        else:
            check["replayed"] = replay(step)
            check["exact"] = exact_equal(step.before, step.after, theory)
            check["numeric"] = numerically_equal(expand(step.before), expand(step.after), here)
            check["domain"] = domain_safe(step.after, theory) and domain_safe(step.before, theory)
            if step.rule == "evaluate_integral":
                check["antiderivative"] = _antiderivatives_check(step)
            check["passed"] = all(check[k] for k in ("replayed", "exact", "numeric", "domain", "antiderivative")
                                  if k in check)
        if part == "premise" and check["passed"] and isinstance(step.after, s.Eq):
            established.append((step.after.lhs, step.after.rhs))
        checks.append(check)
    goal_ok, goal_reason = _goal(problem, found)
    passed = bool(checks) and all(c["passed"] for c in checks) and goal_ok
    return {"passed": passed, "steps": checks, "goal_matched": goal_ok, "goal_reason": goal_reason,
            "sample_points": len(points)}


def _limit_numeric(before: s.Expr, after: s.Expr, h: s.Symbol, points: list) -> bool:
    """Independent of SymPy's limit: evaluate each limit's argument at a tiny h."""
    tiny = s.Rational(1, 10**12)
    at = lambda e: e.replace(lambda q: isinstance(q, s.Limit), lambda q: q.args[0].xreplace({h: tiny}))
    for point in points[:4]:
        a, b = (complex(s.N(at(e).xreplace(point), 30)) for e in (before, after))
        if abs(a - b) > 1e-6*(1 + abs(a) + abs(b)):
            return False
    return bool(points)


def _positive_root(eq: s.Eq) -> bool:
    """v = k sqrt(w) with v > 0 and k > 0: then w = v^2/k^2 > 0, so sqrt(w) > 0 and v + k sqrt(w) > 0."""
    factors = s.Mul.make_args(eq.rhs)
    return bool(eq.lhs.is_positive) and all(f.is_positive or (f.is_Pow and f.exp == s.Rational(1, 2)) for f in factors) \
        and any(f.is_Pow and f.exp == s.Rational(1, 2) for f in factors)


def _antiderivatives_check(step: Step) -> bool:
    """Every integral evaluated in this step: F' = f exactly, and f has no pole in [a, b]."""
    from .rules.calculus import antiderivative
    for integral in step.before.atoms(s.Integral):
        (x, low, high), = integral.limits
        primitive = antiderivative(integral.function, x)
        if s.simplify(s.diff(primitive, x) - integral.function) != 0:
            return False
        denominator = s.fraction(s.together(integral.function))[1]
        poles = s.solveset(denominator, x, s.Interval(low, high))
        if poles != s.S.EmptySet:
            return False
    return True


def _solution(problem: Problem, step: Step) -> bool:
    from .strategies.values import admissible
    x, value = problem.exprs["variable"], step.after.rhs
    original = problem.theory.expand_definitions(problem.exprs["lhs"] - problem.exprs["rhs"])
    plain = s.Symbol(x.name)
    roots = {r.xreplace({plain: x}) for r in s.solve(step.before.lhs.xreplace({x: plain}), plain)}
    return (s.simplify(original.xreplace({x: value})) == 0 and admissible(problem, value)
            and roots == set(step.params.get("roots", ())) and value in roots)


def _same_values(a, b) -> bool:
    from .equality import numbers_equal
    return len(a) == len(b) and all(any(numbers_equal(u, v) for v in b) for u in a)


def _roots(problem: Problem, step: Step) -> bool:
    from .strategies.equations import interval
    x, factor = problem.exprs["variable"], step.params["factor"]
    from .strategies.equations import finite
    recomputed = finite(s.solveset(factor, x, interval(problem)))  # second method for a basic factor
    return (recomputed is not None and _same_values(list(recomputed), list(step.after))
            and all(abs(complex(s.N(factor.xreplace({x: r}), 30))) < 1e-20 for r in step.after))


def _solution_set(problem: Problem, found: dict, step: Step) -> bool:
    """Kept values satisfy the original; rejected ones do not; nothing is missing.

    Nothing is missing because the rewriting chain (each step checked as an equivalence or
    an implication from the original) ends in a product of exactly the factors whose roots
    were listed. A one-call solve of the whole equation is not used: SymPy's solveset misses
    roots of 2cos^2 x - cos x - 1 = 0, for example."""
    from .strategies.equations import _factors, holds
    kept, rejected = list(step.after), list(step.params.get("rejected", ()))
    root_steps = [st for st in found["steps"] if st.relation == "roots"]
    candidates = [r for st in root_steps for r in st.after]
    rewriting = [st for st in found["steps"] if st.relation in ("equivalence", "implication")]
    final = rewriting[-1].after if rewriting else step.before
    covered = (final.rhs == 0 and set(_factors(final.lhs)) == {st.params["factor"] for st in root_steps})
    return (all(holds(problem, r) for r in kept) and not any(holds(problem, r) for r in rejected)
            and _same_values(candidates, kept + rejected) and covered)


def _chain_linked(steps: list[Step]) -> bool:
    return all(a.after == b.before for a, b in zip(steps, steps[1:]))


def _justified(problem: Problem, found: dict) -> bool:
    """Every substitution must come from a derived equation, every replacement from a given."""
    premises = found.get("premises", [])
    solved = {(p.after.lhs, p.after.rhs) for p in premises if p.rule in ("solve_for", "positive_root")}
    givens = set(problem.hypotheses) | set(problem.facts) | {(p.after.lhs, p.after.rhs) for p in premises if isinstance(p.after, s.Eq)}
    for step in found.get("steps", []):
        if step.rule == "substitute" and (step.params["variable"], step.params["value"]) not in solved:
            return False
        if step.rule == "replace_given" and (step.params["lhs"], step.params["rhs"]) not in givens:
            return False
        if step.rule == "replace_givens" and not set(step.params["pairs"]) <= givens:
            return False
    return True


def _goal(problem: Problem, found: dict) -> tuple[bool, str]:
    steps, kind = found.get("steps", []), problem.kind
    if kind in ("prove_identity", "prove_from_hypotheses"):
        lhs, rhs = problem.exprs["lhs"], problem.exprs["rhs"]
        form = found.get("form", "chain")
        start, end = {"chain": (lhs, rhs), "difference": (lhs - rhs, s.Integer(0)),
                      "logs": (s.log(lhs), s.log(rhs))}[form]
        if not steps:
            ok = start == end
        else:
            ok = _chain_linked(steps) and steps[0].before == start and steps[-1].after == end
        if form == "logs":
            conclusion = found.get("conclusion")
            ok = ok and conclusion is not None and conclusion.after == s.Eq(lhs, rhs, evaluate=False)
        ok = ok and _justified(problem, found)
        if problem.about_unknown_function and any(st.rule in PROPERTY_RULES for st in steps):
            return False, "Circular: a property of integrals cannot be proved by quoting such a property."
        return ok, {"chain": "Chain runs from the stated LHS to the stated RHS.",
                    "difference": "Chain shows LHS - RHS = 0.",
                    "logs": "Chain shows log LHS = log RHS; both sides are positive."}[form]
    if kind == "first_principles":
        x, f = problem.exprs["variable"], problem.exprs["function"]
        ok = (bool(steps) and _chain_linked(steps) and steps[0].before == s.Derivative(f, x)
              and isinstance(steps[1].before, s.Limit) and s.simplify(steps[-1].after - s.diff(f, x)) == 0)
        return ok, "Starts from the limit definition and ends at the derivative."
    if kind == "monotonic":
        x, f = problem.exprs["variable"], problem.exprs["function"]
        wanted = s.StrictGreaterThan if problem.spec.goal["direction"] == "increasing" else s.StrictLessThan
        ok = (bool(steps) and _chain_linked(steps) and steps[0].before == s.Derivative(f, x)
              and isinstance(steps[-1].after, wanted))
        return ok, "The derivative is shown to have the required sign on the domain."
    if kind == "extremum":
        relations = [st.relation for st in steps]
        claims = problem.spec.goal.get("claims", [])
        ok = ("critical_point" in relations and "second_derivative" in relations
              and relations.count("claim") == len(claims))
        return ok, "Unique critical point in the domain, second-derivative test, and each claim checked at it."
    if kind == "evaluate":
        from .strategies.calculus import simplified
        start, answer = problem.exprs["expr"], simplified(problem.exprs["expr"], problem.theory)
        ok = (not steps and start == answer) or (bool(steps) and _chain_linked(steps) and steps[0].before == start
                                                  and steps[-1].after == answer)
        return ok, "Chain runs from the expression to its simplified value."
    if kind == "solve_equation":
        equation = s.Eq(problem.exprs["lhs"], problem.exprs["rhs"], evaluate=False)
        rewriting = [st for st in steps if st.relation in ("equivalence", "implication")]
        ok = (bool(steps) and steps[-1].relation == "solution_set" and steps[-1].before == equation
              and (not rewriting or (rewriting[0].before == equation and _chain_linked(rewriting))))
        return ok, "Every kept value satisfies the original equation, and an independent solve finds no others."
    if kind == "find_value":
        ok = (_chain_linked(steps) and bool(steps)
              and steps[0].before == s.Eq(problem.exprs["lhs"], problem.exprs["rhs"], evaluate=False)
              and steps[-1].relation == "solution")
        return ok, "The chosen value satisfies the original equation and the constraints."
    if kind == "factor_theorem":
        x, p, f = (problem.exprs[k] for k in ("variable", "polynomial", "factor"))
        final = steps[-1].after if steps else None
        ok = (s.Poly(p, x).rem(s.Poly(f, x)).is_zero and final is not None and _chain_linked(steps)
              and steps[0].before == p and s.expand(final - p) == 0
              and any(s.cancel(g/f).is_Number for g in s.Mul.make_args(final)))
        return bool(ok), "Remainder is zero and the final product expands to the polynomial and contains the factor."
    if kind == "show_no_real_roots":
        x, p = problem.exprs["variable"], problem.exprs["polynomial"]
        method_used = problem.spec.prescribed_method != "completing_square" or any(st.rule == "complete_square" for st in steps)
        ok = (not s.Poly(p, x).real_roots() and _chain_linked(steps) and steps[0].before == p
              and isinstance(steps[-1].after, s.StrictGreaterThan) and method_used)
        return bool(ok), "Sturm count finds no real root; the trace ends in a strict positivity statement."
    if kind == "geometry_jgex":
        return found.get("diagnostics", {}).get("solver_goal_checked") is True, "Newclid goal check plus coordinate replay."
    return False, f"No goal check for {kind}"


def _geometry(step: Step) -> bool:
    from newclid_probe import independent_replay
    name = step.params.get("check")
    if name == "solver_goal_checked":
        return independent_replay()["passed"]
    return independent_replay()["checks"].get(name) is True

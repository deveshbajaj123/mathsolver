"""Strategy `solve_equation`: solve a trig (or polynomial) equation in an interval.

1. Rewrite with equivalence steps (move terms, one-function form, double angles,
   factorise) until every factor is a basic equation such as 2 sin x - 1 = 0.
   A fraction equal to zero becomes its numerator equal to zero (an implication,
   which can add extra roots; step 3 removes them).
2. Solve each basic factor in the interval.
3. Check every candidate in the original equation; keep it only where the original
   is defined and true.
Completeness comes from the structure: each rewriting step is an equivalence or an
implication from the original, so every solution is a root of a final factor, and each
factor's roots are found by the general-solution formula and cross-checked by SymPy.
"""
from __future__ import annotations

import sympy as s

from ..engine import Step
from ..equality import TRIG, numbers_equal
from ..problem import Problem
from ..rules import build

REWRITES = ["move_terms", "numerator_zero", "double_angle_sin", "pythagorean_even_cos", "pythagorean_even_sin",
            "secant_identity", "cosecant_identity", "factor_equation"]


def finite(values) -> tuple | None:
    """The values of a finite solution set (possibly empty), else None."""
    if values == s.S.EmptySet:
        return ()
    return tuple(values) if isinstance(values, s.FiniteSet) else None


def interval(problem: Problem) -> s.Interval:
    low, high = problem.exprs["low"], problem.exprs["high"]
    return s.Interval(low, high, right_open=bool(problem.spec.goal.get("high_open", False)))


def _factors(expr: s.Expr) -> list:
    return [f.base if f.is_Pow and f.exp.is_Integer and f.exp > 0 else f
            for f in s.Mul.make_args(expr) if not f.is_number]


def _basic(factor: s.Expr, x: s.Symbol) -> bool:
    """One trig function of one angle (or x itself), appearing linearly."""
    functions = {f for f in factor.atoms(s.Function) if f.func in TRIG}
    if len(functions) > 1:
        return False
    atom = functions.pop() if functions else x
    t = s.Dummy("t")
    replaced = factor.xreplace({atom: t})
    return not replaced.has(x) and replaced.is_polynomial(t) and s.degree(replaced, t) == 1


def _rewrite(equation: s.Eq, x, theory) -> tuple[s.Eq, list]:
    """Breadth-first over the equation rules until all factors are basic (depth 4)."""
    frontier, seen = [(equation, [])], {equation}
    for _ in range(4):
        next_frontier = []
        for eq, steps in frontier:
            if eq.rhs == 0 and all(_basic(f, x) for f in _factors(eq.lhs)):
                return eq, steps
            for name in REWRITES:
                rule = build(name, theory)
                try:
                    new = rule.apply(eq)
                except Exception:  # a rule that does not fit this equation
                    continue
                if not isinstance(new, s.Eq) or new in seen:
                    continue
                seen.add(new)
                relation = "implication" if name == "numerator_zero" else "equivalence"
                next_frontier.append((new, steps + [Step(eq, new, rule.name, rule.reason, relation=relation)]))
        frontier = next_frontier
    for eq, steps in frontier:
        if eq.rhs == 0 and all(_basic(f, x) for f in _factors(eq.lhs)):
            return eq, steps
    return None, []


GENERAL = {  # principal value p of the inverse function -> one period of solutions, and the period
    s.sin: (s.asin, lambda p: (p, s.pi - p), 2*s.pi),
    s.cos: (s.acos, lambda p: (p, -p), 2*s.pi),
    s.tan: (s.atan, lambda p: (p,), s.pi),
    s.cot: (s.acot, lambda p: (p,), s.pi),
}
RECIPROCAL = {s.sec: s.cos, s.csc: s.sin}


def basic_solutions(factor: s.Expr, x: s.Symbol, domain: s.Interval) -> tuple:
    """Roots of a basic equation a*T(u) + b = 0 in the interval, from the general-solution
    formulae (e.g. sin u = c gives u = asin c + 2k pi or pi - asin c + 2k pi)."""
    functions = [f for f in factor.atoms(s.Function) if f.func in TRIG]
    t = s.Dummy("t")
    atom = functions[0] if functions else x
    value = s.solve(factor.xreplace({atom: t}), t)[0]
    if not functions:
        return (value,) if value in domain else ()
    function, angle = atom.func, atom.args[0]
    if function in RECIPROCAL:
        if value == 0:
            return ()
        function, value = RECIPROCAL[function], 1/value
    if function in (s.sin, s.cos) and abs(value) > 1:
        return ()
    inverse, branches, period = GENERAL[function]
    slope = angle.coeff(x)
    offset = s.expand(angle - slope*x)
    if not (slope.is_Rational and slope != 0 and not offset.has(x)):
        raise ValueError(f"Angle {angle} is not linear in {x}")
    found = []
    span = int(abs(slope)*(domain.end - domain.start)/period) + 2
    for branch in branches(inverse(value)):
        for k in range(-span - 1, span + 2):
            root = s.nsimplify(s.simplify((branch + k*period - offset)/slope))
            if root in domain and not any(s.simplify(root - r) == 0 for r in found):
                found.append(root)
    return tuple(sorted(found, key=lambda r: float(r)))


def holds(problem: Problem, value: s.Expr) -> bool:
    """The original equation is defined and true at value."""
    x = problem.exprs["variable"]
    for condition in problem.conditions:
        at = condition.expr.xreplace({x: value})
        if condition.relation == "!=0" and numbers_equal(at, s.Integer(0)):
            return False
    lhs, rhs = (problem.exprs[k].xreplace({x: value}) for k in ("lhs", "rhs"))
    if lhs.has(s.zoo, s.nan) or rhs.has(s.zoo, s.nan):
        return False
    return numbers_equal(lhs, rhs)


def solve_equation(problem: Problem) -> dict:
    x, theory = problem.exprs["variable"], problem.theory
    start = s.Eq(problem.exprs["lhs"], problem.exprs["rhs"], evaluate=False)
    final, steps = _rewrite(start, x, theory)
    if final is None:
        return {"strategy": "solve_equation", "status": "UNSUPPORTED", "premises": [], "steps": [],
                "reason": "Could not reduce the equation to basic factors."}
    domain = interval(problem)
    candidates = []
    for factor in _factors(final.lhs):
        try:
            ordered = basic_solutions(factor, x, domain)
        except (ValueError, IndexError) as exc:
            return {"strategy": "solve_equation", "status": "INCONCLUSIVE", "premises": [], "steps": steps,
                    "reason": f"Could not list the roots of {factor} = 0 in the interval: {exc}"}
        steps.append(Step(s.Eq(factor, 0, evaluate=False), ordered, "basic_roots",
                          "Use the general solution and keep the values in the interval.", {"factor": factor},
                          relation="roots"))
        candidates += [r for r in ordered if r not in candidates]
    kept = tuple(sorted((r for r in candidates if holds(problem, r)), key=lambda r: float(r)))
    rejected = tuple(r for r in candidates if r not in kept)
    reason = "Check each value in the original equation"
    if rejected:
        reason += "; reject those where it is undefined or false"
    steps.append(Step(start, kept, "check_roots", reason + ".", {"rejected": rejected}, relation="solution_set"))
    return {"strategy": "solve_equation", "status": "SOLVED", "form": "solutions", "premises": [], "steps": steps,
            "diagnostics": {"solutions": kept, "rejected": rejected}}

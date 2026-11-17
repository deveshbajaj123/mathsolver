"""Strategy `general_solution`: every solution of a trig equation, as families in an integer n.

1. The same checked rewriting as `solve_equation` reduces the equation to basic factors.
2. Each basic factor a*T(kx + c) + b = 0 gives T(u) = v, and the school formula:
   sin u = sin α  ⇒ u = nπ + (−1)ⁿα;   cos u = cos α  ⇒ u = 2nπ ± α;   tan u = tan α  ⇒ u = nπ + α.
3. Each family is then solved for x.

verify.py checks (a) every family at n = −6 … 6 satisfies the original equation, and is
defined there, and (b) completeness: the families' values in [0, 2π) equal SymPy's solveset
of the original on [0, 2π) when that is finite, and in any case the rewriting ends in a
product of exactly the factors whose families were listed. A family on which the original
is undefined (from clearing a denominator) is not handled: the strategy reports it.
"""
from __future__ import annotations

import sympy as s

from ..engine import Step
from ..problem import Problem
from .equations import RECIPROCAL, _factors, _rewrite, holds

N = s.Symbol("n", integer=True)
FORMULA = {
    s.sin: (s.asin, lambda a: (N*s.pi + (-1)**N*a,), r"\sin u = \sin\alpha \implies u = n\pi + (-1)^{n}\alpha"),
    s.cos: (s.acos, lambda a: (2*N*s.pi + a, 2*N*s.pi - a), r"\cos u = \cos\alpha \implies u = 2n\pi \pm \alpha"),
    s.tan: (s.atan, lambda a: (N*s.pi + a,), r"\tan u = \tan\alpha \implies u = n\pi + \alpha"),
    s.cot: (s.acot, lambda a: (N*s.pi + a,), r"\cot u = \cot\alpha \implies u = n\pi + \alpha"),
}


def families(factor: s.Expr, x: s.Symbol) -> tuple[tuple, str] | None:
    """x-families solving a basic factor = 0, and the formula used; () if it has no solution."""
    functions = [f for f in factor.atoms(s.Function) if f.func in FORMULA or f.func in RECIPROCAL]
    t = s.Dummy("t")
    atom = functions[0] if functions else x
    value = s.solve(factor.xreplace({atom: t}), t)[0]
    if not functions:
        return (value,), "linear"
    function, angle = atom.func, atom.args[0]
    if function in RECIPROCAL:
        if value == 0:
            return (), "no value"
        function, value = RECIPROCAL[function], 1/value
    if function in (s.sin, s.cos) and abs(value) > 1:
        return (), f"{function.__name__} cannot be {value}"
    slope = angle.coeff(x)
    offset = s.expand(angle - slope*x)
    if not (slope.is_Rational and slope != 0 and not offset.has(x)):
        return None
    inverse, make, formula = FORMULA[function]
    principal = inverse(value)
    return tuple(s.expand((u - offset)/slope) for u in make(principal)), formula


def general_solution(problem: Problem) -> dict:
    x, theory = problem.exprs["variable"], problem.theory
    start = s.Eq(problem.exprs["lhs"], problem.exprs["rhs"], evaluate=False)
    final, steps = _rewrite(start, x, theory)
    if final is None:
        return {"strategy": "general_solution", "status": "UNSUPPORTED", "premises": [], "steps": [],
                "reason": "Could not reduce the equation to basic factors."}
    found = []
    for factor in _factors(final.lhs):
        result = families(factor, x)
        if result is None:
            return {"strategy": "general_solution", "status": "UNSUPPORTED", "premises": [], "steps": steps,
                    "reason": f"The angle in {factor} is not linear in {x}."}
        forms, formula = result
        steps.append(Step(s.Eq(factor, 0, evaluate=False), forms, "general_family", formula, {"factor": factor},
                          relation="family"))
        found += [f for f in forms if f not in found]
    for family in found:  # a family on which the original is undefined or false is not a solution
        if not all(holds(problem, family.xreplace({N: k})) for k in range(-3, 4)):
            return {"strategy": "general_solution", "status": "INCONCLUSIVE", "premises": [], "steps": steps,
                    "reason": f"The family {family} does not solve the original equation everywhere."}
    steps.append(Step(start, tuple(found), "general_set", "Collect the families.", relation="general_set"))
    return {"strategy": "general_solution", "status": "SOLVED", "form": "general", "premises": [], "steps": steps,
            "diagnostics": {"families": tuple(str(f) for f in found)}}


def check_families(problem: Problem, found: dict) -> bool:
    """Independent check used by verify.py (see the module docstring)."""
    x = problem.exprs["variable"]
    steps = found.get("steps", [])
    family_steps = [st for st in steps if st.relation == "family"]
    families_ = [f for st in family_steps for f in st.after]
    if not steps or steps[-1].relation != "general_set" or set(steps[-1].after) != set(families_):
        return False
    for family in families_:
        if not all(holds(problem, family.xreplace({N: k})) for k in range(-6, 7)):
            return False
    rewriting = [st for st in steps if st.relation in ("equivalence", "implication")]
    final = rewriting[-1].after if rewriting else steps[-1].before
    if not (final.rhs == 0 and set(_factors(final.lhs)) == {st.params["factor"] for st in family_steps}):
        return False
    window = s.Interval.Ropen(0, 2*s.pi)
    listed = set()
    for family in families_:
        for k in range(-40, 41):
            value = s.nsimplify(s.simplify(family.xreplace({N: k})))
            if value in window:
                listed.add(str(s.N(value, 15)))
    try:
        other = s.solveset(s.Eq(problem.exprs["lhs"], problem.exprs["rhs"]), x, window)
    except Exception:
        return True
    if isinstance(other, s.FiniteSet):
        return {str(s.N(v, 15)) for v in other} == listed
    return True

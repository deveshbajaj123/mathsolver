"""Step 5: strategy selection. Code chooses; a prescribed method is mandatory."""
from __future__ import annotations

import sympy as s

from ..problem import Problem
from .calculus import definite_integral, derivative_relation, evaluate, extremum, first_principles, monotonic
from .equations import solve_equation
from .geometry import newclid
from .identity import conditional, difference, identity, take_logs
from .polynomial import factor_theorem, no_real_roots
from .values import find_value

ROUTES = {
    "prove_identity": [identity, difference, take_logs],
    "prove_from_hypotheses": [conditional, difference, take_logs],
    "factor_theorem": [factor_theorem],
    "show_no_real_roots": [no_real_roots],
    "find_value": [find_value],
    "solve_equation": [solve_equation],
    "evaluate": [evaluate],
    "monotonic": [monotonic],
    "extremum": [extremum],
    "first_principles": [first_principles],
    "geometry_jgex": [newclid],
}
PRESCRIBED = {"factor_theorem": factor_theorem, "completing_square": no_real_roots}


def select(problem: Problem) -> list:
    method = problem.spec.prescribed_method
    if method:
        return [PRESCRIBED[method]] if PRESCRIBED[method] in ROUTES[problem.kind] else []
    if problem.kind == "prove_from_hypotheses" and problem.ctx.chain:
        return [derivative_relation]  # a relation between y and its derivatives
    if problem.kind == "prove_identity" and problem.exprs["lhs"].has(s.Integral):
        # Proving a property of an unspecified f must not use rules that quote such properties.
        return [definite_integral] if problem.about_unknown_function else [definite_integral, identity]
    return ROUTES[problem.kind]

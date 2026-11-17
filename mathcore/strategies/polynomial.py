"""Strategy `polynomial`: factor theorem and completing the square, migrated from the
old pipeline. Steps use registered rules so verify.py can replay them."""
from __future__ import annotations

import sympy as s

from ..engine import Step
from ..problem import Problem
from ..rules import build


def factor_theorem(problem: Problem) -> dict:
    x, p, f = (problem.exprs[k] for k in ("variable", "polynomial", "factor"))
    root = s.solve(f, x)[0]
    theory = problem.theory
    evaluate = build("evaluate_at", theory)
    remainder = evaluate.apply(s.Subs(p, x, root))
    if remainder != 0:
        return {"strategy": "polynomial", "status": "INCONCLUSIVE", "premises": [], "steps": [],
                "reason": f"Remainder {remainder} is not zero."}
    evaluation = Step(s.Subs(p, x, root), remainder, evaluate.name, evaluate.reason, relation="evaluation")
    divide = build("divide_by_factor", theory, {"factor": f, "variable": x})
    divided = divide.apply(p)
    factor_all = build("algebra_factor", theory)
    steps = [Step(p, divided, divide.name, divide.reason, divide.params),
             Step(divided, factor_all.apply(divided), factor_all.name, factor_all.reason)]
    return {"strategy": "polynomial", "status": "SOLVED", "premises": [evaluation], "steps": steps,
            "diagnostics": {"root": root}}


def no_real_roots(problem: Problem) -> dict:
    x, p = problem.exprs["variable"], problem.exprs["polynomial"]
    if s.Poly(p, x).degree() != 2:
        return {"strategy": "polynomial", "status": "UNSUPPORTED", "premises": [], "steps": [],
                "reason": "Completing the square is implemented for quadratics only."}
    square = build("complete_square", problem.theory, {"variable": x})
    positive = build("square_plus_positive", problem.theory, {"variable": x})
    completed = square.apply(p)
    try:
        conclusion = positive.apply(completed)
    except ValueError as exc:
        return {"strategy": "polynomial", "status": "INCONCLUSIVE", "premises": [], "steps": [], "reason": str(exc)}
    steps = [Step(p, completed, square.name, square.reason, square.params),
             Step(completed, conclusion, positive.name, positive.reason, positive.params, relation="implication")]
    return {"strategy": "polynomial", "status": "SOLVED", "premises": [], "steps": steps}

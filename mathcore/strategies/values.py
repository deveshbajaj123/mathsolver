"""Strategy `find_value`: rewrite an equation in one unknown, solve it, and keep the
roots that meet the stated constraints (integer, range). Shows existence by example."""
from __future__ import annotations

import sympy as s

from ..engine import Step
from ..problem import Problem
from ..rules import build, names


def admissible(problem: Problem, value: s.Expr) -> bool:
    x = problem.exprs["variable"]
    if not value.is_real or (x.is_integer and not value.is_integer) or (x.is_positive and not value.is_positive):
        return False
    low, high = problem.exprs.get("low"), problem.exprs.get("high")
    return (low is None or value >= low) and (high is None or value <= high)


def find_value(problem: Problem) -> dict:
    x, theory = problem.exprs["variable"], problem.theory
    equation, steps = s.Eq(problem.exprs["lhs"], problem.exprs["rhs"], evaluate=False), []
    for name in names("sequence") + ["move_terms", "factor_equation"]:
        rule = build(name, theory)
        new = rule.apply(equation)
        if new != equation:
            steps.append(Step(equation, new, rule.name, rule.reason, relation="equivalence"))
            equation = new
    if equation.lhs.free_symbols != {x}:
        return {"strategy": "find_value", "status": "UNSUPPORTED", "premises": [], "steps": steps,
                "reason": "The equation does not reduce to one unknown."}
    plain = s.Symbol(x.name)  # solve without x's assumptions, so rejected roots can be shown
    roots = [r.xreplace({plain: x}) for r in s.solve(equation.lhs.xreplace({x: plain}), plain)]
    chosen = [r for r in roots if admissible(problem, r)]
    if not chosen:
        return {"strategy": "find_value", "status": "INCONCLUSIVE", "premises": [], "steps": steps,
                "reason": f"No root in the allowed set; roots {roots}."}
    rejected = [r for r in roots if r not in chosen]
    steps.append(Step(equation, s.Eq(x, chosen[0], evaluate=False), "choose_root",
                      "Keep the root that satisfies the conditions" + (f"; reject {', '.join(map(str, rejected))}." if rejected else "."),
                      {"roots": tuple(roots)}, relation="solution"))
    return {"strategy": "find_value", "status": "SOLVED", "form": "value", "premises": [], "steps": steps,
            "diagnostics": {"value": chosen[0], "rejected": rejected}}

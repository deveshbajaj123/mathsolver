"""Step 4: bounded best-first rewrite search between the two sides of a claim.

Generalises automatic_trig_solver.solve: any symbols and angles, any rule list,
and the two sides may meet in the middle (LHS = ... = X = ... = RHS), which is how
school proofs that "simplify both sides" are written. Every edge is checked when
it is added; verify.py replays the finished trace independently.
"""
from __future__ import annotations

import heapq
import itertools
import time
from dataclasses import dataclass, field

import sympy as s

from .equality import VIEWS, Theory, domain_safe, exact_equal, finish_holds, freeze
from .rules import Rule

MAX_OPS = 100
FINISH = {
    "algebra_finish": "Simplify algebraically.",
    "reciprocal_quotient_finish": "Use the reciprocal and quotient identities and simplify.",
}


@dataclass
class Step:
    before: s.Expr
    after: s.Expr
    rule: str
    reason: str
    params: dict = field(default_factory=dict)
    relation: str = "equality"   # equality | implication | evaluation
    reverse: bool = False        # rule maps after -> before (step taken from the RHS side)


def edge_ok(before: s.Expr, after: s.Expr, rule: Rule | str, theory: Theory) -> bool:
    if isinstance(rule, str):
        applied = finish_holds(rule, before, after)
    else:
        try:
            applied = rule.apply(before) == after
        except Exception:
            return False
    return applied and domain_safe(after, theory) and exact_equal(before, after, theory)


def _score(e: s.Expr, goal: s.Expr) -> float:
    # Heuristic only; correctness comes from edge_ok and verify.py.
    return float(s.count_ops(e) + s.count_ops(s.cancel(freeze(e) - freeze(goal)))/2)


def search(lhs: s.Expr, rhs: s.Expr, rules: list[Rule], theory: Theory,
           max_states: int = 400, max_depth: int = 8, seconds: float = 90) -> dict:
    # The budget is the number of states, so results do not depend on machine speed;
    # `seconds` is only a safety cap.
    start = time.monotonic()
    serial = itertools.count()
    queue, parent, visited = [], {}, set()
    keys = {"LHS": {}, "RHS": {}}  # side -> {(finish rule, key): expr}
    origin = {"LHS": lhs, "RHS": rhs}
    for side, other in (("LHS", "RHS"), ("RHS", "LHS")):
        heapq.heappush(queue, (_score(origin[side], origin[other]), next(serial), 0, side, origin[side]))
        parent[(side, origin[side])] = None
    explored = 0
    while queue and explored < max_states and time.monotonic() - start < seconds:
        _, _, depth, side, current = heapq.heappop(queue)
        if (side, current) in visited:
            continue
        visited.add((side, current))
        explored += 1
        other = "RHS" if side == "LHS" else "LHS"
        for finish in FINISH:
            key = (finish, s.cancel(VIEWS[finish](current)))
            partner = keys[other].get(key)
            if partner is not None and (partner == current or edge_ok(current, partner, finish, theory)):
                steps = _assemble(parent, side, current, other, partner, finish)
                return {"status": "SOLVED", "steps": steps, "states_explored": explored,
                        "elapsed_seconds": round(time.monotonic() - start, 3)}
            keys[side].setdefault(key, current)
        if depth >= max_depth:
            continue
        for rule in rules:
            try:
                new = rule.apply(current)
            except Exception:
                continue
            if new == current or (side, new) in parent or new.has(s.zoo, s.nan) or s.count_ops(new) > MAX_OPS:
                continue
            if not edge_ok(current, new, rule, theory):
                continue
            parent[(side, new)] = ((side, current), rule)
            heapq.heappush(queue, (_score(new, origin[other]) + 2*depth, next(serial), depth + 1, side, new))
    return {"status": "INCONCLUSIVE", "states_explored": explored,
            "reason": "Search budget exhausted; no approved derivation found.",
            "elapsed_seconds": round(time.monotonic() - start, 3)}


def _path(parent: dict, side: str, expr: s.Expr) -> list[Step]:
    steps, key = [], (side, expr)
    while parent[key] is not None:
        previous, rule = parent[key]
        steps.append(Step(previous[1], key[1], rule.name, rule.reason, rule.params))
        key = previous
    return steps[::-1]


def _assemble(parent, side, current, other, partner, finish) -> list[Step]:
    """Chain from the original LHS to the original RHS."""
    lhs_end, rhs_end = (current, partner) if side == "LHS" else (partner, current)
    steps = _path(parent, "LHS", lhs_end)
    if lhs_end != rhs_end:
        # The closing simplification is shown from the more complicated side to the simpler one.
        toward_rhs = s.count_ops(rhs_end) <= s.count_ops(lhs_end)
        steps.append(Step(lhs_end, rhs_end, finish, FINISH[finish], reverse=not toward_rhs))
    for step in reversed(_path(parent, "RHS", rhs_end)):
        steps.append(Step(step.after, step.before, step.rule, step.reason, step.params, reverse=True))
    return steps

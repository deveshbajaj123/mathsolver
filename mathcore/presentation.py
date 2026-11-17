"""Milestone 4: measurable presentation checks for a rendered answer.

A 'large jump' is a plain simplification step (simplify, cancel, expand) that, read in
the direction the answer shows it, starts from at least LARGE operations and loses at
least CHANGE of them at once. Expanding (which grows) is easy to follow and is not
counted. These are the steps a reader is most likely to stumble on.
"""
from __future__ import annotations

import sympy as s

SIMPLIFY_RULES = ("algebra_finish", "reciprocal_quotient_finish", "algebra_cancel", "algebra_expand")
LARGE, CHANGE = 12, 6


def _operations(e) -> int:
    return int(s.count_ops(e)) if isinstance(e, s.Basic) else 0


def report(found: dict) -> dict:
    steps = found.get("premises", []) + found.get("steps", [])
    jumps = []
    for step in steps:
        shown_from, shown_to = (step.after, step.before) if step.reverse else (step.before, step.after)
        before, after = _operations(shown_from), _operations(shown_to)
        if step.rule in SIMPLIFY_RULES and before >= LARGE and before - after >= CHANGE:
            jumps.append({"rule": step.rule, "operations_before": before, "operations_after": after})
    return {"steps": len(steps), "large_jumps": jumps}

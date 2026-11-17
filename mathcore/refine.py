"""Milestone 4: split large algebraic jumps into the steps a student would write.

After the search finds a proof, each big 'simplify' step is replaced by short stages:
take a common denominator, expand the numerator, factorise. For a closing step that joins
the two sides, both sides are taken to the same factorised form, the way a textbook
shows that each side equals a²r²ⁿ(rⁿ − 1)²/(r − 1)². Every inserted step is a registered
rule, so verify.py checks the refined trace like any other; the pipeline keeps the
search's own trace if refinement does not verify.
"""
from __future__ import annotations

import sympy as s

from .engine import Step
from .equality import finish_holds
from .rules import build

FINISHES = ("algebra_finish", "reciprocal_quotient_finish")
SUM_STAGES = ("simplify_each_term", "combine_fractions", "algebra_common_denominator", "expand_numerator",
              "algebra_factor")
FRACTION_STAGES = ("clear_fractions", "factor_parts", "algebra_cancel")
MIN_OPERATIONS = 8


def _common_factor(e: s.Expr) -> bool:
    numerator, denominator = s.fraction(e)  # not together(): it would cancel the factor first
    return denominator != 1 and not s.gcd(numerator, denominator).is_number


def _simple_fraction(e: s.Expr) -> bool:
    """A single fraction whose top and bottom have no fractions inside them."""
    if e.is_Add:
        return False
    parts = s.fraction(e)
    return not any(p.is_Pow and p.exp.is_negative for part in parts for p in part.atoms(s.Pow))


def _stages(start: s.Expr, theory) -> list[tuple[str, s.Expr, s.Expr]]:
    """(rule, before, after) for each stage that changes the expression. A sum is put over
    one denominator; a single fraction has inner fractions cleared, then is factorised top
    and bottom and cancelled, but only if top and bottom share a factor."""
    stages, current = [], start
    for name in FRACTION_STAGES if _simple_fraction(start) else SUM_STAGES:
        if name == "algebra_common_denominator" and any(n == "combine_fractions" for n, _, _ in stages):
            continue  # already over one denominator
        if name in ("factor_parts", "algebra_cancel") and not _common_factor(current):
            continue
        try:
            new = build(name, theory).apply(current)
        except (ValueError, NotImplementedError):
            continue
        if new != current and s.latex(new) != s.latex(current):  # skip stages that look the same
            stages.append((name, current, new))
            current = new
    return stages


def _reason(name: str, before: s.Expr, after: s.Expr, theory) -> str:
    """The reason a reader needs for what this stage actually did."""
    if after.is_number:
        return "Cancel."
    if name == "algebra_cancel":
        return "Cancel the common factor."
    if name == "algebra_common_denominator":
        if _simple_fraction(before):
            return "Simplify the fraction."
        if s.fraction(after)[1] == 1:
            return "Collect like terms."
    if name == "algebra_factor":
        return "Factorise."
    if name == "simplify_each_term" and all(s.fraction(t)[1].is_number for t in s.Add.make_args(before)):
        return "Expand."
    if name == "clear_fractions":
        from .rules.algebra import clearing_factor
        return f"Multiply the numerator and the denominator by {clearing_factor(before)}."
    return build(name, theory).reason


def _forward(stages, theory) -> list[Step]:
    return [Step(before, after, name, _reason(name, before, after, theory)) for name, before, after in stages]


def _backward(stages, theory) -> list[Step]:
    """Stages computed from the RHS, placed in the LHS-to-RHS chain as reversed steps."""
    return [Step(after, before, name, _reason(name, before, after, theory), reverse=True)
            for name, before, after in reversed(stages)]


def _refine_finish(step: Step, theory) -> list[Step]:
    left, right = step.before, step.after
    if max(s.count_ops(left), s.count_ops(right)) < MIN_OPERATIONS:
        return [step]
    view = "algebra_finish" if step.rule == "algebra_finish" else None
    if view is None:
        return [step]
    # Only a side that is itself complicated is worked in stages.
    left_stages = _stages(left, theory) if s.count_ops(left) >= MIN_OPERATIONS else []
    right_stages = _stages(right, theory) if s.count_ops(right) >= MIN_OPERATIONS else []
    left_end = left_stages[-1][2] if left_stages else left
    right_end = right_stages[-1][2] if right_stages else right
    if not finish_holds("algebra_finish", left_end, right_end):
        return [step]
    middle = [] if left_end == right_end else [
        Step(left_end, right_end, "algebra_finish", "Simplify.",
             reverse=s.count_ops(right_end) > s.count_ops(left_end))]
    return _forward(left_stages, theory) + middle + _backward(right_stages, theory)


GENERATED = ("substitute", "replace_given", "replace_givens")


def _refine_cancel(step: Step, following: Step | None, theory) -> tuple[list[Step], bool]:
    """Returns (steps, whether `following` was absorbed). If the next step substitutes a
    given, it is applied to the staged form directly, so the answer does not swing back to
    the search's expanded form before using the given."""
    if step.reverse or s.count_ops(step.before) < MIN_OPERATIONS:
        if s.count_ops(step.after) > s.count_ops(step.before):  # the 'cancel' rule only expanded
            return [Step(step.before, step.after, step.rule, "Expand the numerator and the denominator.",
                         step.params, step.relation, step.reverse)], False
        return [step], False
    stages = [stage for stage in _stages(step.before, theory) if stage[0] != "algebra_factor"]
    if not stages:
        return [step], False
    end = stages[-1][2]
    if following is not None and not following.reverse and following.rule in GENERATED:
        rule = build(following.rule, theory, following.params)
        try:
            used = rule.apply(end)
        except Exception:
            used = None
        if used is not None and used != end and finish_holds("algebra_finish", used, following.after):
            tail = [Step(end, used, rule.name, rule.reason, following.params)]
            if used != following.after:
                tail.append(Step(used, following.after, "algebra_finish", "Simplify."))
            return _forward(stages, theory) + tail, True
    tail = [] if end == step.after else [Step(end, step.after, "algebra_finish", "Simplify.")]
    if tail and not finish_holds("algebra_finish", end, step.after):
        return [step], False
    return _forward(stages, theory) + tail, False


def refine(found: dict, theory) -> dict:
    if found.get("status") != "SOLVED" or found.get("form", "chain") not in ("chain", "difference", "logs"):
        return found
    steps, original, index = [], found["steps"], 0
    while index < len(original):
        step = original[index]
        following = original[index + 1] if index + 1 < len(original) else None
        if step.rule in FINISHES:
            steps += _refine_finish(step, theory)
        elif step.rule == "algebra_cancel":
            refined, absorbed = _refine_cancel(step, following, theory)
            steps += refined
            index += absorbed
        else:
            steps.append(step)
        index += 1
    return {**found, "steps": steps}

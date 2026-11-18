"""Figure facts for coordinate geometry, checked independently of the proof.

A spec that uses coordinates lists what the question and figure state, e.g.
["midpoint", "D", "B", "C"] or ["right_angle", "A", "B", "C"] (the angle at B). The
coordinates are chosen by whoever writes the spec, so each fact is checked here: an
exact check that it holds for those coordinates (under the givens). A fact that fails
means the coordinates do not describe the figure, and the spec is rejected.
"""
from __future__ import annotations

import sympy as s

from .equality import exact_equal
from .parse import geometry_value

RELATIONS = {
    # name: (number of points, words)
    "midpoint": (3, "{0} is the midpoint of {1}{2}"),
    "right_angle": (3, "∠{0}{1}{2} = 90°"),
    "perpendicular": (4, "{0}{1} ⊥ {2}{3}"),
    "parallel": (4, "{0}{1} ∥ {2}{3}"),
    "equal_length": (4, "{0}{1} = {2}{3}"),
    "collinear": (3, "{0}, {1}, {2} are collinear"),
    "on_line": (3, "{0} lies on line {1}{2}"),
}


def words(fact: list) -> str:
    return RELATIONS[fact[0]][1].format(*fact[1:])


def zeros(fact: list, points: dict) -> list:
    """Expressions that must all be zero for the fact to hold."""
    name, at = fact[0], [points[n] for n in fact[1:]]
    if name == "midpoint":
        (mx, my), (ax, ay), (bx, by) = at
        return [2*mx - ax - bx, 2*my - ay - by]
    if name == "right_angle":
        a, b, c = at
        return [geometry_value("dot", [b, a, b, c])]
    if name == "perpendicular":
        return [geometry_value("dot", at)]
    if name == "parallel":
        return [geometry_value("cross", at)]
    if name == "equal_length":
        return [geometry_value("dist2", at[:2]) - geometry_value("dist2", at[2:])]
    p, a, b = at  # collinear and on_line: P on line AB
    return [geometry_value("cross", [a, b, a, p])]


def check(spec, problem) -> tuple[bool, str]:
    coordinates = problem.ctx.points
    for fact in spec.figure:
        for zero in zeros(fact, coordinates):
            if not exact_equal(s.expand(zero), s.Integer(0), problem.theory):
                return False, f"The coordinates do not satisfy the figure fact: {words(fact)}."
    return True, ""

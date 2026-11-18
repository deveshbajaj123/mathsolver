"""Numeric points that satisfy the hypotheses and the domain, used by validate.py
(is the claim true?) and verify.py (an equality check independent of Groebner bases)."""
from __future__ import annotations

import random

import sympy as s

from .parse import Condition

PRECISION = 50
TOLERANCE = s.Float("1e-30", PRECISION)


def _random_value(symbol: s.Symbol, rng: random.Random, interval=None) -> s.Expr:
    if interval is not None:  # strictly inside the stated interval
        low, high = interval
        return low + (high - low)*s.Rational(rng.randint(1, 19), 20)
    if symbol.is_real is None:  # declared complex
        return s.Rational(rng.randint(-40, 40), rng.randint(1, 9)) + s.I*s.Rational(rng.randint(1, 40), rng.randint(1, 9))
    if symbol.is_integer:
        low = 1 if symbol.is_positive else -12
        values = [v for v in range(low, 13) if v != 0 or not symbol.is_nonzero]
        return s.Integer(rng.choice(values))
    numerator = rng.randint(1 if symbol.is_positive else -40, 40)
    if numerator == 0 and symbol.is_nonzero:
        numerator = 1
    return s.Rational(numerator, rng.randint(1, 9))


def _solve_hypotheses(hypotheses: list, symbols: list, prefer: tuple = ()) -> list[dict]:
    """Solve hypotheses for some variables, preferring `prefer` (e.g. y, y1, y2 when y is a
    function of x), then variables the hypothesis is linear in."""
    unknowns = []
    for h in hypotheses:
        numerator = s.together(h).as_numer_denom()[0]
        candidates = [v for v in symbols if v not in unknowns and numerator.has(v)]
        if not candidates:
            return []
        rank = lambda v: prefer.index(v) if v in prefer else len(prefer)
        # A variable that is only a monomial factor (c in c*(t - u) = 0) would be solved as c = 0: try others first.
        try:
            factors = [f for f, _ in s.factor_list(numerator)[1] if not f.is_Symbol]
        except (s.PolynomialError, NotImplementedError):
            factors = [numerator]
        inside = lambda v: 0 if any(f.has(v) for f in factors) else 1
        candidates.sort(key=lambda v: (rank(v), inside(v), s.degree(numerator, v) if numerator.is_polynomial(v) else 99,
                                       v.name))
        unknowns.append(candidates[0])
    if not unknowns:
        return [{}]
    try:
        return s.solve(hypotheses, unknowns, dict=True)
    except NotImplementedError:
        return []


def admissible_points(symbols: list, hypotheses: list, conditions: list[Condition],
                      count: int = 12, seed: int = 0, tries: int = 400, prefer: tuple = (),
                      intervals: dict | None = None) -> list[dict]:
    intervals = intervals or {}
    rng = random.Random(seed)
    branches = _solve_hypotheses(hypotheses, symbols, prefer)
    points = []
    for _ in range(tries):
        if not branches or len(points) >= count:
            break
        branch = rng.choice(branches)
        point = {v: _random_value(v, rng, intervals.get(v)) for v in symbols if v not in branch}
        try:
            for v, expr in branch.items():
                point[v] = expr.xreplace(point)
            values = {v: complex(s.N(value, PRECISION)) for v, value in point.items()}
        except (TypeError, ValueError, ZeroDivisionError):
            continue
        if any(abs(z.imag) > 1e-12 for v, z in values.items() if v.is_real):
            continue
        if any(v.is_integer and point[v].is_integer is not True for v in branch):
            continue
        if any(v.is_positive and values[v].real <= 0 for v in point):
            continue
        if any(v.is_nonnegative and values[v].real < 0 for v in point):
            continue
        if all(_holds(c, point) for c in conditions) and all(abs(complex(s.N(h.xreplace(point), 30))) < 1e-20
                                                              for h in hypotheses):
            points.append(point)
    return points


def _holds(condition: Condition, point: dict) -> bool:
    try:
        value = complex(s.N(condition.expr.xreplace(point), PRECISION))
    except (TypeError, ValueError):
        return False
    if condition.relation == "!=0":
        return abs(value) > 1e-9
    if abs(value.imag) > 1e-12:
        return False
    return { ">0": value.real > 1e-9, ">=0": value.real >= -1e-30}[condition.relation]


def numerically_equal(a: s.Expr, b: s.Expr, points: list[dict]) -> bool:
    """True when a = b to 30 significant digits at every point (requires at least one point)."""
    if not points:
        return False
    if (a - b).has(s.Integral):  # definite integrals, possibly of an unspecified f: test-function quadrature
        from .equality import integrals_equal
        return integrals_equal(a - b)

    def at(e, point):
        # Derivatives are carried out first; subs (not xreplace) keeps an integral's own variable bound.
        e = e.replace(lambda d: isinstance(d, s.Derivative) or type(d).__name__ == "Bracket", lambda d: d.doit())
        return s.N(e.subs(point) if e.has(s.Integral) else e.xreplace(point), PRECISION)

    for point in points:
        try:
            difference = at(a - b, point)
            scale = 1 + abs(at(a, point)) + abs(at(b, point))
        except (TypeError, ValueError):
            return False
        if difference.has(s.zoo, s.nan, s.oo) or abs(difference) > TOLERANCE*scale:
            return False
    return True

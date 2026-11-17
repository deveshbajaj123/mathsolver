"""Step 4: exact equality and domain safety, generalised from automatic_trig_solver.

Every trig function of an angle u is written with two fresh symbols sin(u), cos(u)
tied by sin(u)^2 + cos(u)^2 = 1; every surd g = b^(p/q) is tied by g^q = b^p.
Logs and real powers are put in a normal form (log laws, primes for rational
arguments, b^e = exp(e log b)); the parser has already recorded the positivity
conditions those laws need. Equality is then decided by ideal membership, or by
radical membership saturated by the domain: f vanishes wherever the hypotheses
hold and the original expressions are defined. Both tests are sound.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from functools import lru_cache

import sympy as s
from sympy.core.function import AppliedUndef

from .parse import named_class, sum_class, sum_formula, term_class, term_formula, expand_geometry

TRIG = (s.sin, s.cos, s.tan, s.cot, s.sec, s.csc)
Z, T = s.Symbol("_Z"), s.Symbol("_T")


@dataclass(frozen=True)
class Theory:
    """Everything that may be used to judge a step: definitions, hypotheses, domain."""
    sequences: tuple = ()     # (name, "ap" | "gp", first, difference or ratio)
    hypotheses: tuple = ()    # expressions equal to zero
    domain: tuple = ()        # nonzero factors in normal form
    definitions: tuple = ()   # (name, variable, expression) for named functions such as C(x)
    points: tuple = ()        # (name, x, y): coordinates that define AB^2, ar(ABC), ...
    intervals: tuple = ()     # (symbol, low, high): x lies strictly between low and high

    def with_facts(self, equations) -> "Theory":
        """Add derived equations (already verified consequences of the givens)."""
        extra = tuple(l - r for l, r in equations if (l - r) not in self.hypotheses)
        return replace(self, hypotheses=self.hypotheses + extra)

    def expand_definitions(self, e: s.Expr) -> s.Expr:
        if self.points:
            e = expand_geometry(e, {name: (x, y) for name, x, y in self.points})
        for name, variable, expr in self.definitions:
            e = e.replace(named_class(name), lambda arg, v=variable, x=expr: x.xreplace({v: arg}))
        for name, kind, a, step in self.sequences:
            e = e.replace(term_class(name), lambda k, kind=kind, a=a, step=step: term_formula(kind, a, step, k))
            e = e.replace(sum_class(name), lambda n, kind=kind, a=a, step=step: sum_formula(kind, a, step, n))
        return e


def sc_pair(angle: s.Expr) -> tuple[s.Symbol, s.Symbol]:
    return s.Symbol(f"sin({angle})"), s.Symbol(f"cos({angle})")


def trig_angles(e: s.Expr) -> list:
    return sorted({f.args[0] for f in e.atoms(s.Function) if f.func in TRIG}, key=str)


@lru_cache(None)
def to_sc(e: s.Expr) -> s.Expr:
    """Rewrite all trig functions with sin/cos symbols; no identity is applied."""
    mapping = {}
    for f in e.atoms(s.Function):
        if f.func in TRIG:
            S, C = sc_pair(f.args[0])
            mapping[f] = {s.sin: S, s.cos: C, s.tan: S/C, s.cot: C/S, s.sec: 1/C, s.csc: 1/S}[f.func]
    return e.xreplace(mapping)


def _rational_log(q: s.Rational) -> s.Expr:
    """log(p1^k1 ... / ...) as k1 log p1 + ... (exact for positive rationals)."""
    total = s.Integer(0)
    for part, sign in ((q.p, 1), (q.q, -1)):
        for prime, power in s.factorint(part).items():
            total += sign*power*s.log(prime)
    return total


@lru_cache(None)
def log_normal(e: s.Expr) -> s.Expr:
    """Normal form for logs and real powers. Uses positivity recorded by the parser."""
    is_real_power = lambda p: p.is_Pow and not p.exp.is_Number and not p.exp.is_integer
    if not (e.has(s.log, s.exp) or any(is_real_power(p) for p in e.atoms(s.Pow))):
        return e
    e = e.replace(is_real_power, lambda p: s.exp(p.exp*s.log(p.base)))
    e = s.expand_log(e, force=True)
    e = e.replace(lambda f: f.func == s.log and f.args[0].is_Rational and f.args[0] > 0,
                  lambda f: _rational_log(f.args[0]))
    e = e.replace(lambda f: f.func == s.exp, lambda f: s.exp(s.expand(f.args[0])))
    e = s.powsimp(e, combine="exp")
    return e.replace(lambda f: f.func == s.exp, lambda f: s.exp(s.expand(f.args[0])))


@lru_cache(None)
def freeze(e: s.Expr) -> s.Expr:
    """Replace every function application by an independent symbol (pure algebra view)."""
    mapping = {f: s.Symbol(str(f)) for f in e.atoms(s.Function)}
    return e.xreplace(mapping)


@lru_cache(None)
def angle_normal(e: s.Expr) -> s.Expr:
    """Express every trig function through base angles, so related angles (A, B and A - B;
    x, 3x and 27x; alpha/2 and alpha) share variables. Each angle must be a rational
    combination of variables plus a rational multiple of pi; the base for variable v is
    v/L, with L the lcm of v's coefficient denominators. Anything else is left alone,
    which can only make equality harder to prove, never wrong."""
    functions = [f for f in e.atoms(s.Function) if f.func in TRIG and f.args[0].free_symbols]
    if not functions or all(f.args[0].is_Symbol for f in functions) and len({f.args[0] for f in functions}) == 1:
        return e
    scale = {}
    for f in functions:
        angle = f.args[0]
        if not angle.is_polynomial(*angle.free_symbols) or s.Poly(angle, *angle.free_symbols).total_degree() > 1:
            return e
        for v in angle.free_symbols:
            c = angle.coeff(v)
            if not c.is_Rational:
                return e
            scale[v] = s.ilcm(scale.get(v, 1), c.q)
        constant = angle.subs({v: 0 for v in angle.free_symbols})
        if not (constant/s.pi).is_Rational:
            return e
    base = {v: v if k == 1 else s.Symbol(f"({v})/{k}", real=True) for v, k in scale.items()}
    mapping = {}
    for f in functions:
        angle = f.args[0].xreplace({v: k*base[v] for v, k in scale.items()})
        mapping[f] = s.expand_trig(f.func(s.expand(angle)))
    return e.xreplace(mapping)


@lru_cache(None)
def normal(e: s.Expr) -> s.Expr:
    return freeze(log_normal(to_sc(angle_normal(e))))


TEST_FUNCTIONS = (lambda u: s.exp(u/3) + u**2, lambda u: s.sin(u) + 2, lambda u: 1/(u**2 + 1))


def integrals_equal(difference: s.Expr) -> bool:
    """Definite integrals: the difference is 0 to 30 digits by numerical integration. An
    unspecified function f is replaced by several test functions and each free symbol by
    test values, so a property of integrals is checked on many instances. Evaluation steps
    are also checked exactly in verify.py, by differentiating the antiderivative back."""
    difference = difference.replace(lambda b: type(b).__name__ == "Bracket", lambda b: b.doit())
    unknowns = difference.atoms(AppliedUndef)
    names = {f.func for f in unknowns}
    symbols = sorted(difference.free_symbols, key=str)
    instances = TEST_FUNCTIONS if names else (None,)
    values = ([{v: s.Rational(k + 2, 3) for k, v in enumerate(symbols)},
               {v: s.Rational(7, k + 3) for k, v in enumerate(symbols)}] if symbols else [{}])
    for test in instances:
        expr = difference
        if test is not None:
            expr = expr.replace(lambda f: f.func in names, lambda f: test(f.args[0]))
        for point in values:
            try:
                value = complex(integral_value(expr.subs(point)))
            except (TypeError, ValueError, ZeroDivisionError):
                return False
            if abs(value) > 1e-12:
                return False
    return True


def integral_value(e: s.Expr):
    """Numerical value, with each definite integral done by mpmath's quadrature (20 digits)."""
    import mpmath
    mpmath.mp.dps = 20
    def quadrature(integral):
        (x, low, high), = integral.limits
        f = s.lambdify(x, integral.function, "mpmath")
        return s.Float(mpmath.quad(f, [float(s.N(low, 20)), float(s.N(high, 20))]), 20)
    while e.has(s.Integral):
        innermost = [i for i in e.atoms(s.Integral) if not i.function.has(s.Integral)]
        e = e.xreplace({i: quadrature(i) for i in innermost})
    return s.N(e, 20)


def numbers_equal(a: s.Expr, b: s.Expr) -> bool:
    """Exact test for two closed-form numbers (e.g. cos 20 deg cos 40 deg cos 80 deg = 1/8)."""
    difference = a - b
    if difference == 0:
        return True
    x = s.Dummy("x")
    try:
        return s.minimal_polynomial(difference, x) == x
    except (NotImplementedError, ValueError, s.polys.polyerrors.NotAlgebraic):
        return False


@lru_cache(None)
def algebra_view(e: s.Expr) -> s.Expr:
    """Pure algebra: functions, surds and real powers become independent symbols, so a
    closing 'simplify' step cannot hide index laws, log laws or surd arithmetic."""
    e = freeze(e)
    powers = {p: s.Symbol(f"pow({p})") for p in e.atoms(s.Pow)
              if not p.exp.is_Integer and not p.exp.is_integer}
    return e.xreplace(powers)


VIEWS = {"algebra_finish": algebra_view, "reciprocal_quotient_finish": lambda e: algebra_view(to_sc(e))}


def finish_holds(rule: str, a: s.Expr, b: s.Expr) -> bool:
    """The two closing moves: pure algebra, or algebra after reciprocal/quotient rewriting."""
    if rule not in VIEWS:
        return False
    return s.cancel(VIEWS[rule](a) - VIEWS[rule](b)) == 0


def _numerator(e: s.Expr) -> s.Expr:
    return s.expand(s.fraction(s.cancel(e))[0])


def _prepare(polys: list) -> tuple[list, list]:
    """Replace each surd b^(p/q) by a symbol g with g^q = b^p, and add sin^2 + cos^2 = 1
    for each angle. Returns the rewritten polynomials and their generators."""
    surds = {}
    for p in polys:
        for g in p.atoms(s.Pow):
            if g.exp.is_Rational and not g.exp.is_Integer:
                surds[g] = s.Symbol(f"surd({g})")
    constants = {c: s.Symbol(f"const({c})") for p in polys for c in p.atoms(s.NumberSymbol)}  # pi is transcendental
    polys = [s.expand(p.xreplace(surds).xreplace(constants)) for p in polys]
    relations = [symbol**g.exp.q - g.base**g.exp.p for g, symbol in surds.items()]
    relations += [s.Symbol(f"inv({c})")*symbol - 1 for c, symbol in constants.items()]  # pi != 0
    names = {str(x) for p in polys for x in p.free_symbols}
    angles = {n[4:-1] for n in names if n.startswith(("sin(", "cos("))}
    relations += [s.Symbol(f"sin({a})")**2 + s.Symbol(f"cos({a})")**2 - 1 for a in sorted(angles)]
    found = set()
    for p in polys + relations:
        if not p.is_Number:
            found |= set(s.Poly(p).gens)
    return polys + relations, sorted(found, key=str)


@lru_cache(None)
def hypothesis_ideal(theory: Theory) -> tuple:
    return tuple(_numerator(normal(theory.expand_definitions(h))) for h in theory.hypotheses)


def in_ideal(target: s.Expr, ideal: list) -> bool:
    if target == 0:
        return True
    ideal = [p for p in ideal if p != 0]
    polys, gens = _prepare([target] + ideal)
    if len(polys) == 1:
        return polys[0] == 0
    return s.groebner(polys[1:], *gens, order="grevlex", domain="QQ").reduce(polys[0])[1] == 0


def in_radical(target: s.Expr, ideal: list, nonzero: s.Expr = s.Integer(1)) -> bool:
    """target vanishes on every common zero of the ideal where `nonzero` is nonzero."""
    polys, gens = _prepare([p for p in ideal if p != 0] + [1 - T*target, Z*nonzero - 1])
    return list(s.groebner(polys, *gens, order="grevlex", domain="QQ")) == [s.Integer(1)]


INVERSE_TRIG = (s.asin, s.acos, s.atan, s.acot)


def _piece_bounds(expr: s.Expr, v: s.Symbol, low, high, pieces: int = 128):
    """Guaranteed lower bound of expr on each of `pieces` equal parts of [low, high]
    (mpmath interval arithmetic), or None if it cannot be evaluated."""
    import mpmath
    iv = mpmath.iv
    iv.dps = 30
    try:
        f = s.lambdify(v, expr, modules=[{"mpf": iv.mpf, "sin": iv.sin, "cos": iv.cos, "tan": iv.tan, "sqrt": iv.sqrt,
                                          "exp": iv.exp, "log": iv.log, "pi": iv.pi}, "mpmath"])
        a, b = (iv.mpf(str(s.N(x, 40))) for x in (low, high))
        a, b = a.a, b.b  # widen to cover the exact endpoints
        width = (b - a)/pieces
        return [iv.mpf(f(iv.mpf([a + k*width, a + (k + 1)*width]))).a for k in range(pieces)]
    except Exception:
        return None


def _interval_bounds(expr: s.Expr, v: s.Symbol, low, high):
    bounds = _piece_bounds(expr, v, low, high)
    return None if bounds is None else min(bounds)


def _positive_inside(expr: s.Expr, v: s.Symbol, low, high, strict: bool) -> bool:
    """expr > 0 (or >= 0) for low < v < high, by interval arithmetic. A zero at an excluded
    endpoint is allowed when expr is >= 0 there and moves away from zero on the end piece
    (derivative positive at the low end, negative at the high end)."""
    bounds = _piece_bounds(expr, v, low, high)
    if bounds is None:
        return False
    good = [b > 0 if strict else b >= 0 for b in bounds]
    if not all(good[1:-1]):
        return False
    derivative = s.diff(expr, v)
    for index, end, sign in ((0, low, 1), (len(bounds) - 1, high, -1)):
        if good[index]:
            continue
        at_end = s.N(expr.xreplace({v: end}), 50)
        if not at_end.is_real or at_end < -s.Float("1e-45"):
            return False
        piece = (high - low)/len(bounds)
        part = (end, end + piece) if sign == 1 else (end - piece, end)
        slope = _piece_bounds(sign*derivative, v, *part, pieces=8)
        if slope is None or not all(b > 0 for b in slope):
            return False
    return True


@lru_cache(None)
def positive_on(expr: s.Expr, theory: Theory, strict: bool = True) -> bool:
    """expr > 0 (or >= 0) for every admissible value. A number: its sign to 50 digits. One
    variable with an interval in the spec (strictly between low and high): SymPy's minimum on
    the closed interval (a zero only at an excluded endpoint is allowed), else a guaranteed
    lower bound from interval arithmetic."""
    if expr.is_number:
        value = s.N(expr, 50)
        if not value.is_real:
            return False
        return bool(value > s.Float("1e-40")) if strict else bool(value >= 0)
    symbols = expr.free_symbols
    intervals = {v: (low, high) for v, low, high in theory.intervals}
    if len(symbols) != 1 or next(iter(symbols)) not in intervals:
        return False
    v = next(iter(symbols))
    low, high = intervals[v]
    if _positive_inside(expr, v, low, high, strict):  # fast and guaranteed
        return True
    if s.count_ops(expr) > 12:
        return False  # SymPy's minimum is too slow on large expressions; interval arithmetic was inconclusive
    try:
        least = s.minimum(expr, v, s.Interval(low, high))
        if least is not None and least.is_number:
            least = s.N(least, 50)
            if least > s.Float("1e-40"):
                return True
            if abs(least) <= s.Float("1e-40"):
                inside = s.solveset(expr, v, s.Interval.open(low, high))
                return inside == s.S.EmptySet if strict else True
            return False
    except (NotImplementedError, ValueError, TypeError):
        pass
    return False


def _inverse_equal(a: s.Expr, b: s.Expr, theory: Theory) -> bool:
    """Equality of expressions with inverse trig functions, which Groebner bases do not cover.
    The same inverse function on both sides: compare the arguments exactly. Otherwise compare
    to 50 digits: a number directly, a function of one variable at 12 points inside its stated
    interval. The rules that change an inverse function prove their branch condition themselves."""
    if type(a) is type(b) and isinstance(a, INVERSE_TRIG) and exact_equal(a.args[0], b.args[0], theory):
        return True
    return _interval_numeric(a - b, theory)


def _interval_numeric(difference: s.Expr, theory: Theory) -> bool:
    symbols = difference.free_symbols
    if not symbols:
        return abs(s.N(difference, 60)) < s.Float("1e-45")
    intervals = {v: (low, high) for v, low, high in theory.intervals}
    if not symbols <= set(intervals):
        return False
    for k in range(1, 13):
        point = {v: low + (high - low)*s.Rational(k, 13) + (high - low)*s.Rational(1, 997)
                 for v, (low, high) in intervals.items() if v in symbols}
        value = s.N(difference.xreplace(point), 60)
        if not value.is_number or abs(value) > s.Float("1e-40"):
            return False
    return True


@lru_cache(None)
def exact_equal(a: s.Expr, b: s.Expr, theory: Theory = Theory()) -> bool:
    try:
        if _exact_equal(a, b, theory):
            return True
    except (s.PolynomialError, s.GeneratorsNeeded, NotImplementedError):
        pass
    # An inverse trig function is an opaque atom above; an identity that changes it (2 tan^-1 x = ...)
    # holds only on a branch, and is compared as described in _inverse_equal.
    if (a - b).has(*INVERSE_TRIG):
        return _inverse_equal(theory.expand_definitions(a), theory.expand_definitions(b), theory)
    return False


def _exact_equal(a: s.Expr, b: s.Expr, theory: Theory) -> bool:
    if theory.intervals and any(p.exp == s.Rational(1, 2) for p in (a - b).atoms(s.Pow)):
        # Groebner bases prove a square root only up to sign; on the stated interval the branch
        # is fixed, so the sides are compared there (see _interval_numeric).
        return _interval_numeric(theory.expand_definitions(a - b), theory)
    difference = theory.expand_definitions(a - b)
    difference = difference.replace(lambda x: type(x).__name__ == "Bracket", lambda x: x.doit())
    if difference.has(s.Derivative):
        difference = difference.replace(lambda d: isinstance(d, s.Derivative), lambda d: d.doit())
    if difference.has(s.Integral):
        return integrals_equal(difference)
    if not difference.free_symbols and numbers_equal(difference, s.Integer(0)):
        return True  # otherwise (e.g. logs, which are not algebraic numbers) use the normal form below
    if any(p.exp == s.Rational(1, 2) for p in difference.atoms(s.Pow)) and s.expand(difference) == 0:
        # SymPy takes a square root of a square using the declared signs (sqrt(d^2/4) = d/2 for d >= 0),
        # which Groebner bases cannot: they know a root only up to sign.
        return True
    n = _numerator(normal(difference))
    hyps = list(hypothesis_ideal(theory))
    if in_ideal(n, hyps):
        return True
    if not hyps:
        return False
    return in_radical(n, hyps, s.prod(theory.domain))


def denominator_factors(e: s.Expr, theory: Theory = Theory()) -> tuple:
    """Nonzero factors an expression needs, in normal form. Poles are kept even if removable.
    An integral's own variable is bound, so its integrand's poles are not conditions on the
    answer (verify.py checks the integrand has no pole between the limits instead)."""
    e = e.replace(lambda i: isinstance(i, s.Integral) or type(i).__name__ == "Bracket", lambda i: s.Dummy("bound"))
    polynomials = []
    for f in e.atoms(s.Function):
        if f.func in (s.tan, s.sec):
            polynomials.append(_numerator(normal(s.cos(f.args[0]))))
        elif f.func in (s.cot, s.csc):
            polynomials.append(_numerator(normal(s.sin(f.args[0]))))
    for p in e.atoms(s.Pow):
        if p.exp.is_Number and p.exp < 0:
            polynomials.append(_numerator(normal(theory.expand_definitions(p.base))))
    factors = set()
    for p in polynomials:
        if p.is_Number:
            continue
        for factor, _ in s.factor_list(p)[1]:
            factors.add(factor)
    return tuple(sorted(factors, key=str))


def certified_nonzero(e: s.Expr, theory: Theory) -> bool:
    """Certificate that e cannot vanish where the givens hold and the domain is defined."""
    if e.is_number:
        return abs(complex(s.N(e, 30))) > 1e-20
    numerator, denominator = s.fraction(s.cancel(normal(theory.expand_definitions(e))))
    original = s.prod(theory.domain)
    for f, _ in s.factor_list(s.expand(numerator))[1]:
        if f.is_number or f.is_nonzero or f in theory.domain:
            continue  # a nonzero constant such as pi, or nonzero by the declared domains (e.g. r > 0)
        polys, gens = _prepare([f, Z*original - 1] + list(hypothesis_ideal(theory)))
        if list(s.groebner(polys, *gens, domain="QQ")) != [s.Integer(1)]:
            return False
    return True


@lru_cache(None)
def _signed_denominators(e: s.Expr, theory: Theory) -> bool:
    """Every denominator keeps one sign on the stated interval, so none can vanish there."""
    bases = [p.base for p in e.atoms(s.Pow) if p.exp.is_Number and p.exp < 0]
    bases += [s.cos(f.args[0]) for f in e.atoms(s.tan, s.sec)] + [s.sin(f.args[0]) for f in e.atoms(s.cot, s.csc)]
    intervals = {v: (low, high) for v, low, high in theory.intervals}

    def one_sign(b):
        if len(b.free_symbols) == 1 and next(iter(b.free_symbols)) in intervals:
            v = next(iter(b.free_symbols))
            if any(_positive_inside(c, v, *intervals[v], strict=True) for c in (b, -b)):
                return True  # interval arithmetic first: fast and guaranteed
        return positive_on(b, theory) or positive_on(-b, theory)
    return all(one_sign(b) for b in bases)


def domain_safe(e: s.Expr, theory: Theory) -> bool:
    """A new denominator is allowed only with a certificate that it cannot vanish."""
    if e.has(s.zoo, s.oo, -s.oo, s.nan):
        return False
    if theory.intervals and _signed_denominators(e, theory):
        return True
    original = s.prod(theory.domain)
    for f in denominator_factors(e, theory):
        if f in theory.domain or f.is_nonzero:  # e.g. 6x + 5 when x is declared positive
            continue
        polys, gens = _prepare([f, Z*original - 1] + list(hypothesis_ideal(theory)))
        if list(s.groebner(polys, *gens, domain="QQ")) != [s.Integer(1)]:
            return False
    return True

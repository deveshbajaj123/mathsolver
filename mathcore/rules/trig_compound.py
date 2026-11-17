"""Compound, double, triple and half angles; sum-to-product and back; special values.

Each rule rewrites the first pattern it can in every term, and is checked like any
other rule (exact equality through the angle basis, numeric check, domain certificate).
"""
from __future__ import annotations

import sympy as s

from .base import static

SIN, COS, TAN, COT = s.sin, s.cos, s.tan, s.cot


def _terms(e: s.Expr) -> list:
    return list(s.Add.make_args(e))


def _rebuild(terms: list) -> s.Expr:
    return s.Add(*terms)


# --- compound angles -------------------------------------------------------

def _compound(f):
    angle = f.args[0]
    if not angle.is_Add:
        return f
    a, b = angle.args[0], s.Add(*angle.args[1:])
    if f.func == SIN:
        return SIN(a)*COS(b) + COS(a)*SIN(b)
    if f.func == COS:
        return COS(a)*COS(b) - SIN(a)*SIN(b)
    if f.func == TAN:
        return (TAN(a) + TAN(b))/(1 - TAN(a)*TAN(b))
    if f.func == COT:
        return (COT(a)*COT(b) - 1)/(COT(a) + COT(b))
    return f


def compound_angle(e: s.Expr) -> s.Expr:
    return e.replace(lambda f: f.func in (SIN, COS, TAN, COT) and f.args[0].is_Add and f.args[0].free_symbols,
                     _compound)


# --- double and triple angles --------------------------------------------

def _multiple(f, n):
    if f.func not in (SIN, COS, TAN):
        return False
    c, rest = f.args[0].as_coeff_Mul()
    return bool(c.is_Integer and c % n == 0 and rest.free_symbols)


def _double(form):
    def expand(f):
        u = f.args[0]/2
        if f.func == SIN:
            return 2*SIN(u)*COS(u)
        if f.func == TAN:
            return 2*TAN(u)/(1 - TAN(u)**2)
        return {"cos2": COS(u)**2 - SIN(u)**2, "cos": 2*COS(u)**2 - 1, "sin": 1 - 2*SIN(u)**2}[form]
    applies = (lambda f: _multiple(f, 2)) if form == "cos2" else (lambda f: _multiple(f, 2) and f.func == COS)
    return lambda e: e.replace(applies, expand)


def triple_angle(e: s.Expr) -> s.Expr:
    def expand(f):
        u = f.args[0]/3
        return {SIN: 3*SIN(u) - 4*SIN(u)**3, COS: 4*COS(u)**3 - 3*COS(u)}.get(f.func, f)
    return e.replace(lambda f: _multiple(f, 3) and f.func in (SIN, COS), expand)


def double_angle_contract(e: s.Expr) -> s.Expr:
    """sin u cos u = (1/2) sin 2u, wherever both appear to the first power in a product."""
    def contract(term):
        factors = s.Mul.make_args(term)
        for f in factors:
            if f.func == SIN and COS(f.args[0]) in factors:
                u = f.args[0]
                rest = [g for g in factors if g not in (f, COS(u))]
                return s.Mul(*rest)*SIN(2*u)/2
        return term
    return _rebuild([contract(t) for t in _terms(e)])


def cos_double_contract(e: s.Expr) -> s.Expr:
    for u in sorted({f.args[0] for f in e.atoms(SIN, COS)}, key=str):
        e = e.subs(COS(u)**2 - SIN(u)**2, COS(2*u)).subs(1 - 2*SIN(u)**2, COS(2*u)).subs(2*COS(u)**2 - 1, COS(2*u))
    return e


# --- half angles ------------------------------------------------------------

def half_angle(e: s.Expr) -> s.Expr:
    """1 - cos u = 2 sin^2(u/2) and 1 + cos u = 2 cos^2(u/2)."""
    for u in sorted({f.args[0] for f in e.atoms(COS)}, key=str):
        e = e.subs(1 - COS(u), 2*SIN(u/2)**2).subs(1 + COS(u), 2*COS(u/2)**2)
    return e


def to_half_angles(e: s.Expr) -> s.Expr:
    """sin u = 2 sin(u/2) cos(u/2), only where the half angle u/2 already appears."""
    present = {f.args[0] for f in e.atoms(SIN, COS, TAN)}
    return e.xreplace({f: 2*SIN(f.args[0]/2)*COS(f.args[0]/2) for f in e.atoms(SIN) if f.args[0]/2 in present})


def tan_square_half(e: s.Expr) -> s.Expr:
    """tan^2 v = (1 - cos 2v)/(1 + cos 2v)."""
    return e.replace(lambda p: p.is_Pow and p.exp == 2 and p.base.func == TAN,
                     lambda p: (1 - COS(2*p.base.args[0]))/(1 + COS(2*p.base.args[0])))


# --- sums and products ------------------------------------------------------

def _pair(terms, function):
    for i, t in enumerate(terms):
        c1, f1 = t.as_coeff_Mul()
        if f1.func != function:
            continue
        for j in range(i + 1, len(terms)):
            c2, f2 = terms[j].as_coeff_Mul()
            if f2.func == function and abs(c1) == abs(c2):
                return i, j, c1, f1.args[0], c2, f2.args[0]
    return None


def sum_to_product(e: s.Expr) -> s.Expr:
    terms = _terms(e)
    for function in (SIN, COS):
        found = _pair(terms, function)
        if not found:
            continue
        i, j, c1, p, c2, q = found
        half_sum, half_difference = (p + q)/2, (p - q)/2
        if function == SIN:
            combined = 2*SIN(half_sum)*COS(half_difference) if c1 == c2 else 2*COS(half_sum)*SIN(half_difference)
        else:
            combined = 2*COS(half_sum)*COS(half_difference) if c1 == c2 else -2*SIN(half_sum)*SIN(half_difference)
        rest = [t for k, t in enumerate(terms) if k not in (i, j)]
        return _rebuild(rest + [c1*combined])
    return e


def product_to_sum(e: s.Expr) -> s.Expr:
    def split(term):
        factors = list(s.Mul.make_args(term))
        trig = [f for f in factors if f.func in (SIN, COS)]
        if len(trig) < 2:
            return term
        f, g = trig[0], trig[1]
        if f.func == COS and g.func == SIN:
            f, g = g, f
        p, q = f.args[0], g.args[0]
        if f.func == SIN and g.func == COS:
            value = (SIN(p + q) + SIN(p - q))/2
        elif f.func == COS:
            value = (COS(p + q) + COS(p - q))/2
        else:
            value = (COS(p - q) - COS(p + q))/2
        rest = list(factors)
        rest.remove(trig[0])
        rest.remove(trig[1])
        return s.Mul(*rest)*value
    return _rebuild([split(t) for t in _terms(e)])


def tan_difference(e: s.Expr) -> s.Expr:
    """tan P - tan Q = sin(P - Q)/(cos P cos Q)."""
    terms = _terms(e)
    found = _pair(terms, TAN)
    if not found:
        return e
    i, j, c1, p, c2, q = found
    if c1 != -c2:
        return e
    rest = [t for k, t in enumerate(terms) if k not in (i, j)]
    return _rebuild(rest + [c1*SIN(p - q)/(COS(p)*COS(q))])


def tan_difference_contract(e: s.Expr) -> s.Expr:
    """sin(P - Q)/(cos P cos Q) = tan P - tan Q, in every term where it fits."""
    def contract(term):
        factors = s.Mul.make_args(term)
        sines = [f for f in factors if f.func == SIN]
        cosines = [f.base.args[0] for f in factors if f.is_Pow and f.exp == -1 and f.base.func == COS]
        for sine in sines:
            for p in cosines:
                for q in cosines:
                    if p != q and s.expand(sine.args[0] - (p - q)) == 0:
                        rest = [g for g in factors if g not in (sine, COS(p)**-1, COS(q)**-1)]
                        return s.Mul(*rest)*(TAN(p) - TAN(q))
        return term
    return _rebuild([contract(t) for t in _terms(e)])


def multiply_by_cos(e: s.Expr) -> s.Expr:
    """sin u / cos v = sin u cos u / (cos u cos v): multiply above and below by cos u."""
    def widen(term):
        factors = s.Mul.make_args(term)
        sines = [f for f in factors if f.func == SIN]
        cosines = [f.base for f in factors if f.is_Pow and f.exp == -1 and f.base.func == COS]
        if len(sines) == 1 and len(cosines) == 1 and cosines[0].args[0] != sines[0].args[0]:
            u = sines[0].args[0]
            return s.Mul(*factors, COS(u), s.Pow(COS(u), -1, evaluate=False), evaluate=False)
        return term
    terms = [widen(t) for t in _terms(e)]
    return s.Add(*terms, evaluate=False) if len(terms) > 1 else terms[0]


# --- special angles ------------------------------------------------------------

def special_values(e: s.Expr) -> s.Expr:
    def value(f):
        evaluated = f.func(f.args[0])
        return evaluated if not evaluated.has(f.func) else f
    return e.replace(lambda f: f.func in (SIN, COS, TAN, COT) and f.args[0].is_number, value)


def reduce_angle(e: s.Expr) -> s.Expr:
    """sin(180 deg - t) = sin t and cos(180 deg - t) = -cos t, for numeric angles past 90 deg."""
    def reduce(f):
        ratio = f.args[0]/s.pi
        if not (ratio.is_Rational and s.Rational(1, 2) < ratio < 1):
            return f
        other = s.pi - f.args[0]
        return SIN(other, evaluate=False) if f.func == SIN else -COS(other, evaluate=False)
    return e.replace(lambda f: f.func in (SIN, COS) and f.args[0].is_number, reduce)


static("compound_angle", "trig_compound", "Use the compound-angle formula.", compound_angle)
static("double_angle_sin", "trig_compound", r"Use $\sin 2A = 2\sin A\cos A$ (and $\cos 2A = \cos^2 A - \sin^2 A$).", _double("cos2"))
static("double_angle_cos_c", "trig_compound", r"Use $\cos 2A = 2\cos^2 A - 1$.", _double("cos"))
static("double_angle_cos_s", "trig_compound", r"Use $\cos 2A = 1 - 2\sin^2 A$.", _double("sin"))
static("triple_angle", "trig_compound", r"Use $\sin 3A = 3\sin A - 4\sin^3 A$ and $\cos 3A = 4\cos^3 A - 3\cos A$.", triple_angle)
static("double_angle_contract", "trig_compound", r"Use $2\sin A\cos A = \sin 2A$.", double_angle_contract)
static("cos_double_contract", "trig_compound", r"Use $\cos^2 A - \sin^2 A = \cos 2A$.", cos_double_contract)
static("half_angle", "trig_compound", r"Use $1 - \cos A = 2\sin^2\frac{A}{2}$ and $1 + \cos A = 2\cos^2\frac{A}{2}$.", half_angle)
static("to_half_angles", "trig_compound", r"Use $\sin A = 2\sin\frac{A}{2}\cos\frac{A}{2}$.", to_half_angles)
static("tan_square_half", "trig_compound", r"Use $\tan^2\theta = \frac{1 - \cos 2\theta}{1 + \cos 2\theta}$.", tan_square_half)
static("sum_to_product", "trig_compound", r"Use the sum-to-product formulae, e.g. $\sin P + \sin Q = 2\sin\frac{P+Q}{2}\cos\frac{P-Q}{2}$.", sum_to_product)
static("product_to_sum", "trig_compound", r"Use the product-to-sum formulae, e.g. $2\cos P\cos Q = \cos(P+Q) + \cos(P-Q)$.", product_to_sum)
static("tan_difference", "trig_compound", r"Use $\tan P - \tan Q = \frac{\sin(P-Q)}{\cos P\cos Q}$.", tan_difference)
static("tan_difference_contract", "trig_compound", r"Use $\frac{\sin(P-Q)}{\cos P\cos Q} = \tan P - \tan Q$.", tan_difference_contract)
static("multiply_by_cos", "trig_compound", r"Multiply the numerator and denominator by $\cos$ of the numerator's angle.", multiply_by_cos)
static("special_values", "trig_compound", "Use the values of the trigonometric ratios of standard angles.", special_values)
static("reduce_angle", "trig_compound", r"Use $\sin(180^\circ - \theta) = \sin\theta$ and $\cos(180^\circ - \theta) = -\cos\theta$.", reduce_angle)

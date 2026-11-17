"""Inverse trigonometric rules. Each identity holds only on a branch, so every rule first
proves its branch condition and does nothing if it cannot:

- for a number, by evaluating to 50 digits (the sign of a nonzero number is then certain);
- for an expression in one variable, by SymPy's minimum over the interval the spec states
  for that variable (spec field "intervals").

verify.py replays each rule (so the condition is proved again) and compares both sides
numerically at points inside the interval.
"""
from __future__ import annotations

import sympy as s

from ..equality import Theory, positive_on
from .base import Rule, register

INVERSE = (s.asin, s.acos, s.atan, s.acot)


def _terms(e: s.Expr):
    return s.Add.make_args(e)


def _rule(name: str, reason: str, rewrite_term, theory: Theory) -> Rule:
    """A rule that rewrites the first term of a sum it applies to."""
    def transform(e: s.Expr) -> s.Expr:
        for term in sorted(e.atoms(s.Function, s.Mul, s.Pow), key=s.default_sort_key):
            new = rewrite_term(term, theory)
            if new is not None:
                return e.xreplace({term: new})
        return e
    return Rule(name, reason, transform, "inverse_trig")


@register("double_tan_inverse", "inverse_trig")
def double_tan_inverse(theory: Theory) -> Rule:
    def rewrite(term, theory):
        if term.is_Mul and term.args[0] == 2 and len(term.args) == 2 and isinstance(term.args[1], s.atan):
            a = term.args[1].args[0]
            if positive_on(1 - a**2, theory):
                return s.atan(2*a/(1 - a**2))
        return None
    return _rule("double_tan_inverse", r"Use $2\tan^{-1} x = \tan^{-1}\frac{2x}{1 - x^{2}}$, valid as $|x| < 1$.",
                 rewrite, theory)


@register("cos_inverse_to_tan_inverse", "inverse_trig")
def cos_inverse_to_tan_inverse(theory: Theory) -> Rule:
    def rewrite(term, theory):
        if isinstance(term, s.acos):
            a = term.args[0]
            if positive_on(a, theory) and positive_on(1 - a**2, theory, strict=False):
                return s.atan(s.sqrt(1 - a**2)/a)
        return None
    return _rule("cos_inverse_to_tan_inverse",
                 r"Use $\cos^{-1} x = \tan^{-1}\frac{\sqrt{1 - x^{2}}}{x}$, valid as $0 < x \le 1$.", rewrite, theory)


@register("sin_inverse_to_tan_inverse", "inverse_trig")
def sin_inverse_to_tan_inverse(theory: Theory) -> Rule:
    def rewrite(term, theory):
        if isinstance(term, s.asin):
            a = term.args[0]
            if positive_on(1 - a**2, theory):
                return s.atan(a/s.sqrt(1 - a**2))
        return None
    return _rule("sin_inverse_to_tan_inverse",
                 r"Use $\sin^{-1} x = \tan^{-1}\frac{x}{\sqrt{1 - x^{2}}}$, valid as $|x| < 1$.", rewrite, theory)


@register("tan_inverse_sum", "inverse_trig")
def tan_inverse_sum(theory: Theory) -> Rule:
    def transform(e: s.Expr) -> s.Expr:
        terms = [t for t in _terms(e) if isinstance(t, s.atan)]
        for i, first in enumerate(terms):
            for second in terms[i + 1:]:
                a, b = first.args[0], second.args[0]
                if positive_on(1 - a*b, theory):
                    rest = [t for t in _terms(e) if t not in (first, second)]
                    return s.Add(s.atan((a + b)/(1 - a*b)), *rest)
        return e
    return Rule("tan_inverse_sum", r"Use $\tan^{-1} x + \tan^{-1} y = \tan^{-1}\frac{x + y}{1 - xy}$, valid as $xy < 1$.",
                transform, "inverse_trig")


def _cot_angle(arg: s.Expr):
    """u when arg is written as cot u or cos u / sin u."""
    if isinstance(arg, s.cot):
        return arg.args[0]
    numerator, denominator = arg.as_numer_denom()
    if isinstance(numerator, s.cos) and isinstance(denominator, s.sin) and numerator.args[0] == denominator.args[0]:
        return numerator.args[0]
    return None


@register("inverse_of_cot", "inverse_trig")
def inverse_of_cot(theory: Theory) -> Rule:
    def rewrite(term, theory):
        if isinstance(term, s.acot):
            u = _cot_angle(term.args[0])
            if u is not None and positive_on(u, theory) and positive_on(s.pi - u, theory):
                return u
        if isinstance(term, s.atan) and isinstance(term.args[0], s.tan):
            u = term.args[0].args[0]
            if positive_on(u + s.pi/2, theory) and positive_on(s.pi/2 - u, theory):
                return u
        return None
    return _rule("inverse_of_cot", r"Use $\cot^{-1}(\cot u) = u$ for $0 < u < \pi$ (and $\tan^{-1}(\tan u) = u$ "
                 r"for $-\frac{\pi}{2} < u < \frac{\pi}{2}$); the given interval puts $u$ there.", rewrite, theory)


@register("half_angle_root", "inverse_trig")
def half_angle_root(theory: Theory) -> Rule:
    def rewrite(term, theory):
        if not (term.is_Pow and term.exp == s.Rational(1, 2)):
            return None
        base = term.base
        for f in (s.sin, s.cos):
            for sign in (1, -1):
                for v in {g.args[0] for g in base.atoms(f)}:
                    if s.expand(base - (1 + sign*f(v))) != 0:
                        continue
                    c, h = s.cos(v/2), s.sin(v/2)
                    root = c + sign*h if f is s.sin else (s.sqrt(2)*c if sign == 1 else s.sqrt(2)*h)
                    if positive_on(root, theory, strict=False):
                        return root
        return None
    return _rule("half_angle_root",
                 r"Use $1 \pm \sin x = \left(\cos\frac{x}{2} \pm \sin\frac{x}{2}\right)^{2}$ (and $1 + \cos x = "
                 r"2\cos^{2}\frac{x}{2}$, $1 - \cos x = 2\sin^{2}\frac{x}{2}$); the root is the nonnegative one on the "
                 r"given interval.", rewrite, theory)

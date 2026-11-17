"""Calculus rules: differentiation (explicit, implicit, logarithmic), definitions, and
definite integrals (antiderivative, reflection property, change of variable).

A function y of x is represented by a symbol y with derivative symbols y1, y2 (school
notation y₁, y₂); the total derivative of an expression is ∂/∂x plus ∂/∂y·y1 plus
∂/∂y1·y2, i.e. the chain rule. Differentiating both sides of an equation that holds for
every x keeps it true; verify.py replays every differentiation exactly.
"""
from __future__ import annotations

import sympy as s
from sympy.core.function import AppliedUndef

from ..equality import Theory
from .base import Rule, register, static


def total_derivative(e: s.Expr, variable: s.Symbol, chain: tuple) -> s.Expr:
    result = s.diff(e, variable)
    for symbol, derivative in chain:
        result += s.diff(e, symbol)*derivative
    return result


@register("differentiate_both_sides", "calculus_equation")
def differentiate_both_sides(theory: Theory, variable: s.Symbol, chain: tuple) -> Rule:
    def transform(eq: s.Eq) -> s.Eq:
        return s.Eq(total_derivative(eq.lhs, variable, chain), total_derivative(eq.rhs, variable, chain),
                    evaluate=False)
    return Rule("differentiate_both_sides", f"Differentiate both sides with respect to ${s.latex(variable)}$.",
                transform, "calculus_equation", {"variable": variable, "chain": chain})


def _log_both_sides(eq: s.Eq) -> s.Eq:
    if not eq.rhs.is_positive:
        raise ValueError("Taking logs needs a positive side")
    return s.Eq(s.log(eq.lhs), s.expand_log(s.log(eq.rhs), force=True), evaluate=False)


def use_definition(theory: Theory) -> Rule:
    return Rule("use_definition", "Use the definition.", theory.expand_definitions, "calculus")


def differentiate(e: s.Expr) -> s.Expr:
    """Carry out every derivative written as d/dx(...)."""
    return e.replace(lambda d: isinstance(d, s.Derivative), lambda d: d.doit())


def antiderivative(function: s.Expr, variable: s.Symbol) -> s.Expr:
    """A school-style antiderivative (SymPy's step-by-step integrator), or ValueError. The
    step-by-step integrator fails quickly instead of stalling on hard integrands."""
    from sympy.integrals.manualintegrate import manualintegrate
    if function.atoms(AppliedUndef):
        raise ValueError("Unspecified function")
    # 1/sin^2 u and 1/cos^2 u are recognised as cosec^2 u and sec^2 u.
    standard = function.replace(lambda p: p.is_Pow and p.exp == -2 and p.base.func in (s.sin, s.cos),
                                lambda p: (s.csc if p.base.func == s.sin else s.sec)(p.base.args[0])**2)
    u = s.Dummy("u")
    for candidate in (standard, function):
        for primitive in _substitutions(candidate, variable, u):
            if primitive is not None and not primitive.has(s.Integral):
                return primitive
    raise ValueError("No antiderivative found")


def _substitutions(f: s.Expr, x: s.Symbol, u: s.Dummy):
    """School substitutions, then SymPy's step-by-step integrator: a linear argument
    (u = ax + b), u = cos x (when f = g(cos x) sin x) and u = sin x (when f = g(sin x) cos x)."""
    from sympy.integrals.manualintegrate import manualintegrate
    angles = {g.args[0] for g in f.atoms(s.Function) if g.func in (s.sin, s.cos, s.tan, s.cot, s.sec, s.csc)}
    if len(angles) == 1:
        angle = angles.pop()
        slope = s.diff(angle, x)
        if angle != x and slope.is_number and slope != 0 and not f.xreplace({angle: u}).has(x):
            yield manualintegrate(f.xreplace({angle: u}), u).xreplace({u: angle})/slope
    for outer, inner, sign in ((s.cos, s.sin, -1), (s.sin, s.cos, 1)):
        g = s.cancel(f/(sign*inner(x))).xreplace({outer(x): u})
        if not g.has(x):
            yield manualintegrate(g, u).xreplace({u: outer(x)})
    yield manualintegrate(f, x)


def _antiderivative(integral: s.Integral):
    (variable, low, high), = integral.limits
    return variable, low, high, antiderivative(integral.function, variable)


class Bracket(s.Expr):
    """[F(x)] from a to b, shown as in school; equal to F(b) - F(a)."""
    def __new__(cls, primitive, variable, low, high):
        return s.Expr.__new__(cls, primitive, variable, low, high)

    def doit(self, **hints):
        primitive, variable, low, high = self.args
        return primitive.xreplace({variable: high}) - primitive.xreplace({variable: low})

    def _eval_evalf(self, prec):
        return self.doit()._eval_evalf(prec)

    def _latex(self, printer):
        primitive, _, low, high = self.args
        return rf"\left[{printer._print(primitive)}\right]_{{{printer._print(low)}}}^{{{printer._print(high)}}}"


def evaluate_integral(e: s.Expr) -> s.Expr:
    """Integrate: the integral becomes [F(x)] from a to b."""
    def evaluate(integral):
        variable, low, high, primitive = _antiderivative(integral)
        return Bracket(primitive, variable, low, high)
    return e.replace(lambda i: isinstance(i, s.Integral) and len(i.limits[0]) == 3, evaluate)


def substitute_limits(e: s.Expr) -> s.Expr:
    """[F(x)] from a to b = F(b) - F(a)."""
    def substitute(bracket):
        primitive, variable, low, high = bracket.args
        upper, lower = primitive.xreplace({variable: high}), primitive.xreplace({variable: low})
        if lower == 0:
            return upper
        if lower.is_number and lower.is_negative:  # F(b) - F(a) with F(a) < 0 is written F(b) + |F(a)|
            return s.Add(upper, -lower, evaluate=False)
        return s.Add(upper, s.Mul(-1, lower, evaluate=False), evaluate=False)
    return e.replace(lambda b: isinstance(b, Bracket), substitute)


def half_angle_denominator(e: s.Expr) -> s.Expr:
    """1 + sin u = 2cos^2(pi/4 - u/2), 1 - sin u = 2sin^2(pi/4 - u/2), 1 + cos u = 2cos^2(u/2),
    1 - cos u = 2sin^2(u/2). Unlike multiplying by the conjugate (which gives sec^2 u - sec u tan u,
    undefined at u = pi/2), this keeps the antiderivative continuous across the interval."""
    def match(p):
        if not (p.is_Pow and p.exp == -1 and p.base.is_Add and len(p.base.args) == 2):
            return None
        constant, other = sorted(p.base.args, key=lambda t: not t.is_Number)
        coefficient, function = other.as_coeff_Mul()
        if constant != 1 or abs(coefficient) != 1 or function.func not in (s.sin, s.cos):
            return None
        return function.func, function.args[0], int(coefficient)

    def rewrite(p):
        func, u, sign = match(p)
        if func == s.sin:
            v = s.pi/4 - u/2
            square = 2*s.cos(v)**2 if sign == 1 else 2*s.sin(v)**2
        else:
            square = 2*s.cos(u/2)**2 if sign == 1 else 2*s.sin(u/2)**2
        return 1/square
    return e.replace(lambda p: match(p) is not None, rewrite)


def pull_constant(e: s.Expr) -> s.Expr:
    """∫ c g(x) dx = c ∫ g(x) dx for a constant c."""
    def pull(integral):
        (variable, *limits), = integral.limits
        constant, rest = integral.function.as_independent(variable, as_Add=False)
        if constant == 1:
            return integral
        return s.Mul(constant, s.Integral(rest, (variable, *limits)), evaluate=False)
    return e.replace(lambda i: isinstance(i, s.Integral), pull)


@register("simplify_value", "generated")
def simplify_value(theory: Theory, target: s.Expr) -> Rule:
    """A closed-form number rewritten as the stated value; allowed only for numbers, and
    checked exactly (surds and pi included) by exact_equal."""
    from ..equality import exact_equal

    def transform(e):
        if e.free_symbols or e.has(s.Integral) or not exact_equal(e, target, theory):  # numbers only, never an integral
            raise ValueError("Not the stated value")
        return target
    return Rule("simplify_value", "Simplify.", transform, "generated", {"target": target})


def expand_integrand(e: s.Expr) -> s.Expr:
    return e.replace(lambda i: isinstance(i, s.Integral), lambda i: s.Integral(s.expand(i.function), *i.limits))


def reflection(integral: s.Integral) -> s.Integral:
    (variable, low, high), = integral.limits
    return s.Integral(integral.function.xreplace({variable: low + high - variable}), (variable, low, high))


def average_with_reflection(e: s.Expr) -> s.Expr:
    """I = (1/2)(I + I'), where I' is I after x -> a + b - x (equal by the reflection property)."""
    return e.replace(lambda i: isinstance(i, s.Integral) and len(i.limits[0]) == 3,
                     lambda i: s.Mul(s.Rational(1, 2), s.Add(i, reflection(i), evaluate=False), evaluate=False))


def combine_integrals(e: s.Expr) -> s.Expr:
    """∫f + ∫g over the same limits = ∫(f + g)."""
    def combine(add):
        groups = {}
        for term in s.Add.make_args(add):
            coefficient, rest = term.as_coeff_Mul()
            if isinstance(rest, s.Integral):
                groups.setdefault(rest.limits, []).append(coefficient*rest.function)
            else:
                return add
        if len(groups) != 1:
            return add
        (limits, functions), = groups.items()
        return s.Integral(s.Add(*functions), *limits)
    return e.replace(lambda a: a.is_Add and all(isinstance(t.as_coeff_Mul()[1], s.Integral) for t in a.args), combine)


def flip_limits(e: s.Expr) -> s.Expr:
    """∫ from b to a = -∫ from a to b, when the upper limit is below the lower one."""
    def flip(integral):
        (variable, low, high), = integral.limits
        if not (low - high).is_positive:
            return integral
        return s.Mul(-1, s.Integral(integral.function, (variable, high, low)), evaluate=False)
    return e.replace(lambda i: isinstance(i, s.Integral) and len(i.limits[0]) == 3, flip)


def simplify_integrand(e: s.Expr) -> s.Expr:
    return e.replace(lambda i: isinstance(i, s.Integral),
                     lambda i: s.Integral(s.factor(s.cancel(s.expand(i.function))), *i.limits))


@register("sign_on_domain", "calculus_sign")
def sign_on_domain(theory: Theory, variable: s.Symbol) -> Rule:
    """e > 0 (or < 0) for every allowed value, read from the signs of its factors."""
    def transform(e):
        if e.is_positive:
            return s.StrictGreaterThan(e, 0, evaluate=False)
        if e.is_negative:
            return s.StrictLessThan(e, 0, evaluate=False)
        raise ValueError("Sign not fixed on the domain")
    return Rule("sign_on_domain", f"Each factor has a fixed sign for the allowed values of ${s.latex(variable)}$.",
                transform, "calculus_sign", {"variable": variable})


def limits_equal(a: s.Expr, b: s.Expr, h: s.Symbol) -> bool:
    """Two expressions involving limits as h -> 0 are equal: when both are a single limit,
    their arguments agree for every h != 0 (exact); otherwise each limit is evaluated by
    SymPy and the values compared exactly."""
    from ..equality import exact_equal
    if isinstance(a, s.Limit) and isinstance(b, s.Limit):
        return exact_equal(a.args[0], b.args[0], Theory(domain=(h,)))
    values = [e.replace(lambda q: isinstance(q, s.Limit), lambda q: q.doit()) for e in (a, b)]
    if any(v.has(s.Limit) for v in values):
        return False
    return s.simplify(values[0] - values[1]) == 0


@register("limit_step", "calculus_limit")
def limit_step(theory: Theory, target: s.Expr, h: s.Symbol, reason: str) -> Rule:
    """One stage of a first-principles derivation; checked by limits_equal."""
    def transform(e):
        if not limits_equal(e, target, h):
            raise ValueError("Not equal")
        return target
    return Rule("limit_step", reason, transform, "calculus_limit", {"target": target, "h": h, "reason": reason})


@register("change_variable", "calculus_integral")
def change_variable(theory: Theory, old: s.Symbol, new: s.Symbol, expression: s.Expr) -> Rule:
    def transform(e):
        return e.replace(lambda i: isinstance(i, s.Integral) and i.limits[0][0] == old,
                         lambda i: i.transform(old, (expression, new)))
    slope = s.diff(expression, new)
    scale = {1: "", -1: "-"}.get(slope, s.latex(slope) + r"\\,")
    reason = (f"Put ${s.latex(old)} = {s.latex(expression)}$, so $d{s.latex(old)} = {scale}d{s.latex(new)}$, "
              "and change the limits.")
    return Rule("change_variable", reason, transform, "calculus_integral",
                {"old": old, "new": new, "expression": expression})


@register("rename_variable", "calculus_integral")
def rename_variable(theory: Theory, old: s.Symbol, new: s.Symbol) -> Rule:
    def transform(e):
        return e.replace(lambda i: isinstance(i, s.Integral) and i.limits[0][0] == old,
                         lambda i: s.Integral(i.function.xreplace({old: new}), (new,) + tuple(i.limits[0][1:])))
    return Rule("rename_variable", "A definite integral does not depend on the letter used for its variable.",
                transform, "calculus_integral", {"old": old, "new": new})


register("use_definition", "calculus")(use_definition)


@register("use_coordinates", "geometry")
def use_coordinates(theory: Theory) -> Rule:
    return Rule("use_coordinates", "Write each length, area or product in coordinates (see above).",
                theory.expand_definitions, "geometry")
static("log_both_sides", "calculus_equation", "Take logarithms of both sides.", _log_both_sides)
static("differentiate", "calculus", "Differentiate.", differentiate)
static("evaluate_integral", "integral", "Integrate.", evaluate_integral)
static("substitute_limits", "integral", "Substitute the limits.", substitute_limits)
static("half_angle_denominator", "integral",
       r"Use $1 + \sin x = 2\cos^2\left(\frac{\pi}{4} - \frac{x}{2}\right)$ (and the like for $1 - \sin x$, $1 \pm \cos x$).",
       half_angle_denominator)
static("expand_integrand", "integral", "Split the integrand into simpler terms.", expand_integrand)
static("pull_constant", "integral", "Take the constant outside the integral.", pull_constant)
static("average_with_reflection", "integral",
       r"Use $\int_a^b f(x)\,dx = \int_a^b f(a+b-x)\,dx$, so $I$ is half the sum of the two.", average_with_reflection)
static("combine_integrals", "integral", "Add the integrals over the same limits.", combine_integrals)
static("simplify_integrand", "integral", "Simplify the integrand.", simplify_integrand)
static("flip_limits", "integral", r"Use $\int_b^a = -\int_a^b$ to put the limits in order.", flip_limits)

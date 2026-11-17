"""Algebra rules. Function applications are frozen first, so pure algebra can never
silently apply a trig identity or a sequence definition.

The equation rules (cross_multiply ... positive_root) derive usable facts from a
given condition; verify.py checks every derived equation follows from the givens.
"""
from __future__ import annotations

import sympy as s
from sympy.polys.polyfuncs import symmetrize

from ..equality import Theory, algebra_view
from .base import Rule, register, static


def frozen(operation):
    """Apply a pure-algebra operation with functions, surds and real powers held fixed,
    so surd arithmetic and index laws must be separate, named steps."""
    def transform(e: s.Expr) -> s.Expr:
        forward = {f: s.Symbol(f"fn({f})") for f in e.atoms(s.Function)}
        e = e.xreplace(forward)
        powers = {p: s.Symbol(f"pow({p})") for p in e.atoms(s.Pow) if not p.exp.is_Integer and not p.exp.is_integer}
        forward.update(powers)
        back = {v: k for k, v in forward.items()}
        result = operation(e.xreplace(powers)).xreplace(back)
        # Putting surds and powers back lets SymPy simplify them (sqrt(3)**2 -> 3, power
        # denesting). Refuse the step unless it is also valid as pure algebra.
        if s.cancel(algebra_view(result) - algebra_view(e.xreplace(back))) != 0:
            raise ValueError("Step needs more than algebra")
        return result
    return transform


def checked(operation):
    """Apply an operation directly, so an unevaluated display form (cos^4 A / cos^4 A)
    survives, and refuse it unless the step is valid as pure algebra."""
    def transform(e: s.Expr) -> s.Expr:
        result = operation(e)
        if s.cancel(algebra_view(result) - algebra_view(e)) != 0:
            raise ValueError("Step needs more than algebra")
        return result
    return transform


def symmetric_form(e: s.Expr) -> s.Expr:
    """Rewrite a symmetric polynomial using a+b+c, ab+bc+ca and abc."""
    variables = sorted(e.free_symbols, key=lambda v: v.name)
    if not 2 <= len(variables) <= 3 or not e.is_polynomial(*variables) or s.Poly(e, *variables).total_degree() < 2:
        return e
    symmetric, remainder, definitions = symmetrize(s.expand(e), *variables, formal=True)
    if remainder != 0:
        return e
    return symmetric.xreplace(dict(definitions))


static("algebra_expand", "algebra", "Expand algebraically.", frozen(s.expand))
static("algebra_factor", "algebra", "Combine and factor the algebraic expression.", frozen(s.factor))
static("algebra_cancel", "algebra", "Simplify the algebraic fraction.", frozen(s.cancel))
static("algebra_common_denominator", "algebra", "Take a common denominator.", frozen(s.together))


def _expand_numerator(e: s.Expr) -> s.Expr:
    numerator, denominator = s.fraction(s.together(e))
    if denominator == 1:
        return s.expand(numerator)
    # Unevaluated so that, e.g., cos^4 A / cos^4 A is shown before it cancels.
    return s.Mul(s.expand(numerator), s.Pow(denominator, -1, evaluate=False), evaluate=False)


def _simplify_each_term(e: s.Expr) -> s.Expr:
    terms = s.Add.make_args(e)
    if len(terms) < 2:
        raise ValueError("Not a sum")
    return s.Add(*[s.cancel(s.together(t)) for t in terms], evaluate=False)


def _combine_fractions(e: s.Expr) -> s.Expr:
    """Fractions with one common denominator, added over it (shown before cancelling)."""
    parts = [s.fraction(t) for t in s.Add.make_args(e)]
    denominators = {d for _, d in parts}
    if len(parts) < 2 or len(denominators) != 1 or denominators == {1}:
        raise ValueError("Not fractions over one denominator")
    numerator = s.Add(*[n for n, _ in parts], evaluate=False)
    return s.Mul(numerator, s.Pow(denominators.pop(), -1, evaluate=False), evaluate=False)


def _factor_parts(e: s.Expr) -> s.Expr:
    """Factorise the numerator and the denominator separately, before cancelling."""
    numerator, denominator = s.fraction(e)
    if denominator == 1:
        raise ValueError("Not a fraction")
    return s.Mul(s.factor(numerator), s.Pow(s.factor(denominator), -1, evaluate=False), evaluate=False)


def clearing_factor(e: s.Expr) -> s.Integer:
    """The number to multiply top and bottom by to clear fractions inside a fraction."""
    numerator, denominator = s.fraction(e)
    inner = [s.fraction(s.together(part))[1] for part in (numerator, denominator)]
    return s.ilcm(*[int(d) for d in inner]) if all(d.is_Integer for d in inner) else s.Integer(1)


def _clear_fractions(e: s.Expr) -> s.Expr:
    numerator, denominator = s.fraction(e)
    k = clearing_factor(e)
    if k == 1 or denominator == 1:
        raise ValueError("No fractions inside the fraction")
    return s.Mul(s.expand(k*numerator), s.Pow(s.expand(k*denominator), -1, evaluate=False), evaluate=False)


# Used only by refine.py to show a long simplification in stages, not by the search.
static("clear_fractions", "presentation", "Multiply the numerator and the denominator by the same number.",
       checked(_clear_fractions))
static("factor_parts", "presentation", "Factorise the numerator and the denominator.", checked(_factor_parts))
static("expand_numerator", "presentation", "Expand the numerator.", checked(_expand_numerator))
static("simplify_each_term", "presentation", "Simplify each fraction.", checked(_simplify_each_term))
static("combine_fractions", "presentation", "Add the fractions over their common denominator.", checked(_combine_fractions))
static("symmetric_form", "symmetric", "Write the expression in terms of the sum, the sum of products and the product of the variables.",
       symmetric_form)


# Equation rules: each maps Eq -> Eq.

def _cross_multiply(eq: s.Eq) -> s.Eq:
    (nl, dl), (nr, dr) = s.fraction(s.together(eq.lhs)), s.fraction(s.together(eq.rhs))
    if dl == 1 and dr == 1:
        raise ValueError("No denominators to clear")
    return s.Eq(nl*dr, nr*dl, evaluate=False)


def _move_terms(eq: s.Eq) -> s.Eq:
    return s.Eq(s.expand(eq.lhs - eq.rhs, power_exp=False), 0, evaluate=False)


def _factor_equation(eq: s.Eq) -> s.Eq:
    return s.Eq(s.factor(eq.lhs), eq.rhs, evaluate=False)


def _numerator_zero(eq: s.Eq) -> s.Eq:
    numerator, denominator = s.fraction(s.together(eq.lhs - eq.rhs))
    if denominator == 1:
        raise ValueError("No fraction")
    return s.Eq(numerator, 0, evaluate=False)


static("numerator_zero", "equation", "A fraction is zero only when its numerator is zero (the denominator must stay nonzero).",
       _numerator_zero)
static("cross_multiply", "equation", "Cross-multiply to clear the denominators.", _cross_multiply)
static("move_terms", "equation", "Bring every term to one side and expand.", _move_terms)
static("factor_equation", "equation", "Factorise.", _factor_equation)


@register("zero_product", "equation")
def zero_product(theory: Theory, factor: s.Expr) -> Rule:
    def transform(eq):
        bases = [f.base if f.is_Pow else f for f in s.Mul.make_args(eq.lhs)]
        if eq.rhs != 0 or factor not in bases:
            raise ValueError("Not a factor of a product equal to zero")
        return s.Eq(factor, 0, evaluate=False)
    return Rule("zero_product", f"A product is zero only if a factor is zero, and the other factors are nonzero, "
                f"so ${s.latex(factor)} = 0$.", transform, "equation", {"factor": factor})


@register("solve_for", "equation")
def solve_for(theory: Theory, atom: s.Expr) -> Rule:
    t = s.Dummy("t")

    def transform(eq):
        zero = s.expand(eq.lhs - eq.rhs, power_exp=False).xreplace({atom: t})
        if not zero.is_polynomial(t) or s.degree(zero, t) != 1:
            raise ValueError(f"Equation is not linear in {atom}")
        # Other functions are held fixed, so the solver cannot rewrite e^(x - y) as e^x/e^y.
        held = {f: s.Dummy(f"f{i}") for i, f in enumerate(sorted(zero.atoms(s.Function), key=str))}
        value = s.solve(zero.xreplace(held), t)[0]
        return s.Eq(atom, value.xreplace({v: k for k, v in held.items()}), evaluate=False)
    return Rule("solve_for", f"Make ${s.latex(atom)}$ the subject.", transform, "equation", {"atom": atom})


@register("positive_root", "equation")
def positive_root(theory: Theory, variable: s.Symbol) -> Rule:
    def transform(eq):
        if not (variable.is_positive and eq.lhs.is_Pow and eq.lhs.base == variable and eq.lhs.exp.is_Integer):
            raise ValueError("Needs (positive variable)^k = value")
        return s.Eq(variable, eq.rhs**(s.Integer(1)/eq.lhs.exp), evaluate=False)
    return Rule("positive_root", f"Take the positive root, since ${s.latex(variable)} > 0$.", transform,
                "equation", {"variable": variable})


# Expression rules generated from the givens.

@register("substitute", "generated")
def substitute(theory: Theory, variable: s.Expr, value: s.Expr) -> Rule:
    """Replace a derived atom (a variable, a power or a log) by its value."""
    return Rule("substitute", f"Substitute ${s.latex(variable)} = {s.latex(value)}$.",
                lambda e: e.xreplace({variable: value}), "generated", {"variable": variable, "value": value})


@register("replace_givens", "generated")
def replace_givens(theory: Theory, pairs: tuple) -> Rule:
    """Use several givens at once, before automatic simplification can split them."""
    listed = ", ".join(f"${s.latex(l)} = {s.latex(r)}$" for l, r in pairs)
    return Rule("replace_givens", f"Use the givens {listed}.", lambda e: e.xreplace(dict(pairs)), "generated",
                {"pairs": pairs})


@register("replace_given", "generated")
def replace_given(theory: Theory, lhs: s.Expr, rhs: s.Expr) -> Rule:
    return Rule("replace_given", f"Use the given ${s.latex(lhs)} = {s.latex(rhs)}$.",
                lambda e: e.xreplace({lhs: rhs}), "generated", {"lhs": lhs, "rhs": rhs})

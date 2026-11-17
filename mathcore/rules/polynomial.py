"""Polynomial method rules: factor theorem and completing the square."""
from __future__ import annotations

import sympy as s

from ..equality import Theory
from .base import Rule, register


@register("evaluate_at", "polynomial")
def evaluate_at(theory: Theory) -> Rule:
    return Rule("evaluate_at", "Substitute the zero of the proposed factor.",
                lambda e: e.doit() if isinstance(e, s.Subs) else e, "polynomial")


@register("divide_by_factor", "polynomial")
def divide_by_factor(theory: Theory, factor: s.Expr, variable: s.Symbol) -> Rule:
    def transform(p):
        quotient, remainder = s.div(p, factor, variable)
        return s.Mul(factor, quotient, evaluate=False) + remainder
    return Rule("divide_by_factor", f"Divide by ${s.latex(factor)}$.", transform, "polynomial",
                {"factor": factor, "variable": variable})


@register("complete_square", "polynomial")
def complete_square(theory: Theory, variable: s.Symbol) -> Rule:
    def transform(p):
        a, b, c = s.Poly(p, variable).all_coeffs()
        h = -b/(2*a)
        return s.Add(a*(variable - h)**2, c - b**2/(4*a), evaluate=False)
    return Rule("complete_square", "Complete the square.", transform, "polynomial", {"variable": variable})


@register("square_plus_positive", "polynomial")
def square_plus_positive(theory: Theory, variable: s.Symbol) -> Rule:
    def transform(e):
        square, constant = sorted(s.Add.make_args(e), key=lambda t: t.is_Number)
        coefficient, power = square.as_coeff_Mul()
        if not (constant.is_Number and constant > 0 and coefficient > 0 and power.is_Pow
                and power.exp == 2 and power.base.is_polynomial(variable)):
            raise ValueError("Not a positive multiple of a square plus a positive constant")
        return s.StrictGreaterThan(e, 0, evaluate=False)
    return Rule("square_plus_positive", "A real square is nonnegative and the constant is positive.",
                transform, "polynomial", {"variable": variable})

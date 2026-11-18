"""Algebra methods that are not a single rewrite chain.

- componendo_dividendo (prescribed method): from a/b = c/d derive (a + b)/(a - b) = (c + d)/(c - d),
  squaring when a side is a ratio of square roots, until the goal can be made the subject.
  Each derived equation is a step of relation "derived": verify.py replays the rule and checks,
  with Groebner bases and at sample points, that it follows from the givens.
- one_real_roots: "at least one of these quadratics has real roots". The discriminants are
  added, the sum is rewritten (a checked chain, using the givens) into a square times a positive
  number, and so the discriminants cannot both be negative.
- only_solution: "the only real solution is x = v" by contradiction: the equation factorises as
  (x - v)^k g(x) = 0, and g(x) is a square plus a positive number, so it is never zero.
"""
from __future__ import annotations

from dataclasses import replace

import sympy as s

from ..engine import Step
from ..equality import Theory
from ..problem import Problem
from ..rules import build
from ..rules.base import Rule, static
from .identity import conditional


# ---------------------------------------------------------------- componendo and dividendo
def _cd(eq: s.Eq) -> s.Eq:
    (a, b), (c, d) = eq.lhs.as_numer_denom(), eq.rhs.as_numer_denom()
    if b == 1 and d == 1:
        raise ValueError("No ratio to apply componendo and dividendo to")
    return s.Eq(s.cancel((a + b)/(a - b)) if not _has_root(a + b) else (a + b)/(a - b),
                (c + d)/(c - d), evaluate=False)


def _has_root(e: s.Expr) -> bool:
    return any(p.exp == s.Rational(1, 2) for p in e.atoms(s.Pow))


def _square(eq: s.Eq) -> s.Eq:
    if not any(p.exp == s.Rational(1, 2) for p in (eq.lhs - eq.rhs).atoms(s.Pow)):
        raise ValueError("Nothing to square away")
    return s.Eq(eq.lhs**2, eq.rhs**2, evaluate=False)


def _tidy(eq: s.Eq) -> s.Eq:
    def side(e):
        n, d = e.as_numer_denom()
        return e if _has_root(e) else s.factor(s.expand(n))/s.factor(s.expand(d))
    return s.Eq(side(eq.lhs), side(eq.rhs), evaluate=False)


static("componendo_dividendo", "method",
       r"Componendo and dividendo: if $\frac{a}{b} = \frac{c}{d}$ then $\frac{a + b}{a - b} = \frac{c + d}{c - d}$.", _cd)
static("square_both_sides", "method", "Square both sides.", _square)
static("simplify_sides", "method", "Simplify each side.", _tidy)


def componendo_dividendo(problem: Problem) -> dict:
    fail = {"strategy": "componendo_dividendo", "premises": [], "steps": []}
    if problem.spec.prescribed_method != "componendo_dividendo" or len(problem.hypotheses) != 1:
        return {**fail, "status": "UNSUPPORTED", "reason": "Used when the question asks for componendo and dividendo."}
    target, goal_value = problem.exprs["lhs"], problem.exprs["rhs"]
    lhs, rhs = problem.hypotheses[0]
    eq, steps = s.Eq(lhs, rhs, evaluate=False), []
    theory = problem.theory

    def apply(name, params=None) -> bool:
        nonlocal eq
        rule = build(name, theory, params)
        try:
            new = rule.apply(eq)
        except (ValueError, ZeroDivisionError, NotImplementedError, IndexError):
            return False
        if new == eq:
            return False
        steps.append(Step(eq, new, rule.name, rule.reason, rule.params, relation="derived"))
        eq = new
        return True

    for _ in range(3):
        if not apply("componendo_dividendo"):
            break
        apply("simplify_sides")
        if apply("square_both_sides"):
            apply("simplify_sides")
            continue
        break
    atom = target if (target.is_Symbol or target.is_Pow) else None
    apply("cross_multiply")
    if atom is None or not apply("solve_for", {"atom": atom}):
        return {**fail, "steps": steps, "status": "INCONCLUSIVE", "reason": f"Could not make {target} the subject."}
    if s.simplify(eq.rhs - goal_value) != 0 or eq.lhs != target:
        return {**fail, "steps": steps, "status": "INCONCLUSIVE", "reason": "The derived equation is not the goal."}
    return {"strategy": "componendo_dividendo", "status": "SOLVED", "form": "derived", "premises": [], "steps": steps}


# ---------------------------------------------------------------- one quadratic has real roots
def discriminants(problem: Problem) -> list:
    x = problem.exprs["variable"]
    found = []
    for p in problem.exprs["polynomials"]:
        a, b, c = s.Poly(p, x).all_coeffs()
        found.append(s.expand(b**2 - 4*a*c))
    return found


def square_form(e: s.Expr) -> bool:
    """e is c*g^2 with c > 0, or a sum of such terms: so e >= 0 for real values."""
    terms = s.Add.make_args(s.factor(e)) if not s.factor(e).is_Mul else [s.factor(e)]
    for term in terms:
        coefficient, rest = term.as_coeff_Mul()
        if coefficient <= 0:
            return False
        for factor in s.Mul.make_args(rest):
            if not (factor.is_Pow and factor.exp.is_Integer and factor.exp % 2 == 0) and factor != 1:
                return False
    return True


def one_real_roots(problem: Problem) -> dict:
    fail = {"strategy": "one_real_roots", "premises": [], "steps": []}
    total = s.Add(*discriminants(problem))
    options = []  # substitute one variable from a given; keep results that are visibly a square
    for v in sorted(set().union(*(h[0].free_symbols | h[1].free_symbols for h in problem.hypotheses)), key=str):
        for l, r in problem.hypotheses:
            solved = s.solve(l - r, v)
            if len(solved) == 1 and solved[0].is_polynomial():
                candidate = s.factor(s.expand(total.xreplace({v: solved[0]})))
                if square_form(candidate):
                    options.append(candidate)
    target = min(options, key=s.count_ops) if options else None
    if target is None:
        return {**fail, "status": "UNSUPPORTED", "reason": "Could not write the sum of the discriminants as a square."}
    sub = replace(problem, exprs={**problem.exprs, "lhs": total, "rhs": target})
    found = conditional(sub)
    if found["status"] != "SOLVED":
        return {**fail, "status": "INCONCLUSIVE", "reason": found.get("reason", "")}
    return {**found, "strategy": "one_real_roots", "form": "discriminants", "diagnostics": {"sum": total, "square": target}}


# ---------------------------------------------------------------- the only real solution
def only_solution(problem: Problem) -> dict:
    fail = {"strategy": "only_solution", "premises": [], "steps": []}
    x, value = problem.exprs["variable"], problem.exprs["value"]
    polynomial = s.expand(problem.exprs["lhs"] - problem.exprs["rhs"])
    if not polynomial.is_polynomial(x) or s.expand(polynomial.xreplace({x: value})) != 0:
        return {**fail, "status": "UNSUPPORTED", "reason": "Needs a polynomial equation that the value satisfies."}
    quotient, remainder = s.div(polynomial, x - value, x)
    while s.expand(quotient.xreplace({x: value})) == 0:
        quotient = s.div(quotient, x - value, x)[0]
    other = s.expand(quotient)
    if s.Poly(other, x).degree() == 0:
        steps = []
    elif s.Poly(other, x).degree() == 2:
        square = build("complete_square", problem.theory, {"variable": x})
        positive = build("square_plus_positive", problem.theory, {"variable": x})
        completed = square.apply(other)
        try:
            conclusion = positive.apply(completed)
        except ValueError as exc:
            return {**fail, "status": "INCONCLUSIVE", "reason": str(exc)}
        steps = [Step(other, completed, square.name, square.reason, square.params),
                 Step(completed, conclusion, positive.name, positive.reason, positive.params, relation="implication")]
    else:
        return {**fail, "status": "UNSUPPORTED", "reason": "The other factor must be constant or quadratic."}
    factored = s.Mul(s.factor(polynomial.xreplace({x: x}) / other), other, evaluate=False)
    premise = Step(polynomial, factored, "factor_out_root", "Factorise.", {"factor": other}, relation="factorisation")
    return {"strategy": "only_solution", "status": "SOLVED", "form": "contradiction", "premises": [premise],
            "steps": steps, "diagnostics": {"other": other}}

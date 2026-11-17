"""Index laws, log laws and surds. The parser records the positivity each law needs
(a symbolic index or a log argument makes its base positive)."""
from __future__ import annotations

from collections import defaultdict

import sympy as s

from ..equality import _rational_log
from .base import static


def _symbolic(p) -> bool:
    return p.is_Pow and not p.exp.is_Number


def power_of_power(e: s.Expr) -> s.Expr:
    """(x^m)^n = x^(mn), only where an index is symbolic (so the base was recorded positive)."""
    return e.replace(lambda p: p.is_Pow and p.base.is_Pow and (_symbolic(p) or _symbolic(p.base)),
                     lambda p: s.Pow(p.base.base, p.base.exp*p.exp, evaluate=False))


def product_of_powers(e: s.Expr) -> s.Expr:
    """x^m * x^n = x^(m+n) for powers with a symbolic index."""
    def merge(m):
        groups, others = defaultdict(list), []
        for factor in m.args:
            if _symbolic(factor):
                groups[factor.base].append(factor.exp)
            else:
                others.append(factor)
        if not any(len(v) > 1 for v in groups.values()):
            return m
        merged = [s.Pow(b, s.Add(*exps), evaluate=False) for b, exps in groups.items()]
        return s.Mul(*others, *merged, evaluate=False)
    return e.replace(lambda m: m.is_Mul, merge)


def simplify_exponents(e: s.Expr) -> s.Expr:
    return e.replace(_symbolic, lambda p: p.base**s.expand(p.exp))


def log_laws(e: s.Expr) -> s.Expr:
    return s.expand_log(e, force=True)


def log_prime_factors(e: s.Expr) -> s.Expr:
    """log(16/15) = 4 log 2 - log 3 - log 5; coefficients are kept outside the brackets
    so the next step (expand) shows the collection of like terms."""
    splits = lambda f: (f.func == s.log and f.args[0].is_Rational and f.args[0] > 0
                        and _rational_log(f.args[0]) != f)
    terms = []
    for term in s.Add.make_args(e):
        coefficient, rest = term.as_coeff_Mul()
        if splits(rest):
            terms.append(s.Mul(coefficient, _rational_log(rest.args[0]), evaluate=False) if coefficient != 1
                         else _rational_log(rest.args[0]))
        else:
            terms.append(term.replace(splits, lambda f: _rational_log(f.args[0])))
    return s.Add(*terms, evaluate=False) if len(terms) > 1 else terms[0]


def rationalise(e: s.Expr) -> s.Expr:
    """Multiply each fraction by the conjugate of its surd denominator."""
    terms = s.Add.make_args(e)
    new = [s.radsimp(t) if s.fraction(t)[1].has(s.Pow) else t for t in terms]
    return s.Add(*new, evaluate=False) if len(new) > 1 else new[0]


static("power_of_power", "indices", r"Use $(x^m)^n = x^{mn}$.", power_of_power)
static("product_of_powers", "indices", r"Use $x^m \cdot x^n = x^{m+n}$.", product_of_powers)
static("simplify_exponents", "indices", "Simplify the index.", simplify_exponents)
static("log_laws", "logs", r"Use $\log(mn) = \log m + \log n$ and $\log m^k = k \log m$.", log_laws)
static("log_prime_factors", "logs", "Write each logarithm in terms of the logs of primes.", log_prime_factors)
static("rationalise", "surds", "Rationalise each denominator.", rationalise)


def simplify_radicand(e: s.Expr) -> s.Expr:
    """Expand under each square root; a perfect square then comes out using the declared signs."""
    return e.replace(lambda p: p.is_Pow and p.exp == s.Rational(1, 2), lambda p: s.sqrt(s.factor(s.expand(p.base))))


static("simplify_radicand", "surds", "Simplify under the root sign (a square root of a square of a nonnegative "
       "quantity is that quantity).", simplify_radicand)

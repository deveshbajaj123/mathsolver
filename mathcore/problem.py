"""A spec parsed into SymPy objects, with its domain conditions and Theory.

Hypothesis kinds are unpacked here into equations: "in AP" becomes 2b = a + c,
"in GP" b^2 = ac, equal ratios n_i/d_i introduce k with n_i = k d_i (the k-method),
and "equal roots" becomes discriminant = 0.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import sympy as s

from .equality import Theory, denominator_factors, normal
from .parse import Condition, Context, geometry_value, parse_with_conditions, variable_conditions
from .spec import Spec, hypothesis_kind

EXPRESSION_FIELDS = ("lhs", "rhs", "polynomial", "factor", "low", "high", "function", "objective", "expr", "value")


@dataclass
class Problem:
    spec: Spec
    ctx: Context
    exprs: dict = field(default_factory=dict)        # goal field -> Expr
    hypotheses: list = field(default_factory=list)   # [(lhs, rhs)]
    givens: list = field(default_factory=list)       # [{"kind", "text", "equations"}] for rendering
    introduced: list = field(default_factory=list)   # symbols the method introduced, e.g. k
    facts: list = field(default_factory=list)        # [(lhs, rhs)] proved in an earlier part of the question
    conditions: list = field(default_factory=list)   # [Condition]
    intervals: dict = field(default_factory=dict)    # symbol -> (low, high), from the spec
    theory: Theory = Theory()

    @property
    def kind(self) -> str:
        return self.spec.goal["kind"]

    @property
    def symbols(self) -> list:
        return sorted(set(self.ctx.symbols.values()) | set(self.introduced), key=lambda v: v.name)

    @property
    def about_unknown_function(self) -> bool:
        """The goal is a property of an unspecified function f (e.g. ∫f(x) = ∫f(a - x))."""
        names = set(self.ctx.abstract.values())
        return any(f.func in names for e in self.exprs.values() if isinstance(e, s.Basic)
                   for f in e.atoms(s.Function))

    @property
    def solve_order(self) -> tuple:
        """y, y1, y2, ... when y is a function of x: the order in which sampling solves for them."""
        chain = self.ctx.chain
        if not chain:
            return ()
        order = [next(iter(set(chain) - set(chain.values())))]
        while order[-1] in chain:
            order.append(chain[order[-1]])
        return tuple(order)

    def hypothesis_zeros(self) -> list:
        return [self.theory.expand_definitions(l - r) for l, r in self.hypotheses]


def _fresh(ctx: Context, name: str) -> s.Symbol:
    while name in ctx.symbols:
        name += "_1"
    return s.Symbol(name, real=True)


def build(spec: Spec) -> Problem:
    ctx = Context.from_spec(spec)
    problem = Problem(spec, ctx)

    def parse(source: str) -> s.Expr:
        expr, found = parse_with_conditions(source, ctx)
        problem.conditions.extend(found)
        return expr

    goal = spec.goal
    for name in EXPRESSION_FIELDS:
        if name in goal:
            problem.exprs[name] = parse(goal[name])
    if "polynomials" in goal:
        problem.exprs["polynomials"] = [parse(p) for p in goal["polynomials"]]
    if "in_ap" in goal:
        t1, t2, t3 = map(parse, goal["in_ap"])
        problem.exprs.update(lhs=t2 - t1, rhs=t3 - t2)
    if "in_gp" in goal:
        t1, t2, t3 = map(parse, goal["in_gp"])
        problem.exprs.update(lhs=t2**2, rhs=t1*t3)
    if "variable" in goal:
        problem.exprs["variable"] = ctx.symbols[goal["variable"]]

    for h in spec.hypotheses:
        kind = hypothesis_kind(h)
        if kind == "equation":
            equations = [(parse(h["lhs"]), parse(h["rhs"]))]
        elif kind in ("in_ap", "in_gp"):
            t1, t2, t3 = map(parse, h["terms"])
            equations = [(2*t2, t1 + t3)] if kind == "in_ap" else [(t2**2, t1*t3)]
        elif kind == "equal_ratios":
            k = _fresh(ctx, "k")
            problem.introduced.append(k)
            equations = []
            for numerator, denominator in h["ratios"]:
                n, d = parse(numerator), parse(denominator)
                problem.conditions.append(Condition(d, "!=0"))
                equations.append((n, k*d))
        else:  # equal_roots
            x = ctx.symbols[h["variable"]]
            a, b, c = s.Poly(parse(h["polynomial"]), x).all_coeffs()
            problem.conditions.append(Condition(a, "!=0"))
            equations = [(b**2 - 4*a*c, s.Integer(0))]
        problem.hypotheses += equations
        problem.givens.append({"kind": kind, "text": h.get("quote", ""), "equations": equations})

    for name, (low, high) in spec.intervals.items():
        v, low, high = ctx.symbols[name], parse(low), parse(high)
        problem.intervals[v] = (low, high)
        problem.conditions += [Condition(v - low, ">0"), Condition(high - v, ">0")]
    for p, q, r in spec.nondegenerate:  # a triangle in the figure has nonzero area
        problem.conditions.append(Condition(s.expand(2*geometry_value("area", [ctx.points[n] for n in (p, q, r)])), "!=0"))
    problem.conditions += variable_conditions(ctx)
    problem.conditions = [c for c in dict.fromkeys(problem.conditions) if not c.expr.is_Number]
    # A condition on an integral's own variable (its integrand's denominator) is not a condition on the answer.
    bound = {i.limits[0][0] for e in problem.exprs.values() if isinstance(e, s.Basic) for i in e.atoms(s.Integral)}
    free = set().union(*(e.free_symbols for e in problem.exprs.values() if isinstance(e, s.Basic)), set())
    problem.conditions = [c for c in problem.conditions if not (c.expr.free_symbols & bound - free)]
    sequences = tuple((name, kind, a, step) for name, (kind, a, step) in ctx.sequences.items())
    definitions = tuple((name, v, x) for name, (v, x) in ctx.definitions.items())
    points = tuple((name, x, y) for name, (x, y) in ctx.points.items())
    base = Theory(sequences=sequences, hypotheses=tuple(l - r for l, r in problem.hypotheses), definitions=definitions,
                  points=points)
    factors = set()
    for condition in problem.conditions:
        if condition.relation == ">=0":
            continue  # a radicand may be zero, so it is not a nonzero factor
        numerator = s.fraction(s.cancel(normal(base.expand_definitions(condition.expr))))[0]
        factors |= {f for f, _ in s.factor_list(s.expand(numerator))[1]}
        factors |= set(denominator_factors(condition.expr, base))
    for expr in problem.exprs.values():
        for e in (expr if isinstance(expr, list) else [expr]):
            factors |= set(denominator_factors(e, base))
    factors |= {v for v in problem.symbols if v.is_nonzero}  # declared positive or nonzero
    problem.theory = Theory(sequences=sequences, hypotheses=base.hypotheses,
                            domain=tuple(sorted((f for f in factors if not f.is_Number), key=str)),
                            definitions=definitions, points=points,
                            intervals=tuple((v, low, high) for v, (low, high) in problem.intervals.items()))
    return problem


def add_facts(problem: Problem, facts: list) -> None:
    """Results proved in earlier parts may be used here. They join the theory (used for
    checking) but not the hypotheses, so they do not constrain validation's sampling."""
    problem.facts = list(facts)
    problem.theory = problem.theory.with_facts(facts)


RELATION_LATEX = {"!=0": r"\neq", ">0": ">", ">=0": r"\geq"}


def display_conditions(problem: Problem) -> list[Condition]:
    """Conditions as a reader wants them: x^2 != 0 shown as x != 0, and anything the
    declared domains already guarantee (such as x^(a+b) > 0 for x > 0) left out."""
    shown = []
    for c in problem.conditions:
        if c.relation == "!=0":
            factors = [f.base if f.is_Pow and f.exp.is_Integer else f for f in s.Mul.make_args(c.expr)]
            shown += [Condition(f, "!=0") for f in factors
                      if not f.is_number and (f.is_Symbol or not f.is_nonzero)]
        elif not (c.expr.is_positive if c.relation == ">0" else c.expr.is_nonnegative):
            shown.append(c)
    return list(dict.fromkeys(shown))


def conditions_text(problem: Problem) -> list[str]:
    return [f"${s.latex(c.expr)} {RELATION_LATEX[c.relation]} 0$" for c in display_conditions(problem)]


__all__ = ["Condition", "Problem", "build", "conditions_text"]

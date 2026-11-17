"""Step 1: safe expression parser and source-level domain conditions.

Only a whitelisted Python-expression grammar is accepted; sympify is never
called on question text. Domain conditions are read from the original syntax
so a pole survives even if SymPy would cancel it (sin(A)/sin(A) keeps sin(A) != 0).
"""
from __future__ import annotations

import ast
from dataclasses import dataclass, field

import sympy as s

from .spec import Spec

TRIG = {"sin": s.sin, "cos": s.cos, "tan": s.tan, "cot": s.cot, "sec": s.sec, "csc": s.csc}
INVERSE_TRIG = {"asin": s.asin, "acos": s.acos, "atan": s.atan, "acot": s.acot}
MAX_POWER = 12
_CLASSES: dict[str, type] = {}


def _function_class(name: str, default_label) -> type:
    """One SymPy function class per name, so equal names compare equal across calls."""
    if name not in _CLASSES:
        def latex(self, printer):
            index = printer._print(self.args[0])
            return type(self).label or default_label(index)
        _CLASSES[name] = type(name, (s.Function,), {"nargs": 1, "label": None, "_latex": latex})
    return _CLASSES[name]


def term_class(sequence: str) -> type:
    return _function_class(f"{sequence}_term", lambda k: f"{sequence}_{{{k}}}")


def sum_class(sequence: str) -> type:
    return _function_class(f"{sequence}_sum", lambda n: f"S^{{({sequence})}}_{{{n}}}")


def named_class(name: str) -> type:
    """A function defined in the spec, such as the cost function C(x)."""
    return _function_class(f"def_{name}", lambda arg: f"{name}\\left({arg}\\right)")


@dataclass(frozen=True)
class Condition:
    expr: s.Expr
    relation: str  # "!=0", ">0", ">=0"

    def __str__(self) -> str:
        return f"{self.expr} {self.relation[:-1]} 0"


@dataclass
class Context:
    symbols: dict = field(default_factory=dict)
    sequences: dict = field(default_factory=dict)  # name -> (type, first, difference or ratio)
    chain: dict = field(default_factory=dict)      # y -> y1, y1 -> y2: each symbol's derivative symbol
    variable: s.Symbol | None = None               # the independent variable of y(x)
    definitions: dict = field(default_factory=dict)  # C -> (x, expression)
    abstract: dict = field(default_factory=dict)     # f -> an unspecified SymPy function

    @classmethod
    def from_spec(cls, spec: Spec) -> "Context":
        flags = {"real": "real", "positive": "positive", "nonnegative": "nonnegative", "nonzero": "nonzero",
                 "integer": "integer"}
        symbols = {name: s.Symbol(name, **{flags[a]: True for a in assumptions if a != "complex"})
                   for name, assumptions in spec.variables.items()}
        ctx = cls(symbols=symbols)
        for name, function in spec.functions.items():
            ctx.variable = symbols[function["of"]]
            names = [name] + list(function.get("derivatives", []))
            for n in names:
                symbols.setdefault(n, s.Symbol(n, real=True))
            ctx.chain.update({symbols[a]: symbols[b] for a, b in zip(names, names[1:])})
        ctx.abstract = {name: s.Function(name, real=True) for name in spec.abstract}
        for name, definition in spec.definitions.items():
            argument = symbols[definition["of"]]
            ctx.definitions[name] = (argument, parse(definition["expr"], ctx))
        for name, sequence in spec.sequences.items():
            sum_class(name).label = sequence.get("sum_label")  # e.g. "S_1" as printed in the question
            step = sequence["difference"] if sequence["type"] == "ap" else sequence["ratio"]
            ctx.sequences[name] = (sequence["type"], parse(sequence["first"], ctx), parse(step, ctx))
        return ctx


def term_formula(kind: str, a: s.Expr, step: s.Expr, k: s.Expr) -> s.Expr:
    return a + (k - 1)*step if kind == "ap" else a*step**(k - 1)


def sum_formula(kind: str, a: s.Expr, step: s.Expr, n: s.Expr) -> s.Expr:
    return n*(2*a + (n - 1)*step)/2 if kind == "ap" else a*(step**n - 1)/(step - 1)


def parse(source: str, ctx: Context) -> s.Expr:
    return parse_with_conditions(source, ctx)[0]


def parse_with_conditions(source: str, ctx: Context) -> tuple[s.Expr, list[Condition]]:
    conditions: list[Condition] = []

    def need(expr: s.Expr, relation: str) -> None:
        """Record a domain condition; a numeric one is decided now instead."""
        if expr.is_number:
            value = complex(s.N(expr, 30))
            holds = {"!=0": abs(value) > 1e-20, ">0": value.real > 0 and abs(value.imag) < 1e-20,
                     ">=0": value.real >= 0 and abs(value.imag) < 1e-20}[relation]
            if not holds:
                raise ValueError(f"Undefined: needs {expr} {relation[:-1]} 0")
            return
        conditions.append(Condition(expr, relation))

    def walk(node: ast.AST) -> s.Expr:
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return s.Integer(node.value)
        if isinstance(node, ast.Name):
            if node.id in ctx.symbols:
                return ctx.symbols[node.id]
            if node.id == "pi":
                return s.pi
            if node.id == "deg":
                return s.pi/180
            raise ValueError(f"Undeclared name {node.id!r}")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and not node.keywords:
            name, args = node.func.id, node.args
            if name in TRIG and len(args) == 1:
                angle = walk(args[0])
                if name in ("tan", "sec"):
                    need(s.cos(angle), "!=0")
                if name in ("cot", "csc"):
                    need(s.sin(angle), "!=0")
                # A special angle such as cos(60 deg) is kept as written; a named step evaluates it.
                return TRIG[name](angle, evaluate=not angle.is_number)
            if name == "exp" and len(args) == 1:
                return s.exp(walk(args[0]))
            if name in INVERSE_TRIG and len(args) == 1:
                argument = walk(args[0])
                if name in ("asin", "acos"):
                    need(1 - argument**2, ">=0")
                return INVERSE_TRIG[name](argument)
            if name == "diff" and len(args) in (2, 3) and isinstance(args[1], ast.Name):
                order = walk(args[2]) if len(args) == 3 else s.Integer(1)
                if not (order.is_Integer and 1 <= order <= 3):
                    raise ValueError("Derivative order must be 1, 2 or 3")
                return s.Derivative(walk(args[0]), (walk(args[1]), int(order)))
            if name == "integral" and len(args) == 4 and isinstance(args[1], ast.Name):
                variable = walk(args[1])
                return s.Integral(walk(args[0]), (variable, walk(args[2]), walk(args[3])))
            if name in ctx.abstract and len(args) == 1:
                return ctx.abstract[name](walk(args[0]))
            if name in ctx.definitions and len(args) == 1:
                return named_class(name)(walk(args[0]))
            if name == "sqrt" and len(args) == 1:
                radicand = walk(args[0])
                need(radicand, ">=0")
                return s.sqrt(radicand)
            if name == "log" and len(args) in (1, 2):
                argument = walk(args[0])
                need(argument, ">0")
                if len(args) == 1:
                    return s.log(argument)
                base = walk(args[1])
                need(base, ">0")
                need(base - 1, "!=0")
                return s.log(argument, base)
            if name in ("term", "sum") and len(args) == 2 and isinstance(args[0], ast.Name) \
                    and args[0].id in ctx.sequences:
                kind, _, step = ctx.sequences[args[0].id]
                if name == "sum" and kind == "gp":
                    need(step - 1, "!=0")  # the GP sum formula divides by r - 1
                cls = (term_class if name == "term" else sum_class)(args[0].id)
                return cls(walk(args[1]))
            raise ValueError(f"Unsupported call {ast.unparse(node)!r}")
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
            value = walk(node.operand)
            return -value if isinstance(node.op, ast.USub) else value
        if isinstance(node, ast.BinOp):
            left, right = walk(node.left), walk(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            keep = _has_real_power(left) or _has_real_power(right)
            if isinstance(node.op, ast.Mult):
                return s.Mul(left, right, evaluate=False) if keep else left*right
            if isinstance(node.op, ast.Div):
                need(right, "!=0")
                return s.Mul(left, s.Pow(right, -1), evaluate=False) if keep else left/right
            if isinstance(node.op, ast.Pow):
                if right.is_Number:
                    if not right.is_Rational or abs(right) > MAX_POWER or right.q > 4:
                        raise ValueError(f"Unsupported exponent {right}")
                    if right < 0:
                        need(left, "!=0")
                    if right.q % 2 == 0:
                        need(left, ">0" if right < 0 else ">=0")
                    return left**right
                if right.has(*TRIG.values()) or not right.free_symbols <= set(ctx.symbols.values()):
                    raise ValueError(f"Unsupported exponent {right}")
                if right.is_integer:
                    if not right.is_nonnegative:
                        need(left, "!=0")
                else:
                    need(left, ">0")  # real powers with a symbolic index
                # Kept unevaluated so (x^m)^n is shown, and simplified only by the index-law rules.
                return s.Pow(left, right, evaluate=False)
        raise ValueError(f"Unsupported expression syntax: {ast.dump(node)}")

    try:
        tree = ast.parse(source, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Cannot parse {source!r}: {exc.msg}") from exc
    return walk(tree.body), conditions


def _has_real_power(e: s.Expr) -> bool:
    return any(p.is_Pow and not p.exp.is_Number and not p.exp.is_integer for p in e.atoms(s.Pow))


def variable_conditions(ctx: Context) -> list[Condition]:
    return [Condition(symbol, "!=0") for symbol in ctx.symbols.values()
            if symbol.is_nonzero and not symbol.is_positive]

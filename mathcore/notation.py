"""School notation for rendered answers.

- source_latex: LaTeX for an expression exactly as the spec writes it (term order,
  unsimplified fractions, degrees), straight from the source text. Display only; the
  maths always uses the parsed expression.
- school: tidy SymPy's LaTeX into school style: sin A rather than sin(A), sin^2 A,
  cosec rather than csc.
"""
from __future__ import annotations

import ast
import re

import sympy as s

FUNCTIONS = {"sin": r"\sin", "cos": r"\cos", "tan": r"\tan", "cot": r"\cot", "sec": r"\sec",
             "csc": r"\operatorname{cosec}"}
ADDITIVE = (ast.Add, ast.Sub)
INVERSE = {"asin": r"\sin^{-1}", "acos": r"\cos^{-1}", "atan": r"\tan^{-1}", "acot": r"\cot^{-1}"}


def derivative_labels(spec) -> dict:
    """y1 -> dy/dx, y2 -> d^2y/dx^2 (or y_1, y_2 when the question writes them that way)."""
    labels = {}
    for name, function in spec.functions.items():
        x = s.latex(s.Symbol(function["of"]))
        for order, derivative in enumerate(function.get("derivatives", []), 1):
            if function.get("notation") == "subscript":
                labels[derivative] = f"{s.latex(s.Symbol(name))}_{{{order}}}"
            elif order == 1:
                labels[derivative] = rf"\frac{{d{name}}}{{d{x}}}"
            else:
                labels[derivative] = rf"\frac{{d^{{{order}}}{name}}}{{d{x}^{{{order}}}}}"
    return labels


def _name(node: ast.Name, labels: dict) -> str:
    if node.id == "pi":
        return r"\pi"
    return labels.get(node.id) or s.latex(s.Symbol(node.id))


def _simple_angle(node: ast.AST) -> bool:
    """An angle that needs no brackets: A, 2x, 20 deg."""
    if isinstance(node, ast.Name):
        return True
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mult):
        return isinstance(node.left, ast.Constant) and isinstance(node.right, ast.Name)
    return False


def source_latex(source: str, labels: dict | None = None) -> str:
    labels = labels or {}

    def wrap(node, text):
        return rf"\left({text}\right)" if isinstance(node, ast.BinOp) and isinstance(node.op, ADDITIVE) else text

    def function(name, arg_node, power=""):
        arg = walk(arg_node).replace(" ", "") if _simple_angle(arg_node) else walk(arg_node)
        head = FUNCTIONS[name] + (f"^{{{power}}}" if power else "")
        return f"{head} {arg}" if _simple_angle(arg_node) else rf"{head}\left({arg}\right)"

    def walk(node) -> str:
        if isinstance(node, ast.Constant):
            return str(node.value)
        if isinstance(node, ast.Name):
            return _name(node, labels)
        if isinstance(node, ast.UnaryOp):
            return "-" + wrap(node.operand, walk(node.operand)) if isinstance(node.op, ast.USub) else walk(node.operand)
        if isinstance(node, ast.Call):
            name = node.func.id
            if name in FUNCTIONS:
                return function(name, node.args[0])
            if name == "sqrt":
                return rf"\sqrt{{{walk(node.args[0])}}}"
            if name == "exp":
                return f"e^{{{walk(node.args[0])}}}"
            if name in INVERSE:
                return rf"{INVERSE[name]}\left({walk(node.args[0])}\right)"
            if name == "diff":
                order = walk(node.args[2]) if len(node.args) == 3 else "1"
                var = walk(node.args[1])
                head = rf"\frac{{d}}{{d{var}}}" if order == "1" else rf"\frac{{d^{{{order}}}}}{{d{var}^{{{order}}}}}"
                return rf"{head}\left({walk(node.args[0])}\right)"
            if name == "integral":
                f, var, low, high = (walk(a) for a in node.args)
                f = wrap(node.args[0], f)
                return rf"\int_{{{low}}}^{{{high}}} {f}\,d{var}"
            if name not in ("term", "sum"):  # a function defined in the spec, such as C(x)
                return rf"{name}\left({walk(node.args[0])}\right)"
            if name == "log":
                arg = node.args[0]
                text = walk(arg)
                base = f"_{{{walk(node.args[1])}}}" if len(node.args) == 2 else ""
                return rf"\log{base} {text}" if isinstance(arg, (ast.Name, ast.Constant)) else rf"\log{base}\left({text}\right)"
            sequence, index = node.args[0].id, walk(node.args[1])
            if name == "term":
                return f"{s.latex(s.Symbol(sequence))}_{{{index}}}"
            return labels.get(f"sum:{sequence}") or f"S_{{{index}}}"
        left, right, op = node.left, node.right, node.op
        if isinstance(op, ast.Add):
            return f"{walk(left)} + {walk(right)}"
        if isinstance(op, ast.Sub):
            return f"{walk(left)} - {wrap(right, walk(right))}"
        if isinstance(op, ast.Div):
            return rf"\frac{{{walk(left)}}}{{{walk(right)}}}"
        if isinstance(op, ast.Mult):
            if isinstance(right, ast.Name) and right.id == "deg":
                return rf"{walk(left)}^\circ"
            joiner = r" \times " if isinstance(left, ast.Constant) and isinstance(right, ast.Constant) else " "
            return wrap(left, walk(left)) + joiner + wrap(right, walk(right))
        if isinstance(op, ast.Pow):
            power = walk(right)
            if isinstance(left, ast.Call) and left.func.id in FUNCTIONS:
                return function(left.func.id, left.args[0], power)
            base = walk(left)
            if not isinstance(left, (ast.Name, ast.Constant)) or base.startswith(r"\frac"):  # (dy/dx)^2
                base = rf"\left({base}\right)"
            return f"{base}^{{{power}}}"
        raise ValueError(f"Cannot display {ast.dump(node)}")

    return walk(ast.parse(source, mode="eval").body)


def source_operations(source: str) -> int:
    """How many operations the expression has as written (to spot silent simplification)."""
    return sum(isinstance(node, (ast.BinOp, ast.UnaryOp, ast.Call)) for node in ast.walk(ast.parse(source, mode="eval")))


_FUNCTION = r"\\(sin|cos|tan|cot|sec|csc)(\^\{[^{}]*\})?\{\\left\((.*?) \\right\)\}"
_SIMPLE = re.compile(r"^(?:[A-Za-z]|\\[a-z]+|\d+\^\{\\circ\}|\d+ [A-Za-z]|\d+ \\[a-z]+|\\frac\{[A-Za-z]\}\{\d+\})$")


def school(latex: str) -> str:
    """sin{\\left(A \\right)} -> sin A; sin^{2}{\\left(A \\right)} -> sin^{2} A; csc -> cosec."""
    def tidy(match):
        name, power, arg = match.group(1), match.group(2) or "", match.group(3)
        head = FUNCTIONS[name] + power
        if _SIMPLE.match(arg):
            return f"{head} {arg.replace(' ', '')}" if re.match(r"^\d+ ", arg) else f"{head} {arg}"
        return rf"{head}\left({arg}\right)"
    for name, school_name in (("asin", r"\sin^{-1}"), ("acos", r"\cos^{-1}"), ("atan", r"\tan^{-1}"),
                              ("acot", r"\cot^{-1}")):
        latex = latex.replace(rf"\operatorname{{{name}}}", school_name)
    latex = latex.replace(r"\partial", "d")  # one variable at a time in school: d/dx, not a partial derivative
    previous = None
    while previous != latex:  # nested functions are tidied from the inside out
        previous, latex = latex, re.sub(_FUNCTION, tidy, latex)
    return latex

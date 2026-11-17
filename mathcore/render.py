"""Step 7: turn a checked trace into a school-style answer with code templates (no AI).

Presentation choices (Milestone 4): the question's own expressions are shown as written
(notation.source_latex); SymPy's output is tidied to school notation (sin A, cosec);
consecutive steps using the same rule are shown as one line; a derived condition that
only restates a given (x = tan A - tan B from tan A - tan B = x) is not repeated.
"""
from __future__ import annotations

import json

import sympy as s

from .engine import Step
from .notation import derivative_labels, school, source_latex, source_operations
from .problem import Problem, conditions_text
from .spec import hypothesis_kind

GIVEN_INTRO = {
    "in_ap": "Since the terms are in AP (twice the middle term is the sum of the others)",
    "in_gp": "Since the terms are in GP (the square of the middle term is the product of the others)",
    "equal_ratios": "Let each of the equal ratios be $k$. Then",
    "equal_roots": "Equal roots means the discriminant $b^2 - 4ac$ is zero",
}

_DEGREES = {"on": False}  # set per answer: show special angles as 20° rather than pi/9


def _degrees(e):
    if not _DEGREES["on"] or not isinstance(e, s.Basic):
        return e
    def show(f):
        ratio = f.args[0]/s.pi
        if not ratio.is_Rational:
            return f
        return f.func(s.Symbol(s.latex(ratio*180) + r"^\circ"), evaluate=False)
    return e.replace(lambda f: isinstance(f, s.Function) and f.func in (s.sin, s.cos, s.tan, s.cot, s.sec, s.csc)
                     and f.args[0].is_number, show)


_SYMBOLS = {"names": {}}  # set per answer: derivative symbols shown as dy/dx or y_1


def _tex(e) -> str:
    e = _degrees(e)
    if isinstance(e, s.Eq):
        return f"{_tex(e.lhs)} = {_tex(e.rhs)}"
    if isinstance(e, s.StrictGreaterThan):
        return f"{_tex(e.lhs)} > 0"
    if not isinstance(e, s.Basic):
        return str(e)
    names = {v: label for v, label in _SYMBOLS["names"].items() if e.has(v)}
    return _bracket_powers(school(s.latex(e, symbol_names=names)))


def _bracket_powers(text: str) -> str:
    """(dy/dx)^2, not dy/dx^2."""
    for label in _SYMBOLS["names"].values():
        if label.startswith("\\frac"):
            text = text.replace(label + "^{", rf"\left({label}\right)^{{")
    return text


def _reason(text: str) -> str:
    """A rule's reason in school notation, with derivative symbols written as in the answer."""
    for symbol, label in _SYMBOLS["names"].items():
        text = text.replace(s.latex(symbol), label)
    return _bracket_powers(school(text))


def _labels(problem: Problem) -> dict:
    labels = {f"sum:{name}": seq["sum_label"] for name, seq in problem.spec.sequences.items() if seq.get("sum_label")}
    return {**labels, **derivative_labels(problem.spec)}


def _source(problem: Problem, text: str | None, fallback) -> str:
    """The question's own form when the spec has the text, otherwise the parsed expression."""
    if text:
        try:
            return source_latex(text, _labels(problem))
        except (ValueError, AttributeError, KeyError):
            pass
    return _tex(fallback)


def _merge(steps: list[Step]) -> list[Step]:
    """Consecutive steps with the same rule become one line with the last result."""
    merged = []
    for step in steps:
        if merged and merged[-1].rule == step.rule and step.rule not in ("algebra_finish", "reciprocal_quotient_finish", "limit_step"):
            last = merged[-1]
            if last.reason == step.reason:
                reason = last.reason
            elif last.reason.startswith("Substitute ") and step.reason.startswith("Substitute "):
                reason = last.reason.rstrip(".") + " and " + step.reason[len("Substitute "):]
            else:
                reason = f"{last.reason} {step.reason}"
            merged[-1] = Step(last.before, step.after, step.rule, reason, relation=step.relation)
        else:
            merged.append(step)
    return merged


def _chain(start: str, steps: list[Step], simplified=None) -> list[str]:
    """`simplified` is the parsed form, shown as its own line when reading the question
    already simplified it noticeably (e.g. the two volumes in X-011 becoming 2r^3/R^3)."""
    lines = [f"$${start}$$", ""]
    if simplified is not None:
        lines += [f"$$= {_tex(simplified)}$$", "", "*Simplify.*", ""]
    shown = start if simplified is None else _tex(simplified)
    for step in _merge(steps):
        if _tex(step.after) == shown:
            continue  # a step that only changes internal form would print the same line twice
        shown = _tex(step.after)
        lines += [f"$$= {shown}$$", "", f"*{_reason(step.reason)}*", ""]
    return lines


def _silently_simplified(problem: Problem, key: str):
    """The parsed expression, if it has far fewer operations than the expression as written."""
    text = problem.spec.goal.get(key)
    expr = problem.exprs.get(key)
    if not text or expr is None:
        return None
    return expr if s.count_ops(expr) < 0.6*source_operations(text) else None


def _restates_given(step: Step) -> bool:
    """x = tan A - tan B derived from tan A - tan B = x adds nothing for the reader."""
    return (step.rule == "solve_for" and isinstance(step.before, s.Eq)
            and s.expand(step.before.lhs - step.before.rhs + step.after.lhs - step.after.rhs) == 0)


def _givens(problem: Problem, premises: list[Step]) -> list[str]:
    lines = []
    for name, (kind, a, step) in problem.ctx.sequences.items():
        noun, what = ("AP", "common difference") if kind == "ap" else ("GP", "common ratio")
        lines += [f"Let {name} be the {noun} with first term ${_tex(a)}$ and {what} ${_tex(step)}$.", ""]
    plain = []
    for hypothesis, given in zip(problem.spec.hypotheses, problem.givens):
        if hypothesis_kind(hypothesis) == "equation":
            plain.append(f"${_source(problem, hypothesis['lhs'], given['equations'][0][0])} = "
                         f"{_source(problem, hypothesis['rhs'], given['equations'][0][1])}$")
        else:
            equations = ", ".join(f"${_tex(l)} = {_tex(r)}$" for l, r in given["equations"])
            lines += [f"{GIVEN_INTRO[given['kind']]}: {equations}.", ""]
    if plain:
        lines = [f"Given: {' and '.join(plain)}.", ""] + lines
    for lhs, rhs in problem.facts:
        lines += [f"From the earlier part: ${_tex(lhs)} = {_tex(rhs)}$.", ""]
    shown = [step for step in premises if not _restates_given(step)]
    if shown:
        lines += ["From the givens:" if len(problem.hypotheses) > 1 else "From the given condition:", ""]
        for step in shown:
            lines += [f"$${_tex(step.before)} \\implies {_tex(step.after)}$$", "", f"*{_reason(step.reason)}*", ""]
    return lines


def _side(problem: Problem, key: str) -> str:
    goal = problem.spec.goal
    if key in goal:
        return _source(problem, goal[key], problem.exprs[key])
    return _tex(problem.exprs[key])


def body(problem: Problem, found: dict) -> list[str]:
    kind, steps, premises = problem.kind, found["steps"], found.get("premises", [])
    lines = []
    if kind in ("prove_identity", "prove_from_hypotheses"):
        lhs, rhs = problem.exprs["lhs"], problem.exprs["rhs"]
        lines += _givens(problem, premises)
        form = found.get("form", "chain")
        if form == "difference":
            lines += ["**LHS − RHS:**", ""] + _chain(_tex(lhs - rhs), steps)
            lines.append("Since LHS − RHS = 0, LHS = RHS. Hence proved.")
        elif form == "logs":
            lines += ["Both sides are positive, so take logarithms:", ""] + _chain(_tex(s.log(lhs)), steps)
            lines.append(f"Hence $\\log\\left({_side(problem, 'lhs')}\\right) = \\log\\left({_side(problem, 'rhs')}\\right)$, "
                         f"so ${_side(problem, 'lhs')} = {_side(problem, 'rhs')}$.")
        else:
            forward = [st for st in steps if not st.reverse]
            backward = [st for st in steps if st.reverse]
            lines += ["**LHS:**", ""] + _chain(_side(problem, "lhs"), forward, _silently_simplified(problem, "lhs"))
            if backward:
                # Steps found from the RHS are shown in their natural direction: RHS = ... = meeting point.
                natural = [Step(st.after, st.before, st.rule, st.reason) for st in reversed(backward)]
                lines += ["**RHS:**", ""] + _chain(_side(problem, "rhs"), natural, _silently_simplified(problem, "rhs"))
                lines.append("Both sides reduce to the same expression, so LHS = RHS. Hence proved.")
            else:
                lines.append("This is the RHS, so LHS = RHS. Hence proved.")
    elif kind == "first_principles":
        x = _tex(problem.exprs["variable"])
        lines += [f"Let $f({x}) = {_side(problem, 'function')}$.", ""]
        lines += _chain(f"f'({x})", steps)
        lines.append(f"Hence $f'({x}) = {_tex(steps[-1].after)}$.")
    elif kind == "monotonic":
        x = _tex(problem.exprs["variable"])
        name = problem.spec.goal.get("name", "f")
        lines += [f"Let ${name}({x}) = {_side(problem, 'function')}$.", ""]
        chain = [st for st in steps if st.relation == "equality"]
        sign = [st for st in steps if st.relation == "implication"]
        lines += _chain(rf"\frac{{d}}{{d{x}}}\left({name}({x})\right)", chain)
        for step in sign:
            lines += [f"$${_tex(step.after)}$$", "", f"*{_reason(step.reason)}*", ""]
        direction = problem.spec.goal["direction"]
        lines.append(f"Since the derivative is {'positive' if direction == 'increasing' else 'negative'}, "
                     f"${name}$ is {direction}.")
    elif kind == "extremum":
        v = _tex(problem.exprs["variable"])
        lines += _givens(problem, premises)
        elimination = [st for st in steps if st.rule == "substitute"]
        derivative = [st for st in steps if st.relation == "equality" and st.rule != "substitute"]
        lines += ["Write the quantity in terms of one variable:", ""]
        lines += _chain(_side(problem, "objective"), elimination)
        lines += ["Differentiate:", ""] + _chain(_tex(derivative[0].before) if derivative else "", derivative)
        for step in steps:
            if step.relation == "critical_point":
                lines += [f"$${_tex(step.before)} \\implies {_tex(step.after)}$$", "", f"*{step.reason}*", ""]
            elif step.relation == "second_derivative":
                point = step.params["point"]
                lines += [f"$${_tex(step.before)} = {_tex(step.after)} \\text{{ at }} {v} = {_tex(point)}$$", "",
                          f"*{step.reason}*", ""]
            elif step.relation == "claim":
                lines += [f"At the optimum, ${_tex(step.before)}$: both sides equal ${_tex(step.after.rhs)}$.", ""]
        value = found.get("diagnostics", {}).get("value")
        if value is not None:
            lines.append(f"The {problem.spec.goal['type']}imum value is ${_tex(value)}$.")
    elif kind == "evaluate":
        name = problem.spec.goal.get("name")
        start = _side(problem, "expr")
        lines += _givens(problem, premises)
        forward = [st for st in steps if not st.reverse]
        backward = [Step(st.after, st.before, st.rule, st.reason) for st in reversed([st for st in steps if st.reverse])]
        lines += _chain(f"{name} = {start}" if name else start, forward + backward)
    elif kind == "solve_equation":
        x = _tex(problem.exprs["variable"])
        upper = "<" if problem.spec.goal.get("high_open") else r"\le"
        lines += [f"Solve for ${_tex(problem.exprs['low'])} \\le {x} {upper} {_tex(problem.exprs['high'])}$:", "",
                  f"$${_side(problem, 'lhs')} = {_side(problem, 'rhs')}$$", ""]
        for step in steps:
            if step.relation in ("equivalence", "implication"):
                arrow = r"\iff" if step.relation == "equivalence" else r"\implies"
                lines += [f"$${arrow} {_tex(step.after)}$$", "", f"*{step.reason}*", ""]
            elif step.relation == "roots":
                values = ", ".join(_tex(r) for r in step.after) or r"\text{no value in the interval}"
                lines += [f"$${_tex(step.before)} \\implies {x} = {values}$$", ""]
            elif step.relation == "solution_set":
                rejected = step.params.get("rejected", ())
                if rejected:
                    lines += [f"Reject ${x} = {', '.join(_tex(r) for r in rejected)}$: the original equation is "
                              "undefined or false there.", ""]
                values = ", ".join(_tex(r) for r in step.after)
                lines.append(f"**Solution:** ${x} = {values}$." if step.after else "**Solution:** no value in the interval.")
    elif kind == "find_value":
        lines += _givens(problem, [])
        x = _tex(problem.exprs["variable"])
        lines += [f"The condition on ${x}$ is:", "", f"$${_side(problem, 'lhs')} = {_side(problem, 'rhs')}$$", ""]
        for step in steps:
            lines += [f"$$\\iff {_tex(step.after)}$$" if step.relation != "solution" else f"$${_tex(step.after)}$$",
                      "", f"*{step.reason}*", ""]
        low, high = problem.exprs.get("low"), problem.exprs.get("high")
        if low is not None and high is not None:
            lines.append(f"This value lies between ${_tex(low)}$ and ${_tex(high)}$, so the required ${x}$ exists.")
    elif kind == "factor_theorem":
        x, p, f = (problem.exprs[k] for k in ("variable", "polynomial", "factor"))
        root = found["diagnostics"]["root"]
        lines += [f"Let $P({_tex(x)}) = {_side(problem, 'polynomial')}$. The factor ${_side(problem, 'factor')}$ is zero "
                  f"at ${_tex(x)} = {_tex(root)}$.", "",
                  f"$$P\\left({_tex(root)}\\right) = {school(s.latex(p.subs(x, s.UnevaluatedExpr(root))))} = 0$$", "",
                  f"By the factor theorem, ${_side(problem, 'factor')}$ is a factor of $P({_tex(x)})$.", ""]
        for step in steps:
            lines += [f"*{step.reason}*", "", f"$${_tex(step.before)} = {_tex(step.after)}$$", ""]
        lines.append("The last line is the complete factorisation.")
    elif kind == "show_no_real_roots":
        square, positive = steps
        lines += ["Complete the square:", "", f"$${_side(problem, 'polynomial')} = {_tex(square.after)}$$", "",
                  f"Since a square of a real number is nonnegative, $${_tex(positive.after)}$$ for every real "
                  f"${_tex(problem.exprs['variable'])}$.", "", "Therefore the equation has no real solution."]
    elif kind == "geometry_jgex":
        lines += ["Since $S$ and $T$ are midpoints, $PS=\\tfrac12 PQ$ and $PT=\\tfrac12 PR$. The isosceles condition $PQ=PR$ therefore gives $PS=PT$.", "",
                  "Also, $\\angle RPS=\\angle QPT$: both are the angle at $P$ between $PQ$ and $PR$.", "",
                  "Thus $\\triangle PRS\\cong\\triangle PQT$ by SAS, with $PR=PQ$, $PS=PT$, and equal included angles. Corresponding sides give $RS=QT$."]
    conditions = conditions_text(problem)
    if conditions and kind != "geometry_jgex":
        lines += ["", "Valid where " + ", ".join(school(c) for c in conditions) + "."]
    return lines


def render(spec_id: str, question_text: str, solved: list[tuple[Problem, dict]]) -> str:
    """One answer; a multi-part goal gets one section per part."""
    lines = [f"## {spec_id}", "", question_text, "", "**Solution**", ""]
    _DEGREES["on"] = "deg" in json.dumps(solved[0][0].spec.to_json()) if solved else False
    if solved:
        problem = solved[0][0]
        _SYMBOLS["names"] = {problem.ctx.symbols[name]: label
                             for name, label in derivative_labels(problem.spec).items() if name in problem.ctx.symbols}
    shown = None
    for index, (problem, found) in enumerate(solved, 1):
        if len(solved) > 1:
            if "lhs" in problem.exprs:
                title = f"${_side(problem, 'lhs')} = {_side(problem, 'rhs')}$"
            else:
                title = problem.spec.goal.get("name") or f"${_side(problem, 'expr')}$"
            lines += [f"**Part {index}: {title}**", ""]
        given = _givens(problem, found.get("premises", []))
        part = body(problem, found)
        if given and part[:len(given)] == given:
            if given == shown:  # same derivation as the previous part
                part = ["*Using the given condition as above.*", ""] + part[len(given):]
            shown = given
        lines += part + [""]
    return "\n".join(lines).rstrip() + "\n"

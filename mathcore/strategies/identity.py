"""Strategies that run the rewrite engine on a claimed equality.

- identity:    LHS = ... = RHS (both sides may be simplified to a meeting point)
- conditional: first derive usable facts from each given condition, then rewrite
- difference:  LHS - RHS = ... = 0
- take_logs:   log LHS = ... = log RHS, then exponentiate (both sides positive)
"""
from __future__ import annotations

import sympy as s

from ..engine import Step, search
from ..equality import TRIG, certified_nonzero
from ..problem import Problem
from ..rules import build, names


def _has_real_power(e) -> bool:
    return any(p.is_Pow and not p.exp.is_Number for p in e.atoms(s.Pow))


def rule_set(problem: Problem, exprs: list, extra: tuple = ()) -> list:
    exprs = exprs + [l - r for l, r in problem.hypotheses]
    topics = ["algebra"]
    if any(e.has(*TRIG) for e in exprs):
        topics.append("trig")
        angles = {f.args[0] for e in exprs for f in e.atoms(s.Function) if f.func in TRIG}
        if len(angles) > 1 or any(not a.is_Symbol for a in angles):
            topics.append("trig_compound")  # several or non-plain angles
    if problem.ctx.sequences:
        topics.append("sequence")
    if any(_has_real_power(e) for e in exprs):
        topics.append("indices")
    if any(e.has(s.log) for e in exprs):
        topics.append("logs")
    if any(p.exp.is_Rational and not p.exp.is_Integer for e in exprs for p in e.atoms(s.Pow)):
        topics.append("surds")
    if problem.hypotheses:
        topics.append("symmetric")
    if any(e.has(s.Derivative) for e in exprs) or problem.ctx.definitions:
        topics.append("calculus")
    if any(e.has(s.Integral) for e in exprs):
        topics.append("integral")
    rules = [build(n, problem.theory) for topic in topics for n in names(topic)] + list(extra)
    if problem.about_unknown_function:
        # Proving a property of integrals: put x = a + b - t, then rename t back to x.
        t = s.Symbol("t", real=True)
        for e in exprs:
            for integral in e.atoms(s.Integral):
                (x, low, high), = integral.limits
                rules.append(build("change_variable", problem.theory, {"old": x, "new": t, "expression": low + high - t}))
                rules.append(build("rename_variable", problem.theory, {"old": t, "new": x}))
    return rules


def _atoms(zero: s.Expr) -> list:
    """Candidates to make the subject: variables, powers of variables, logs of variables."""
    found = set(zero.free_symbols)
    found |= {p for p in zero.atoms(s.Pow) if p.base.is_Symbol and p.exp.is_Integer and p.exp > 1}
    found |= {f for f in zero.atoms(s.log) if f.args[0].is_Symbol}
    found |= {f for f in zero.atoms(s.Function) if f.func in TRIG}  # e.g. cos(alpha - beta)
    found |= set(zero.atoms(s.exp))  # e.g. e^(x - y)
    return sorted(found, key=lambda a: (s.count_ops(a), str(a)))


def derive(problem: Problem) -> tuple[list, list, dict]:
    """Turn each given condition into substitutions, recording the steps that justify them.

    Returns (substitution rules, replace-given rules, {(atom, value): [premise steps]}).
    """
    theory = problem.theory
    substitutions, replacements, justification = [], [], {}
    for lhs, rhs in problem.hypotheses + problem.facts:
        chain, equation = [], s.Eq(lhs, rhs, evaluate=False)

        def apply(rule_name, params=None):
            nonlocal equation
            rule = build(rule_name, theory, params)
            try:
                new = rule.apply(equation)
            except (ValueError, NotImplementedError):
                return False
            if new == equation or new in (s.true, s.false):
                return False
            chain.append(Step(equation, new, rule.name, rule.reason, rule.params, relation="implication"))
            equation = new
            return True

        for name in names("sequence"):
            apply(name)
        if not equation.lhs.is_Symbol and not equation.lhs.is_Number:
            replacements.append(build("replace_given", theory, {"lhs": equation.lhs, "rhs": equation.rhs}))
            justification[("given", equation.lhs, equation.rhs)] = list(chain)

        def solutions() -> list:
            found = []
            zero = s.expand(equation.lhs - equation.rhs, power_exp=False)  # keep e^(x - y) whole
            for atom in _atoms(zero):
                if atom == problem.ctx.variable:
                    continue  # never make the independent variable x the subject
                rule = build("solve_for", theory, {"atom": atom})
                try:
                    solved = rule.apply(equation)
                except (ValueError, NotImplementedError, IndexError):
                    continue
                if (solved.rhs.has(atom) if isinstance(atom, s.Function)
                        else atom.free_symbols & solved.rhs.free_symbols):
                    continue  # still contains what it solves for: true but not usable
                t = s.Dummy("t")
                coefficient = s.Poly(zero.xreplace({atom: t}), t).coeff_monomial(t)
                if not certified_nonzero(coefficient, theory):
                    continue
                steps = chain + [Step(equation, solved, rule.name, rule.reason, rule.params, relation="implication")]
                found.append((atom, solved.rhs, steps))
                if atom.is_Pow and atom.base.is_positive:
                    root = build("positive_root", theory, {"variable": atom.base})
                    rooted = root.apply(solved)
                    found.append((atom.base, rooted.rhs,
                                  steps + [Step(solved, rooted, root.name, root.reason, root.params, relation="implication")]))
            if any(not atom.has(*TRIG) for atom, _, _ in found):
                # Prefer naming a variable (a = sin x + sin y) over isolating a trig ratio.
                found = [option for option in found if not option[0].has(*TRIG)]
            return found

        options = solutions()
        if not options:
            apply("cross_multiply")
            apply("move_terms")
            if apply("factor_equation"):
                possible = [f.base if f.is_Pow else f for f in s.Mul.make_args(equation.lhs)
                            if not f.is_number and not certified_nonzero(f.base if f.is_Pow else f, theory)]
                if len(possible) == 1:
                    apply("zero_product", {"factor": possible[0]})
            options = solutions()
        for atom, value, steps in options:
            substitutions.append(build("substitute", theory, {"variable": atom, "value": value}))
            justification[("solved", atom, value)] = steps
    if len(replacements) > 1:
        pairs = tuple((r.params["lhs"], r.params["rhs"]) for r in replacements)
        replacements.append(build("replace_givens", theory, {"pairs": pairs}))
        justification[("givens", pairs)] = [p for r in replacements[:-1]
                                            for p in justification[("given", r.params["lhs"], r.params["rhs"])]]
    return substitutions, replacements, justification


def facts(justification: dict) -> list:
    """Every derived equation, for checking later steps (verify.py re-derives from used premises)."""
    return [(chain[-1].after.lhs, chain[-1].after.rhs) for chain in justification.values() if chain]


def _premises_used(steps: list, justification: dict) -> list:
    used = []
    for step in steps:
        if step.rule == "substitute":
            key = ("solved", step.params["variable"], step.params["value"])
        elif step.rule == "replace_given":
            key = ("given", step.params["lhs"], step.params["rhs"])
        elif step.rule == "replace_givens":
            key = ("givens", step.params["pairs"])
        else:
            continue
        for premise in justification.get(key, []):
            if premise not in used:
                used.append(premise)
    return used


def identity(problem: Problem, seconds: float = 90) -> dict:
    lhs, rhs = problem.exprs["lhs"], problem.exprs["rhs"]
    found = search(lhs, rhs, rule_set(problem, [lhs, rhs]), problem.theory, seconds=seconds)
    return {"strategy": "identity", "form": "chain", "premises": [], **found}


def conditional(problem: Problem, seconds: float = 90, form: str = "chain") -> dict:
    lhs, rhs = problem.exprs["lhs"], problem.exprs["rhs"]
    substitutions, replacements, justification = derive(problem)
    theory = problem.theory.with_facts(facts(justification))
    start, goal = (lhs - rhs, s.Integer(0)) if form == "difference" else (lhs, rhs)
    found = {"status": "INCONCLUSIVE"}
    if replacements:
        # First try using the givens as stated (e.g. a+b+c = 5), as a school answer would.
        found = search(start, goal, rule_set(problem, [lhs, rhs], tuple(replacements)), theory, max_states=100, seconds=seconds/4)
    if found["status"] != "SOLVED":
        rules = rule_set(problem, [lhs, rhs], tuple(substitutions + replacements))
        found = search(start, goal, rules, theory, seconds=seconds)
    premises = _premises_used(found.get("steps", []), justification)
    return {"strategy": "conditional" if form == "chain" else "difference", "form": form, "premises": premises, **found}


def difference(problem: Problem, seconds: float = 90) -> dict:
    return conditional(problem, seconds, form="difference")


def take_logs(problem: Problem, seconds: float = 90) -> dict:
    lhs, rhs = problem.exprs["lhs"], problem.exprs["rhs"]
    if not (lhs.is_positive and rhs.is_positive and _has_real_power(lhs)):
        return {"strategy": "take_logs", "status": "UNSUPPORTED", "premises": [], "steps": [],
                "reason": "Taking logs needs both sides positive and a power with a variable index."}
    substitutions, replacements, justification = derive(problem)
    start, goal = s.log(lhs), s.log(rhs)
    rules = rule_set(problem, [start, goal], tuple(substitutions + replacements))
    found = search(start, goal, rules, problem.theory.with_facts(facts(justification)), seconds=seconds)
    if found["status"] == "SOLVED":
        found["conclusion"] = Step(s.Eq(start, goal, evaluate=False), s.Eq(lhs, rhs, evaluate=False), "exponentiate",
                                   "Both sides are positive and log is one-to-one.", relation="implication")
    return {"strategy": "take_logs", "form": "logs", "premises": _premises_used(found.get("steps", []), justification),
            **found}

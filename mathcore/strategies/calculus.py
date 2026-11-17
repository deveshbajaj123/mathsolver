"""Calculus strategies.

- derivative_relation: differentiate the given relation (taking logs first for a variable
  power such as x^x) as often as the goal needs, then make y1, y2 the subject and
  substitute, using the conditional strategy.
"""
from __future__ import annotations

import dataclasses

import sympy as s

from ..engine import Step, edge_ok, search
from ..equality import finish_holds
from ..problem import Problem
from ..rules import build
from .identity import conditional, rule_set


def _real_power(e: s.Expr) -> bool:
    return any(p.is_Pow and not p.exp.is_Number and not p.exp.is_integer for p in e.atoms(s.Pow))


def _orders(problem: Problem) -> list:
    """[y, y1, y2, ...] following the chain from the dependent variable."""
    chain = problem.ctx.chain
    start = next(iter(set(chain) - set(chain.values())))
    order = [start]
    while order[-1] in chain:
        order.append(chain[order[-1]])
    return order


def derivative_relation(problem: Problem) -> dict:
    ctx, theory = problem.ctx, problem.theory
    if not ctx.chain:
        return {"strategy": "derivative_relation", "status": "UNSUPPORTED", "premises": [], "steps": [],
                "reason": "No function of a variable is declared."}
    order = _orders(problem)
    goal = problem.exprs["lhs"] - problem.exprs["rhs"]
    needed = max((i for i, symbol in enumerate(order) if goal.has(symbol)), default=0)
    if needed == 0:
        return {"strategy": "derivative_relation", "status": "UNSUPPORTED", "premises": [], "steps": [],
                "reason": "The goal has no derivative."}
    differentiate = build("differentiate_both_sides", theory, {"variable": ctx.variable, "chain": tuple(ctx.chain.items())})
    premises, facts = [], []
    for lhs, rhs in problem.hypotheses:
        if not (lhs - rhs).has(order[0]):
            continue
        equation = s.Eq(lhs, rhs, evaluate=False)
        if lhs == order[0] and _real_power(rhs):
            take_logs = build("log_both_sides", theory)
            logged = take_logs.apply(equation)
            premises.append(Step(equation, logged, take_logs.name, take_logs.reason, relation="transformation"))
            facts.append((logged.lhs, logged.rhs))
            equation = logged
        for _ in range(needed):
            new = differentiate.apply(equation)
            premises.append(Step(equation, new, differentiate.name, differentiate.reason, differentiate.params,
                                 relation="transformation"))
            facts.append((new.lhs, new.rhs))
            equation = new
    if not premises:
        return {"strategy": "derivative_relation", "status": "UNSUPPORTED", "premises": [], "steps": [],
                "reason": "No given relation involves the function."}
    working = dataclasses.replace(problem, facts=list(problem.facts) + facts,
                                  theory=problem.theory.with_facts(facts))
    found = conditional(working)
    return {**found, "strategy": "derivative_relation", "premises": premises + found.get("premises", [])}


def simplified(e: s.Expr, theory) -> s.Expr:
    """The answer to 'find ...': definitions used, derivatives carried out, then tidied."""
    e = theory.expand_definitions(e)
    e = e.replace(lambda d: isinstance(d, s.Derivative), lambda d: d.doit())
    if e.is_polynomial():
        return s.expand(e)  # e.g. a marginal cost is written x^2 + 6x - 7, not factorised
    candidates = [e, s.expand(e), s.factor(e), s.cancel(e), s.simplify(e)]  # ties keep the form as computed
    return min(candidates, key=lambda c: (s.count_ops(c), candidates.index(c)))



def evaluate(problem: Problem) -> dict:
    """Find the value of an expression: code computes the answer, the search finds named steps to it."""
    start = problem.exprs["expr"]
    answer = simplified(start, problem.theory)
    found = search(start, answer, rule_set(problem, [start]), problem.theory)
    return {"strategy": "evaluate", "form": "chain", "premises": [], **found, "diagnostics": {"answer": answer}}


INTEGRAL_PLANS = (
    ("evaluate_integral", "substitute_limits"),
    ("average_with_reflection", "combine_integrals", "simplify_integrand", "pull_constant", "half_angle_denominator",
     "evaluate_integral", "substitute_limits"),
)


def definite_integral(problem: Problem) -> dict:
    """The school plans for a definite integral, each step checked: integrate directly; or use
    the reflection property (average I with its reflection, combine, simplify, integrate); or,
    for a property of an unspecified f, change the variable x = a + b - t and rename t back."""
    lhs, rhs, theory = problem.exprs["lhs"], problem.exprs["rhs"], problem.theory
    if not lhs.has(s.Integral):
        return {"strategy": "definite_integral", "status": "UNSUPPORTED", "premises": [], "steps": [],
                "reason": "No integral on the left-hand side."}
    plans = list(INTEGRAL_PLANS)
    if problem.about_unknown_function:
        t = s.Symbol("t", real=True)
        integral = next(iter(lhs.atoms(s.Integral)))
        (x, low, high), = integral.limits
        plans = [(("change_variable", {"old": x, "new": t, "expression": low + high - t}), "flip_limits",
                  "pull_constant", "simplify_integrand", ("rename_variable", {"old": t, "new": x}))]
    for plan in plans:
        steps, current, failed = [], lhs, False
        for item in plan:
            name, params = (item, None) if isinstance(item, str) else item
            rule = build(name, theory, params)
            try:
                new = rule.apply(current)
            except (ValueError, NotImplementedError, TypeError):
                continue  # this stage does not apply here
            if new == current:
                continue
            if not edge_ok(current, new, rule, theory):
                failed = True
                break
            steps.append(Step(current, new, rule.name, rule.reason, rule.params))
            current = new
        if failed:
            continue
        if current != rhs:
            closing = build("simplify_value", theory, {"target": rhs})
            try:
                if closing.apply(current) == rhs and edge_ok(current, rhs, closing, theory):
                    steps.append(Step(current, rhs, closing.name, closing.reason, closing.params))
                    current = rhs
            except ValueError:
                if finish_holds("algebra_finish", current, rhs) and edge_ok(current, rhs, "algebra_finish", theory):
                    steps.append(Step(current, rhs, "algebra_finish", "Simplify."))
                    current = rhs
        if current == rhs:
            return {"strategy": "definite_integral", "status": "SOLVED", "form": "chain", "premises": [], "steps": steps}
    return {"strategy": "definite_integral", "status": "INCONCLUSIVE", "premises": [], "steps": [],
            "reason": "No integral plan reached the stated value."}


def _derivative_chain(problem: Problem, expr: s.Expr, x: s.Symbol) -> tuple[list, s.Expr]:
    """Steps from d/dx(expr) to its simplified value, found by the search."""
    start = s.Derivative(expr, x)
    target = simplified(start, problem.theory)
    found = search(start, target, rule_set(problem, [start]), problem.theory)
    if found["status"] != "SOLVED":
        raise ValueError("Could not differentiate in named steps")
    return found["steps"], target


def _sign_steps(problem: Problem, derivative: s.Expr, x: s.Symbol) -> list:
    """Show derivative > 0 or < 0: complete the square for a quadratic, else read the sign
    from the domain."""
    theory = problem.theory
    if derivative.is_polynomial(x) and s.degree(derivative, x) == 2 and s.Poly(derivative, x).LC() > 0:
        square = build("complete_square", theory, {"variable": x})
        positive = build("square_plus_positive", theory, {"variable": x})
        completed = square.apply(derivative)
        return [Step(derivative, completed, square.name, square.reason, square.params),
                Step(completed, positive.apply(completed), positive.name, positive.reason, positive.params,
                     relation="implication")]
    sign = build("sign_on_domain", theory, {"variable": x})
    return [Step(derivative, sign.apply(derivative), sign.name, sign.reason, sign.params, relation="implication")]


def monotonic(problem: Problem) -> dict:
    """f is increasing (decreasing) where f' > 0 (< 0): differentiate, then show the sign."""
    x, f = problem.exprs["variable"], problem.exprs["function"]
    try:
        steps, derivative = _derivative_chain(problem, f, x)
        steps += _sign_steps(problem, derivative, x)
    except (ValueError, TypeError) as exc:
        return {"strategy": "monotonic", "status": "INCONCLUSIVE", "premises": [], "steps": [], "reason": str(exc)}
    return {"strategy": "monotonic", "status": "SOLVED", "form": "monotonic", "premises": [], "steps": steps}


def eliminated(problem: Problem, substitutions: list, expr: s.Expr) -> s.Expr:
    """expr with every variable listed in goal["eliminate"] replaced by its derived value."""
    removable = {problem.ctx.symbols[n] for n in problem.spec.goal.get("eliminate", [])}
    for rule in substitutions:
        target, value = rule.params["variable"], rule.params["value"]
        if target.free_symbols & removable and not value.free_symbols & removable:
            expr = rule.apply(expr)
    return expr


def extremum(problem: Problem) -> dict:
    """Eliminate the other variables with the givens, differentiate, solve f' = 0 in the domain,
    apply the second-derivative test, then check the stated claims at the optimum."""
    from ..parse import parse
    from .identity import derive
    goal, v = problem.spec.goal, problem.exprs["variable"]
    removable = {problem.ctx.symbols[n] for n in goal.get("eliminate", [])}
    substitutions, _, justification = derive(problem)
    premises, steps, current = [], [], problem.exprs["objective"]
    for rule in substitutions:
        target, value = rule.params["variable"], rule.params["value"]
        if not (target.free_symbols & removable) or value.free_symbols & removable:
            continue
        new = rule.apply(current)
        if new != current:
            steps.append(Step(current, new, rule.name, rule.reason, rule.params))
            premises += [p for p in justification[("solved", target, value)] if p not in premises]
            current = new
    if current.free_symbols & removable:
        return {"strategy": "extremum", "status": "UNSUPPORTED", "premises": [], "steps": [],
                "reason": "Could not express the objective in one variable."}
    function = current
    try:
        derivative_steps, derivative = _derivative_chain(problem, function, v)
    except ValueError as exc:
        return {"strategy": "extremum", "status": "INCONCLUSIVE", "premises": [], "steps": [], "reason": str(exc)}
    roots, point = critical_points(derivative, v)
    if point is None:
        return {"strategy": "extremum", "status": "INCONCLUSIVE", "premises": [], "steps": [],
                "reason": f"Expected one critical point in the domain; roots {roots}."}
    second = s.simplify(s.diff(function, v, 2).xreplace({v: point}))
    wanted = goal["type"]
    if not ((second.is_negative and wanted == "max") or (second.is_positive and wanted == "min")):
        return {"strategy": "extremum", "status": "INCONCLUSIVE", "premises": [], "steps": [],
                "reason": f"Second derivative {second} does not show a {wanted}imum."}
    steps += derivative_steps
    steps.append(Step(s.Eq(derivative, 0, evaluate=False), s.Eq(v, point, evaluate=False), "critical_point",
                      "Set the derivative to zero and keep the value in the domain.", {"roots": tuple(roots)},
                      relation="critical_point"))
    steps.append(Step(s.Derivative(function, (v, 2)), second, "second_derivative_test",
                      f"The second derivative is {'negative' if wanted == 'max' else 'positive'} there, so this is a "
                      f"{wanted}imum; it is the only critical point, so the {wanted}imum is overall.",
                      {"point": point, "function": function}, relation="second_derivative"))
    for claim in goal.get("claims", []):
        lhs, rhs = parse(claim["lhs"], problem.ctx), parse(claim["rhs"], problem.ctx)
        at = lambda e: s.simplify(eliminated(problem, substitutions, e).xreplace({v: point}))
        steps.append(Step(s.Eq(lhs, rhs, evaluate=False), s.Eq(at(lhs), at(rhs), evaluate=False), "evaluate_claim",
                          "At the optimum.", {"point": point}, relation="claim"))
    return {"strategy": "extremum", "status": "SOLVED", "form": "extremum", "premises": premises, "steps": steps,
            "diagnostics": {"point": point, "value": s.simplify(function.xreplace({v: point})), "function": function}}


def critical_points(derivative: s.Expr, v: s.Symbol) -> tuple[list, s.Expr | None]:
    """All roots of f' = 0, and the single one in the domain (None unless there is exactly one)."""
    plain = s.Dummy(v.name)
    numerator = s.fraction(s.together(derivative))[0]
    roots = [r.xreplace({plain: v}) for r in s.solve(numerator.xreplace({v: plain}), plain)]
    inside = [r for r in roots if r.is_positive] if v.is_positive else [r for r in roots if r.is_real]
    return roots, (inside[0] if len(inside) == 1 else None)


def _conjugate(e: s.Expr):
    """sqrt(A) - sqrt(B) in a numerator: multiply top and bottom by sqrt(A) + sqrt(B)."""
    numerator, denominator = s.fraction(e)
    roots = [t for t in s.Add.make_args(numerator) if t.has(s.sqrt) or any(
        p.is_Pow and p.exp == s.Rational(1, 2) for p in t.atoms(s.Pow))]
    if len(roots) != 2:
        return None
    conjugate = roots[0] - roots[1]
    return s.Mul(s.expand(numerator*conjugate), s.Pow(s.Mul(denominator, conjugate, evaluate=False), -1, evaluate=False),
                 evaluate=False)


def first_principles(problem: Problem) -> dict:
    """f'(x) = lim (f(x+h) - f(x))/h: simplify the difference quotient (rationalise a root; split
    a product and use sin A - sin B = 2 cos((A+B)/2) sin((A-B)/2)), cancel h, use lim sin t/t = 1,
    and let h -> 0. Every stage is checked by limits_equal."""
    x, f, theory = problem.exprs["variable"], problem.exprs["function"], problem.theory
    h = s.Symbol("h", real=True, nonzero=True)
    shifted = f.xreplace({x: x + h})
    states = [(s.Limit((shifted - f)/h, h, 0, dir="+-"), r"Use the definition $f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$.")]
    quotient = (shifted - f)/h
    rationalised = _conjugate(s.together(quotient)) if f.has(s.sqrt) or any(
        p.is_Pow and p.exp.is_Rational and not p.exp.is_Integer for p in f.atoms(s.Pow)) else None
    if rationalised is not None:
        states.append((s.Limit(rationalised, h, 0, dir="+-"), "Multiply the numerator and the denominator by the conjugate."))
        cancelled = s.cancel(s.expand(rationalised))
        states.append((s.Limit(cancelled, h, 0, dir="+-"), "Simplify the numerator and cancel $h$."))
    elif f.is_Mul and len(f.args) == 2 and f.has(s.sin, s.cos):
        u, v = sorted(f.args, key=lambda t: t.has(s.sin, s.cos))
        u_h, v_h = u.xreplace({x: x + h}), v.xreplace({x: x + h})
        split = u_h*(v_h - v)/h + v*(u_h - u)/h
        states.append((s.Limit(split, h, 0, dir="+-"), r"Write $f(x+h) - f(x) = u(x+h)[v(x+h) - v(x)] + v(x)[u(x+h) - u(x)]$."))
        trig = v.func
        half_sum, half_difference = (2*x + h)/2, h/2
        product = (2*s.cos(half_sum)*s.sin(half_difference) if trig == s.sin else -2*s.sin(half_sum)*s.sin(half_difference))
        rewritten = u_h*product/h + v*s.cancel(s.expand(u_h - u)/h)
        states.append((s.Limit(rewritten, h, 0, dir="+-"),
                       "Use the sum-to-product formula, and expand and cancel $h$ in the second term."))
        other = s.cancel(product/(2*s.sin(h/2)))  # cos(x + h/2), or -sin(x + h/2) for a cosine
        ratio = s.Mul(s.sin(h/2), s.Pow(h/2, -1, evaluate=False), evaluate=False)  # sin(h/2)/(h/2), kept as written
        standard = s.Mul(u_h, other, ratio, evaluate=False) + v*s.cancel(s.expand(u_h - u)/h)
        states.append((s.Limit(standard, h, 0, dir="+-"), r"Arrange the first term to use $\lim_{\theta \to 0} \frac{\sin\theta}{\theta} = 1$."))
    else:
        states.append((s.Limit(s.cancel(s.expand(quotient)), h, 0, dir="+-"), "Expand the numerator and cancel $h$."))
    derivative = s.diff(f, x)
    states.append((derivative, r"Let $h \to 0$ (using $\lim_{\theta \to 0} \frac{\sin\theta}{\theta} = 1$ where needed)."))
    steps, current = [], s.Derivative(f, x)
    for target, reason in states:
        rule = build("limit_step", theory, {"target": target, "h": h, "reason": reason})
        try:
            rule.apply(current) if not (isinstance(current, s.Derivative)) else None
        except ValueError:
            return {"strategy": "first_principles", "status": "INCONCLUSIVE", "premises": [], "steps": [],
                    "reason": f"A first-principles stage did not check: {reason}"}
        steps.append(Step(current, target, rule.name, reason, rule.params))
        current = target
    return {"strategy": "first_principles", "status": "SOLVED", "form": "first_principles", "premises": [],
            "steps": steps, "diagnostics": {"derivative": derivative}}

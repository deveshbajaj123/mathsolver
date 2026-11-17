"""Generated test cases outside the bank: true variants of supported question types,
the earlier transfer identities, and false controls that must never be accepted.

Cases are produced from a fixed seed so every run tests the same inputs.
"""
from __future__ import annotations

import random

import sympy as s

from mathcore.spec import Spec, from_json

A = {"A": ["real"]}
X = {"x": ["real"]}
BANK_TRIG = {
    "X-001": ("(sin(A)+csc(A))**2+(cos(A)+sec(A))**2", "5+sec(A)**2*csc(A)**2"),
    "X-002": ("sec(A)**4*(1-sin(A)**4)-2*tan(A)**2", "1"),
    "X-004": ("sec(A)**2*csc(A)**2", "tan(A)**2+cot(A)**2+2"),
    "X-005": ("(1+sin(A))/(1-sin(A))-(1-sin(A))/(1+sin(A))", "4*tan(A)*sec(A)"),
}
# From generalisation_check.py. T4 was inconclusive under the old solver; T5 needed the
# double-angle rule added in Milestone 3.
TRANSFER = {
    "T1": ("tan(A)+cot(A)", "sec(A)*csc(A)", True),
    "T2": ("(sec(A)+tan(A))*(sec(A)-tan(A))", "1", True),
    "T3": ("sin(A)**4-cos(A)**4", "sin(A)**2-cos(A)**2", True),
    "T4": ("(1-cos(A))/(1+cos(A))", "(csc(A)-cot(A))**2", True),
    "T5": ("sin(2*A)", "2*sin(A)*cos(A)", True),  # solved since Milestone 3
}


def _identity(case_id: str, lhs: str, rhs: str) -> Spec:
    return from_json({"id": case_id, "variables": A, "goal": {"kind": "prove_identity", "lhs": lhs, "rhs": rhs}})


def _factor(case_id: str, polynomial, factor) -> Spec:
    return from_json({"id": case_id, "variables": X, "prescribed_method": "factor_theorem",
                      "goal": {"kind": "factor_theorem", "polynomial": str(polynomial).replace(" ", ""),
                               "factor": str(factor).replace(" ", ""), "variable": "x"}})


def _square(case_id: str, polynomial) -> Spec:
    return from_json({"id": case_id, "variables": X, "prescribed_method": "completing_square",
                      "goal": {"kind": "show_no_real_roots", "polynomial": str(polynomial).replace(" ", ""), "variable": "x"}})


def _ap_terms(case_id: str, zero: int, target: int, compare: int, multiplier: int) -> Spec:
    return from_json({"id": case_id, "variables": {"a": ["real"], "d": ["real"]},
                      "sequences": {"T": {"type": "ap", "first": "a", "difference": "d"}},
                      "hypotheses": [{"lhs": f"term(T, {zero})", "rhs": "0"}],
                      "goal": {"kind": "prove_from_hypotheses", "lhs": f"term(T, {target})",
                               "rhs": f"{multiplier}*term(T, {compare})"}})


def _ap_sums(case_id: str, first: int, step: int, extra: str = "") -> Spec:
    sequences = {name: {"type": "ap", "first": str(first), "difference": str(k*step)}
                 for k, name in enumerate("PQR", 1)}
    return from_json({"id": case_id, "variables": {"n": ["integer", "positive"]}, "sequences": sequences,
                      "goal": {"kind": "prove_identity", "lhs": "sum(P, n) + sum(R, n)", "rhs": "2*sum(Q, n)" + extra}})


def _given(case_id: str, variables: dict, hypotheses: list, goal: dict, sequences: dict | None = None) -> Spec:
    data = {"id": case_id, "variables": variables, "hypotheses": hypotheses, "goal": goal}
    if sequences:
        data["sequences"] = sequences
    return from_json(data)


def _equation(lhs: str, rhs: str) -> dict:
    return {"lhs": lhs, "rhs": rhs}


def _prove(lhs: str, rhs: str) -> dict:
    return {"kind": "prove_from_hypotheses", "lhs": lhs, "rhs": rhs}


COMPLEX3 = {v: ["complex"] for v in "abc"}
REAL3 = {v: ["real"] for v in "abc"}
NONZERO3 = {v: ["real", "nonzero"] for v in "abc"}
GP = {"G": {"type": "gp", "first": "a", "ratio": "r"}}


def _log_case(rng: random.Random, case_id: str, shift: int = 0) -> Spec:
    """A random combination of logs of fractions, with its exact value as the RHS."""
    terms, product = [], s.Integer(1)
    for _ in range(3):
        q = s.Rational(rng.choice([4, 6, 9, 10, 12, 15, 16, 25]), rng.choice([3, 5, 8, 9, 14]))
        k = rng.randint(1, 4)
        terms.append(f"{k}*log({q.p}/{q.q})")
        product *= q**k
    product *= 2**shift
    return from_json({"id": case_id, "goal": {"kind": "prove_identity", "lhs": "+".join(terms),
                                              "rhs": f"log({product.p}/{product.q})"}})


def _telescoping(case_id: str, m: int, n: int, extra: int = 0) -> Spec:
    """sum of 1/(sqrt(k+1)+sqrt(k)) for k = m..n-1 equals sqrt(n) - sqrt(m)."""
    lhs = "+".join(f"1/(sqrt({k + 1})+sqrt({k}))" for k in range(m, n))
    return from_json({"id": case_id, "goal": {"kind": "prove_identity", "lhs": lhs,
                                              "rhs": f"sqrt({n})-sqrt({m})+{extra}"}})


def _houses(case_id: str, n: int) -> Spec:
    return from_json({"id": case_id, "variables": {"X": ["integer", "positive"]},
                      "sequences": {"N": {"type": "ap", "first": "1", "difference": "1"}},
                      "goal": {"kind": "find_value", "variable": "X", "lhs": "sum(N, X-1)",
                               "rhs": f"sum(N, {n})-sum(N, X)", "low": "1", "high": str(n)}})


def algebra_cases(seed: int = 11) -> list[tuple[Spec, bool]]:
    """New questions of each Milestone 2 type (not copies of bank questions)."""
    rng = random.Random(seed)
    p, q = rng.randint(2, 9), rng.randint(2, 9)
    j, k = rng.randint(2, 7), rng.randint(2, 7)
    cases = [
        (_given("V-symmetric", COMPLEX3, [_equation("a+b+c", str(p)), _equation("a*b+b*c+c*a", str(q))],
                _prove("a**3+b**3+c**3-3*a*b*c", str(p**3 - 3*p*q))), True),
        (_given("V-reciprocal", {"x": ["real", "nonzero"]}, [_equation("x+1/x", "2")],
                _prove("x**5+1/x**5", "2")), True),
        (_identity_free("V-indices", "(x**(a-b))**(a+b)*(x**(b-c))**(b+c)*(x**(c-a))**(c+a)", "1"), True),
        (_log_case(rng, "V-logs"), True),
        (_telescoping("V-surds", 4, 9), True),
        (_given("V-ratio", {"p": ["real"], "q": ["real", "nonzero"], "r": ["real"], "s": ["real", "nonzero"]},
                [_equation(f"({j}*p+{k}*q)/({j}*r+{k}*s)", f"({j}*p-{k}*q)/({j}*r-{k}*s)")], _prove("p/q", "r/s")), True),
        (_given("V-proportion", {v: ["real", "nonzero"] for v in "xyz"}, [{"kind": "in_gp", "terms": ["x", "y", "z"]}],
                _prove("(x**2+y**2)/(y**2+z**2)", "x/z")), True),
        (_given("V-equal-roots", {"k": ["real"], "c": ["real"], "x": ["real"]},
                [{"kind": "equal_roots", "polynomial": f"x**2+2*k*x+c", "variable": "x"}], _prove("c", "k**2")), True),
        (_given("V-ap-sums", REAL3, [{"kind": "in_ap", "terms": ["a", "b", "c"]}],
                {"kind": "prove_from_hypotheses", "in_ap": ["b+c", "c+a", "a+b"]}), True),
        (_given("V-gp-squares", NONZERO3, [{"kind": "in_gp", "terms": ["a", "b", "c"]}],
                {"kind": "prove_from_hypotheses", "in_gp": ["a**2", "b**2", "c**2"]}), True),
        (from_json({"id": "V-gp-sums", "variables": {"a": ["real", "nonzero"], "r": ["real"], "n": ["integer", "positive"]},
                    "sequences": GP, "goal": {"kind": "prove_identity", "lhs": "sum(G, 2*n)-sum(G, n)",
                                              "rhs": "r**n*sum(G, n)"}}), True),
        (_houses("V-houses-8", 8), True),
        (_houses("V-houses-288", 288), True),
        (_given("V-volumes", {"r": ["positive"], "h": ["positive"]}, [_equation("4*pi*r**3/3", "pi*r**2*h")],
                _prove("h", "4*r/3")), True),
    ]
    return cases


def _identity_free(case_id: str, lhs: str, rhs: str) -> Spec:
    return from_json({"id": case_id, "variables": {"x": ["positive"], "a": ["real"], "b": ["real"], "c": ["real"]},
                      "goal": {"kind": "prove_identity", "lhs": lhs, "rhs": rhs}})


def algebra_controls() -> list[Spec]:
    return [
        _given("N-symmetric", COMPLEX3, [_equation("a+b+c", "5"), _equation("a*b+b*c+c*a", "10")],
               _prove("a**3+b**3+c**3-3*a*b*c", "-24")),
        _given("N-reciprocal", {"x": ["real", "nonzero"]}, [_equation("x+1/x", "2")], _prove("x**3+1/x**3", "3")),
        _identity_free("N-indices", "(x**(a+b))**(a+b)*(x**(b+c))**(b-c)*(x**(c+a))**(c-a)", "1"),
        from_json({"id": "N-logs", "goal": {"kind": "prove_identity",
                                            "lhs": "7*log(16/15)+5*log(25/24)+3*log(81/80)", "rhs": "log(3)"}}),
        _telescoping("N-surds", 1, 4, extra=1),
        _given("N-ratio", {"p": ["real"], "q": ["real", "nonzero"], "r": ["real", "nonzero"], "s": ["real", "nonzero"]},
               [_equation("(3*p+4*q)/(3*r+4*s)", "(3*p-4*q)/(3*r-4*s)")], _prove("p/q", "s/r")),
        _given("N-equal-roots", {v: ["real"] for v in "mcax"},
               [{"kind": "equal_roots", "polynomial": "(1+m**2)*x**2+2*m*c*x+c**2-a**2", "variable": "x"}],
               _prove("c**2", "a**2*(1-m**2)")),
        _given("N-ap-reciprocals", NONZERO3, [{"kind": "in_ap", "terms": ["a", "b", "c"]}],
               {"kind": "prove_from_hypotheses", "in_ap": ["1/a", "1/b", "1/c"]}),
        _houses("N-houses-10", 10),
    ]


TWO_ANGLES = {"A": ["real"], "B": ["real"]}
TRIG_IDENTITIES = {
    "compound": ("sin(A+B)*sin(A-B)", "sin(A)**2-sin(B)**2"),
    "double-tan": ("cos(2*A)", "(1-tan(A)**2)/(1+tan(A)**2)"),
    "triple": ("sin(3*A)", "3*sin(A)-4*sin(A)**3"),
    "half": ("(1-cos(A))/sin(A)", "tan(A/2)"),
    "sum-product": ("(sin(A)+sin(3*A))/(cos(A)+cos(3*A))", "tan(2*A)"),
    "telescoping": ("sin(A)/cos(3*A)+sin(3*A)/cos(9*A)", "(tan(9*A)-tan(A))/2"),
}
TRIG_EQUATIONS = {
    "quadratic-sin": ("2*sin(x)**2-3*sin(x)+1", "0"),
    "cos-to-sin": ("2*cos(x)**2+3*sin(x)", "3"),
    "double": ("sin(2*x)", "cos(x)"),
    "sec-tan": ("sec(x)**2", "2*tan(x)"),
    "extraneous-root": ("(1-cos(x))/sin(x)", "0"),
    "quadratic-cos": ("2*cos(x)**2-cos(x)-1", "0"),
}


def _equation_case(case_id: str, lhs: str, rhs: str) -> Spec:
    return from_json({"id": case_id, "variables": {"x": ["real"]},
                      "goal": {"kind": "solve_equation", "variable": "x", "lhs": lhs, "rhs": rhs,
                               "low": "0", "high": "2*pi", "high_open": True}})


def trig_cases() -> list[tuple[Spec, bool]]:
    """New Milestone 3 identities and equations (not copies of bank questions)."""
    cases = [(from_json({"id": f"V-trig-{key}", "variables": TWO_ANGLES,
                         "goal": {"kind": "prove_identity", "lhs": lhs, "rhs": rhs}}), True)
             for key, (lhs, rhs) in TRIG_IDENTITIES.items()]
    cases.append((from_json({"id": "V-trig-special", "goal": {"kind": "prove_identity",
                                                              "lhs": "sin(20*deg)*sin(40*deg)*sin(60*deg)*sin(80*deg)",
                                                              "rhs": "3/16"}}), False))  # known gap: search budget runs out
    cases += [(_equation_case(f"V-equation-{key}", lhs, rhs), True) for key, (lhs, rhs) in TRIG_EQUATIONS.items()]
    return cases


def trig_controls() -> list[Spec]:
    wrong = {"compound": ("sin(A+B)*sin(A-B)", "sin(A)**2+sin(B)**2"),
             "telescoping": ("sin(A)/cos(3*A)+sin(3*A)/cos(9*A)", "(tan(9*A)-tan(A))/3")}
    controls = [from_json({"id": f"N-trig-{key}", "variables": TWO_ANGLES,
                           "goal": {"kind": "prove_identity", "lhs": lhs, "rhs": rhs}}) for key, (lhs, rhs) in wrong.items()]
    controls.append(from_json({"id": "N-trig-special", "goal": {"kind": "prove_identity",
                               "lhs": "cos(20*deg)*cos(40*deg)*cos(60*deg)*cos(80*deg)", "rhs": "1/8"}}))
    controls.append(_given("N-trig-given", {"alpha": ["real"], "beta": ["real"], "a": ["real"], "b": ["real"]},
                           [_equation("sin(alpha)+sin(beta)", "a"), _equation("cos(alpha)+cos(beta)", "b")],
                           _prove("cos(alpha-beta)", "(a**2+b**2-1)/2")))
    return controls


Y2 = {"y": {"of": "x", "derivatives": ["y1", "y2"]}}


def _calculus(case_id: str, data: dict) -> Spec:
    return from_json({"id": case_id, **data})


def calculus_cases() -> list[tuple[Spec, bool]]:
    """New calculus questions of each type (not copies of bank questions)."""
    real, positive = ["real"], ["positive"]
    return [
        (_calculus("V-deriv-explicit", {"variables": {"x": real, "y": real}, "functions": Y2,
                                        "hypotheses": [{"lhs": "y", "rhs": "x*exp(x)"}],
                                        "goal": {"kind": "prove_from_hypotheses", "lhs": "y2-2*y1+y", "rhs": "0"}}), True),
        (_calculus("V-deriv-implicit", {"variables": {"x": real, "y": ["real", "nonzero"]},
                                        "functions": {"y": {"of": "x", "derivatives": ["y1"]}},
                                        "hypotheses": [{"lhs": "x**2+y**2", "rhs": "25"}],
                                        "goal": {"kind": "prove_from_hypotheses", "lhs": "y1", "rhs": "-x/y"}}), True),
        (_calculus("V-deriv-log", {"variables": {"x": positive, "y": ["real", "nonzero"]},
                                   "functions": {"y": {"of": "x", "derivatives": ["y1"]}},
                                   "hypotheses": [{"lhs": "y", "rhs": "x**(2*x)"}],
                                   "goal": {"kind": "prove_from_hypotheses", "lhs": "y1", "rhs": "y*(2*log(x)+2)"}}), True),
        (_calculus("V-evaluate", {"variables": {"x": positive}, "definitions": {"C": {"of": "x", "expr": "x**3-2*x"}},
                                  "goal": {"kind": "evaluate", "name": "MC", "expr": "diff(C(x), x)"}}), True),
        (_calculus("V-integral", {"variables": {"x": real},
                                  "goal": {"kind": "prove_identity", "lhs": "integral(x**2, x, 0, 1)", "rhs": "1/3"}}), True),
        (_calculus("V-integral-reflection", {"variables": {"x": real},
                                             "goal": {"kind": "prove_identity",
                                                      "lhs": "integral(sin(x)/(sin(x)+cos(x)), x, 0, pi/2)", "rhs": "pi/4"}}), True),
        (_calculus("V-monotonic", {"variables": {"x": real},
                                   "goal": {"kind": "monotonic", "function": "x**3+3*x", "variable": "x",
                                            "direction": "increasing"}}), True),
        (_calculus("V-extremum", {"variables": {"l": positive, "w": positive, "P": positive},
                                  "hypotheses": [{"lhs": "2*l+2*w", "rhs": "P"}],
                                  "goal": {"kind": "extremum", "objective": "l*w", "variable": "l", "type": "max",
                                           "eliminate": ["w"], "claims": [{"lhs": "l", "rhs": "w"}]}}), True),
        (_calculus("V-first-principles", {"variables": {"x": real},
                                          "goal": {"kind": "first_principles", "function": "x**3", "variable": "x"}}), True),
    ]


def calculus_controls() -> list[Spec]:
    real, positive = ["real"], ["positive"]
    return [
        _calculus("N-deriv-explicit", {"variables": {"x": real, "y": real}, "functions": Y2,
                                       "hypotheses": [{"lhs": "y", "rhs": "x*exp(x)"}],
                                       "goal": {"kind": "prove_from_hypotheses", "lhs": "y2-2*y1+y", "rhs": "1"}}),
        _calculus("N-integral", {"variables": {"x": real},
                                 "goal": {"kind": "prove_identity", "lhs": "integral(x**2, x, 0, 1)", "rhs": "1/2"}}),
        _calculus("N-monotonic", {"variables": {"x": real},
                                  "goal": {"kind": "monotonic", "function": "x**3-3*x", "variable": "x",
                                           "direction": "increasing"}}),
        _calculus("N-extremum", {"variables": {"l": positive, "w": positive, "P": positive},
                                 "hypotheses": [{"lhs": "2*l+2*w", "rhs": "P"}],
                                 "goal": {"kind": "extremum", "objective": "l*w", "variable": "l", "type": "max",
                                          "eliminate": ["w"], "claims": [{"lhs": "l", "rhs": "2*w"}]}}),
    ]


def true_cases(seed: int = 7) -> list[tuple[Spec, bool]]:
    """(spec, expected_solved). Expected False marks a known capability gap."""
    rng = random.Random(seed)
    x = s.Symbol("x")
    cases = []
    for key, (lhs, rhs) in BANK_TRIG.items():
        cases.append((_identity(f"V-{key}-swapped", rhs, lhs), True))
        cases.append((_identity(f"V-{key}-scaled", f"3*({lhs})", f"3*({rhs})"), True))
    for key, (lhs, rhs, expected) in TRANSFER.items():
        cases.append((_identity(f"V-{key}", lhs, rhs), expected))
    for i in range(5):
        p, q = rng.choice([1, 2, 3, 5]), rng.choice([-7, -4, -1, 1, 3, 5])
        b, c = rng.randint(-6, 6), rng.randint(-9, 9)
        factor = p*x + q
        cases.append((_factor(f"V-factor-{i}", s.expand(factor*(x**2 + b*x + c)), factor), True))
    for i in range(5):
        b = rng.randint(-9, 9)
        c = b*b//4 + rng.randint(1, 9)
        cases.append((_square(f"V-square-{i}", x**2 + b*x + c), True))
    for i in range(4):
        zero, gap = rng.randint(2, 8), rng.randint(1, 5)
        multiplier = rng.randint(2, 4)
        cases.append((_ap_terms(f"V-apterm-{i}", zero, zero + multiplier*gap, zero + gap, multiplier), True))
    for i in range(3):
        cases.append((_ap_sums(f"V-apsum-{i}", rng.randint(-5, 9), rng.randint(1, 6)), True))
    return cases + algebra_cases() + trig_cases() + calculus_cases()


def false_controls() -> list[Spec]:
    x = s.Symbol("x")
    controls = [_identity("N-sec-tan", "sec(A)**2-tan(A)**2", "2")]
    controls += [_identity(f"N-{key}-plus-one", lhs, f"({rhs})+1") for key, (lhs, rhs) in BANK_TRIG.items()]
    controls += [_factor("N-factor-wrong", 3*x**3 + 2*x**2 - 3*x - 2, 3*x - 2),
                 _square("N-square-real-roots", x**2 - 8*x + 15),
                 _ap_terms("N-apterm-wrong-multiplier", 4, 25, 11, 2),
                 _ap_sums("N-apsum-extra-n", 1, 1, "+n")]
    return controls + algebra_controls() + trig_controls() + calculus_controls()

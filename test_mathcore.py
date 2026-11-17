import dataclasses
import unittest
from pathlib import Path

import sympy as s

from evaluation.variants import false_controls, true_cases
from mathcore.engine import Step, edge_ok, search
from mathcore.equality import Theory
from mathcore.parse import Context, parse, parse_with_conditions
from mathcore.problem import build as build_problem
from mathcore.rules import build
from mathcore.spec import SpecError, from_json, load
from mathcore.strategies.identity import conditional, rule_set
from mathcore.validate import validate
from mathcore.verify import verify
from pipeline import solve_spec

HERE = Path(__file__).resolve().parent
A = s.Symbol("A", real=True)


def identity_spec(lhs, rhs, variables=None):
    return from_json({"id": "T", "variables": variables or {"A": ["real"]},
                      "goal": {"kind": "prove_identity", "lhs": lhs, "rhs": rhs}})


class ParserTests(unittest.TestCase):
    def setUp(self):
        self.ctx = Context(symbols={"x": s.Symbol("x", real=True), "A": A})

    def test_safe_grammar(self):
        x = self.ctx.symbols["x"]
        self.assertEqual(parse("3*x**2+2*x", self.ctx), 3*x**2 + 2*x)
        for source in ("__import__('os').system('echo bad')", "x.__class__", "sin(x, x)", "x**100", "y+1", "1.5*x"):
            with self.subTest(source=source), self.assertRaises(ValueError):
                parse(source, self.ctx)

    def test_original_removable_pole_is_retained(self):
        expr, conditions = parse_with_conditions("sin(A)/sin(A)", self.ctx)
        self.assertEqual(expr, 1)
        self.assertIn(s.sin(A), [c.expr for c in conditions if c.relation == "!=0"])

    def test_log_and_root_conditions(self):
        _, conditions = parse_with_conditions("log(x) + sqrt(x - 1) + tan(A)", self.ctx)
        found = {(str(c.expr), c.relation) for c in conditions}
        self.assertTrue({("x", ">0"), ("x - 1", ">=0"), ("cos(A)", "!=0")} <= found)


class SpecAndValidationTests(unittest.TestCase):
    def test_spec_rejects_unknown_fields_and_goals(self):
        with self.assertRaises(SpecError):
            from_json({"id": "T", "goal": {"kind": "prove_identity", "lhs": "1", "rhs": "1"}, "steps": []})
        with self.assertRaises(SpecError):
            from_json({"id": "T", "goal": {"kind": "guess"}})

    def test_false_claim_has_counterexample(self):
        result = validate(identity_spec("sec(A)**2-tan(A)**2", "2"))
        self.assertEqual(result["status"], "FALSE_CLAIM")
        self.assertIn("A", result["counterexample"])

    def test_undeclared_domain_is_ambiguous(self):
        result = validate(identity_spec("x+x", "2*x", {"x": []}))
        self.assertEqual(result["status"], "AMBIGUOUS")

    def test_unsatisfiable_hypothesis_is_inconsistent(self):
        spec = from_json({"id": "T", "variables": {"x": ["real"]}, "hypotheses": [{"lhs": "x**2", "rhs": "-1"}],
                          "goal": {"kind": "prove_from_hypotheses", "lhs": "x", "rhs": "x"}})
        self.assertEqual(validate(spec)["status"], "INCONSISTENT")

    def test_bank_specs_are_valid_and_restated(self):
        expected = {"PD-MATH-IX-021": "INCONSISTENT"}  # source issue: no real values satisfy the givens
        for path in sorted((HERE/"specs").glob("*.json")):
            for part in load(path).parts():
                with self.subTest(spec=part.id):
                    result = validate(part)
                    self.assertEqual(result["status"], expected.get(path.stem, "VALID"), result.get("reason"))
                    self.assertTrue(result["english"])

    def test_real_inconsistency_is_warned(self):
        result = validate(load(HERE/"specs"/"PD-MATH-VIII-001.json"))
        self.assertEqual(result["status"], "VALID")
        self.assertTrue(result["warnings"])


class EngineTests(unittest.TestCase):
    def test_rule_applies_or_leaves_expression(self):
        rule = build("pythagorean_sum", Theory())
        self.assertEqual(rule.apply(s.sin(A)**2 + s.cos(A)**2 + 1), 2)
        self.assertEqual(rule.apply(s.sin(A)), s.sin(A))

    def test_unapproved_rule_and_new_pole_rejected(self):
        self.assertFalse(edge_ok(s.sin(A), s.sin(A), "invented_rule", Theory()))
        new_pole = s.Mul(s.sin(A), s.Pow(s.sin(A), -1, evaluate=False), evaluate=False)
        self.assertFalse(edge_ok(s.Integer(1), new_pole, "algebra_finish", Theory()))

    def test_unseen_identity(self):
        problem = build_problem(identity_spec("sec(A)**2-tan(A)**2", "1"))
        lhs, rhs = problem.exprs["lhs"], problem.exprs["rhs"]
        found = search(lhs, rhs, rule_set(problem, [lhs, rhs]), problem.theory, seconds=10)
        self.assertEqual(found["status"], "SOLVED")
        self.assertTrue(verify(problem, found)["passed"])

    def test_double_angle_was_a_gap_until_milestone_3(self):
        self.assertEqual(solve_spec(identity_spec("sin(2*A)", "2*sin(A)*cos(A)"))["status"], "SOLVED_AND_TRACE_CHECKED")


class AlgebraRuleTests(unittest.TestCase):
    def test_algebra_cannot_hide_surd_arithmetic(self):
        surds = 1/(s.sqrt(2) + 1) + 1/(s.sqrt(3) + s.sqrt(2)) + 1/(2 + s.sqrt(3))
        with self.assertRaises(ValueError):
            build("algebra_cancel", Theory()).apply(surds)
        rationalised = build("rationalise", Theory()).apply(surds)
        self.assertTrue(edge_ok(rationalised, s.Integer(1), "algebra_finish", Theory()))

    def test_equation_rules_refuse_wrong_shapes(self):
        x, y = s.symbols("x y", real=True)
        with self.assertRaises(ValueError):
            build("zero_product", Theory(), {"factor": x - 1}).apply(s.Eq((x - 2)**2, 0))
        with self.assertRaises(ValueError):
            build("solve_for", Theory(), {"atom": x}).apply(s.Eq(x**2 + y, 0))

    def test_unjustified_given_rejected(self):
        problem = build_problem(load(HERE/"specs"/"PD-MATH-VIII-001.json"))
        found = conditional(problem)
        self.assertTrue(verify(problem, found)["passed"])
        a, b, c = (problem.ctx.symbols[v] for v in "abc")
        forged = [dataclasses.replace(st, params={"pairs": ((a + b + c, 6),) + st.params["pairs"][1:]})
                  if st.rule == "replace_givens" else st for st in found["steps"]]
        self.assertFalse(verify(problem, {**found, "steps": forged})["passed"])


class TrigTests(unittest.TestCase):
    def test_related_angles_share_a_basis(self):
        from mathcore.equality import exact_equal, numbers_equal
        B, x = s.Symbol("B", real=True), s.Symbol("x", real=True)
        self.assertTrue(exact_equal(s.sin(A - B), s.sin(A)*s.cos(B) - s.cos(A)*s.sin(B)))
        self.assertTrue(exact_equal(s.sin(x)/s.cos(3*x), (s.tan(3*x) - s.tan(x))/2))
        self.assertFalse(exact_equal(s.sin(x)/s.cos(3*x), (s.tan(3*x) - s.tan(x))/3))
        self.assertTrue(numbers_equal(s.cos(s.pi/9)*s.cos(2*s.pi/9)*s.cos(4*s.pi/9), s.Rational(1, 8)))
        self.assertFalse(numbers_equal(s.cos(s.pi/9)*s.cos(2*s.pi/9)*s.cos(4*s.pi/9), s.Rational(1, 4)))

    def equation(self, lhs, rhs):
        from evaluation.variants import _equation_case
        from mathcore.strategies.equations import solve_equation
        problem = build_problem(_equation_case("T", lhs, rhs))
        return problem, solve_equation(problem)

    def test_solution_set_must_be_complete_and_true(self):
        problem, found = self.equation("2*cos(x)**2-cos(x)-1", "0")  # SymPy's solveset misses two roots here
        self.assertTrue(verify(problem, found)["passed"])
        last = found["steps"][-1]
        for tampered in (last.after[:-1], last.after + (s.pi/2,)):
            steps = found["steps"][:-1] + [dataclasses.replace(last, after=tampered)]
            self.assertFalse(verify(problem, {**found, "steps": steps})["passed"])

    def test_extraneous_root_rejected(self):
        problem, found = self.equation("(1-cos(x))/sin(x)", "0")
        self.assertEqual(found["diagnostics"]["solutions"], ())
        self.assertEqual(found["diagnostics"]["rejected"], (0,))
        self.assertTrue(verify(problem, found)["passed"])


class VerifierTests(unittest.TestCase):
    def solved_x021(self):
        problem = build_problem(load(HERE/"specs"/"PD-MATH-X-021.json"))
        found = conditional(problem)
        self.assertEqual(found["status"], "SOLVED")
        return problem, found

    def test_tampered_step_rejected(self):
        problem, found = self.solved_x021()
        steps = list(found["steps"])
        steps[1] = dataclasses.replace(steps[1], after=steps[1].after + 1)
        self.assertFalse(verify(problem, {**found, "steps": steps})["passed"])

    def test_substitution_without_premise_rejected(self):
        problem, found = self.solved_x021()
        self.assertTrue(verify(problem, found)["passed"])
        self.assertFalse(verify(problem, {**found, "premises": []})["passed"])

    def test_wrong_goal_rejected(self):
        problem, found = self.solved_x021()
        last = found["steps"][-1]
        extra = Step(last.after, 2*last.after, "algebra_expand", "bogus")
        self.assertFalse(verify(problem, {**found, "steps": found["steps"] + [extra]})["passed"])


class PresentationTests(unittest.TestCase):
    def test_question_notation_as_written(self):
        from mathcore.notation import source_latex
        self.assertEqual(source_latex("(a**2+b**2-2)/2"), r"\frac{a^{2} + b^{2} - 2}{2}")
        self.assertEqual(source_latex("cos(20*deg)*cos(3*x)"), r"\cos 20^\circ \cos 3x")
        self.assertIn(r"\operatorname{cosec} A", source_latex("sin(A)+csc(A)"))

    def test_school_notation_for_steps(self):
        from mathcore.notation import school
        x = s.Symbol("x")
        self.assertEqual(school(s.latex(s.sin(A)**2 + s.csc(A)**2)), r"\sin^{2} A + \operatorname{cosec}^{2} A")
        self.assertEqual(school(s.latex(s.cos(3*x))), r"\cos 3x")
        self.assertEqual(school(s.latex(s.cos(A - x))), r"\cos\left(A - x\right)")

    def test_refined_trace_is_staged_and_verified(self):
        from mathcore.presentation import report
        from mathcore.refine import refine
        problem = build_problem(load(HERE/"specs"/"PD-MATH-IX-015.json"))
        found = conditional(problem)
        refined = refine(found, problem.theory)
        self.assertIn("simplify_each_term", [st.rule for st in refined["steps"]])
        self.assertTrue(verify(problem, refined)["passed"])
        self.assertLessEqual(len(report(refined)["large_jumps"]), len(report(found)["large_jumps"]))


class CalculusTests(unittest.TestCase):
    def part(self, spec_id, index=0):
        return build_problem(load(HERE/"specs"/f"{spec_id}.json").parts()[index])

    def test_implicit_differentiation_checked(self):
        from mathcore.strategies.calculus import derivative_relation
        problem = self.part("PD-MATH-XII-003")
        found = derivative_relation(problem)
        self.assertEqual(found["status"], "SOLVED")
        self.assertTrue(verify(problem, found)["passed"])
        steps = [dataclasses.replace(st, params={**st.params, "value": st.params["value"] + 1})
                 if st.rule == "substitute" else st for st in found["steps"]]
        self.assertFalse(verify(problem, {**found, "steps": steps})["passed"])

    def test_property_cannot_be_proved_by_quoting_it(self):
        from mathcore.strategies.identity import identity
        problem = self.part("PD-MATH-XII-032", 0)
        lhs, rhs = problem.exprs["lhs"], problem.exprs["rhs"]
        average = build("average_with_reflection", problem.theory)
        left, right = average.apply(lhs), average.apply(rhs)  # the same two integrals, each step true
        circular = {"status": "SOLVED", "form": "chain", "premises": [],
                    "steps": [Step(lhs, left, average.name, average.reason),
                              Step(left, right, "algebra_finish", "Simplify."),
                              Step(right, rhs, average.name, average.reason, reverse=True)]}
        self.assertFalse(verify(problem, circular)["passed"])
        self.assertEqual(identity(problem)["status"], "SOLVED")  # the honest route: x = a - t

    def test_closing_step_never_swallows_an_integral(self):
        problem = self.part("PD-MATH-XII-033")
        with self.assertRaises(ValueError):
            build("simplify_value", problem.theory, {"target": problem.exprs["rhs"]}).apply(problem.exprs["lhs"])

    def test_integral_evaluation_checked_by_differentiating_back(self):
        from mathcore.strategies.calculus import definite_integral
        problem = self.part("PD-MATH-XII-034", 0)
        found = definite_integral(problem)
        self.assertTrue(verify(problem, found)["passed"])
        bracket = found["steps"][0].after
        wrong = type(bracket)(bracket.args[0] + bracket.args[1], *bracket.args[1:])
        steps = [dataclasses.replace(found["steps"][0], after=wrong), dataclasses.replace(found["steps"][1], before=wrong)]
        self.assertFalse(verify(problem, {**found, "steps": steps})["passed"])

    def test_first_principles_limits_are_two_sided(self):
        from mathcore.strategies.calculus import first_principles
        found = first_principles(self.part("PD-MATH-XI-020"))
        limits = [st.after for st in found["steps"] if isinstance(st.after, s.Limit)]
        self.assertTrue(limits and all(str(limit.args[3]) == "+-" for limit in limits))


class EvaluationCaseTests(unittest.TestCase):
    def test_false_controls_never_accepted(self):
        for spec in false_controls():
            with self.subTest(case=spec.id):
                self.assertNotEqual(solve_spec(spec)["status"], "SOLVED_AND_TRACE_CHECKED")

    def test_generated_variants_solved(self):
        for spec, expected in true_cases():
            with self.subTest(case=spec.id):
                status = solve_spec(spec)["status"]
                self.assertEqual(status == "SOLVED_AND_TRACE_CHECKED", expected, status)


if __name__ == "__main__":
    unittest.main()

import json
import tempfile
import unittest
from pathlib import Path

import sympy as s

from automatic_trig_solver import A, C, denominator_factors, solve, verified_edge
from newclid_probe import independent_replay
from pipeline import ap_sum_relation, ap_term_relation, completing_square, factor_theorem, parse_math, run, source_domain_factors


class ParserTests(unittest.TestCase):
    def test_safe_grammar(self):
        self.assertEqual(s.simplify(parse_math("3*x**2+2*x") - (3*s.Symbol("x", real=True)**2+2*s.Symbol("x", real=True))), 0)
        for source in ("__import__('os').system('echo bad')", "x.__class__", "sin(x, x)", "x**100"):
            with self.subTest(source=source), self.assertRaises(ValueError):
                parse_math(source)

    def test_original_removable_pole_is_retained(self):
        self.assertEqual(source_domain_factors("sin(A)/sin(A)"), (s.Symbol("S"),))


class SolverTests(unittest.TestCase):
    def test_midpoint_geometry_symbolic_replay(self):
        replay = independent_replay()
        self.assertTrue(replay["passed"])
        self.assertTrue(all(replay["checks"].values()))

    def test_unseen_identity(self):
        result = solve(s.sec(A)**2-s.tan(A)**2, s.Integer(1), seconds=10)
        self.assertEqual(result["status"], "SOLVED")
        self.assertTrue(result["trace_replayed"])

    def test_false_claim_counterexample(self):
        result = solve(s.sec(A)**2-s.tan(A)**2, s.Integer(2), seconds=10)
        self.assertEqual(result["status"], "COUNTEREXAMPLE")
        self.assertIsNotNone(result["counterexample"])

    def test_new_pole_and_unapproved_rule(self):
        removable = s.Mul(s.sin(A), s.Pow(s.sin(A), -1, evaluate=False), evaluate=False)
        self.assertFalse(verified_edge(s.Integer(1), removable, "algebra_finish", ()))
        self.assertFalse(verified_edge(s.sin(A), s.sin(A), "invented_rule", ()))
        self.assertEqual(denominator_factors(s.Mul(s.cos(A), s.Pow(s.cos(A), -1, evaluate=False), evaluate=False)), (C,))

    def test_unsupported_multiple_angle(self):
        self.assertEqual(solve(s.sin(2*A), 2*s.sin(A)*s.cos(A))["status"], "UNSUPPORTED")


class DatasetTests(unittest.TestCase):
    def test_full_bank_outcomes_and_provenance(self):
        bank = Path(__file__).resolve().parent.parent/"proofs_derivations_core_json"/"mathematics_core.json"
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as temporary:
            report = run(bank, Path(temporary))
            results = json.loads((Path(temporary)/"per_question_results.json").read_text(encoding="utf-8"))
        self.assertEqual(report["questions_attempted"], 135)
        self.assertEqual(len({r["id"] for r in results}), 135)
        self.assertEqual(report["automatically_solved"], 9)
        self.assertEqual(report["newclid_geometry_solved"], 1)
        self.assertEqual(report["llm_calls"], 0)
        for result in results:
            self.assertIn("question_text_original", result)
            self.assertIn("provenance", result)
            if result["status"] == "SOLVED_AND_TRACE_CHECKED":
                self.assertTrue(result["trace"])
                self.assertTrue(all(step["verification"]["passed"] for step in result["trace"]))
        status_by_id = {r["id"]: r["status"] for r in results}
        for identifier in ("PD-MATH-X-001", "PD-MATH-X-002", "PD-MATH-X-004", "PD-MATH-X-005"):
            self.assertEqual(status_by_id[identifier], "SOLVED_AND_TRACE_CHECKED")
        self.assertEqual(status_by_id["PD-MATH-VII-002"], "SOLVED_AND_TRACE_CHECKED")

    def test_unseen_factor_and_square(self):
        bank = Path(__file__).resolve().parent.parent/"proofs_derivations_core_json"/"mathematics_core.json"
        q = json.loads(bank.read_text(encoding="utf-8"))["questions"][0]
        factor = factor_theorem(q, {"method": "factor_theorem", "polynomial": "2*x**2+5*x+2", "factor": "2*x+1", "variable": "x"})
        square = completing_square(q, {"method": "completing_square_no_real_root", "polynomial": "x**2+2*x+3", "variable": "x"})
        self.assertEqual(factor["status"], "SOLVED_AND_TRACE_CHECKED")
        self.assertEqual(square["status"], "SOLVED_AND_TRACE_CHECKED")

    def test_unseen_ap_patterns(self):
        bank = Path(__file__).resolve().parent.parent/"proofs_derivations_core_json"/"mathematics_core.json"
        q = json.loads(bank.read_text(encoding="utf-8"))["questions"][0]
        term = ap_term_relation(q, {"method": "ap_term_relation", "zero_term_index": 2,
                                    "target_term_index": 7, "comparison_term_index": 4, "multiplier": 2})
        valid_term = ap_term_relation(q, {"method": "ap_term_relation", "zero_term_index": 2,
                                          "target_term_index": 5, "comparison_term_index": 3, "multiplier": 3})
        sums = ap_sum_relation(q, {"method": "ap_sum_relation", "first_term": 5,
                                   "common_differences": [2, 4, 6], "claim_coefficients": [1, -2, 1]})
        self.assertEqual(term["status"], "INCONCLUSIVE")  # T7=5d, whereas 2T4=4d.
        self.assertEqual(valid_term["status"], "SOLVED_AND_TRACE_CHECKED")
        self.assertEqual(sums["status"], "SOLVED_AND_TRACE_CHECKED")


if __name__ == "__main__":
    unittest.main()

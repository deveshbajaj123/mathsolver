import json
import os
import tempfile
import unittest
from pathlib import Path

import sympy as s

from automatic_trig_solver import A, solve
from bank_map import build
from newclid_probe import independent_replay
from pipeline import run

HERE = Path(__file__).resolve().parent
BANK = Path(os.environ.get("MATH_BANK", HERE.parent/"proofs_derivations_core_json"/"mathematics_core.json"))
SOURCE_ISSUES = {"PD-MATH-IX-021": "INPUT_AMBIGUOUS"}  # givens have no real solution; see the spec note


@unittest.skipUnless(BANK.exists(), f"main bank not found at {BANK}; set MATH_BANK")
class DatasetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with tempfile.TemporaryDirectory(dir=HERE) as temporary:
            cls.report = run(BANK, Path(temporary))
            cls.results = json.loads((Path(temporary)/"per_question_results.json").read_text(encoding="utf-8"))
            cls.mapping = build(BANK, Path(temporary)/"per_question_results.json")

    def test_full_bank_outcomes_and_provenance(self):
        self.assertEqual(self.report["questions_attempted"], 135)
        self.assertEqual(len({r["id"] for r in self.results}), 135)
        self.assertEqual(self.report["automatically_solved"], len(list((HERE/"specs").glob("*.json"))) - len(SOURCE_ISSUES))
        self.assertEqual(self.report["newclid_geometry_solved"], 1)
        self.assertEqual(self.report["llm_calls"], 0)
        for result in self.results:
            self.assertIn("question_text_original", result)
            self.assertIn("provenance", result)
            if result["status"] == "SOLVED_AND_TRACE_CHECKED":
                self.assertTrue(result["trace"])
                self.assertTrue(all(step["verification"]["passed"] for step in result["trace"]))
                self.assertTrue(result["answer"].startswith(f"## {result['id']}"))
        status_by_id = {r["id"]: r["status"] for r in self.results}
        for path in (HERE/"specs").glob("*.json"):
            self.assertEqual(status_by_id[path.stem], SOURCE_ISSUES.get(path.stem, "SOLVED_AND_TRACE_CHECKED"), path.stem)

    def test_method_map_covers_bank(self):
        self.assertEqual(len(self.mapping["questions"]), 135)
        self.assertEqual(sum(e["questions"] for e in self.mapping["engines"]), 135)
        self.assertEqual(sum(e["solved"] for e in self.mapping["engines"]), self.report["automatically_solved"])
        engine_status = {e["engine"]: e["status"] for e in self.mapping["engines"]}
        for path in (HERE/"specs").glob("*.json"):
            if path.stem in SOURCE_ISSUES:
                continue
            self.assertNotEqual(engine_status[self.mapping["questions"][path.stem]["engine"]], "missing", path.stem)


class GeometryAndLegacyTests(unittest.TestCase):
    def test_midpoint_geometry_symbolic_replay(self):
        replay = independent_replay()
        self.assertTrue(replay["passed"])
        self.assertTrue(all(replay["checks"].values()))

    def test_standalone_trig_demo_still_works(self):
        self.assertEqual(solve(s.sec(A)**2-s.tan(A)**2, s.Integer(1), seconds=10)["status"], "SOLVED")
        self.assertEqual(solve(s.sec(A)**2-s.tan(A)**2, s.Integer(2), seconds=10)["status"], "COUNTEREXAMPLE")


if __name__ == "__main__":
    unittest.main()

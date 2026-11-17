"""Fixed transfer tests for the existing solvers; no production route is changed.

Run with .venv Python. Each case executes in its own process with a 45s limit.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
OUT = HERE / "results" / "generalisation_check"
TRIG = [
    {"id": "T1", "lhs": "tan(A)+cot(A)", "rhs": "sec(A)*csc(A)", "description": "Sum of tangent and cotangent"},
    {"id": "T2", "lhs": "(sec(A)+tan(A))*(sec(A)-tan(A))", "rhs": "1", "description": "Product of conjugate expressions"},
    {"id": "T3", "lhs": "sin(A)**4-cos(A)**4", "rhs": "sin(A)**2-cos(A)**2", "description": "Difference of fourth powers"},
    {"id": "T4", "lhs": "(1-cos(A))/(1+cos(A))", "rhs": "(csc(A)-cot(A))**2", "description": "Rational identity with original domain restrictions"},
    {"id": "T5", "lhs": "sin(2*A)", "rhs": "2*sin(A)*cos(A)", "description": "Double-angle identity outside the documented single-angle grammar"},
]
GEOMETRY = [
    {"id": "G1", "bank_id": "PD-MATH-IX-001", "description": "Perpendicular diagonals bisecting each other imply a rhombus",
     "points": {"a": [3.7, 0], "b": [0, 2.3], "c": [-3.7, 0], "d": [0, -2.3], "o": [0, 0]},
     "assumptions": ["midp o a c", "midp o b d", "perp a c b d"],
     "goals": ["cong a b b c", "cong b c c d", "cong c d d a"],
     "translation": "Rhombus conclusion expanded to four equal sides; coordinates are a matching diagram, not proof premises."},
    {"id": "G2", "bank_id": "PD-MATH-IX-002", "description": "Circle on an isosceles triangle's equal side as diameter bisects the base",
     "points": {"a": [0, 4.3], "b": [-2.7, 0], "c": [2.7, 0], "d": [0, 0]},
     "assumptions": ["cong a b a c", "coll b d c", "perp d a d b", "diff b d", "ncoll a b c"],
     "goals": ["midp d b c"],
     "translation": "D denotes the second intersection with BC. Thales' theorem translates the diameter condition to AD perpendicular BD. This preprocessing was supplied manually."},
    {"id": "G3", "bank_id": "PD-MATH-IX-004", "description": "Midpoints of square sides form another square",
     "points": {"a": [0, 0], "b": [4.1, 0], "c": [4.1, 4.1], "d": [0, 4.1],
                "p": [2.05, 0], "q": [4.1, 2.05], "r": [2.05, 4.1], "s": [0, 2.05]},
     "assumptions": ["para a b c d", "para a d b c", "perp a b b c", "cong a b b c", "midp p a b", "midp q b c", "midp r c d", "midp s d a"],
     "goals": ["para p q r s", "para q r s p", "perp p q q r", "cong p q q r", "cong q r r s", "cong r s s p"],
     "translation": "Square premise and conclusion expanded to parallel/perpendicular/equal-length predicates."},
    {"id": "G4", "bank_id": "PD-MATH-IX-007", "description": "Right triangle midpoint squared-length sum",
     "points": {"a": [0, 3.9], "b": [0, 0], "c": [5.3, 0], "d": [2.65, 0], "e": [0, 1.95]},
     "assumptions": ["perp a b b c", "midp d b c", "midp e a b"],
     "goals": ["lequation 1 a d * a d 1 c e * c e -5 d e * d e 0"],
     "translation": "AD^2+CE^2-5DE^2=0 is represented with Newclid's length-equation predicate."},
    {"id": "G5", "bank_id": "PD-MATH-IX-024", "description": "Rectangle interior point: opposite squared-distance sums",
     "points": {"a": [0, 0], "b": [5.9, 0], "c": [5.9, 3.2], "d": [0, 3.2], "o": [1.7, 1.1]},
     "assumptions": ["para a b c d", "para a d b c", "perp a b b c"],
     "goals": ["lequation 1 o a * o a 1 o c * o c -1 o b * o b -1 o d * o d 0"],
     "translation": "Rectangle expanded into parallelism and a right angle. O is inside the sample diagram; the equality also holds outside, so no stronger location premise is needed."},
]
CONTROLS = [
    {"id": "N1", "lhs": "sec(A)**2-tan(A)**2", "rhs": "2", "description": "False trigonometric claim; must not solve"},
    {"id": "N2", "bank_id": None, "description": "Generic triangle falsely claimed to have equal sides",
     "points": {"a": [0, 0], "b": [4.7, 0], "c": [1.2, 3.1]},
     "assumptions": ["ncoll a b c"], "goals": ["cong a b a c"],
     "translation": "Negative control: no equal-side assumption."},
]


def environment():
    scratch = HERE / ".tmp"
    scratch.mkdir(exist_ok=True)
    os.environ.update(TEMP=str(scratch), TMP=str(scratch), MPLCONFIGDIR=str(HERE/".mplconfig"))
    os.environ["PATH"] = str(HERE/".venv"/"Scripts") + os.pathsep + os.environ["PATH"]


def worker(case):
    environment()
    started = time.perf_counter()
    result = {"id": case["id"], "description": case["description"], "input": case,
              "llm_api_calls": 0, "llm_api_tokens": 0, "counted_in_production_metrics": False}
    try:
        if "lhs" in case:
            from legacy_pipeline import trig
            bank = json.loads((HERE.parent/"proofs_derivations_core_json"/"mathematics_core.json").read_text(encoding="utf-8"))
            q = dict(next(q for q in bank["questions"] if q["id"] == "PD-MATH-X-001"))
            q.update(id=case["id"], question_text_original=case["lhs"]+" = "+case["rhs"], question_text_cleaned=case["description"])
            spec = {"method": "rational_trig_identity", "lhs": case["lhs"], "rhs": case["rhs"], "input_note": "New transfer-test input; not a bank question."}
            outcome = trig(q, spec)
            result.update(status=outcome["status"], trace=outcome["trace"], diagnostics=outcome["diagnostics"],
                          domain_conditions=outcome["domain_conditions"],
                          independently_checked=outcome["status"] == "SOLVED_AND_TRACE_CHECKED")
            if outcome["status"] == "SOLVED_AND_TRACE_CHECKED":
                from legacy_pipeline import render_answer
                result["rendered_answer"] = render_answer(outcome)
        else:
            from newclid.api import GeometricSolverBuilder
            from newclid.numerical.geometries import PointNum
            from newclid.problem import ProblemSetup, PredicateConstruction
            from newclid.symbols.points_registry import Point
            logging.getLogger("py_yuclid.yuclid_adapter").setLevel(logging.CRITICAL)
            setup = ProblemSetup(points=tuple(Point(name=n, num=PointNum(x=xy[0], y=xy[1])) for n, xy in case["points"].items()),
                                 assumptions=tuple(PredicateConstruction.from_str(p) for p in case["assumptions"]),
                                 goals=tuple(PredicateConstruction.from_str(p) for p in case["goals"]))
            result["stage"] = "build_solver"
            solver = GeometricSolverBuilder(rng=1).build(setup)
            result["stage"] = "run_solver"
            success = solver.run()
            result.update(status="ENGINE_PROVED_PENDING_INDEPENDENT_CHECK" if success else "INCONCLUSIVE",
                          solver_goal_checked=bool(solver.proof_state.check_goals()),
                          run_infos=solver.run_infos.model_dump(),
                          independently_checked=False,
                          independent_checker="Existing checker only supports PD-MATH-VII-002; it cannot check these cases.",
                          production_adapter="UNSUPPORTED: no saved formalization, route, general checker or renderer for this bank question.")
            result["stage"] = "write_proof"
            result["proof_text"] = solver.proof()
    except Exception as exc:
        result.update(status="ERROR", error_type=type(exc).__name__, error=str(exc)[:1500], independently_checked=False)
    result["seconds"] = round(time.perf_counter()-started, 3)
    return result


def run(report_only=False):
    OUT.mkdir(parents=True, exist_ok=True)
    cases = TRIG+GEOMETRY+CONTROLS
    frozen_files = ("legacy_pipeline.py", "automatic_trig_solver.py", "newclid_probe.py", "formalizations.json")
    hashes = {n: hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in frozen_files}
    if report_only:
        manifest = json.loads((OUT/"manifest.json").read_text(encoding="utf-8"))
        if manifest['cases'] != cases or manifest['solver_sha256'] != hashes:
            raise ValueError("Saved results do not match the current manifest or solver files")
    else:
        (OUT/"manifest.json").write_text(json.dumps({"cases": cases, "solver_sha256": hashes,
                                                   "selection": "Purposive small transfer test; five new true trig identities and five previously unsupported geometry bank questions, plus two false controls. Not random and not a population accuracy estimate."},indent=2),encoding="utf-8")
    outcomes = []
    for case in cases:
        if report_only:
            outcomes.append(json.loads((OUT/f"{case['id']}.json").read_text(encoding="utf-8")))
            continue
        try:
            completed = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--case", case["id"]],
                                       cwd=HERE, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=45)
            if completed.returncode:
                outcome = {"id":case["id"], "status":"WORKER_ERROR", "stderr":completed.stderr[-1800:]}
            else:
                outcome = json.loads(completed.stdout)
        except subprocess.TimeoutExpired:
            outcome = {"id":case["id"], "status":"TIMEOUT", "seconds_limit":45}
        outcomes.append(outcome)
        (OUT/f"{case['id']}.json").write_text(json.dumps(outcome,ensure_ascii=False,indent=2),encoding="utf-8")
        print(json.dumps({k:outcome[k] for k in ("id","status","seconds","error") if k in outcome}),flush=True)
    unchanged = hashes == {n: hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in frozen_files}
    from legacy_pipeline import classify_unsolved
    bank = {q['id']:q for q in json.loads((HERE.parent/"proofs_derivations_core_json"/"mathematics_core.json").read_text(encoding="utf-8"))['questions']}
    production_specs = json.loads((HERE/"formalizations.json").read_text(encoding="utf-8"))
    for case, outcome in zip(cases, outcomes):
        if case['id'].startswith('G'):
            if case['bank_id'] in production_specs:
                raise AssertionError("Transfer case unexpectedly has a production formalization")
            production = classify_unsolved(bank[case['bank_id']])
            outcome['production_status'] = production['status']
            outcome['production_reason'] = production['reason']
            (OUT/f"{case['id']}.json").write_text(json.dumps(outcome,ensure_ascii=False,indent=2),encoding="utf-8")
    report = {"solver_code_unchanged": unchanged, "outcomes":outcomes,
              "trig_checked_out_of_5":sum(x.get("status")=="SOLVED_AND_TRACE_CHECKED" for x in outcomes if x["id"].startswith("T")),
              "geometry_engine_proved_out_of_5":sum(x.get("status")=="ENGINE_PROVED_PENDING_INDEPENDENT_CHECK" for x in outcomes if x["id"].startswith("G")),
              "geometry_independently_checked_out_of_5":0,
              "production_geometry_new_questions_supported_out_of_5":sum(x.get('production_status')=='SOLVED_AND_TRACE_CHECKED' for x in outcomes if x['id'].startswith('G')),
              "runtime_llm_calls":0,"runtime_llm_tokens":0,
              "earlier_chat_work_excluded":"Test selection and mathematical transcription were prepared in this chat. Those model tokens are not available to this script."}
    (OUT/"results.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    lines=["# Transfer test: five trigonometry and five geometry questions", "",
           "This is a small, purposive test, not a random accuracy estimate. All ten are new to the saved production formalizations. Inputs were transcribed in this chat. No solver, rule library, production formalization or checker was changed to make these cases pass.", "",
           "Trigonometry uses the existing reusable route with new inputs. Geometry tests the Newclid engine directly using supplied predicates; the production geometry adapter remains limited to its original question. Numerical diagrams guide matching and do not prove a universal statement.", "",
           f"Trigonometry checked: {report['trig_checked_out_of_5']}/5. Geometry engine proved: {report['geometry_engine_proved_out_of_5']}/5. New geometry cases independently checked by existing code: 0/5. Production results are not changed.", "",
           "| Case | Result | Seconds |", "|---|---|---|"]
    lines += [f"| {x['id']} | {x['status']} | {x.get('seconds','—')} |" for x in outcomes]
    for case, result in zip(cases,outcomes):
        lines += ["",f"## {case['id']}: {case['description']}",""]
        if case.get("bank_id"):
            lines += [bank[case['bank_id']]['question_text_original'], ""]
        lines += ["Exact input:","","```json",json.dumps(case,ensure_ascii=False,indent=2),"```", "", "Output:", "", "```json",
                  json.dumps({k:v for k,v in result.items() if k not in ("input","proof_text","rendered_answer")},ensure_ascii=False,indent=2),"```",""]
        if result.get("proof_text"):
            lines += ["Raw engine proof (not independently replayed by the existing adapter):","",result['proof_text'],""]
        if result.get("rendered_answer"):
            lines += [result['rendered_answer'],""]
    lines += ["", "LLM boundary for every worker: request=None; response=None; runtime API calls=0; runtime API tokens=0. Input preparation and this report's interpretation use the surrounding chat and are excluded. No LLM-only baseline was run."]
    (OUT/"report.md").write_text("\n".join(lines),encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k != "outcomes"},indent=2))


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--case")
    parser.add_argument("--report-only", action="store_true", help="Regenerate the report from saved case outputs without rerunning solvers")
    args=parser.parse_args()
    if args.case:
        sys.stdout.reconfigure(encoding="utf-8")
        print(json.dumps(worker(next(c for c in TRIG+GEOMETRY+CONTROLS if c['id']==args.case)),ensure_ascii=True))
    else:
        run(report_only=args.report_only)

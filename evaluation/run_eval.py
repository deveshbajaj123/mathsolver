"""Run the bank, generated variants and false controls; write results/eval_report.json.

    python -m evaluation.run_eval          # exits 1 if any false control is accepted

The bank is split into development and evaluation questions by a hash of the ID
(split.json). Rules and strategies should be written against development questions
only; evaluation questions measure transfer.
"""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path

from pipeline import HERE, run, solve_spec
from .variants import false_controls, true_cases

SPLIT_FILE = Path(__file__).resolve().parent/"split.json"
EVALUATION_SHARE = 5  # one in five questions is held out


def split(ids: list[str]) -> dict:
    held_out = sorted(i for i in ids if int(hashlib.sha256(i.encode()).hexdigest(), 16) % EVALUATION_SHARE == 0)
    return {"rule": f"sha256(id) % {EVALUATION_SHARE} == 0 -> evaluation",
            "evaluation": held_out, "development": sorted(set(ids) - set(held_out))}


def main(bank_path: Path = HERE.parent/"proofs_derivations_core_json"/"mathematics_core.json") -> dict:
    started = time.monotonic()
    ids = [q["id"] for q in json.loads(bank_path.read_text(encoding="utf-8"))["questions"]]
    expected_split = split(ids)
    if SPLIT_FILE.exists() and json.loads(SPLIT_FILE.read_text(encoding="utf-8")) != expected_split:
        raise ValueError("split.json no longer matches the bank; re-split deliberately, not silently")
    SPLIT_FILE.write_text(json.dumps(expected_split, indent=2) + "\n", encoding="utf-8")

    with tempfile.TemporaryDirectory(dir=HERE) as temporary:
        bank_report = run(bank_path, Path(temporary))
        bank_results = json.loads((Path(temporary)/"per_question_results.json").read_text(encoding="utf-8"))
    status = {r["id"]: r["status"] for r in bank_results}
    bank = {}
    for part in ("development", "evaluation"):
        part_ids = expected_split[part]
        bank[part] = {"questions": len(part_ids), "status_counts": dict(Counter(status[i] for i in part_ids)),
                      "solved_ids": [i for i in part_ids if status[i] == "SOLVED_AND_TRACE_CHECKED"]}

    variants = []
    for spec, expected in true_cases():
        t = time.monotonic()
        outcome = solve_spec(spec)
        variants.append({"id": spec.id, "expected_solved": expected, "status": outcome["status"],
                         "seconds": round(time.monotonic() - t, 2)})
    controls = []
    for spec in false_controls():
        outcome = solve_spec(spec)
        controls.append({"id": spec.id, "status": outcome["status"],
                         "accepted": outcome["status"] == "SOLVED_AND_TRACE_CHECKED"})

    solved = lambda rows, flag: sum(r["status"] == "SOLVED_AND_TRACE_CHECKED" for r in rows if r["expected_solved"] == flag)
    report = {
        "bank": bank, "bank_runtime_seconds": bank_report["runtime_seconds"],
        "variants": {"expected_solvable": sum(r["expected_solved"] for r in variants),
                     "solved": solved(variants, True),
                     "known_gaps": [r["id"] for r in variants if not r["expected_solved"]],
                     "known_gaps_unexpectedly_solved": solved(variants, False),
                     "regressions": [r for r in variants if r["expected_solved"] and r["status"] != "SOLVED_AND_TRACE_CHECKED"],
                     "cases": variants},
        "false_controls": {"count": len(controls), "false_accepts": sum(r["accepted"] for r in controls),
                           "status_counts": dict(Counter(r["status"] for r in controls)), "cases": controls},
        "llm_calls": 0, "llm_tokens": 0,
        "runtime_seconds": round(time.monotonic() - started, 1),
        "readability_review": "not done; sample from results/sample_answers.md",
    }
    (HERE/"results"/"eval_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    result = main()
    print(json.dumps({"bank": {k: v["status_counts"] for k, v in result["bank"].items()},
                      "variants_solved": f"{result['variants']['solved']}/{result['variants']['expected_solvable']}",
                      "regressions": [r["id"] for r in result["variants"]["regressions"]],
                      "false_accepts": result["false_controls"]["false_accepts"],
                      "control_statuses": result["false_controls"]["status_counts"],
                      "runtime_seconds": result["runtime_seconds"]}, indent=2))
    sys.exit(1 if result["false_controls"]["false_accepts"] else 0)

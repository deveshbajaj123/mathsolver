"""Bank driver: spec -> validate -> select strategy -> search -> verify -> render.

Run from this directory:
    python pipeline.py                      # whole bank, specs from specs/
    python pipeline.py --spec specs/X.json  # one spec, no bank needed
No LLM is called. specs/ holds problem inputs only, never solution steps.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import os
import time
from collections import Counter
from pathlib import Path

import sympy as s

from mathcore.engine import Step
from mathcore.presentation import report as presentation_report
from mathcore.problem import add_facts
from mathcore.refine import refine
from mathcore.render import render
from mathcore.spec import Spec, load, load_dir
from mathcore.strategies import select
from mathcore.validate import validate
from mathcore.verify import verify

HERE = Path(__file__).resolve().parent
STATUSES = {"SOLVED_AND_TRACE_CHECKED", "COUNTEREXAMPLE", "INCONCLUSIVE",
            "UNSUPPORTED", "INPUT_AMBIGUOUS", "SOURCE_NEEDS_CORRECTION"}
CHECKER = "rule replay + exact ideal reduction + 50-digit numeric check + domain certificate (mathcore.verify)"


def common_fields(q: dict) -> dict:
    """Fields copied from the bank record. Optional fields default, so a paper extracted with
    fewer fields still runs."""
    source = q.get("source", {})
    return {"id": q["id"], "topic": q.get("topic"), "class": q.get("class"),
            "task_kind": q.get("task_kind"),
            "question_text_original": q.get("question_text_original", ""),
            "question_text_cleaned": q.get("question_text_cleaned", q.get("question_text_original", "")),
            "stated_assumptions": q.get("stated_assumptions", []),
            "inferred_assumptions": q.get("inferred_assumptions", []),
            "proposed_corrections": [],
            "provenance": {"source_question_id": q.get("source_question_id"),
                           "source_id": source.get("source_id"),
                           "paper": source.get("paper"),
                           "pdf_pages": source.get("pdf_pages"),
                           "board_status": q.get("board_status")},
            "figure_required": bool(q.get("context_requirements", {}).get("given_diagram_required", False)),
            "trace": [], "method_approval": "draft_unverified",
            "presentation_review": "not_reviewed",
            "formalization_review": "draft_manual_transcription"}


def classify_unsolved(q: dict) -> dict:
    result = common_fields(q)
    if q["id"] == "PD-MATH-XII-030":
        result.update(status="SOURCE_NEEDS_CORRECTION", reason="Displayed plane equation needs a x b != 0; otherwise it does not specify a unique plane.",
                      proposed_corrections=["Qualify the conclusion with a x b != 0, or state the degenerate case separately."])
    elif q["id"] == "PD-MATH-XII-036":
        result.update(status="SOURCE_NEEDS_CORRECTION", reason="Printed logarithmic family omits y=0 and real sign branches; completeness is not established.",
                      proposed_corrections=["Include the zero solution and the signed nonzero branches on intervals where sin(2x) has fixed sign."])
    else:
        reason = ("The supplied figure has no verified symbolic geometry encoding or Newclid replay."
                  if result["figure_required"] else "No spec has been written for this question yet.")
        result.update(status="UNSUPPORTED", reason=reason)
    return result


def _show(value) -> str:
    return str(value)


def _latex(value) -> str | None:
    return s.latex(value) if isinstance(value, s.Basic) else None


def serialize(step: Step, part: str, check: dict) -> dict:
    return {"input": _show(step.before), "output": _show(step.after), "rule_id": step.rule,
            "reason": step.reason, "relation": step.relation, "part": part, "reverse": step.reverse,
            "params": {k: str(v) for k, v in step.params.items()},
            "verification": {"passed": bool(check["passed"]), "checker": CHECKER,
                             "details": {k: v for k, v in check.items() if k not in ("part", "rule", "relation")}},
            "origin": "code_search" if part == "step" and step.relation == "equality" else "method_template",
            "input_latex": _latex(step.before), "output_latex": _latex(step.after)}


def solve_part(spec: Spec, facts: list = ()) -> dict:
    """Validate, try each selected strategy, and keep the first trace the verifier accepts.
    `facts` are equalities proved in earlier parts of the same question."""
    checked = validate(spec)
    outcome = {"validation": {k: v for k, v in checked.items() if k != "problem"}, "attempts": []}
    if checked["status"] == "FALSE_CLAIM":
        return {**outcome, "status": "COUNTEREXAMPLE", "reason": checked["reason"]}
    if checked["status"] != "VALID":
        return {**outcome, "status": "INPUT_AMBIGUOUS", "reason": checked["reason"]}
    problem = checked["problem"]
    add_facts(problem, facts)
    strategies = select(problem)
    if not strategies:
        return {**outcome, "status": "UNSUPPORTED", "reason": "The prescribed method does not apply to this goal."}
    for strategy in strategies:
        found = strategy(problem)
        attempt = {"strategy": found["strategy"], "status": found["status"], "reason": found.get("reason"),
                   "states_explored": found.get("states_explored"), "elapsed_seconds": found.get("elapsed_seconds")}
        outcome["attempts"].append(attempt)
        if found["status"] == "SOLVED":
            refined = refine(found, problem.theory)
            check = verify(problem, refined)
            if check["passed"]:
                found = refined
            else:  # keep the search's own trace if the presentation split did not verify
                check = verify(problem, found)
            if check["passed"]:
                parts = [("premise", st) for st in found["premises"]] + [("step", st) for st in found["steps"]]
                if found.get("conclusion"):
                    parts.append(("conclusion", found["conclusion"]))
                trace = [serialize(st, part, c) for (part, st), c in zip(parts, check["steps"])]
                return {**outcome, "status": "SOLVED_AND_TRACE_CHECKED", "method": found["strategy"],
                        "problem": problem, "found": found, "trace": trace, "goal_check": check["goal_reason"],
                        "diagnostics": {k: str(v) for k, v in found.get("diagnostics", {}).items()},
                        "presentation": presentation_report(found)}
            attempt.update(status="VERIFICATION_FAILED", verification=check)
    unsupported = all(a["status"] == "UNSUPPORTED" for a in outcome["attempts"])
    return {**outcome, "status": "UNSUPPORTED" if unsupported else "INCONCLUSIVE",
            "reason": "; ".join(filter(None, (a.get("reason") for a in outcome["attempts"]))) or "No strategy succeeded."}


def solve_spec(spec: Spec, q: dict | None = None) -> dict:
    result = common_fields(q) if q else {"id": spec.id, "question_text_original": spec.quotes.get("goal", ""),
                                         "trace": [], "figure_required": False}
    result["spec"] = spec.to_json()
    try:
        parts = spec.parts()
    except ValueError as exc:
        return {**result, "status": "INPUT_AMBIGUOUS", "reason": str(exc)}
    outcomes, facts = [], []
    for part in parts:
        outcomes.append(solve_part(part, facts))
        if outcomes[-1]["status"] == "SOLVED_AND_TRACE_CHECKED" and "lhs" in part.goal:
            proved = outcomes[-1]["problem"]
            facts.append((proved.exprs["lhs"], proved.exprs["rhs"]))
    result["validation"] = outcomes[0]["validation"] if len(outcomes) == 1 else [o["validation"] for o in outcomes]
    result["attempts"] = outcomes[0]["attempts"] if len(outcomes) == 1 else [o["attempts"] for o in outcomes]
    statuses = [o["status"] for o in outcomes]
    for blocking in ("COUNTEREXAMPLE", "INPUT_AMBIGUOUS"):
        if blocking in statuses:
            return {**result, "status": blocking, "reason": outcomes[statuses.index(blocking)]["reason"]}
    if all(status == "SOLVED_AND_TRACE_CHECKED" for status in statuses):
        trace = [{**step, "goal_part": index} for index, o in enumerate(outcomes, 1) for step in o["trace"]]
        conditions = outcomes[0]["validation"]["conditions"]
        return {**result, "status": "SOLVED_AND_TRACE_CHECKED",
                "method": "+".join(dict.fromkeys(o["method"] for o in outcomes)), "trace": trace,
                "domain_conditions": conditions, "goal_check": [o["goal_check"] for o in outcomes],
                "diagnostics": outcomes[0]["diagnostics"] if len(outcomes) == 1 else [o["diagnostics"] for o in outcomes],
                "presentation_review": "template_rendered_unreviewed",
                "presentation": {"steps": sum(o["presentation"]["steps"] for o in outcomes),
                                 "large_jumps": [j for o in outcomes for j in o["presentation"]["large_jumps"]]},
                "answer": render(spec.id, result["question_text_original"], [(o["problem"], o["found"]) for o in outcomes])}
    unsolved = [o for o in outcomes if o["status"] != "SOLVED_AND_TRACE_CHECKED"]
    return {**result, "status": "UNSUPPORTED" if all(o["status"] == "UNSUPPORTED" for o in unsolved) else "INCONCLUSIVE",
            "reason": "; ".join(o["reason"] for o in unsolved)}


def run(bank_path: Path, output_dir: Path, specs_dir: Path = HERE/"specs") -> dict:
    start = time.monotonic()
    bank_bytes = bank_path.read_bytes()
    bank = json.loads(bank_bytes)
    specs = load_dir(specs_dir)
    in_bank = {q["id"] for q in bank["questions"]}
    used = sorted(set(specs) & in_bank)  # specs for other papers are simply not used
    results = []
    for q in bank["questions"]:
        result = solve_spec(specs[q["id"]], q) if q["id"] in specs else classify_unsolved(q)
        if result["status"] not in STATUSES:
            raise AssertionError(result["status"])
        results.append(result)
    output_dir.mkdir(parents=True, exist_ok=True)
    counts = Counter(x["status"] for x in results)
    solved = [x for x in results if x["status"] == "SOLVED_AND_TRACE_CHECKED"]
    report = {"bank_sha256": hashlib.sha256(bank_bytes).hexdigest(),
              "bank_question_count": len(bank["questions"]),
              "questions_attempted": len(results), "specs_count": len(used),
              "questions_without_spec": len(in_bank) - len(used),
              "status_counts": dict(counts),
              "automatically_solved": len(solved),
              "trace_verification_success": sum(all(st["verification"]["passed"] for st in x["trace"]) for x in solved),
              "solved_by_method": dict(Counter(x["method"] for x in solved)),
              "domain_or_source_issues": [x["id"] for x in results if x["status"] in ("SOURCE_NEEDS_CORRECTION", "INPUT_AMBIGUOUS")],
              "method_approved": 0, "presentation_human_reviewed": 0,
              "complete_answer_accuracy_observed": None,
              "accuracy_uncertainty": "Not estimable: no independent marking or expert-reviewed random sample.",
              "figure_required_questions": sum(x["figure_required"] for x in results),
              "llm_calls": 0, "llm_tokens": 0, "runtime_seconds": round(time.monotonic()-start, 3),
              "sympy_version": s.__version__, "newclid_available": importlib.util.find_spec("newclid") is not None,
              "newclid_available_meaning": "Python module found only; solver execution is checked separately.",
              "newclid_geometry_solved": sum(x.get("method") == "geometry" for x in solved),
              "failure_count": counts["INCONCLUSIVE"],
              "answers_with_large_jumps": [x["id"] for x in solved if x["presentation"]["large_jumps"]],
              "large_jump_definition": "a simplify/cancel/expand step that, read as shown, starts from at least 12 operations and loses at least 6"}
    (output_dir/"per_question_results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir/"metrics.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    answers = "# Rendered sample answers\n\nThese are machine generated and still require presentation review.\n\n"
    answers += "\n".join(x["answer"] for x in solved)
    (output_dir/"sample_answers.md").write_text(answers, encoding="utf-8")
    with (output_dir/"summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["id", "status", "method", "reason"])
        for x in results:
            writer.writerow([x["id"], x["status"], x.get("method", ""), x.get("reason", "")])
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bank", type=Path, default=Path(os.environ.get("MATH_BANK", HERE.parent/"proofs_derivations_core_json"/"mathematics_core.json")))
    parser.add_argument("--output", type=Path, default=HERE/"results")
    parser.add_argument("--specs", type=Path, default=HERE/"specs", help="Folder of spec files (one JSON per question id).")
    parser.add_argument("--spec", type=Path, help="Solve one spec file without the bank.")
    args = parser.parse_args()
    if args.spec:
        outcome = solve_spec(load(args.spec))
        print(outcome.get("answer") or json.dumps({k: outcome[k] for k in ("id", "status", "reason") if k in outcome}, indent=2))
    else:
        print(json.dumps(run(args.bank, args.output, args.specs), indent=2))

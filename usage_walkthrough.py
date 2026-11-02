"""Rerun two existing routes and save their actual inputs and outputs.

This walkthrough never invokes an LLM. It does not estimate tokens saved.
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

import sympy as sp

from automatic_trig_solver import domain_safe, exact_equal
from pipeline import (HERE, isosceles_midpoint_geometry, parse_math,
                      render_answer, source_domain_factors, trig)

OUT = HERE / "results" / "usage_walkthrough"


def stage(name, engine, inputs, outputs, explanation):
    return {"stage": name, "engine": engine, "input": inputs, "output": outputs,
            "explanation": explanation, "llm_call_executed": False}


def coordinate_details():
    qx, qy, rx, ry = sp.symbols("qx qy rx ry", real=True)
    q, r = sp.Matrix([qx, qy]), sp.Matrix([rx, ry])
    squared = lambda v: sp.expand(v.dot(v))
    rs2, qt2 = squared(r-q/2), squared(q-r/2)
    residual = sp.expand(rs2-qt2-sp.Rational(3, 4)*(squared(r)-squared(q)))
    return {"coordinate_input": {"P": "(0,0)", "Q": "(qx,qy)", "R": "(rx,ry)",
                                  "S": "(qx/2,qy/2)", "T": "(rx/2,ry/2)"},
            "RS_squared": str(rs2), "QT_squared": str(qt2),
            "difference": str(sp.expand(rs2-qt2)),
            "identity_residual": str(residual),
            "given": "PR = PQ, hence PR^2 - PQ^2 = 0",
            "conclusion": "RS^2 = QT^2; nonnegative lengths imply RS = QT",
            "scope": "Checks this encoded conclusion independently; does not replay Yuclid's individual deductions or validate rendered SAS prose."}


def run():
    OUT.mkdir(parents=True, exist_ok=True)
    bank_path = HERE.parent / "proofs_derivations_core_json" / "mathematics_core.json"
    raw_bank = bank_path.read_bytes()
    questions = {q["id"]: q for q in json.loads(raw_bank)["questions"]}
    specs = json.loads((HERE/"formalizations.json").read_text(encoding="utf-8"))
    examples = []
    for topic, identifier, route in (("trigonometry", "PD-MATH-X-001", trig),
                                      ("geometry", "PD-MATH-VII-002", isosceles_midpoint_geometry)):
        q, spec = questions[identifier], specs[identifier]
        steps = [stage("1. Read the source", "Python JSON reader", {"question_id": identifier},
                       {"question_text_original": q["question_text_original"],
                        "figure_required": q["context_requirements"]["given_diagram_required"]},
                       "Reads the existing extracted bank; OCR/extraction and any earlier chat assistance are outside this run.")]
        if topic == "trigonometry":
            lhs, rhs = parse_math(spec["lhs"]), parse_math(spec["rhs"])
            domain = tuple(sorted(set(source_domain_factors(spec["lhs"])+source_domain_factors(spec["rhs"])), key=str))
            parsed = {"lhs": str(lhs), "rhs": str(rhs),
                      "domain": [f"{f} != 0" for f in domain], "notation": "S=sin(A), C=cos(A)"}
        else:
            parsed = {"jgex_input": spec["jgex_input"], "figure_asset_id": spec["figure_asset_id"],
                      "givens": ["PQ = PR", "S is midpoint of PQ", "T is midpoint of PR"], "goal": "RS = QT"}
        steps.append(stage("2. Load the saved formalization", "Python parser", spec, parsed,
                           "The saved input was transcribed and reviewed beforehand. This stage does not automatically understand new prose or figures."))
        started = time.perf_counter()
        result = route(q, spec)
        elapsed = time.perf_counter()-started
        if topic == "trigonometry":
            solver_output = {"diagnostics": result["diagnostics"],
                             "derivation": [{k: edge[k] for k in ("input", "output", "rule_id", "reason")} for edge in result["trace"]]}
            verification = {"scope": "Search replays its permitted rules; the serialized trace is also checked for exact equality and domain safety.",
                            "steps": [{"rule": edge["rule_id"],
                                       "exact_equality": bool(exact_equal(parse_math(edge["input"]), parse_math(edge["output"]))),
                                       "domain_safe": bool(domain_safe(parse_math(edge["output"]), domain)),
                                       "pipeline_verification": edge["verification"]} for edge in result["trace"]]}
            engine = "Bounded Python rule search using SymPy"
        else:
            probe = json.loads((HERE/"results"/"newclid_probe.json").read_text(encoding="utf-8"))
            solver_output = {"status": probe["status"], "raw_proof_text": probe.get("proof_text"),
                             "solver_goal_checked": probe.get("solver_goal_checked")}
            verification = {"figure_sha256_verified": probe["figure_sha256_verified"],
                            "figure_review": probe["figure_encoding_review"],
                            "proof_inputs_and_goal_checked": probe.get("proof_inputs_and_goal_checked"),
                            "independent_replay": probe.get("independent_replay"),
                            "symbolic_working": coordinate_details()}
            engine = "Newclid Python interface + Yuclid C++ proof engine"
        steps.append(stage("3. Discover the proof", engine, parsed, solver_output,
                           "A fresh local solver run produces these outputs. No LLM selects the steps during execution."))
        steps.append(stage("4. Check the mathematics", "SymPy and pipeline checks", parsed, verification,
                           "Acceptance is limited to the checks listed here; formalization and school presentation have separate review status."))
        rendered = render_answer(result)
        steps.append(stage("5. Render the student answer", "Python render_answer template", result["trace"],
                           {"answer_markdown": rendered, "presentation_review": result["presentation_review"]},
                           "This prose is assembled by code. In geometry the SAS explanation is a separate handwritten template, not a translation or automatic verification of the raw Newclid trace."))
        boundary = {"before_llm_call": {"available_input": "The checked proof and rendered answer above", "request_sent": None},
                    "call": {"executed": False, "reason": "No LLM client or invocation exists on this route"},
                    "after_llm_call": {"response": None, "answer_changed_by_llm": False},
                    "runtime_api_usage": {"calls": 0, "input_tokens": 0, "output_tokens": 0},
                    "baseline_llm_usage": None, "tokens_saved_vs_baseline": None}
        steps.append(stage("6. Show the LLM boundary", "No LLM call", {"answer_available": True}, boundary,
                           "There is no actual before/after model response in this pipeline. Zero runtime API use excludes the AI used to build code, prepare inputs, or explain this walkthrough in chat."))
        examples.append({"topic": topic, "question_id": identifier, "fresh_route_seconds": round(elapsed, 3),
                         "status": result["status"], "stages": steps})
        (OUT/f"{topic}_answer.md").write_text(rendered, encoding="utf-8")
    report = {"bank_sha256": hashlib.sha256(raw_bank).hexdigest(), "examples": examples,
              "interpretation": "These two supported, already formalized examples run without LLM API calls. No LLM-only baseline was run, so a savings percentage, cost, or general coverage claim cannot be inferred. Original pipeline llm_calls/llm_tokens fields are literal zero values, not provider-reported telemetry."}
    (OUT/"walkthrough.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# Existing pipeline: actual trigonometry and geometry outputs", "", report["interpretation"], "",
             "The run below is fresh. Each stage lists the input, output, engine and whether an LLM was called. Earlier AI-assisted development and formalization are outside the runtime totals.", ""]
    for example in examples:
        lines += [f"## {example['topic'].title()} — {example['question_id']}", "",
                  f"Result: {example['status']}. Fresh route time: {example['fresh_route_seconds']} seconds.", ""]
        for item in example["stages"]:
            lines += [f"### {item['stage']}", "", f"Engine: {item['engine']}. LLM call: no.", "", item["explanation"], "",
                      "Input:", "", "```json", json.dumps(item["input"], ensure_ascii=False, indent=2), "```", "", "Output:", ""]
            if item["stage"].startswith("3.") and example["topic"] == "geometry":
                lines += [item["output"]["raw_proof_text"] or "No proof returned.", ""]
            elif item["stage"].startswith("5."):
                lines += [item["output"]["answer_markdown"], ""]
            else:
                lines += ["```json", json.dumps(item["output"], ensure_ascii=False, indent=2), "```", ""]
    (OUT/"report.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"report": str(OUT/"report.md"), "examples": [{k: x[k] for k in ("topic", "question_id", "status", "fresh_route_seconds")} for x in examples]}, indent=2))


if __name__ == "__main__":
    run()

"""Group the bank by solver engine and rank the missing engines.

Run from this directory: python bank_map.py
Reads method_map.json (curated assignments) and results/per_question_results.json
(latest pipeline statuses); writes results/bank_map.json and BANK_MAP.md.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
FEASIBILITY_WEIGHT = {"high": 1.0, "medium": 0.5, "low": 0.1}
SOLVED = "SOLVED_AND_TRACE_CHECKED"


def build(bank_path: Path, results_path: Path) -> dict:
    bank = {q["id"]: q for q in json.loads(bank_path.read_text(encoding="utf-8"))["questions"]}
    mapping = json.loads((HERE/"method_map.json").read_text(encoding="utf-8"))
    engines, assigned = mapping["engines"], mapping["questions"]
    status = {r["id"]: r["status"] for r in json.loads(results_path.read_text(encoding="utf-8"))}
    if set(assigned) != set(bank):
        raise ValueError(f"Map/bank mismatch: unmapped {sorted(set(bank)-set(assigned))}, "
                         f"unknown {sorted(set(assigned)-set(bank))}")
    for qid, a in assigned.items():
        if a["engine"] not in engines or a["feasibility"] not in FEASIBILITY_WEIGHT:
            raise ValueError(f"{qid}: bad engine or feasibility {a}")

    rows = []
    for name, info in engines.items():
        ids = sorted(q for q, a in assigned.items() if a["engine"] == name)
        open_ids = [q for q in ids if status.get(q) != SOLVED]
        rows.append({
            "engine": name, **info, "questions": len(ids),
            "solved": len(ids) - len(open_ids),
            "open": len(open_ids),
            "open_by_feasibility": dict(Counter(assigned[q]["feasibility"] for q in open_ids)),
            "figure_required": sum(bank[q]["context_requirements"]["given_diagram_required"] for q in ids),
            "classes": sorted({bank[q]["class"] for q in ids}),
            "priority_score": round(sum(FEASIBILITY_WEIGHT[assigned[q]["feasibility"]] for q in open_ids), 1),
            "question_ids": ids,
        })
    rows.sort(key=lambda r: (-r["priority_score"], -r["open"], r["engine"]))
    by_engine = {r["engine"]: r for r in rows}
    phases = mapping["build_order"]
    phased = [e for p in phases for e in p["engines"]]
    if sorted(phased) != sorted(engines):
        raise ValueError("build_order must list every engine exactly once")
    build_order = [{**p, "open": sum(by_engine[e]["open"] for e in p["engines"]),
                    "priority_score": round(sum(by_engine[e]["priority_score"] for e in p["engines"]), 1)}
                   for p in phases]
    return {"bank_question_count": len(bank), "status_counts": dict(Counter(status.values())),
            "build_order": build_order,
            "priority_formula": "sum over unsolved questions of feasibility weight " + json.dumps(FEASIBILITY_WEIGHT),
            "engines": rows,
            "questions": {q: {**assigned[q], "status": status.get(q), "class": bank[q]["class"],
                              "topic": bank[q]["topic"],
                              "figure_required": bank[q]["context_requirements"]["given_diagram_required"]}
                          for q in sorted(bank)}}


def render(report: dict) -> str:
    out = ["# Bank method map", "",
           f"{report['bank_question_count']} questions mapped to {len(report['engines'])} reusable engines. "
           "Assignments are curated judgements in `method_map.json`, not solver output.", "",
           f"Priority score = {report['priority_formula']}. It estimates how many extra questions an engine could "
           "reach SOLVED_AND_TRACE_CHECKED; it is not a measured result.", "",
           "| Rank | Engine | Status | Questions | Solved | Open (high/med/low) | Figures | Classes | Score |",
           "|---:|---|---|---:|---:|---|---:|---|---:|"]
    for i, r in enumerate(report["engines"], 1):
        f = r["open_by_feasibility"]
        out.append(f"| {i} | {r['title']} (`{r['engine']}`) | {r['status']} | {r['questions']} | {r['solved']} | "
                   f"{f.get('high', 0)}/{f.get('medium', 0)}/{f.get('low', 0)} | {r['figure_required']} | "
                   f"{', '.join(map(str, r['classes']))} | {r['priority_score']} |")
    out += ["", "## Recommended build order", "",
            "Phases group engines that share implementation work, so they differ from the per-engine score ranking.", "",
            "| Phase | Name | Engines | Open | Score | Rationale |", "|---:|---|---|---:|---:|---|"]
    for p in report["build_order"]:
        out.append(f"| {p['phase']} | {p['name']} | {', '.join(f'`{e}`' for e in p['engines'])} | "
                   f"{p['open']} | {p['priority_score']} | {p['rationale']} |")
    out += ["", "## Engines", ""]
    for r in report["engines"]:
        out += [f"### {r['title']} (`{r['engine']}`)", "",
                f"- Existing code: {r['code'] or 'none'}",
                f"- Check: {r['check']}",
                f"- Gaps: {r['gaps']}", "",
                "| Question | Class | Feasibility | Status | Note |", "|---|---:|---|---|---|"]
        for q in r["question_ids"]:
            a = report["questions"][q]
            out.append(f"| {q} | {a['class']} | {a['feasibility']} | {a['status']} | {a['note']} |")
        out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bank", type=Path, default=HERE.parent/"proofs_derivations_core_json"/"mathematics_core.json")
    parser.add_argument("--results", type=Path, default=HERE/"results"/"per_question_results.json")
    args = parser.parse_args()
    report = build(args.bank, args.results)
    (HERE/"results"/"bank_map.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (HERE/"BANK_MAP.md").write_text(render(report), encoding="utf-8")
    for i, r in enumerate(report["engines"], 1):
        print(f"{i:2} {r['engine']:28} open={r['open']:3} score={r['priority_score']}")

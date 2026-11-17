"""Write a readability review sheet for a teacher: a fixed, stratified sample of solved
answers, each with the same short rubric.

    python -m evaluation.review_sheet            # reads results/per_question_results.json

The sample takes answers from every solving method first, then fills up at random, with
a fixed seed so the same sheet is produced until the answers change.
"""
from __future__ import annotations

import json
import random
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
SAMPLE_SIZE = 10
SEED = 20261117
RUBRIC = [
    "Uses a method taught for this class",
    "Each step can be followed by a student",
    "Notation matches the classroom (sin A, cosec, degrees)",
    "Conditions (where it is valid) are stated sensibly",
    "Would receive full marks as written",
]


def sample(results: list[dict], size: int = SAMPLE_SIZE, seed: int = SEED) -> list[dict]:
    solved = sorted((r for r in results if r["status"] == "SOLVED_AND_TRACE_CHECKED"), key=lambda r: r["id"])
    by_method = defaultdict(list)
    for r in solved:
        by_method[r["method"]].append(r)
    rng = random.Random(seed)
    chosen = [rng.choice(group) for _, group in sorted(by_method.items())]
    rest = [r for r in solved if r not in chosen]
    rng.shuffle(rest)
    return sorted(chosen + rest[:max(0, size - len(chosen))], key=lambda r: r["id"])


def sheet(chosen: list[dict]) -> str:
    lines = ["# Readability review", "",
             "For a mathematics teacher. Each answer below was produced and checked by code (`mathcore`); "
             "the maths has passed the checker, so this review is about presentation only.", "",
             "For each answer, score each line 1–5 (5 = exactly as you would want it in class) and add a comment "
             "where something should change. About 3 minutes per answer.", "",
             f"Sample: {len(chosen)} answers, at least one per solving method, seed {SEED}.", ""]
    for result in chosen:
        lines += ["---", "", result["answer"].rstrip(), "",
                  f"*Method: `{result['method']}`. Steps shown: {result.get('presentation', {}).get('steps', '?')}.*", "",
                  "| Check | Score (1–5) | Comment |", "|---|---|---|"]
        lines += [f"| {item} |  |  |" for item in RUBRIC]
        lines += [""]
    return "\n".join(lines) + "\n"


def main() -> Path:
    results = json.loads((HERE/"results"/"per_question_results.json").read_text(encoding="utf-8"))
    output = HERE/"results"/"readability_review.md"
    output.write_text(sheet(sample(results)), encoding="utf-8")
    return output


if __name__ == "__main__":
    print(main())

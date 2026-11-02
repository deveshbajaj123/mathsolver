"""Run a real Newclid proof attempt for one figure-checked bank question.

This is an environment/encoding probe, not a certified geometry answer.
Run with the project's .venv Python from this directory: python newclid_probe.py
"""
from __future__ import annotations

import base64
import hashlib
import json
import logging
import os
import tempfile
from pathlib import Path
import sympy as sp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
QUESTION_ID = "PD-MATH-VII-002"
FIGURE_ID = "IMG-1c994300cc53caa15324"

# This states only the givens and goal. It contains no solution sequence.
# The figure shows P at the apex, Q/R at the base, S on PQ and T on PR.
JGEX_INPUT = (
    "p q r = iso_triangle0 p q r; "
    "s = midpoint s p q; "
    "t = midpoint t p r ? cong r s q t"
)


def independent_replay() -> dict:
    """Check the midpoint/isosceles proof for arbitrary exact coordinates."""
    qx, qy, rx, ry = sp.symbols("qx qy rx ry", real=True)
    q, r = sp.Matrix([qx, qy]), sp.Matrix([rx, ry])
    s, t = q / 2, r / 2  # P is the origin; S and T are the stated midpoints.
    squared = lambda v: sp.expand(v.dot(v))
    pq2, pr2 = squared(q), squared(r)
    ps2, pt2 = squared(s), squared(t)
    rs2, qt2 = squared(r - s), squared(q - t)
    checks = {
        "PS_squared_is_PQ_squared_over_4": sp.simplify(ps2 - pq2 / 4) == 0,
        "PT_squared_is_PR_squared_over_4": sp.simplify(pt2 - pr2 / 4) == 0,
        "RS_QT_squared_difference_follows_equal_sides":
            sp.simplify((rs2 - qt2) - sp.Rational(3, 4) * (pr2 - pq2)) == 0,
    }
    return {"passed": all(checks.values()), "checks": checks,
            "reason": "For midpoints S=Q/2 and T=R/2, RS²−QT²=3(PR²−PQ²)/4=0; segment lengths are nonnegative."}


def main() -> dict:
    bank = json.loads((ROOT / "proofs_derivations_core_json" / "mathematics_core.json").read_text(encoding="utf-8"))
    image_bank = json.loads((ROOT / "proofs_derivations_core_json" / "image_assets.json").read_text(encoding="utf-8"))
    question = next(item for item in bank["questions"] if item["id"] == QUESTION_ID)
    asset = image_bank["image_assets"][FIGURE_ID]
    actual_sha = hashlib.sha256(base64.b64decode(asset["data"])).hexdigest()
    if actual_sha != asset["sha256"]:
        raise ValueError("Figure checksum mismatch")
    if not any(image["asset_id"] == FIGURE_ID for image in question["context_requirements"]["images"]):
        raise ValueError("Figure not linked to question")

    scratch = HERE / ".tmp"
    scratch.mkdir(exist_ok=True)
    plot_cache = HERE / ".mplconfig"
    plot_cache.mkdir(exist_ok=True)
    os.environ["TEMP"] = str(scratch)
    os.environ["TMP"] = str(scratch)
    os.environ["MPLCONFIGDIR"] = str(plot_cache)
    os.environ["PATH"] = str(HERE / ".venv" / "Scripts") + os.pathsep + os.environ["PATH"]
    tempfile.tempdir = str(scratch)
    logging.getLogger("py_yuclid.yuclid_adapter").setLevel(logging.CRITICAL)

    result = {"question_id": QUESTION_ID, "question_text_original": question["question_text_original"],
              "figure_id": FIGURE_ID, "figure_sha256_verified": True,
              "figure_encoding_review": "visually_checked_against_bank_figure",
              "jgex_input": JGEX_INPUT,
              "goal": "RS = QT", "proof_accepted_by_pipeline": False}
    try:
        from newclid.api import GeometricSolverBuilder
        from newclid.jgex.problem_builder import JGEXProblemBuilder

        setup = JGEXProblemBuilder(rng=1).with_problem_from_txt(JGEX_INPUT).build()
        solver = GeometricSolverBuilder(rng=1).build(setup)
        if solver.run():
            proof = solver.proof()
            replay = independent_replay()
            goal_checked = bool(solver.proof_state.check_goals())
            proof_has_inputs = (any(line in proof for line in ("[C0] : PR = PQ", "[C0] : PQ = PR"))
                                and "[C1] : S is the midpoint of PQ" in proof
                                and "[C2] : T is the midpoint of PR" in proof
                                and any(line in proof for line in ("QT = RS : Proved", "RS = QT : Proved")))
            result["proof_text"] = proof
            result["independent_replay"] = replay
            result["solver_goal_checked"] = goal_checked
            result["proof_inputs_and_goal_checked"] = proof_has_inputs
            result["proof_accepted_by_pipeline"] = bool(replay["passed"] and goal_checked and proof_has_inputs)
            result["status"] = ("NEWCLID_PROVED_INDEPENDENTLY_CHECKED" if result["proof_accepted_by_pipeline"]
                                else "NEWCLID_PROVED_PENDING_TRACE_REPLAY")
        else:
            result["status"] = "INCONCLUSIVE"
    except Exception as exc:
        result["status"] = "ENGINE_ERROR"
        result["error_type"] = type(exc).__name__
        message = str(exc)
        result["error"] = ("yuclid.exe exited with Windows status 3221225781 (0xC0000135) before a proof was returned."
                           if "3221225781" in message else message[:500])

    output = HERE / "results" / "newclid_probe.json"
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(main(), ensure_ascii=True, indent=2))

"""Strategy `geometry`: the existing Newclid route. It has an independent checker for
one reviewed encoding only (PD-MATH-VII-002); generalising it is Milestone 5 of BANK_MAP."""
from __future__ import annotations

from ..engine import Step
from ..problem import Problem


def newclid(problem: Problem) -> dict:
    from newclid_probe import FIGURE_ID, JGEX_INPUT, QUESTION_ID, main as run_probe
    spec = problem.spec
    if (spec.id, spec.goal["figure_asset_id"], spec.goal["jgex"]) != (QUESTION_ID, FIGURE_ID, JGEX_INPUT):
        return {"strategy": "geometry", "status": "UNSUPPORTED", "premises": [], "steps": [],
                "reason": "Only the figure-reviewed encoding of PD-MATH-VII-002 has an independent checker."}
    probe = run_probe()  # fresh engine run; a cached proof cannot promote the result
    if not probe["proof_accepted_by_pipeline"]:
        return {"strategy": "geometry", "status": "INCONCLUSIVE", "premises": [], "steps": [],
                "reason": f"Newclid status {probe['status']}"}
    steps = [Step("S is midpoint of PQ", "PS² = PQ²/4", "midpoint_S", "S lies halfway from P to Q.",
                  {"check": "PS_squared_is_PQ_squared_over_4"}, relation="geometry"),
             Step("T is midpoint of PR", "PT² = PR²/4", "midpoint_T", "T lies halfway from P to R.",
                  {"check": "PT_squared_is_PR_squared_over_4"}, relation="geometry"),
             Step("RS² - QT²", "3(PR² - PQ²)/4", "midpoint_distance_identity",
                  "Expand both squared distances using the midpoint coordinates.",
                  {"check": "RS_QT_squared_difference_follows_equal_sides"}, relation="geometry"),
             Step("PR = PQ", "RS = QT", "equal_sides_nonnegative_lengths",
                  "Equal original sides make the squared-distance difference zero; both lengths are nonnegative.",
                  {"check": "solver_goal_checked"}, relation="geometry")]
    return {"strategy": "geometry", "status": "SOLVED", "premises": [], "steps": steps,
            "diagnostics": {"figure_id": FIGURE_ID, "figure_sha256_verified": probe["figure_sha256_verified"],
                            "newclid_status": probe["status"], "solver_goal_checked": probe["solver_goal_checked"]}}

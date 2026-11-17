# Mathematics Solution Pipeline

A Python foundation for solving mathematics questions, checking the working, and producing clear student answers.

**Our goal:** build on SymPy, Newclid/Yuclid, and the existing programs to cover all or most methods needed by our question bank. We want reusable methods that handle many questions, with LLM assistance where needed and measurable AI usage.

## What works today

Milestones 1 (core), 2 (algebra), 3 (trigonometry) and 4 (presentation, awaiting a teacher's review) of [`BUILD_PLAN.md`](BUILD_PLAN.md) are done, and calculus, coordinate geometry, inverse trig, general solutions and three new algebra methods have been added. Every question goes through one general path in the `mathcore` package:

```text
specs/<id>.json → validate (numeric truth check, domain, plain-words restatement)
→ select strategy → rewrite search over named rules → independent verifier → template renderer
```

- **Input format:** one JSON spec per question: variables with domains, given conditions, AP/GP definitions, goal, prescribed method, source quotes. No solution steps. Given conditions may be equations, "in AP/GP", equal ratios (the k-method) or "equal roots". Goals may be an equality, "in AP/GP", several parts (a later part may use an earlier part's proved result), "find a value" with constraints, or "solve an equation" on an interval. Angles may be written in degrees (`20*deg`).
- **Rules and search:** named algebra, index, log, surd, symmetric-function, AP/GP and trig rules (compound, double, triple and half angles, sum-to-product and back, tan P − tan Q, special values, angle reduction), each with the reason a student would write. One best-first search works between the two sides, which may meet in the middle. It handles any variables and angles. The trig rules are generalised from `automatic_trig_solver.py`.
- **Strategies:** `identity`; `conditional` (process each given condition, cross-multiplying, factorising and using the zero-product rule, then solve for a variable, power or log and substitute, or use the givens directly); `difference` (LHS − RHS = 0); `take_logs`; `find_value` (solve, keep admissible roots); `solve_equation` (rewrite by equivalences into basic factors, use the general-solution formulae on the interval, reject values where the original is undefined or false); `polynomial` (factor theorem, completing the square); `general_solution` (every solution of a trig equation as families in an integer n); `componendo_dividendo` (prescribed method); `one_real_roots` (sum of discriminants is a square); `only_solution` (proof by contradiction); and `geometry` (the existing Newclid route for one question).
- **Verifier:** each step is replayed from the rule registry and checked exactly and numerically (50 digits at fresh admissible points). The exact check is ideal or radical membership, with surds, logs and real powers in normal form, and every angle written through base angles (so sin(A−B), cos 27x and cos(α/2) relate to sin A, cos x and cos α). Closed-form numbers such as cos 20°·cos 40°·cos 80° are compared by minimal polynomial. New denominators need a nonvanishing certificate. Derived facts must follow from the givens. The trace must prove exactly the stated goal.
- **Presentation:** answers show the question's own expressions as written and school notation (sin A, cosec A, 20°). Large simplifications are split into checked stages (simplify each fraction, common denominator, expand, factorise, cancel), and when a proof meets in the middle both sides are taken to the same factorised form. Each answer records its "large jumps" (none at present). The search budget is a number of states, so results do not depend on machine speed.
- **Step honesty:** a plain algebra step (expand, cancel, simplify) is refused if it only holds through surd arithmetic, index laws or log laws, so those appear as their own named steps.

64 bank questions are solved with no per-question code (9 after Milestone 1, 26 after Milestone 2, 30 after Milestone 3, 46 with calculus, 64 with geometry, inverse trig and the new algebra methods).

- **Geometry by coordinates:** a spec may give points with coordinates; `dist2(A,B)` (AB²), `dot`, `cross`, `area` and coordinates are named quantities, and a checked step writes them in coordinates (the answer shows each one worked out, e.g. AD² = (c − 0)² + (0 − 2a)²). The spec must list the figure facts its coordinates encode (midpoint, right angle, parallel, perpendicular, equal length, on a line); each is checked exactly, and a wrong encoding is rejected. Givens about the figure (e.g. DE ∥ BC) are written in coordinates and used like any other given. Solved: IX-001, IX-004, IX-006, IX-007, IX-009, IX-014, IX-019, IX-024, IX-025, X-017, X-025, X-028. Not used for Pythagoras' theorem itself (X-029), which the distance formula assumes.
- **Inverse trig:** rules for 2tan⁻¹x, cos⁻¹/sin⁻¹ to tan⁻¹, tan⁻¹x + tan⁻¹y, cot⁻¹(cot u) and the half-angle square roots √(1 ± sin x). Each proves its branch condition before it applies: for a number by its sign to 50 digits; for x on an interval stated in the spec, by guaranteed interval arithmetic (mpmath), allowing a zero only at an excluded endpoint. Steps with inverse functions are compared exactly when the same inverse function is on both sides, otherwise to 50 digits inside the interval. Solved: XII-010, XII-011.
- **General solutions:** sin u = sin α ⇒ u = nπ + (−1)ⁿα, cos u = cos α ⇒ u = 2nπ ± α, tan u = tan α ⇒ u = nπ + α, after the same checked rewriting as interval equations. Checked: every family solves the original at n = −6 … 6, the rewriting ends in exactly the listed factors, and the families' values in [0, 2π) equal SymPy's solveset there when that is finite.
- **Algebra:** componendo–dividendo (each derived equation must follow from the given, by Groebner bases and at sample points: X-009); at least one quadratic has real roots (XI-025); the only real solution, by contradiction (XI-030); AM/GM recovery with the larger number named first (XI-006); a square root of a square of a nonnegative quantity simplified using the declared signs.

- **Calculus:** relations between y and its derivatives (implicit and logarithmic differentiation, by differentiating the given relation with the chain rule); finding a value (marginal cost); first principles (rationalise, or split a product and use sum-to-product, then lim sin θ/θ = 1); monotonicity (sign of f′); maxima and minima (eliminate a variable with the givens, unique critical point, second-derivative test, claims checked at the optimum); definite integrals (school substitutions, the reflection property, change of variable for proving that property).
- **Calculus checks:** differentiation replayed exactly; integral evaluations checked by differentiating the antiderivative back and by checking there is no pole between the limits, plus quadrature; limits checked by SymPy and numerically at small h; a property of an unspecified f is checked on several test functions and may not be proved by quoting such a property; the closing "simplify" may only rewrite a closed-form number. Generated variants and false controls test transfer (see Results).

Current execution makes **no LLM API calls**. AI helped prepare inputs, develop code, and interpret results. Total AI savings have not been measured against an LLM-only workflow.

## What we need to build

Inputs are still written by hand into `specs/`. The full workflow is:

```text
New question and any figure
→ interpret wording and diagram, using an LLM where needed
→ validate the structured mathematical input
→ select a supported solver and method
→ generate mathematical steps
→ verify the steps, conditions, and final result
→ produce a student-friendly answer
```

### TODO

- [x] **Map the bank:** group questions by mathematical method, identify missing capabilities, and prioritise reusable methods. See [`BANK_MAP.md`](BANK_MAP.md); assignments are curated and should be re-checked as engines are built.
- [ ] **Interpret new questions:** convert text and figures into givens, expressions, domains, goals, and any prescribed method.
- [ ] **Validate interpretation:** check notation, assumptions, figure relationships, and missing information; request clarification when needed. *Partly done: `mathcore/validate.py` checks parsing, declared domains, satisfiable conditions and the claim's truth, and restates the spec in words. Figure relationships are not checked.*
- [ ] **Select methods automatically:** route structured problems to suitable solvers and try alternatives within a defined budget. *Partly done: `mathcore/strategies` routes by goal kind and prescribed method.*
- [ ] **Strengthen verification:** preserve domains, reject extra roots, handle branches and cases, and check completeness where required.
- [ ] **Improve explanations:** show manageable steps and their reasons, including explicit conditions. *Milestone 4 done in code (`mathcore/notation.py`, `refine.py`, `presentation.py`); `results/readability_review.md` is a 10-answer sheet for a teacher to score. Not done: the teacher's review itself.*
- [ ] **Measure progress:** use separate development and evaluation questions; record coverage, correctness, readability, runtime, and actual LLM tokens. *Partly done: `evaluation/` has a fixed development/evaluation split, generated variants and false controls. Readability review and real token counts wait for the agents.*

Covering most methods in the bank is the development target. It is not a guarantee that every possible question will be solved.

## How answers are checked

Before solving, `mathcore/validate.py` tests the claim at random points that satisfy the given conditions and the domain. A false claim is reported as `COUNTEREXAMPLE`, with the point. After solving, `mathcore/verify.py` checks every step, without calling the search:

1. Rebuild the named rule from the registry and replay it.
2. Confirm equality exactly: reduce modulo sin²+cos²=1, the surd relations and the given conditions, or use radical membership limited to the domain. Logs and real powers are put in a normal form first, and angles are written through base angles.
3. Confirm equality numerically, at 50 digits on fresh points.
4. Require a certificate that every new denominator cannot vanish where the original expression is defined.

A derived condition ("from the givens, a = …") must follow from the givens. Taking a positive root also needs both sides positive. The trace must then prove exactly the spec's goal. Substitutions and uses of a given must come from a derived condition or a stated given, and a factorisation must expand back and contain the factor. A "no real roots" claim is confirmed by a root count, and a prescribed method must appear in the trace. For an equation, each kept value must satisfy the original and each rejected one must not. No root can be missed: every rewriting step is checked as an equivalence (or an implication from the original), and each basic factor's roots come from the general-solution formula and are cross-checked by SymPy. A one-call SymPy solve is deliberately not trusted: `solveset` misses two roots of 2cos²x − cos x − 1 = 0 on [0, 2π).

The current geometry check independently verifies one conclusion with symbolic coordinates. It does **not** replay every Newclid deduction. Its student explanation uses a separate prepared template.

`SOLVED_AND_TRACE_CHECKED` means the implemented checks passed. Correct interpretation, complete reasoning, and readable school-style presentation still need separate evaluation. Unsupported or inconclusive results are not accepted as solved.

## Results so far

| Experiment | Saved result |
|---|---|
| Main bank: 135 questions | 64 accepted, 68 unsupported, 3 source issues (development split 54 solved, evaluation split 10) |
| Geometry, inverse trig, algebra | 18 more solved: 12 geometry (IX-001, IX-004, IX-006, IX-007, IX-009, IX-014, IX-019, IX-024, IX-025, X-017, X-025, X-028), XII-010, XII-011, X-009, XI-006, XI-025, XI-030 |
| Calculus | 16 of 18 calculus questions solved: XI-015, XI-020, XII-001 to 004, XII-016 to 019, XII-021, XII-022, XII-032 to 035. Not solved: XII-020 (two curves at once), XII-036 (source issue). |
| Source issues found by validation | IX-021: the givens have no real solution with distinct a, b, c, so the claim is vacuous. VIII-001: no real a, b, c satisfy the givens, so it is proved over complex numbers with a warning. |
| Generated variants (`evaluation/variants.py`) | 65/65 expected-solvable cases solved, including 9 new calculus questions. They include 14 new questions of the Milestone 2 types and 12 of the Milestone 3 types (compound, double, triple and half angles, sum-to-product, telescoping, and six trig equations including one with an extraneous root) |
| False controls (`evaluation/variants.py`) | 26/26 rejected (23 `COUNTEREXAMPLE`, 3 `INCONCLUSIVE`); 0 false accepts |
| Known gap | sin 20°·sin 40°·sin 60°·sin 80° = 3/16 (search budget runs out; needs the multiply-by-2-sin method). The earlier gap sin 2A = 2 sin A cos A is solved. |
| Five additional trig identities (old solver) | 3 solved and checked, 1 inconclusive, 1 unsupported; the new core also solves the inconclusive T4 |
| Five additional geometry encodings | Newclid proved 3; 2 hit an unimplemented length-equation adapter |
| Existing independent checker for those five new geometry cases | None supported; no additions to the production solved count |
| Presentation (`metrics.json`) | 0 of 64 answers have a large jump (a simplify step that, as shown, starts from 12 or more operations and loses 6 or more) |
| Last recorded automated test suite | 43 tests passed (`test_mathcore`, `test_pipeline`) |

The variants were generated from question types that are already supported, so they test robustness, not coverage. Milestone 2's targets were chosen from the whole bank, so 6 of them are in the evaluation split; that split is not a clean held-out test for this milestone. These small selected tests do not establish a general accuracy percentage. No complete-answer marking-scheme evaluation or equivalent LLM-only benchmark has been completed.

## Code and data

| File | Role |
|---|---|
| `pipeline.py` | Bank driver: spec → validate → strategy → verify → render. `--spec FILE` solves one spec without the bank. |
| `mathcore/spec.py`, `parse.py`, `problem.py` | Input format, safe parser, source-level domain conditions. |
| `mathcore/validate.py`, `sampling.py` | Pre-solve checks: claim truth at admissible points, consistency, plain-words restatement. |
| `mathcore/rules/` | Named rule library (algebra, trig, AP, polynomial) with a registry the verifier replays from. |
| `mathcore/engine.py`, `equality.py` | Rewrite search; exact equality and domain certificates. |
| `mathcore/strategies/` | `identity`, `conditional`, `polynomial`, `geometry`; selection by goal and prescribed method. |
| `mathcore/verify.py`, `render.py` | Independent trace checker; school-style answer templates. |
| `specs/` | One problem spec per supported bank question. |
| `evaluation/` | Development/evaluation split, generated variants, false controls; `python -m evaluation.run_eval` writes `results/eval_report.json`. |
| `automatic_trig_solver.py` | Original single-angle trig search; kept as a standalone demo. |
| `newclid_probe.py` | Geometry proof attempt and its specific independent conclusion check (used by the `geometry` strategy). |
| `repair_yuclid_windows.py` | Repairs the missing Boost runtime for the tested Windows Yuclid executable. |
| `legacy_pipeline.py`, `formalizations.json` | The previous per-method pipeline and its inputs, kept so the two experiment scripts below still reproduce. |
| `usage_walkthrough.py` | Shows actual inputs and outputs at each stage (legacy pipeline). |
| `generalisation_check.py` | Runs the five-plus-five transfer experiment and false controls (legacy pipeline). Its saved manifest records hashes of the old file name, so `--report-only` needs a fresh run. |
| `evaluation/review_sheet.py` | Writes `results/readability_review.md`, a fixed stratified sample with a rubric for a teacher. |
| `test_mathcore.py`, `test_pipeline.py` | Unit tests for the core; bank integration tests. |
| `profiles.json` | Draft class/method metadata; currently not enforced. |
| `method_map.json` | Curated assignment of every bank question to a reusable engine, with feasibility and build order. |
| `bank_map.py` | Validates `method_map.json` against the bank and latest results; writes `BANK_MAP.md` and `results/bank_map.json`. |

The bank and figure workflows expect matching data **outside the code checkout**:

```text
workspace/
├── proofs_derivations_core_json/
│   ├── mathematics_core.json
│   └── image_assets.json
└── math_solution_pipeline/       # code checkout
```

A code-only clone needs these inputs to reproduce the bank runs. The geometry probe and integration tests retain assumptions about this specific bank.

## Run locally

Tested with Python 3.12, SymPy 1.13.3, Newclid 3.0.1, and py-yuclid 3.0.0 on Windows. From the code folder:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-geometry.txt
.\.venv\Scripts\python.exe pipeline.py
.\.venv\Scripts\python.exe -m evaluation.run_eval
.\.venv\Scripts\python.exe -m unittest -v test_mathcore test_pipeline
```

**To run your own question papers, see [`RUNNING.md`](RUNNING.md)**: the command, the spec format, and what each status means. To try one question, write a spec in the same format as `specs/` and run `pipeline.py --spec path\to\spec.json`.

If the tested Windows Yuclid executable fails to load its Boost DLLs, run `repair_yuclid_windows.py` with the same Python. It checksum-verifies a pinned Boost package, retains the original executable, patches its DLL import names, and tests startup. It requires network access on first download, Windows `tar`, and compatible installed Microsoft C++ runtime libraries. This workaround targets the tested wheel.

For a bank-free trig demonstration, install `requirements.txt` and run `automatic_trig_solver.py`. Run `usage_walkthrough.py` or `generalisation_check.py` for the documented experiments.

Generated bank outputs are `results/per_question_results.json`, `results/metrics.json`, and `results/sample_answers.md`. Run `bank_map.py` after `pipeline.py` to refresh `BANK_MAP.md` and `results/bank_map.json`. Detailed experiment inputs, traces, proofs, and errors are saved under `results/usage_walkthrough/` and `results/generalisation_check/`.

# Running a question paper through the pipeline

This guide is for auditing: run one or more extracted papers and see which questions pass and which fail.

## 1. Setup (once)

Needs Python 3.12.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-geometry.txt
```

(On macOS/Linux: `python3.12 -m venv .venv` and `.venv/bin/python`. `requirements.txt` is enough if you skip geometry.)

Check it works on the bundled sample paper:

```powershell
.\.venv\Scripts\python.exe pipeline.py --bank examples\sample_paper.json --specs examples\specs --output out\sample
```

Expected: EX-001 to EX-003 `SOLVED_AND_TRACE_CHECKED`, EX-004 `COUNTEREXAMPLE` (a deliberately false claim), EX-005 `UNSUPPORTED` (no spec written).

## 2. How a question gets solved

The pipeline makes **no LLM calls**. Each question needs two things:

1. **The question record** in the paper JSON: the same extraction format as `mathematics_core.json`, i.e. `{"questions": [{"id": ..., "question_text_original": ..., ...}]}`. Only `id` is required; other fields (`topic`, `class`, `task_kind`, `question_text_cleaned`, `source`, `board_status`, `context_requirements`, ...) are copied into the output if present.
2. **A spec**: a small JSON file `specs/<id>.json` that states, in machine-readable maths, what is given and what is asked. It never contains solution steps. Code then finds the steps, checks them independently, and writes the answer.

A question **without a spec comes out `UNSUPPORTED`** ("No spec has been written for this question yet"). So for a new paper, the work is: write one spec per question (a Claude session can do this from the question text, see section 4), then run.

## 3. Run a paper

```powershell
.\.venv\Scripts\python.exe pipeline.py --bank path\to\paper.json --specs path\to\paper_specs --output out\paper1
```

| Option | Meaning |
|---|---|
| `--bank` | The paper JSON (default: `../proofs_derivations_core_json/mathematics_core.json`, or the `MATH_BANK` environment variable) |
| `--specs` | Folder of spec files, one `<id>.json` per question (default: `specs/`). Specs whose id is not in the paper are ignored, so one folder can serve several papers. |
| `--output` | Where results go (default: `results/`) |
| `--spec file.json` | Solve one spec on its own and print the answer (no paper needed) |

Outputs in the `--output` folder:

| File | What it holds |
|---|---|
| `summary.csv` | One row per question: id, status, method, reason. **Start here.** |
| `metrics.json` | Counts by status and method, runtime |
| `per_question_results.json` | Full record per question: spec, steps, verification evidence, attempts |
| `sample_answers.md` | The written answers for solved questions |

### Statuses

| Status | Pass? | Meaning |
|---|---|---|
| `SOLVED_AND_TRACE_CHECKED` | Pass | Solved, and every step was checked by the independent verifier |
| `UNSUPPORTED` | Fail (coverage) | No spec, or no strategy for this kind of question yet |
| `INCONCLUSIVE` | Fail | A strategy applied but did not finish within budget, or its answer failed verification |
| `COUNTEREXAMPLE` | Fail (claim false) | The stated result is false at an admissible point: usually a spec or extraction error, sometimes a misprint in the paper |
| `INPUT_AMBIGUOUS` | Fail (input) | The spec is malformed or the givens are inconsistent |
| `SOURCE_NEEDS_CORRECTION` | Fail (source) | A known misprint in the original paper |

An answer is only marked as a pass when the verifier accepts it; a wrong proof should never be reported as solved. If you find one, that is the most important bug to report.

## 4. Writing specs (what to tell the Claude session)

Point the session at this file, `mathcore/spec.py` (the schema, checked on load) and the 47 examples in `specs/`. Ask it to write one `<id>.json` per question, **transcribing** the question only, never adding steps. Then run the pipeline.

Spec fields:

| Field | Meaning |
|---|---|
| `id` | Must equal the question id and the file name |
| `goal` | What is asked; `kind` is one of the kinds below |
| `variables` | `{"x": ["real"], "a": ["positive"]}`; assumptions from `real, positive, nonnegative, nonzero, integer, complex` |
| `hypotheses` | Givens: `[{"lhs": "...", "rhs": "...", "quote": "source words"}]`, or `{"kind": "in_ap"/"in_gp", "terms": [3 terms]}`, `equal_ratios`, `equal_roots` |
| `functions` | `{"y": {"of": "x", "derivatives": ["y1", "y2"]}}`: y depends on x, and y1, y2 stand for dy/dx, d²y/dx² |
| `definitions` | `{"C": {"of": "x", "expr": "..."}}`: a named function C(x) |
| `abstract` | Names of unspecified functions, e.g. `["f"]` for a property of integrals |
| `sequences` | `{"a": {"type": "ap", "first": "a1", "difference": "d"}}` (or `gp` with `ratio`) |
| `prescribed_method` | Only if the question says "using ...": `factor_theorem` or `completing_square` |
| `quotes` | Source words for each field, e.g. `{"goal": "..."}`, so a reviewer can check the transcription |
| `note` | Any interpretation made (e.g. "log base not printed; natural log used") |

Goal kinds:

| `kind` | Required keys | Use for |
|---|---|---|
| `prove_identity` | `lhs`, `rhs` (or `in_ap` / `in_gp` / `parts`) | Prove an identity with no givens |
| `prove_from_hypotheses` | `lhs`, `rhs` + `hypotheses` | "If ..., prove that ..." (incl. implicit/log differentiation) |
| `find_value` | `variable`, `lhs`, `rhs` | Find the value of an unknown |
| `solve_equation` | `variable`, `lhs`, `rhs`, `low`, `high` | Solve on an interval |
| `evaluate` | `expr` | Evaluate an expression |
| `factor_theorem` | `polynomial`, `factor`, `variable` | Show a factor divides a polynomial |
| `show_no_real_roots` | `polynomial`, `variable` | Show a polynomial has no real roots |
| `first_principles` | `function`, `variable` | Derivative from first principles |
| `monotonic` | `function`, `variable`, `direction` | Increasing / decreasing |
| `extremum` | `objective`, `variable`, `type` (`max`/`min`); optional `eliminate`, `claims` | Maxima and minima word problems |
| `geometry_jgex` | `jgex`, `figure_asset_id` | Euclidean geometry (Newclid) |

Expressions use SymPy syntax: `x**2`, `sqrt(2)`, `sin(x)`, `exp(x)`, `log(x)` (natural), `pi`, `diff(f, x)`, `integral(f, x, a, b)`.

Example (`examples/specs/EX-003.json`):

```json
{
  "id": "EX-003",
  "variables": {"x": ["real"], "y": ["real"]},
  "functions": {"y": {"of": "x", "derivatives": ["y1"]}},
  "hypotheses": [{"lhs": "y", "rhs": "log(x**2+1)", "quote": "y = log(x^2 + 1)"}],
  "goal": {"kind": "prove_from_hypotheses", "lhs": "(x**2+1)*y1", "rhs": "2*x"},
  "quotes": {"goal": "(x^2 + 1) dy/dx = 2x"},
  "note": "y1 denotes dy/dx."
}
```

To check one spec quickly: `.\.venv\Scripts\python.exe pipeline.py --spec path\to\spec.json`.

## 5. What is covered today

Algebra (identities, conditional identities, AP/GP, factor theorem, polynomials, logs and indices), trigonometry (identities, compound angles, conditional identities, values, equations on an interval), calculus (implicit/log differentiation, first principles, monotonicity, maxima/minima, definite integrals and their properties) and one geometry route. On the main bank: 46 of 135 solved, 86 unsupported (mostly topics not built yet: vectors, matrices, statistics, coordinate geometry, integration by parts, area, differential equations), 3 source issues. See `README.md` and `BUILD_PLAN.md` for detail and known gaps.

## 6. Tests

```powershell
.\.venv\Scripts\python.exe -m unittest -v test_mathcore test_pipeline
```

The main-bank tests need `mathematics_core.json` (set `MATH_BANK` to its path); they are skipped if it is not found.

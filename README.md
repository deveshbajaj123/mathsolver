# Mathematics Solution Pipeline

A Python foundation for solving mathematics questions, checking the working, and producing clear student answers.

**Our goal:** build on SymPy, Newclid/Yuclid, and the existing programs to cover all or most methods needed by our question bank. We want reusable methods that handle many questions, with LLM assistance where needed and measurable AI usage.

## What works today

The program reads an existing JSON question bank and looks up prepared mathematical inputs in `formalizations.json`. It runs the saved method, records the checks, and renders accepted results using Python templates.

- **Trigonometry:** searches a limited library of algebraic and trig transformations using SymPy.
- **Algebra:** implements factor-theorem and completing-the-square methods.
- **Arithmetic progressions:** checks selected term and sum relationships.
- **Geometry:** uses Newclid/Yuclid, with a complete production checking route for one isosceles-triangle midpoint question.

Current execution makes **no LLM API calls**. AI helped prepare inputs, develop code, and interpret results. Total AI savings have not been measured against an LLM-only workflow.

## What we need to build

The current lookup of prepared inputs must expand into this workflow:

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

- [ ] **Map the bank:** group questions by mathematical method, identify missing capabilities, and prioritise reusable methods.
- [ ] **Interpret new questions:** convert text and figures into givens, expressions, domains, goals, and any prescribed method.
- [ ] **Validate interpretation:** check notation, assumptions, figure relationships, and missing information; request clarification when needed.
- [ ] **Select methods automatically:** route structured problems to suitable solvers and try alternatives within a defined budget.
- [ ] **Expand trigonometry:** add more identity transformations, compound/double angles, substitutions, and equation-solving methods.
- [ ] **Expand algebra:** add broader factorisation, equations, simultaneous equations, rational expressions, radicals, and inequalities.
- [ ] **Generalise geometry:** support new encodings, resolve adapter gaps, add suitable independent checks, and render arbitrary supported proofs.
- [ ] **Strengthen verification:** preserve domains, reject extra roots, handle branches and cases, and check completeness where required.
- [ ] **Improve explanations:** show manageable steps and their reasons, including explicit conditions.
- [ ] **Measure progress:** use separate development and evaluation questions; record coverage, correctness, readability, runtime, and actual LLM tokens.

Covering most methods in the bank is the development target. It is not a guarantee that every possible question will be solved.

## How answers are checked

Trig steps are checked against permitted rules, exact symbolic equality, and domain conditions, then replayed. Algebra/AP routes use method-specific checks such as expanding factors back, checking polynomial remainders, or simplifying symbolic relations.

The current geometry check independently verifies one conclusion with symbolic coordinates. It does **not** replay every Newclid deduction. Its student explanation uses a separate prepared template.

`SOLVED_AND_TRACE_CHECKED` means the implemented checks passed. Correct interpretation, complete reasoning, and readable school-style presentation still need separate evaluation. Unsupported or inconclusive results are not accepted as solved.

## Results so far

| Experiment | Saved result |
|---|---|
| Main bank: 135 questions | 9 accepted, 124 unsupported, 2 source issues |
| Five additional trig identities | 3 solved and checked, 1 inconclusive, 1 unsupported |
| Five additional geometry encodings | Newclid proved 3; 2 hit an unimplemented length-equation adapter |
| Existing independent checker for those five new geometry cases | None supported; no additions to the production solved count |
| Last recorded automated test suite | 10 tests passed |

These small selected tests do not establish a general accuracy percentage. No complete-answer marking-scheme evaluation or equivalent LLM-only benchmark has been completed.

## Code and data

| File | Role |
|---|---|
| `pipeline.py` | Reads the bank, parses inputs, dispatches methods, records traces, and renders answers. |
| `automatic_trig_solver.py` | Trig rules, search, equality/domain checks, and standalone examples. |
| `newclid_probe.py` | Original geometry proof attempt and its specific independent conclusion check. |
| `repair_yuclid_windows.py` | Repairs the missing Boost runtime for the tested Windows Yuclid executable. |
| `formalizations.json` | Prepared question inputs and method names. |
| `usage_walkthrough.py` | Shows actual inputs and outputs at each stage. |
| `generalisation_check.py` | Runs the five-plus-five transfer experiment and false controls. |
| `test_pipeline.py` | Automated tests for implemented behaviour. |
| `profiles.json` | Draft class/method metadata; currently not enforced. |

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
.\.venv\Scripts\python.exe -m unittest -v test_pipeline
```

If the tested Windows Yuclid executable fails to load its Boost DLLs, run `repair_yuclid_windows.py` with the same Python. It checksum-verifies a pinned Boost package, retains the original executable, patches its DLL import names, and tests startup. It requires network access on first download, Windows `tar`, and compatible installed Microsoft C++ runtime libraries. This workaround targets the tested wheel.

For a bank-free trig demonstration, install `requirements.txt` and run `automatic_trig_solver.py`. Run `usage_walkthrough.py` or `generalisation_check.py` for the documented experiments.

Generated bank outputs are `results/per_question_results.json`, `results/metrics.json`, and `results/sample_answers.md`. Detailed experiment inputs, traces, proofs, and errors are saved under `results/usage_walkthrough/` and `results/generalisation_check/`.

# Build plan: general algebra and trigonometry solver

Principle: **code computes and checks; agents interpret and hint.** Every mathematical step that reaches a student answer is produced or replayed by code. An LLM never supplies an accepted step on its own authority.

```
question text (+ figure)
   │  Step 8  Interpretation agent (LLM, one call)      ← main AI cost
   ▼
problem spec (JSON)
   │  Step 2  Spec validation (code)                    → FALSE_CLAIM / INCONSISTENT / AMBIGUOUS
   ▼
validated spec
   │  Step 5  Strategy selection + strategies (code)
   │            uses Step 3 rule library + Step 4 rewrite engine
   │  Step 9  Hint agent (LLM, only if inconclusive)    ← occasional AI cost
   ▼
step trace
   │  Step 6  Independent verification (code)           → SOLVED_AND_TRACE_CHECKED or rejected
   ▼
   │  Step 7  Explanation renderer (code templates)
   ▼
student answer          Step 10 Evaluation harness measures every stage
```

Running example used below, PD-MATH-X-003: *If x, y, z are in continued proportion, prove that (x+y)²/(y+z)² = x/z.*

---

## Step 1 — Problem spec and safe parser

**Goal.** One input format for every algebra/trig question, replacing the per-method shapes in `formalizations.json`.

**Spec fields**
- `variables`: name → assumptions (`real`, `positive`, `nonzero`, `integer`, interval).
- `hypotheses`: list of equations/relations, each with a `kind` (`equation`, `proportion`, `in_ap`, `in_gp`, `ratio_equal`, …) and a source quote.
- `goal`: one of `prove_identity`, `prove_from_hypotheses`, `solve_equation`, `factorise`, `show_no_real_roots`, `show_condition`, `evaluate_exact`.
- `prescribed_method`: e.g. `componendo_dividendo`, `factor_theorem`, `completing_square`, or null.
- `source_quotes`: the words each field came from (for back-checking).

Example (X-003):
```json
{"id": "PD-MATH-X-003",
 "variables": {"x": ["real", "nonzero"], "y": ["real", "nonzero"], "z": ["real", "nonzero"]},
 "hypotheses": [{"kind": "proportion", "terms": ["x", "y", "z"], "quote": "x, y, z are in continued proportion"}],
 "goal": {"kind": "prove_from_hypotheses", "lhs": "(x+y)**2/(y+z)**2", "rhs": "x/z"},
 "prescribed_method": null}
```

**Parser.** Extend the existing AST whitelist in `pipeline.py` (never `sympify` on untrusted text): declared symbols only; integers and rationals; `pi`; `sqrt`, rational exponents; `log`/`ln` with base; `sin cos tan cot sec csc` and inverses; any angle expression (`2*A`, `A-B`, `20*deg`). Keep the original syntax tree so original poles survive simplification (as `source_domain_factors` does today).

**Files.** `mathcore/spec.py` (dataclasses + JSON schema), `mathcore/parse.py`, `specs/<id>.json` (one per question).

**Done when.** The 9 current formalizations convert to the new schema; parser rejects the existing unsafe-input test cases; round-trip spec → JSON → spec is lossless.

---

## Step 2 — Spec validation (code, no AI)

**Goal.** Catch a bad interpretation before any solving. This is the main defence against an LLM misreading a question.

**Checks**
1. Everything parses; no undeclared symbols; each field has a source quote.
2. Hypotheses are satisfiable: find a numeric point that satisfies them (solve for some variables, sample the rest).
3. Goal is true under hypotheses: test at many random admissible points with high precision. A failure gives `FALSE_CLAIM` with the counterexample. Most misreadings land here, because a misread claim is usually false.
4. Domain: collect every denominator ≠ 0, log argument > 0, even-root radicand ≥ 0, `tan` cosine ≠ 0 into an explicit condition list.
5. Back-render the spec to plain English (`"Given x:y = y:z, prove …"`) for side-by-side comparison with the source.

**Outcomes.** `VALID`, `FALSE_CLAIM`, `INCONSISTENT`, `AMBIGUOUS` (e.g. missing variable domain).

**Files.** `mathcore/validate.py`.

**Done when.** All 9 current specs are `VALID`; deliberately wrong specs (swapped sides, wrong exponent) are rejected with counterexamples.

---

## Step 3 — Rule library

**Goal.** A shared, named set of school-level rewrite rules. Adding coverage should mostly mean adding rules.

**Each rule has** a name, the reason text a student would write, an applicability test, the transform, and the side conditions it introduces (e.g. cancelling `(1+k)` adds `1+k ≠ 0`). Rules are tagged by topic and class so `profiles.json` can finally restrict which rules a given class may use.

**Rule sets**
- *Algebra:* expand, factor, cancel, common denominator, cross-multiply, substitute a hypothesis, standard identities ((a±b)², a³±b³, a³+b³+c³−3abc), difference of squares, rationalise a denominator, perfect square recognition.
- *Indices/logs/surds:* index laws, log laws, change of base, surd simplification.
- *Trigonometry:* the existing 12 rules, plus compound angle, double/triple angle, half angle, sum-to-product and product-to-sum, complementary angles, special-angle values.
- *Generated rules:* one "substitute" rule per hypothesis, created from the spec.

**Files.** `mathcore/rules/{algebra,indices,trig}.py`, `mathcore/rules/base.py`.

**Done when.** Each rule has a unit test showing one correct application and one refused application (wrong form or unsafe domain).

---

## Step 4 — Rewrite engine

**Goal.** Generalise `automatic_trig_solver.solve` from one angle `A` to any spec.

**Changes from today**
- States can be expressions or equations, over any declared symbols and angles.
- Equality test generalised: algebraic expressions by `cancel` modulo the hypothesis ideal (Gröbner basis); trig by mapping each distinct base angle to its own (sin, cos) pair with sin² + cos² = 1.
- Domain safety generalised from the current Gröbner certificate to multiple symbols and to log/root conditions.
- Search is unchanged in spirit: best-first from either side, scored by size and distance to goal, with state/depth/time budgets; every edge verified when added.

**Files.** `mathcore/engine.py`, `mathcore/equality.py`, `mathcore/domain.py`.

**Done when.** The 4 solved trig identities pass through the new engine with the same or shorter traces, and the existing false-claim and domain controls still fail as they should.

---

## Step 5 — Strategies and selection

**Goal.** A small number of methods that drive the engine; one strategy covers many questions.

| Strategy | Used for | Example |
|---|---|---|
| `identity` | LHS ⇄ RHS rewriting | X-001, IX-020 |
| `conditional` | prove from hypotheses: substitute, eliminate, or parametrise ("k method" for proportions), then `identity` | X-003, X-010, VIII-001, IX-015 |
| `equation` | solve, then check each root in the original equation and reject extra roots | trig equations, radical equations |
| `polynomial` | factor/remainder theorem, completing the square, discriminant conditions (migrated from `pipeline.py`) | X-007, X-030, X-015 |
| `exact_value` | evaluate a closed expression exactly (surds, logs, special angles) | IX-005, XI-003 |
| `sequence` | AP/GP general term and sum formulas, "are in AP/GP" conditions, then `conditional` | X-021, XI-005, XI-013 |

**Selection** is code: goal kind + features (hypotheses present, trig present, prescribed method) → an ordered list of strategies, each with its own budget. A prescribed method is mandatory, not a preference.

X-003 under `conditional`: hypothesis `x:y = y:z` → let `y = xk`, `z = xk²` (side condition k ≠ 0) → LHS = (1+k)²/(k²(1+k)²) → cancel (adds 1+k ≠ 0, which follows from y+z ≠ 0) → 1/k² = RHS.

**Files.** `mathcore/strategies/*.py`, `mathcore/select.py`.

**Done when.** The milestone question lists below are solved without per-question code.

---

## Step 6 — Independent verification

**Goal.** A separate checker that does not reuse search code, so a search bug cannot certify itself.

**Checks**
1. Replay every step: re-apply the named rule and compare.
2. Confirm each step's equality by a second method (exact symbolic and high-precision numeric at random admissible points).
3. Every side condition used is in the final answer's condition list.
4. The final line is exactly the spec's goal; a hypothesis was not silently strengthened.
5. For equations: every reported root satisfies the original equation and domain, and no root found by an independent solve is missing.

**Statuses.** Only a pass gives `SOLVED_AND_TRACE_CHECKED`. Otherwise `INCONCLUSIVE`, `COUNTEREXAMPLE` or `UNSUPPORTED`, as today.

**Files.** `mathcore/verify.py`.

---

## Step 7 — Explanation renderer

**Goal.** Turn a checked trace into a school-style answer without AI.

- Fixed layout: **Given**, **To prove**, **Proof** (one line per step with its reason), conditions stated explicitly, **Hence proved**.
- Merge consecutive routine algebra steps; cap visible steps; keep each rule's reason text.
- Strategy-specific templates (e.g. the "k method" introduces "Let y/x = z/y = k, so y = xk and z = xk²").
- Output Markdown + LaTeX. If an LLM polish pass is ever added, the maths tokens are locked and the text is re-verified.

**Files.** `mathcore/render.py`, replacing `render_answer` in `pipeline.py`.

---

## Step 8 — Interpretation agent (LLM)

**Goal.** Question text → Step 1 spec. Built *after* Steps 1–7 so the schema is stable.

- One call with the schema, a few worked spec examples and the question text; output must be JSON only.
- Step 2 validates it; on failure, one retry that includes the validator's error message; then `INPUT_AMBIGUOUS` for human review.
- Every call logs model, input and output tokens, and latency to a token ledger.
- Until this exists, specs are written by a person or an offline agent into `specs/`, in the same schema.

**Files.** `agents/interpret.py`, `agents/ledger.py`, `agents/prompts/interpret.md`.

---

## Step 9 — Hint agent (LLM, fallback only)

**Goal.** Rescue `INCONCLUSIVE` cases without trusting the model.

- Called only after all selected strategies exhaust their budgets.
- Returns a hint, not a proof: a substitution, an intermediate expression to aim for, or a rule order.
- The engine tries the hint; every resulting step goes through Step 6. A wrong hint only costs a failed attempt.
- Hints that work are logged; ones that recur become new rules or strategies, so AI use falls over time.

**Files.** `agents/hint.py`.

---

## Step 10 — Evaluation harness (start in Milestone 1)

- Fixed development/evaluation split of the bank (by hashed ID); evaluation questions are not used to write rules.
- Generated variants of solved questions (changed numbers, renamed variables, swapped sides) to test generalisation, since the bank is small.
- False controls (deliberately wrong claims) must never be accepted: false-accept rate is a hard gate of 0.
- Per run: coverage, solved-and-checked count, false accepts, runtime, LLM calls and tokens per question, and a sample for human readability review.

**Files.** `evaluation/run_eval.py`, `evaluation/split.json`, `evaluation/variants.py` (named `evaluation`, not `eval`, to avoid confusion with the Python built-in).

---

## Milestones

| Milestone | Steps | Target questions | Gate |
|---|---|---|---|
| M1 Core ✅ | 1, 2, 3 (existing rules), 4, 6, 7, 10 | The 9 already solved, through the new path | Done: 9 solved, 29/29 variants, 0/9 false accepts; old dispatch kept only as `legacy_pipeline.py` for the recorded experiments |
| M2 Algebra ✅ | 3 (algebra, indices, logs, surds, symmetric), 5 `identity` `conditional` `difference` `take_logs` `find_value` `polynomial` | VIII-001, VIII-002, VIII-005, IX-005, IX-013, IX-015, IX-020, IX-021, X-003, X-006, X-010, X-011, X-015, X-023, X-026, XI-005, XI-009, XI-013 | Done: 17/18 solved, no per-question code; IX-021 flagged as a source issue (givens have no real solution). 43/43 variants, 0/18 false accepts. Deferred: XI-006 (needs ordering/sign reasoning), X-009 (componendo–dividendo with radicals) |
| M3 Trigonometry ✅ | 3 (compound/double/triple/half angles, sum-to-product and back, special values in degrees), 4 (angle basis, minimal polynomials), 5 `solve_equation` | XI-002, XI-003, XI-004, XI-010; trig equations as generated cases (the bank has none) | Done: 4/4 solved; 56/56 variants, 0/22 false accepts. A later part may use an earlier part's result. Equation completeness is structural, not a one-call solve (SymPy's `solveset` misses roots of 2cos²x − cos x − 1 = 0). Deferred: inverse trig (XII-010, XII-011), general solutions, sin 20° sin 40° sin 60° sin 80° |
| M4 Presentation ✅ (code) | 7 | All solved questions | Done in code: question notation as written, school notation, staged simplification (both sides to one factorised form), merged steps, a large-jump metric (0 of 30), state-based search budget, review sheet. Gate still open: a teacher scores `results/readability_review.md` |
| Calculus ✅ | 1 (functions y(x), named functions, diff, integral, unknown f), 3, 5, 6 | XI-015, XI-020, XII-001–004, XII-016–019, XII-021, XII-022, XII-032–035 | Done: 16/18 solved; 65/65 variants, 0/26 false accepts. Not done: XII-020 (two curves), XII-036 (source issue). XII-032 is in the evaluation split. |
| Expansion ✅ | 1 (points, figure facts, intervals), 3 (inverse trig, radicands), 5 `general_solution` `componendo_dividendo` `one_real_roots` `only_solution`, 6 (figure facts, branch checks, family checks) | IX-001, IX-004, IX-006, IX-007, IX-009, IX-014, IX-019, IX-024, IX-025, X-017, X-025, X-028, XII-010, XII-011, X-009, XI-006, XI-025, XI-030 | Done: 18/18 solved (64 in the bank); 65/65 variants, 0/26 false accepts. Not yet: angle-bisector and circle geometry, congruence write-ups, multiply-by-2-sin products, irrationality proofs. |
| M5 Agents | 8, 9 | New questions from text only | Token ledger in metrics; no false accepts |

M2 targets are taken from `BANK_MAP.md` (phase 1 and the sequence/polynomial engines). Questions needing X-009's radicals or a figure (X-024) are deferred until the parser and figure workflow support them.

## Proposed layout

```
math_solution_pipeline/
├── mathcore/        spec, parse, validate, rules/, engine, equality, domain, strategies/, select, verify, render
├── agents/          interpret, hint, ledger, prompts/
├── specs/           one JSON spec per question (replaces formalizations.json)
├── evaluation/      split, variants, run_eval
├── pipeline.py      thin driver: spec → validate → select → strategies → verify → render
└── tests/
```

# Evaluation, 25 October 2026

## Observed run

The local bank contained 135 questions: 127 proofs and 8 derivations in 46 topics. All 135 received a per-question status. The run used SymPy 1.13.3 and zero LLM calls or tokens. Runtime for the latest run is recorded in `results/metrics.json`.

| Outcome | Questions |
|---|---:|
| `SOLVED_AND_TRACE_CHECKED` | 9 |
| `SOURCE_NEEDS_CORRECTION` | 2 |
| `UNSUPPORTED` | 124 |
| `COUNTEREXAMPLE`, `INCONCLUSIVE`, `INPUT_AMBIGUOUS` | 0 |

The nine accepted questions are PD-MATH-X-001, X-002, X-004, X-005, X-007, X-021, X-022, X-030 and PD-MATH-VII-002. All nine emitted traces passed their method-specific checks. This is **6.67% accepted coverage** of this finite bank, not an accuracy estimate. Four are the original trig regression questions. Other routes cover the factor theorem, AP terms and sums, completing the square, and one geometry conclusion checked independently with symbolic coordinates. That geometry check does not replay arbitrary Newclid deductions. The test suite also exercises additional factorisation, quadratic and AP examples, a false trig claim, a new pole, an unapproved rule, unsupported multiple-angle input, and parser injection attempts.

No complete answer has been independently marked against an applicable scheme or by a qualified expert in this run. Thus the observed complete-answer accuracy has **sample size 0 and is unmeasured**; an uncertainty interval or 99% claim would be misleading. A 9/9 self-verified trace count only measures passing the implemented checks on a selected subset. Method approval and human presentation review are each 0/135. No failures occurred in the final run; 124 unsupported outcomes are capability gaps, not solver crashes.

## Source and domain issues

PD-MATH-XII-030 needs `a × b ≠ 0` for its displayed equation to define a unique plane. PD-MATH-XII-036's displayed logarithmic family omits the zero solution and sign branches on admissible intervals. The pipeline records both as `SOURCE_NEEDS_CORRECTION` and keeps their printed wording untouched. Neither is silently repaired or counted as solved.

The trig questions carry their original nonzero denominator conditions in the trace. The factor theorem route uses exact rational arithmetic and logs its quotient and remainder. The completing-square route requires real `x`; its result depends on the square being nonnegative. Other bank problems may need radical sign, inverse-trig branch, extraneous-root, zero-vector, geometry degeneracy, interval-endpoint or lost-division checks. Their unsupported status prevents an unchecked answer from being emitted.

## Marking and readability rubric

For any future human review, score each dimension 0, 1 or 2:

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Mathematical correctness | Wrong or unproved claim | Correct conclusion with a gap | All material steps and conditions justified |
| Required method | Violates explicit method | Plausible but unapproved | Matches the prescribed and approved profile |
| Working and readability | Opaque jumps | Some omitted intermediate work | Familiar notation, explicit working and reasons |
| Conclusion and scope | Missing or overclaimed | Present but conditions unclear | Clear conclusion on the correct domain |

A perfect 8/8 score on this four-dimension rubric would be an internal assessment, not a claim of full examination marks. This rubric has not yet been applied by an independent reviewer. A board mark claim requires an applicable marking scheme or a clearly labelled expert assessment. The current machine-rendered trig answers still have compressed algebraic jumps, especially X-002 and X-004, so their presentation review remains pending. The rendered file is a sample, not a certified student answer set.

## Concrete obstacles

The 15 figure-dependent questions need figure-to-symbol encodings checked against the printed statement before Newclid can be used. One question has a checked input encoding, a Newclid proof, and an independent exact symbolic replay integrated into the pipeline. Other geometry items still need theorem libraries and nondegeneracy checks. The remaining symbolic families need parsers, premise-aware method templates, rule checkers and domain/branch handling. SymPy can calculate final results for many of them, but that alone is not a school derivation. Board/class/year profiles require authoritative syllabus and method review; all current profiles are drafts. Integration and derivative step generators were only inspected for local availability, not wired into the solver.

Subsequent geometry repair and probe: PD-MATH-VII-002 was encoded from its original isosceles triangle figure and checked against the image asset checksum. The Windows Yuclid runtime was repaired using the SHA-256 verified conda-forge Boost 1.88 package. Newclid returned a proof with the expected givens and goal. An independent symbolic calculation established `RS²−QT²=3(PR²−PQ²)/4=0`, so the nonnegative lengths satisfy `RS=QT`. The pipeline now counts this one geometry result as solved and trace checked; teacher presentation and board-method reviews remain pending.

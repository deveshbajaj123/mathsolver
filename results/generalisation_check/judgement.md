# Generalisation judgement

The trigonometry search is reusable within a restricted class of inputs. The geometry engine is reusable, but the existing production geometry adapter, independent checker and answer renderer are specific to the original midpoint question.

Five new true trigonometry identities and five previously unsupported geometry bank questions were selected before executing this test. These were a purposive set, not a random sample. Test inputs were transcribed in the surrounding AI chat. SHA-256 checks confirm that pipeline.py, automatic_trig_solver.py, newclid_probe.py and formalizations.json were unchanged by the test.

## Trigonometry: existing route with new symbolic inputs

| Case | Identity | Output |
|---|---|---|
| T1 | tan(A)+cot(A)=sec(A)csc(A) | Solved and trace checked |
| T2 | (sec(A)+tan(A))(sec(A)-tan(A))=1 | Solved and trace checked |
| T3 | sin(A)^4-cos(A)^4=sin(A)^2-cos(A)^2 | Solved and trace checked |
| T4 | (1-cos(A))/(1+cos(A))=(csc(A)-cot(A))^2 | Inconclusive: exact identity check passed, but no permitted derivation was found; 21 states explored |
| T5 | sin(2A)=2sin(A)cos(A) | Unsupported: the grammar supports functions of A only |

Result: 3/5 new identities solved with rule replay, symbolic equality and domain checks. The same renderer produced answers for those three. This demonstrates transfer beyond the four original examples, but does not establish a 60% accuracy or coverage rate over arbitrary trigonometry questions. The solver handles rational single-angle expressions with integer powers and a bounded rule library. Automatic prose-to-expression conversion is absent.

T4 also exposed a reporting limitation: the inconclusive result does not retain its original domain list in the returned result, although the search computes and uses domain conditions. This result was not accepted.

## Geometry: direct Newclid tests and production coverage

| Case | Bank question | Engine output | Existing production workflow |
|---|---|---|---|
| G1 | IX-001: perpendicular diagonals bisect each other, prove rhombus | Proved all three equal-side goals | Unsupported |
| G2 | IX-002: circle with equal triangle side as diameter bisects base | Proved midpoint goal after supplied Thales translation | Unsupported |
| G3 | IX-004: square side midpoints form a square | Proved all six parallel/perpendicular/equal-side goals | Unsupported |
| G4 | IX-007: AD^2+CE^2=5DE^2 | Adapter error: LengthEquationPredicate is not implemented | Unsupported |
| G5 | IX-024: OA^2+OC^2=OB^2+OD^2 in rectangle | Same adapter error | Unsupported |

Engine result: 3/5 proved after manual predicate encoding. Existing independent geometry checker: 0/5 supported. Existing complete production workflow: 0/5 supported. The three engine proofs have not been promoted to solved answers or added to the bank metrics.

The predicate encodings use numeric diagrams for matching. Those numerical coordinates are not universal proof certificates. G2 required a manually supplied mathematical preprocessing step (diameter condition to perpendicularity); G1 and G3 also required expanding shape definitions. Neither task is automated by the existing code.

The previous geometry check independently verifies one midpoint conclusion with symbolic coordinates. It does not replay arbitrary Newclid proofs. The geometry renderer is a handwritten SAS template for that one original question. A generic proof checker and renderer are still needed for new geometry questions.

## Controls and AI usage

The false identity sec(A)^2-tan(A)^2=2 returned COUNTEREXAMPLE. The false equal-side claim in a generic triangle was rejected because its goal failed the numerical check. Neither was accepted. The latter rejection is a numerical guard, not a general proof checker.

All solver workers made zero LLM API calls. Selection, encoding, script development and interpretation used this AI chat and are excluded from those runtime totals. No LLM-only baseline was executed, so total token or cost savings are unmeasured.

## Engineering judgement

The current code can reduce repeated LLM solving for supported, already formalized trig inputs. Newclid can provide reusable geometric deduction after a correct encoding, as the three new proofs demonstrate. The complete system is not yet a general school-mathematics solution pipeline. Its main gaps are automatic input formalization, geometry predicate support in the adapter, independent verification across geometry problems, and general student-answer rendering.

The next useful improvement is a generic geometry interface and independent checker, followed by filling specific missing rule families. A larger random holdout is needed before making broad coverage claims. Algebra was outside this test.

All exact inputs, outputs, derivations, errors and raw Newclid proofs are in report.md and the individual T1–T5/G1–G5 JSON files. Run `.\.venv\Scripts\python.exe generalisation_check.py` from math_solution_pipeline to repeat the experiment.

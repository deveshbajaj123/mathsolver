# Bank method map

135 questions mapped to 21 reusable engines. Assignments are curated judgements in `method_map.json`, not solver output.

Priority score = sum over unsolved questions of feasibility weight {"high": 1.0, "medium": 0.5, "low": 0.1}. It estimates how many extra questions an engine could reach SOLVED_AND_TRACE_CHECKED; it is not a measured result.

| Rank | Engine | Status | Questions | Solved | Open (high/med/low) | Figures | Classes | Score |
|---:|---|---|---:|---:|---|---:|---|---:|
| 1 | Synthetic Euclidean proofs (congruence, circles, similarity, areas) (`synthetic_geometry`) | partial | 28 | 9 | 0/15/4 | 13 | 7, 8, 9, 10 | 7.9 |
| 2 | Coordinate and 3D analytic geometry (`analytic_coordinate`) | external | 8 | 0 | 6/2/0 | 0 | 9, 10, 11, 12 | 7.0 |
| 3 | Vector identities (`vector_algebra`) | missing | 8 | 0 | 5/3/0 | 0 | 12 | 6.5 |
| 4 | Set identities, logic and counterexamples (`boolean_membership`) | missing | 6 | 0 | 5/0/1 | 0 | 11 | 5.1 |
| 5 | Determinant and matrix identities (`determinant_matrix`) | missing | 6 | 0 | 3/3/0 | 0 | 12 | 4.5 |
| 6 | Relation and function properties (`relation_function`) | missing | 5 | 0 | 3/1/1 | 0 | 12 | 3.6 |
| 7 | Complex-number identities (`complex_algebra`) | missing | 3 | 0 | 3/0/0 | 0 | 11 | 3.0 |
| 8 | Probability from axioms (`probability_atoms`) | missing | 3 | 0 | 3/0/0 | 0 | 12 | 3.0 |
| 9 | Mathematical induction (`induction`) | missing | 3 | 0 | 2/1/0 | 0 | 11 | 2.5 |
| 10 | Factorial and binomial-coefficient identities (`factorial_binomial`) | missing | 3 | 0 | 1/2/0 | 0 | 11 | 2.0 |
| 11 | Derivatives, implicit differentiation, first principles, ODE verification (`differentiation`) | implemented | 10 | 8 | 1/1/0 | 0 | 11, 12 | 1.5 |
| 12 | Relations under given conditions (`constrained_relation`) | implemented | 12 | 10 | 0/2/0 | 1 | 8, 9, 10 | 1.0 |
| 13 | Contradiction, irrationality and inequalities (`contradiction_inequality`) | partial | 5 | 2 | 0/0/3 | 1 | 9, 11 | 0.3 |
| 14 | Exact algebraic, index, log and surd identities (`algebraic_identity`) | implemented | 3 | 3 | 0/0/0 | 0 | 8, 9 | 0 |
| 15 | Definite integrals and areas (`definite_integration`) | implemented | 3 | 3 | 0/0/0 | 0 | 12 | 0 |
| 16 | Maxima/minima and monotonicity (`extremum_monotonicity`) | implemented | 5 | 5 | 0/0/0 | 0 | 12 | 0 |
| 17 | Inverse trigonometric identities (`inverse_trig_branch`) | implemented | 2 | 2 | 0/0/0 | 0 | 12 | 0 |
| 18 | Length/area relations proved by Pythagoras (`metric_geometry_coordinates`) | implemented | 4 | 4 | 0/0/0 | 0 | 9, 10 | 0 |
| 19 | Factor theorem, completing the square, discriminant (`polynomial_theorems`) | implemented | 3 | 3 | 0/0/0 | 0 | 10 | 0 |
| 20 | AP/GP term and sum relations (`sequence_series`) | implemented | 7 | 7 | 0/0/0 | 0 | 10, 11 | 0 |
| 21 | Trigonometric identities (`trig_identity`) | implemented | 8 | 8 | 0/0/0 | 0 | 10, 11 | 0 |

## Recommended build order

Phases group engines that share implementation work, so they differ from the per-engine score ranking.

| Phase | Name | Engines | Open | Score | Rationale |
|---:|---|---|---:|---:|---|
| 1 | Symbolic core | `constrained_relation`, `algebraic_identity`, `sequence_series`, `complex_algebra`, `metric_geometry_coordinates`, `analytic_coordinate`, `vector_algebra`, `determinant_matrix` | 27 | 22.0 | One shared piece of work (safe parser with log/sqrt/symbols/vectors, a generic hypotheses-and-goal spec, elimination and exact-zero checks) serves eight engines. Mostly high-feasibility text-only questions. |
| 2 | Calculus | `differentiation`, `extremum_monotonicity`, `definite_integration` | 2 | 1.5 | Reuses the phase 1 parser and spec; adds diff/limit/integrate with domain tracking. |
| 3 | Discrete and logic | `boolean_membership`, `probability_atoms`, `relation_function`, `induction`, `factorial_binomial` | 20 | 16.2 | Small, decidable checkers with high feasibility; independent of each other. |
| 4 | Trig extensions | `trig_identity`, `inverse_trig_branch`, `polynomial_theorems` | 0 | 0 | Extend existing code: constrained identities, special angles, branches, discriminant. |
| 5 | Synthetic geometry | `synthetic_geometry` | 19 | 7.9 | Largest group but highest cost per question: figure encoding, Newclid adapter gaps and school-style write-ups. Needs the interpretation stage for figures. |
| 6 | Open-ended | `contradiction_inequality` | 3 | 0.3 | Lowest automation yield; likely LLM-drafted with human review. |

## Engines

### Synthetic Euclidean proofs (congruence, circles, similarity, areas) (`synthetic_geometry`)

- Existing code: newclid_probe.py, mathcore/strategies/geometry.py (one question)
- Check: Newclid proof plus independent symbolic-coordinate check of the conclusion
- Gaps: Coordinate proofs cover lengths, midpoints, parallels, perpendiculars and areas. Not yet: angle equalities (bisectors), circles and arcs, congruence/similarity write-ups, constructions; Newclid has one reviewed encoding

| Question | Class | Feasibility | Status | Note |
|---|---:|---|---|---|
| PD-MATH-IX-001 | 9 | medium | SOLVED_AND_TRACE_CHECKED | Converse: rhombus from diagonals |
| PD-MATH-IX-002 | 9 | medium | UNSUPPORTED | Angle in semicircle |
| PD-MATH-IX-003 | 9 | medium | UNSUPPORTED | Figure; incentre concurrency |
| PD-MATH-IX-004 | 9 | medium | SOLVED_AND_TRACE_CHECKED | Midpoint theorem; coordinate check easy |
| PD-MATH-IX-006 | 9 | medium | SOLVED_AND_TRACE_CHECKED | Figure; auxiliary parallelogram |
| PD-MATH-IX-008 | 9 | medium | UNSUPPORTED | Figure; area equality |
| PD-MATH-IX-009 | 9 | medium | SOLVED_AND_TRACE_CHECKED | Figure; Varignon via midpoint theorem |
| PD-MATH-IX-012 | 9 | medium | UNSUPPORTED | Equal inscribed angles give equal arcs |
| PD-MATH-IX-016 | 9 | medium | UNSUPPORTED | Isosceles base angles and angle sum |
| PD-MATH-IX-017 | 9 | medium | UNSUPPORTED | Figure; trapezium midline |
| PD-MATH-IX-018 | 9 | low | UNSUPPORTED | Figure; chord distances from centre |
| PD-MATH-IX-019 | 9 | medium | SOLVED_AND_TRACE_CHECKED | Centroid area ratio; coordinate check easy |
| PD-MATH-IX-025 | 9 | medium | SOLVED_AND_TRACE_CHECKED | Midpoint theorem on trapezium |
| PD-MATH-VII-001 | 7 | medium | UNSUPPORTED | Figure; ASA with vertically opposite angles |
| PD-MATH-VII-002 | 7 | high | SOLVED_AND_TRACE_CHECKED | Solved: Newclid + coordinate replay |
| PD-MATH-VII-003 | 7 | medium | UNSUPPORTED | Figure; RHS congruence, three parts |
| PD-MATH-VIII-003 | 8 | medium | UNSUPPORTED | Figure; parallelogram angle bisectors |
| PD-MATH-VIII-004 | 8 | medium | UNSUPPORTED | Angle chasing only |
| PD-MATH-X-008 | 10 | medium | UNSUPPORTED | Figure; intersecting chords AP.PB = CP.PD |
| PD-MATH-X-012 | 10 | low | UNSUPPORTED | Construction with justification |
| PD-MATH-X-013 | 10 | medium | UNSUPPORTED | Figure; cyclic AA similarity then length |
| PD-MATH-X-014 | 10 | medium | UNSUPPORTED | Figure; tangent-chord AA similarity |
| PD-MATH-X-017 | 10 | low | SOLVED_AND_TRACE_CHECKED | Basic proportionality theorem from area ratios |
| PD-MATH-X-018 | 10 | medium | UNSUPPORTED | Radius perpendicular to tangent |
| PD-MATH-X-019 | 10 | medium | UNSUPPORTED | Quadrilateral angle sum |
| PD-MATH-X-025 | 10 | medium | SOLVED_AND_TRACE_CHECKED | RHS congruence |
| PD-MATH-X-027 | 10 | low | UNSUPPORTED | Similarity scale argument |
| PD-MATH-X-029 | 10 | low | UNSUPPORTED | Pythagoras theorem itself; checker must not assume it |

### Coordinate and 3D analytic geometry (`analytic_coordinate`)

- Existing code: ../coordinate_solver_generalisation_v2/engine_v1.py
- Check: Distance, section, area and line formulas with exact arithmetic
- Gaps: Not yet wired into this pipeline; symbolic-parameter coordinates

| Question | Class | Feasibility | Status | Note |
|---|---:|---|---|---|
| PD-MATH-IX-022 | 9 | high | UNSUPPORTED | Collinearity with symbolic a, b |
| PD-MATH-X-016 | 10 | high | UNSUPPORTED | Equidistant point with symbolic coordinates |
| PD-MATH-X-020 | 10 | high | UNSUPPORTED | Numeric triangle areas |
| PD-MATH-XI-012 | 11 | medium | UNSUPPORTED | Line through unit-circle points; half-angle |
| PD-MATH-XI-016 | 11 | medium | UNSUPPORTED | Focal perpendicular product |
| PD-MATH-XI-017 | 11 | high | UNSUPPORTED | Intercept form distance |
| PD-MATH-XI-027 | 11 | high | UNSUPPORTED | Symbolic centroid averaging |
| PD-MATH-XII-031 | 12 | high | UNSUPPORTED | Inconsistent parametric equations |

### Vector identities (`vector_algebra`)

- Existing code: none
- Check: Generic 3D components, dot/cross product identities
- Gaps: Either/or conclusions need case output

| Question | Class | Feasibility | Status | Note |
|---|---:|---|---|---|
| PD-MATH-XII-023 | 12 | high | UNSUPPORTED | Affine combination |
| PD-MATH-XII-024 | 12 | high | UNSUPPORTED | Squared norms |
| PD-MATH-XII-025 | 12 | high | UNSUPPORTED | Equal direction cosines |
| PD-MATH-XII-026 | 12 | high | UNSUPPORTED | Unit vectors; half angle |
| PD-MATH-XII-027 | 12 | medium | UNSUPPORTED | Sine rule via cross products |
| PD-MATH-XII-028 | 12 | medium | UNSUPPORTED | Either/or conclusion |
| PD-MATH-XII-029 | 12 | high | UNSUPPORTED | Scalar triple product |
| PD-MATH-XII-030 | 12 | medium | SOURCE_NEEDS_CORRECTION | Source issue: needs a x b != 0 |

### Set identities, logic and counterexamples (`boolean_membership`)

- Existing code: none
- Check: Per-element membership truth tables (decides these quantifier-free set statements); finite counterexample search
- Gaps: Power-set argument (XI-026) is not per-element

| Question | Class | Feasibility | Status | Note |
|---|---:|---|---|---|
| PD-MATH-XI-001 | 11 | high | UNSUPPORTED | Element chasing |
| PD-MATH-XI-007 | 11 | high | UNSUPPORTED | Per-element implication |
| PD-MATH-XI-014 | 11 | high | UNSUPPORTED | Per-element implication |
| PD-MATH-XI-021 | 11 | high | UNSUPPORTED | Truth table |
| PD-MATH-XI-026 | 11 | low | UNSUPPORTED | Power sets: needs singleton argument |
| PD-MATH-XI-031 | 11 | high | UNSUPPORTED | Finite counterexample |

### Determinant and matrix identities (`determinant_matrix`)

- Existing code: none
- Check: Symbolic determinant expansion and factor comparison; transpose algebra with noncommutative symbols
- Gaps: Students expect row/column operations, so the trace must record them

| Question | Class | Feasibility | Status | Note |
|---|---:|---|---|---|
| PD-MATH-XII-012 | 12 | high | UNSUPPORTED | Symmetric determinant factorisation |
| PD-MATH-XII-013 | 12 | high | UNSUPPORTED | Rank-one perturbation |
| PD-MATH-XII-014 | 12 | medium | UNSUPPORTED | GP terms; log column dependence |
| PD-MATH-XII-015 | 12 | medium | UNSUPPORTED | Vandermonde factor; distinct variables |
| PD-MATH-XII-040 | 12 | medium | UNSUPPORTED | Transpose algebra, noncommutative |
| PD-MATH-XII-041 | 12 | high | UNSUPPORTED | 2x2 symbolic with half-angle |

### Relation and function properties (`relation_function`)

- Existing code: none
- Check: Reflexive/symmetric/transitive by symbolic rewriting; injective/surjective by solving for preimages
- Gaps: Geometric relation XII-008 needs counterexample by construction

| Question | Class | Feasibility | Status | Note |
|---|---:|---|---|---|
| PD-MATH-XII-005 | 12 | high | UNSUPPORTED | Affine bijection |
| PD-MATH-XII-006 | 12 | medium | UNSUPPORTED | Invariant 1/a + 1/d = 1/b + 1/c |
| PD-MATH-XII-007 | 12 | high | UNSUPPORTED | Congruence mod 4 |
| PD-MATH-XII-008 | 12 | low | UNSUPPORTED | Lines in a plane; geometric counterexamples |
| PD-MATH-XII-009 | 12 | high | UNSUPPORTED | Rational bijection and inverse |

### Complex-number identities (`complex_algebra`)

- Existing code: none
- Check: Split into real/imaginary parts with real symbols; omega reduction via 1+w+w^2=0
- Gaps: None beyond parser

| Question | Class | Feasibility | Status | Note |
|---|---:|---|---|---|
| PD-MATH-XI-008 | 11 | high | UNSUPPORTED | Conjugate multiplication |
| PD-MATH-XI-019 | 11 | high | UNSUPPORTED | Expand (x + iy)^3 |
| PD-MATH-XI-022 | 11 | high | UNSUPPORTED | Omega reduction |

### Probability from axioms (`probability_atoms`)

- Existing code: none
- Check: Express events over Venn atoms with non-negative atom probabilities; linear/polynomial identity
- Gaps: Independence is a product constraint

| Question | Class | Feasibility | Status | Note |
|---|---:|---|---|---|
| PD-MATH-XII-037 | 12 | high | UNSUPPORTED | Complement independence |
| PD-MATH-XII-038 | 12 | high | UNSUPPORTED | Total probability |
| PD-MATH-XII-039 | 12 | high | UNSUPPORTED | Axiom bounds |

### Mathematical induction (`induction`)

- Existing code: none
- Check: Base case evaluation and symbolic step P(k) => P(k+1) (sum or divisibility quotient)
- Gaps: None beyond parser

| Question | Class | Feasibility | Status | Note |
|---|---:|---|---|---|
| PD-MATH-XI-018 | 11 | medium | UNSUPPORTED | Divisibility of a^n - b^n |
| PD-MATH-XI-028 | 11 | high | UNSUPPORTED | Telescoping rational sum |
| PD-MATH-XI-029 | 11 | high | UNSUPPORTED | Divisibility by 64 |

### Factorial and binomial-coefficient identities (`factorial_binomial`)

- Existing code: none
- Check: Symbolic factorial ratios and general-term exponent matching
- Gaps: Products like 1.3.5...(2n-1) need a double-factorial encoding

| Question | Class | Feasibility | Status | Note |
|---|---:|---|---|---|
| PD-MATH-XI-011 | 11 | medium | UNSUPPORTED | Odd products as double factorials |
| PD-MATH-XI-023 | 11 | medium | UNSUPPORTED | Matching general-term coefficients |
| PD-MATH-XI-024 | 11 | high | UNSUPPORTED | Consecutive coefficient ratios |

### Derivatives, implicit differentiation, first principles, ODE verification (`differentiation`)

- Existing code: mathcore/rules/calculus.py, mathcore/strategies/calculus.py (derivative_relation, evaluate, first_principles)
- Check: SymPy diff/limit and substitution back into the stated relation, with domain
- Gaps: Two curves at once (XII-020, orthogonal curves); first principles covers roots, products with trig and polynomials

| Question | Class | Feasibility | Status | Note |
|---|---:|---|---|---|
| PD-MATH-XI-015 | 11 | medium | SOLVED_AND_TRACE_CHECKED | First principles, product |
| PD-MATH-XI-020 | 11 | medium | SOLVED_AND_TRACE_CHECKED | First principles, rationalisation |
| PD-MATH-XII-001 | 12 | high | SOLVED_AND_TRACE_CHECKED | Implicit, second derivative |
| PD-MATH-XII-002 | 12 | high | SOLVED_AND_TRACE_CHECKED | Logarithmic differentiation, x > 0 |
| PD-MATH-XII-003 | 12 | high | SOLVED_AND_TRACE_CHECKED | Implicit differentiation |
| PD-MATH-XII-004 | 12 | high | SOLVED_AND_TRACE_CHECKED | Repeated differentiation |
| PD-MATH-XII-020 | 12 | high | UNSUPPORTED | Slopes at intersection |
| PD-MATH-XII-021 | 12 | high | SOLVED_AND_TRACE_CHECKED | Marginal and average cost |
| PD-MATH-XII-035 | 12 | high | SOLVED_AND_TRACE_CHECKED | Verify ODE solution with two constants |
| PD-MATH-XII-036 | 12 | medium | SOURCE_NEEDS_CORRECTION | Source issue: missing branches |

### Relations under given conditions (`constrained_relation`)

- Existing code: mathcore/strategies/identity.py (derive, conditional, difference, take_logs)
- Check: Eliminate hypotheses (substitution, Groebner basis or parametrisation) and reduce target to zero; record non-zero divisors
- Gaps: Inequality givens; componendo–dividendo is implemented as a prescribed method (X-009)

| Question | Class | Feasibility | Status | Note |
|---|---:|---|---|---|
| PD-MATH-IX-013 | 9 | high | SOLVED_AND_TRACE_CHECKED | Eliminate l, b, h |
| PD-MATH-IX-015 | 9 | high | SOLVED_AND_TRACE_CHECKED | abc = 1 substitution |
| PD-MATH-IX-021 | 9 | medium | INPUT_AMBIGUOUS | Source issue: the givens have no real solution with distinct a, b, c |
| PD-MATH-VIII-001 | 8 | high | SOLVED_AND_TRACE_CHECKED | Symmetric-function identity with numeric constraints; givens have no real solution (proved over complex numbers) |
| PD-MATH-VIII-002 | 8 | high | SOLVED_AND_TRACE_CHECKED | x + 1/x = 2 forces x = 1 |
| PD-MATH-X-003 | 10 | high | SOLVED_AND_TRACE_CHECKED | Continued proportion y = xk, z = xk^2 |
| PD-MATH-X-006 | 10 | medium | SOLVED_AND_TRACE_CHECKED | Equality case: (ay - bx)^2 = 0 over reals |
| PD-MATH-X-009 | 10 | medium | SOLVED_AND_TRACE_CHECKED | Componendo-dividendo prescribed; radicals |
| PD-MATH-X-010 | 10 | high | SOLVED_AND_TRACE_CHECKED | Cross multiplication |
| PD-MATH-X-011 | 10 | high | SOLVED_AND_TRACE_CHECKED | Mensuration formulas, equal surface area |
| PD-MATH-X-024 | 10 | medium | UNSUPPORTED | Figure; arc length plus trig lengths |
| PD-MATH-X-026 | 10 | high | SOLVED_AND_TRACE_CHECKED | Equilateral area formula on side and diagonal |

### Contradiction, irrationality and inequalities (`contradiction_inequality`)

- Existing code: mathcore/strategies/algebra_methods.py (one_real_roots, only_solution)
- Check: Case analysis and certified inequalities
- Gaps: Sum of discriminants and 'only real solution' are implemented; irrationality and triangle inequalities are not

| Question | Class | Feasibility | Status | Note |
|---|---:|---|---|---|
| PD-MATH-IX-010 | 9 | low | UNSUPPORTED | Irrationality of sqrt 2 then 3 - sqrt 2 |
| PD-MATH-IX-011 | 9 | low | UNSUPPORTED | Figure; repeated triangle inequality |
| PD-MATH-IX-023 | 9 | low | UNSUPPORTED | Triangle inequality in two triangles |
| PD-MATH-XI-025 | 11 | medium | SOLVED_AND_TRACE_CHECKED | Sum of discriminants >= 0 |
| PD-MATH-XI-030 | 11 | medium | SOLVED_AND_TRACE_CHECKED | x(x^2 + 8) = 0 over reals |

### Exact algebraic, index, log and surd identities (`algebraic_identity`)

- Existing code: mathcore/rules/indices_logs.py, mathcore/rules/algebra.py
- Check: Exact simplification of LHS - RHS with recorded domain (positivity for logs/indices)
- Gaps: Radical equations; nested surds

| Question | Class | Feasibility | Status | Note |
|---|---:|---|---|---|
| PD-MATH-IX-005 | 9 | high | SOLVED_AND_TRACE_CHECKED | Exact log identity |
| PD-MATH-IX-020 | 9 | high | SOLVED_AND_TRACE_CHECKED | Surd rationalisation, telescoping |
| PD-MATH-VIII-005 | 8 | high | SOLVED_AND_TRACE_CHECKED | Index laws |

### Definite integrals and areas (`definite_integration`)

- Existing code: mathcore/rules/calculus.py, mathcore/strategies/calculus.py (definite_integral)
- Check: Exact integration, reflection property, region bounds
- Gaps: Antiderivatives from school substitutions and SymPy's step-by-step integrator; integration by parts not yet

| Question | Class | Feasibility | Status | Note |
|---|---:|---|---|---|
| PD-MATH-XII-032 | 12 | medium | SOLVED_AND_TRACE_CHECKED | Reflection property then evaluation |
| PD-MATH-XII-033 | 12 | medium | SOLVED_AND_TRACE_CHECKED | Reflection symmetry |
| PD-MATH-XII-034 | 12 | medium | SOLVED_AND_TRACE_CHECKED | Region between two parabolas |

### Maxima/minima and monotonicity (`extremum_monotonicity`)

- Existing code: mathcore/strategies/calculus.py (monotonic, extremum)
- Check: Critical points, second-derivative or sign test on the stated domain
- Gaps: Exactly one critical point in the domain; closed-interval endpoint comparisons not yet

| Question | Class | Feasibility | Status | Note |
|---|---:|---|---|---|
| PD-MATH-XII-016 | 12 | medium | SOLVED_AND_TRACE_CHECKED | Cylinder in sphere |
| PD-MATH-XII-017 | 12 | medium | SOLVED_AND_TRACE_CHECKED | Fixed hypotenuse |
| PD-MATH-XII-018 | 12 | medium | SOLVED_AND_TRACE_CHECKED | Half cylinder fixed volume |
| PD-MATH-XII-019 | 12 | high | SOLVED_AND_TRACE_CHECKED | Derivative is a completed square plus positive |
| PD-MATH-XII-022 | 12 | high | SOLVED_AND_TRACE_CHECKED | MC' < 0 for x >= 0 |

### Inverse trigonometric identities (`inverse_trig_branch`)

- Existing code: mathcore/rules/inverse_trig.py
- Check: Principal-branch interval tracking, then exact tan/cos evaluation
- Gaps: Branch conditions are proved for numbers and for one variable on a stated interval; several variables not yet

| Question | Class | Feasibility | Status | Note |
|---|---:|---|---|---|
| PD-MATH-XII-010 | 12 | medium | SOLVED_AND_TRACE_CHECKED | Exact sum with branch control |
| PD-MATH-XII-011 | 12 | medium | SOLVED_AND_TRACE_CHECKED | Half-angle with x in (0, pi/4) |

### Length/area relations proved by Pythagoras (`metric_geometry_coordinates`)

- Existing code: mathcore/parse.py (points, dist2/dot/cross/area), mathcore/figure.py (figure facts checked), mathcore/render.py
- Check: Symbolic coordinates with right angle at origin; identity in squared lengths
- Gaps: Answers use coordinates, not Pythagoras on named triangles

| Question | Class | Feasibility | Status | Note |
|---|---:|---|---|---|
| PD-MATH-IX-007 | 9 | high | SOLVED_AND_TRACE_CHECKED | Right angle at B; squared lengths |
| PD-MATH-IX-014 | 9 | high | SOLVED_AND_TRACE_CHECKED | Right angle at Q; squared lengths |
| PD-MATH-IX-024 | 9 | high | SOLVED_AND_TRACE_CHECKED | British flag theorem |
| PD-MATH-X-028 | 10 | high | SOLVED_AND_TRACE_CHECKED | Auxiliary altitude, squared lengths |

### Factor theorem, completing the square, discriminant (`polynomial_theorems`)

- Existing code: mathcore/rules/polynomial.py, mathcore/strategies/polynomial.py, equal_roots givens
- Check: Remainder evaluation, expand-back, discriminant identity
- Gaps: Higher-degree factorisation beyond the factor theorem

| Question | Class | Feasibility | Status | Note |
|---|---:|---|---|---|
| PD-MATH-X-007 | 10 | high | SOLVED_AND_TRACE_CHECKED | Solved |
| PD-MATH-X-015 | 10 | high | SOLVED_AND_TRACE_CHECKED | Discriminant = 0 |
| PD-MATH-X-030 | 10 | high | SOLVED_AND_TRACE_CHECKED | Solved |

### AP/GP term and sum relations (`sequence_series`)

- Existing code: mathcore/rules/sequences.py (AP and GP), mathcore/strategies/values.py
- Check: Substitute general term/sum formulas and simplify the claimed relation
- Gaps: XI-006 is solved by naming the larger number first (b + d, d >= 0)

| Question | Class | Feasibility | Status | Note |
|---|---:|---|---|---|
| PD-MATH-X-021 | 10 | high | SOLVED_AND_TRACE_CHECKED | Solved |
| PD-MATH-X-022 | 10 | high | SOLVED_AND_TRACE_CHECKED | Solved |
| PD-MATH-X-023 | 10 | medium | SOLVED_AND_TRACE_CHECKED | Integer existence: x = 35 |
| PD-MATH-XI-005 | 11 | high | SOLVED_AND_TRACE_CHECKED | 'in AP' condition |
| PD-MATH-XI-006 | 11 | high | SOLVED_AND_TRACE_CHECKED | AM/GM to quadratic roots |
| PD-MATH-XI-009 | 11 | medium | SOLVED_AND_TRACE_CHECKED | GP converse via perfect square |
| PD-MATH-XI-013 | 11 | high | SOLVED_AND_TRACE_CHECKED | GP block sums |

### Trigonometric identities (`trig_identity`)

- Existing code: mathcore/rules/trig.py, mathcore/rules/trig_compound.py, mathcore/strategies/equations.py, mathcore/equality.py (angle basis)
- Check: Permitted-rule rewrite search, exact equality, domain replay
- Gaps: Special-angle products that need the multiply-by-2-sin trick (e.g. sin 20° sin 40° sin 60° sin 80°). General solutions are implemented (mathcore/strategies/general.py).

| Question | Class | Feasibility | Status | Note |
|---|---:|---|---|---|
| PD-MATH-X-001 | 10 | high | SOLVED_AND_TRACE_CHECKED | Solved |
| PD-MATH-X-002 | 10 | high | SOLVED_AND_TRACE_CHECKED | Solved |
| PD-MATH-X-004 | 10 | high | SOLVED_AND_TRACE_CHECKED | Solved |
| PD-MATH-X-005 | 10 | high | SOLVED_AND_TRACE_CHECKED | Solved |
| PD-MATH-XI-002 | 11 | medium | SOLVED_AND_TRACE_CHECKED | Constrained compound-angle identity |
| PD-MATH-XI-003 | 11 | medium | SOLVED_AND_TRACE_CHECKED | Special-angle product |
| PD-MATH-XI-004 | 11 | medium | SOLVED_AND_TRACE_CHECKED | Constrained sum-to-product |
| PD-MATH-XI-010 | 11 | medium | SOLVED_AND_TRACE_CHECKED | Telescoping tangent differences |

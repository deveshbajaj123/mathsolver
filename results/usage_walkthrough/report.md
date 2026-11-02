# Existing pipeline: actual trigonometry and geometry outputs

These two supported, already formalized examples run without LLM API calls. No LLM-only baseline was run, so a savings percentage, cost, or general coverage claim cannot be inferred. Original pipeline llm_calls/llm_tokens fields are literal zero values, not provider-reported telemetry.

The run below is fresh. Each stage lists the input, output, engine and whether an LLM was called. Earlier AI-assisted development and formalization are outside the runtime totals.

## Trigonometry — PD-MATH-X-001

Result: SOLVED_AND_TRACE_CHECKED. Fresh route time: 0.694 seconds.

### 1. Read the source

Engine: Python JSON reader. LLM call: no.

Reads the existing extracted bank; OCR/extraction and any earlier chat assistance are outside this run.

Input:

```json
{
  "question_id": "PD-MATH-X-001"
}
```

Output:

```json
{
  "question_text_original": "3. a) Prove the following Identity:\n\n$$(\\sin A + \\text{cosec } A)^2 + (\\cos A + \\text{sec } A)^2 = 5 + \\text{sec}^2 A \\text{ cosec}^2 A \\tag{3}$$",
  "figure_required": false
}
```

### 2. Load the saved formalization

Engine: Python parser. LLM call: no.

The saved input was transcribed and reviewed beforehand. This stage does not automatically understand new prose or figures.

Input:

```json
{
  "method": "rational_trig_identity",
  "lhs": "(sin(A)+csc(A))**2+(cos(A)+sec(A))**2",
  "rhs": "5+sec(A)**2*csc(A)**2",
  "input_note": "Transcribed from the displayed identity; cosec normalized to csc."
}
```

Output:

```json
{
  "lhs": "(sin(A) + csc(A))**2 + (cos(A) + sec(A))**2",
  "rhs": "csc(A)**2*sec(A)**2 + 5",
  "domain": [
    "C != 0",
    "S != 0"
  ],
  "notation": "S=sin(A), C=cos(A)"
}
```

### 3. Discover the proof

Engine: Bounded Python rule search using SymPy. LLM call: no.

A fresh local solver run produces these outputs. No LLM selects the steps during execution.

Input:

```json
{
  "lhs": "(sin(A) + csc(A))**2 + (cos(A) + sec(A))**2",
  "rhs": "csc(A)**2*sec(A)**2 + 5",
  "domain": [
    "C != 0",
    "S != 0"
  ],
  "notation": "S=sin(A), C=cos(A)"
}
```

Output:

```json
{
  "diagnostics": {
    "starting_side": "LHS",
    "states_explored": 26,
    "elapsed_seconds": 0.688,
    "trace_replayed": true
  },
  "derivation": [
    {
      "input": "(sin(A) + csc(A))**2 + (cos(A) + sec(A))**2",
      "output": "(sin(A) + 1/sin(A))**2 + (cos(A) + 1/cos(A))**2",
      "rule_id": "reciprocal_quotient",
      "reason": "Use the reciprocal and quotient identities."
    },
    {
      "input": "(sin(A) + 1/sin(A))**2 + (cos(A) + 1/cos(A))**2",
      "output": "sin(A)**2 + cos(A)**2 + 4 + cos(A)**(-2) + sin(A)**(-2)",
      "rule_id": "algebra_expand",
      "reason": "Expand algebraically."
    },
    {
      "input": "sin(A)**2 + cos(A)**2 + 4 + cos(A)**(-2) + sin(A)**(-2)",
      "output": "5 + cos(A)**(-2) + sin(A)**(-2)",
      "rule_id": "pythagorean_sum",
      "reason": "Use sin² A + cos² A = 1."
    },
    {
      "input": "5 + cos(A)**(-2) + sin(A)**(-2)",
      "output": "(5*sin(A)**2*cos(A)**2 + sin(A)**2 + cos(A)**2)/(sin(A)**2*cos(A)**2)",
      "rule_id": "algebra_factor",
      "reason": "Combine and factor the algebraic expression."
    },
    {
      "input": "(5*sin(A)**2*cos(A)**2 + sin(A)**2 + cos(A)**2)/(sin(A)**2*cos(A)**2)",
      "output": "(5*sin(A)**2*cos(A)**2 + 1)/(sin(A)**2*cos(A)**2)",
      "rule_id": "pythagorean_sum",
      "reason": "Use sin² A + cos² A = 1."
    },
    {
      "input": "(5*sin(A)**2*cos(A)**2 + 1)/(sin(A)**2*cos(A)**2)",
      "output": "csc(A)**2*sec(A)**2 + 5",
      "rule_id": "reciprocal_quotient_finish",
      "reason": "Use reciprocal/quotient identities and simplify to obtain the other side."
    }
  ]
}
```

### 4. Check the mathematics

Engine: SymPy and pipeline checks. LLM call: no.

Acceptance is limited to the checks listed here; formalization and school presentation have separate review status.

Input:

```json
{
  "lhs": "(sin(A) + csc(A))**2 + (cos(A) + sec(A))**2",
  "rhs": "csc(A)**2*sec(A)**2 + 5",
  "domain": [
    "C != 0",
    "S != 0"
  ],
  "notation": "S=sin(A), C=cos(A)"
}
```

Output:

```json
{
  "scope": "Search replays its permitted rules; the serialized trace is also checked for exact equality and domain safety.",
  "steps": [
    {
      "rule": "reciprocal_quotient",
      "exact_equality": true,
      "domain_safe": true,
      "pipeline_verification": {
        "passed": true,
        "checker": "exact_sympy_rule_replay"
      }
    },
    {
      "rule": "algebra_expand",
      "exact_equality": true,
      "domain_safe": true,
      "pipeline_verification": {
        "passed": true,
        "checker": "exact_sympy_rule_replay"
      }
    },
    {
      "rule": "pythagorean_sum",
      "exact_equality": true,
      "domain_safe": true,
      "pipeline_verification": {
        "passed": true,
        "checker": "exact_sympy_rule_replay"
      }
    },
    {
      "rule": "algebra_factor",
      "exact_equality": true,
      "domain_safe": true,
      "pipeline_verification": {
        "passed": true,
        "checker": "exact_sympy_rule_replay"
      }
    },
    {
      "rule": "pythagorean_sum",
      "exact_equality": true,
      "domain_safe": true,
      "pipeline_verification": {
        "passed": true,
        "checker": "exact_sympy_rule_replay"
      }
    },
    {
      "rule": "reciprocal_quotient_finish",
      "exact_equality": true,
      "domain_safe": true,
      "pipeline_verification": {
        "passed": true,
        "checker": "exact_sympy_rule_replay"
      }
    }
  ]
}
```

### 5. Render the student answer

Engine: Python render_answer template. LLM call: no.

This prose is assembled by code. In geometry the SAS explanation is a separate handwritten template, not a translation or automatic verification of the raw Newclid trace.

Input:

```json
[
  {
    "input": "(sin(A) + csc(A))**2 + (cos(A) + sec(A))**2",
    "output": "(sin(A) + 1/sin(A))**2 + (cos(A) + 1/cos(A))**2",
    "rule_id": "reciprocal_quotient",
    "supporting_premises": [
      "original expression"
    ],
    "relation": "equality",
    "required_assumptions": [
      "C != 0",
      "S != 0"
    ],
    "verification": {
      "passed": true,
      "checker": "exact_sympy_rule_replay"
    },
    "origin": "code_search",
    "reason": "Use the reciprocal and quotient identities.",
    "input_latex": "\\left(\\sin{\\left(A \\right)} + \\csc{\\left(A \\right)}\\right)^{2} + \\left(\\cos{\\left(A \\right)} + \\sec{\\left(A \\right)}\\right)^{2}",
    "output_latex": "\\left(\\sin{\\left(A \\right)} + \\frac{1}{\\sin{\\left(A \\right)}}\\right)^{2} + \\left(\\cos{\\left(A \\right)} + \\frac{1}{\\cos{\\left(A \\right)}}\\right)^{2}"
  },
  {
    "input": "(sin(A) + 1/sin(A))**2 + (cos(A) + 1/cos(A))**2",
    "output": "sin(A)**2 + cos(A)**2 + 4 + cos(A)**(-2) + sin(A)**(-2)",
    "rule_id": "algebra_expand",
    "supporting_premises": [
      "original expression"
    ],
    "relation": "equality",
    "required_assumptions": [
      "C != 0",
      "S != 0"
    ],
    "verification": {
      "passed": true,
      "checker": "exact_sympy_rule_replay"
    },
    "origin": "code_search",
    "reason": "Expand algebraically.",
    "input_latex": "\\left(\\sin{\\left(A \\right)} + \\frac{1}{\\sin{\\left(A \\right)}}\\right)^{2} + \\left(\\cos{\\left(A \\right)} + \\frac{1}{\\cos{\\left(A \\right)}}\\right)^{2}",
    "output_latex": "\\sin^{2}{\\left(A \\right)} + \\cos^{2}{\\left(A \\right)} + 4 + \\frac{1}{\\cos^{2}{\\left(A \\right)}} + \\frac{1}{\\sin^{2}{\\left(A \\right)}}"
  },
  {
    "input": "sin(A)**2 + cos(A)**2 + 4 + cos(A)**(-2) + sin(A)**(-2)",
    "output": "5 + cos(A)**(-2) + sin(A)**(-2)",
    "rule_id": "pythagorean_sum",
    "supporting_premises": [
      "trig identity"
    ],
    "relation": "equality",
    "required_assumptions": [
      "C != 0",
      "S != 0"
    ],
    "verification": {
      "passed": true,
      "checker": "exact_sympy_rule_replay"
    },
    "origin": "code_search",
    "reason": "Use sin² A + cos² A = 1.",
    "input_latex": "\\sin^{2}{\\left(A \\right)} + \\cos^{2}{\\left(A \\right)} + 4 + \\frac{1}{\\cos^{2}{\\left(A \\right)}} + \\frac{1}{\\sin^{2}{\\left(A \\right)}}",
    "output_latex": "5 + \\frac{1}{\\cos^{2}{\\left(A \\right)}} + \\frac{1}{\\sin^{2}{\\left(A \\right)}}"
  },
  {
    "input": "5 + cos(A)**(-2) + sin(A)**(-2)",
    "output": "(5*sin(A)**2*cos(A)**2 + sin(A)**2 + cos(A)**2)/(sin(A)**2*cos(A)**2)",
    "rule_id": "algebra_factor",
    "supporting_premises": [
      "original expression"
    ],
    "relation": "equality",
    "required_assumptions": [
      "C != 0",
      "S != 0"
    ],
    "verification": {
      "passed": true,
      "checker": "exact_sympy_rule_replay"
    },
    "origin": "code_search",
    "reason": "Combine and factor the algebraic expression.",
    "input_latex": "5 + \\frac{1}{\\cos^{2}{\\left(A \\right)}} + \\frac{1}{\\sin^{2}{\\left(A \\right)}}",
    "output_latex": "\\frac{5 \\sin^{2}{\\left(A \\right)} \\cos^{2}{\\left(A \\right)} + \\sin^{2}{\\left(A \\right)} + \\cos^{2}{\\left(A \\right)}}{\\sin^{2}{\\left(A \\right)} \\cos^{2}{\\left(A \\right)}}"
  },
  {
    "input": "(5*sin(A)**2*cos(A)**2 + sin(A)**2 + cos(A)**2)/(sin(A)**2*cos(A)**2)",
    "output": "(5*sin(A)**2*cos(A)**2 + 1)/(sin(A)**2*cos(A)**2)",
    "rule_id": "pythagorean_sum",
    "supporting_premises": [
      "trig identity"
    ],
    "relation": "equality",
    "required_assumptions": [
      "C != 0",
      "S != 0"
    ],
    "verification": {
      "passed": true,
      "checker": "exact_sympy_rule_replay"
    },
    "origin": "code_search",
    "reason": "Use sin² A + cos² A = 1.",
    "input_latex": "\\frac{5 \\sin^{2}{\\left(A \\right)} \\cos^{2}{\\left(A \\right)} + \\sin^{2}{\\left(A \\right)} + \\cos^{2}{\\left(A \\right)}}{\\sin^{2}{\\left(A \\right)} \\cos^{2}{\\left(A \\right)}}",
    "output_latex": "\\frac{5 \\sin^{2}{\\left(A \\right)} \\cos^{2}{\\left(A \\right)} + 1}{\\sin^{2}{\\left(A \\right)} \\cos^{2}{\\left(A \\right)}}"
  },
  {
    "input": "(5*sin(A)**2*cos(A)**2 + 1)/(sin(A)**2*cos(A)**2)",
    "output": "csc(A)**2*sec(A)**2 + 5",
    "rule_id": "reciprocal_quotient_finish",
    "supporting_premises": [
      "original expression"
    ],
    "relation": "equality",
    "required_assumptions": [
      "C != 0",
      "S != 0"
    ],
    "verification": {
      "passed": true,
      "checker": "exact_sympy_rule_replay"
    },
    "origin": "code_search",
    "reason": "Use reciprocal/quotient identities and simplify to obtain the other side.",
    "input_latex": "\\frac{5 \\sin^{2}{\\left(A \\right)} \\cos^{2}{\\left(A \\right)} + 1}{\\sin^{2}{\\left(A \\right)} \\cos^{2}{\\left(A \\right)}}",
    "output_latex": "\\csc^{2}{\\left(A \\right)} \\sec^{2}{\\left(A \\right)} + 5"
  }
]
```

Output:

## PD-MATH-X-001

3. a) Prove the following Identity:

$$(\sin A + \text{cosec } A)^2 + (\cos A + \text{sec } A)^2 = 5 + \text{sec}^2 A \text{ cosec}^2 A \tag{3}$$

**Solution**

Starting with the LHS:

$$\left(\sin{\left(A \right)} + \csc{\left(A \right)}\right)^{2} + \left(\cos{\left(A \right)} + \sec{\left(A \right)}\right)^{2}$$

$$= \left(\sin{\left(A \right)} + \frac{1}{\sin{\left(A \right)}}\right)^{2} + \left(\cos{\left(A \right)} + \frac{1}{\cos{\left(A \right)}}\right)^{2}$$

Use the reciprocal and quotient identities.

$$= \sin^{2}{\left(A \right)} + \cos^{2}{\left(A \right)} + 4 + \frac{1}{\cos^{2}{\left(A \right)}} + \frac{1}{\sin^{2}{\left(A \right)}}$$

Expand algebraically.

$$= 5 + \frac{1}{\cos^{2}{\left(A \right)}} + \frac{1}{\sin^{2}{\left(A \right)}}$$

Use sin² A + cos² A = 1.

$$= \frac{5 \sin^{2}{\left(A \right)} \cos^{2}{\left(A \right)} + \sin^{2}{\left(A \right)} + \cos^{2}{\left(A \right)}}{\sin^{2}{\left(A \right)} \cos^{2}{\left(A \right)}}$$

Combine and factor the algebraic expression.

$$= \frac{5 \sin^{2}{\left(A \right)} \cos^{2}{\left(A \right)} + 1}{\sin^{2}{\left(A \right)} \cos^{2}{\left(A \right)}}$$

Use sin² A + cos² A = 1.

$$= \csc^{2}{\left(A \right)} \sec^{2}{\left(A \right)} + 5$$

Use reciprocal/quotient identities and simplify to obtain the other side.

Hence the identity holds wherever both original sides are defined.


### 6. Show the LLM boundary

Engine: No LLM call. LLM call: no.

There is no actual before/after model response in this pipeline. Zero runtime API use excludes the AI used to build code, prepare inputs, or explain this walkthrough in chat.

Input:

```json
{
  "answer_available": true
}
```

Output:

```json
{
  "before_llm_call": {
    "available_input": "The checked proof and rendered answer above",
    "request_sent": null
  },
  "call": {
    "executed": false,
    "reason": "No LLM client or invocation exists on this route"
  },
  "after_llm_call": {
    "response": null,
    "answer_changed_by_llm": false
  },
  "runtime_api_usage": {
    "calls": 0,
    "input_tokens": 0,
    "output_tokens": 0
  },
  "baseline_llm_usage": null,
  "tokens_saved_vs_baseline": null
}
```

## Geometry — PD-MATH-VII-002

Result: SOLVED_AND_TRACE_CHECKED. Fresh route time: 5.177 seconds.

### 1. Read the source

Engine: Python JSON reader. LLM call: no.

Reads the existing extracted bank; OCR/extraction and any earlier chat assistance are outside this run.

Input:

```json
{
  "question_id": "PD-MATH-VII-002"
}
```

Output:

```json
{
  "question_text_original": "20.\n\nIn the given diagram, $\\triangle PQR$ is an isosceles triangle. S and T are the midpoints of PQ and PR respectively. Prove that $RS = QT$.",
  "figure_required": true
}
```

### 2. Load the saved formalization

Engine: Python parser. LLM call: no.

The saved input was transcribed and reviewed beforehand. This stage does not automatically understand new prose or figures.

Input:

```json
{
  "method": "isosceles_midpoint_geometry",
  "figure_asset_id": "IMG-1c994300cc53caa15324",
  "jgex_input": "p q r = iso_triangle0 p q r; s = midpoint s p q; t = midpoint t p r ? cong r s q t",
  "input_note": "Original statement and figure checked; only givens and goal encoded."
}
```

Output:

```json
{
  "jgex_input": "p q r = iso_triangle0 p q r; s = midpoint s p q; t = midpoint t p r ? cong r s q t",
  "figure_asset_id": "IMG-1c994300cc53caa15324",
  "givens": [
    "PQ = PR",
    "S is midpoint of PQ",
    "T is midpoint of PR"
  ],
  "goal": "RS = QT"
}
```

### 3. Discover the proof

Engine: Newclid Python interface + Yuclid C++ proof engine. LLM call: no.

A fresh local solver run produces these outputs. No LLM selects the steps during execution.

Input:

```json
{
  "jgex_input": "p q r = iso_triangle0 p q r; s = midpoint s p q; t = midpoint t p r ? cong r s q t",
  "figure_asset_id": "IMG-1c994300cc53caa15324",
  "givens": [
    "PQ = PR",
    "S is midpoint of PQ",
    "T is midpoint of PR"
  ],
  "goal": "RS = QT"
}
```

Output:

# Problem setup:

## Points

- P(-1.8396, 0.9941)
- Q(-0.2450, -1.4926)
- R(0.9556, 0.0385)
- S(-1.0423, -0.2493)
- T(-0.4420, 0.5163)

## Assumptions:

[C0] : PQ = PR
[C1] : S is the midpoint of PQ
[C2] : T is the midpoint of PR

## Numerical checks

[N0] : ▲QST has the same orientation as ▲RST
[N1] : P ≠ Q
[N2] : P ≠ S
[N3] : Q ≠ S
[N4] : P ≠ R
[N5] : P ≠ T
[N6] : R ≠ T


# Goals

QT = RS : Proved [14]


# Proof:

000. | S is the midpoint of PQ [C1] =(r51 Midpoint splits in two)> PQ:PS = 2/1 [0]
001. | T is the midpoint of PR [C2] =(r51 Midpoint splits in two)> PR:PT = 2/1 [1]
002. | PQ = PR [C0], PQ:PS = 2/1 [0], PR:PT = 2/1 [1] =(AR Deduction)> PT = PS [2]
003. | PT = PS [2] =(r13 Isosceles triangle equal angles)> ∠(PS,ST) = ∠(ST,PT) [3]
004. | S is the midpoint of PQ [C1] =(r56 Properties of midpoint (coll))> P, Q, S are collinear [4]
005. | P, Q, S are collinear [4], P ≠ Q [N1], P ≠ S [N2], Q ≠ S [N3] =(r82 Parallel from collinear)> QS ∥ PS [5]
006. | T is the midpoint of PR [C2] =(r56 Properties of midpoint (coll))> P, R, T are collinear [6]
007. | P, R, T are collinear [6], P ≠ R [N4], P ≠ T [N5], R ≠ T [N6] =(r82 Parallel from collinear)> RT ∥ PT [7]
008. | ∠(PS,ST) = ∠(ST,PT) [3], QS ∥ PS [5], RT ∥ PT [7] =(AR Deduction)> ∠(QS,ST) = ∠(ST,RT) [8]
009. | S is the midpoint of PQ [C1] =(r51 Midpoint splits in two)> PQ:QS = 2/1 [9]
010. | T is the midpoint of PR [C2] =(r51 Midpoint splits in two)> PR:RT = 2/1 [10]
011. | PQ = PR [C0], PQ:QS = 2/1 [9], PR:RT = 2/1 [10] =(AR Deduction)> QS:RT = ST:ST [11]
012. | ∠(QS,ST) = ∠(ST,RT) [8], QS:RT = ST:ST [11], ▲QST has the same orientation as ▲RST [N0] =(r63 SAS Similarity of triangles (Reverse))> ▲QST ≅ ▲RTS [12]
013. | ▲QST has the same orientation as ▲RST [N0], ▲QST ≅ ▲RTS [12] =(r53 Properties of similar triangles (Reverse))> QT:RS = ST:ST [13]
014. | QT:RS = ST:ST [13] =(AR Deduction)> QT = RS [14]


# Appendix: AR deductions:



002. | Ratio Chasing to prove PT = PS:
| Premise PQ = PR gives a linear equation with coefficients {PQ²: 1, PR²: -1}
| Premise PQ:PS = 2/1 gives a linear equation with coefficients {PQ²: 1, PS²: -1}
| Then {PQ²: 1, PR²: -1} + -1 x {PQ²: 1, PS²: -1}
|    = {PR²: -1, PS²: 1}
| Premise PR:PT = 2/1 gives a linear equation with coefficients {PR²: 1, PT²: -1}
| Then {PR²: -1, PS²: 1} + 1 x {PR²: 1, PT²: -1}
|    = {PS²: 1, PT²: -1}
We are left with a linear equation with coefficients {PS²: 1, PT²: -1} that gives PT = PS



008. | Angle Chasing to prove ∠(QS,ST) = ∠(ST,RT):
| Premise ∠(PS,ST) = ∠(ST,PT) gives a linear equation with coefficients {Âˆ PS: -1, Âˆ PT: -1, Âˆ ST: 2}
| Premise QS ∥ PS gives a linear equation with coefficients {Âˆ PS: 1, Âˆ QS: -1}
| Then {Âˆ PS: -1, Âˆ PT: -1, Âˆ ST: 2} + 1 x {Âˆ PS: 1, Âˆ QS: -1}
|    = {Âˆ PT: -1, Âˆ ST: 2, Âˆ QS: -1}
| Premise RT ∥ PT gives a linear equation with coefficients {Âˆ PT: 1, Âˆ RT: -1}
| Then {Âˆ PT: -1, Âˆ ST: 2, Âˆ QS: -1} + 1 x {Âˆ PT: 1, Âˆ RT: -1}
|    = {Âˆ ST: 2, Âˆ QS: -1, Âˆ RT: -1}
We are left with a linear equation with coefficients {Âˆ ST: 2, Âˆ QS: -1, Âˆ RT: -1} that gives ∠(QS,ST) = ∠(ST,RT)



011. | Ratio Chasing to prove QS:RT = ST:ST:
| Premise PQ = PR gives a linear equation with coefficients {PQ²: 1, PR²: -1}
| Premise PQ:QS = 2/1 gives a linear equation with coefficients {PQ²: 1, QS²: -1}
| Then {PQ²: 1, PR²: -1} + -1 x {PQ²: 1, QS²: -1}
|    = {PR²: -1, QS²: 1}
| Premise PR:RT = 2/1 gives a linear equation with coefficients {PR²: 1, RT²: -1}
| Then {PR²: -1, QS²: 1} + 1 x {PR²: 1, RT²: -1}
|    = {QS²: 1, RT²: -1}
We are left with a linear equation with coefficients {QS²: 1, RT²: -1} that gives QS:RT = ST:ST



014. | Ratio Chasing to prove QT = RS:
| Premise QT:RS = ST:ST gives a linear equation with coefficients {QT²: 1, RS²: -1}
We are left with a linear equation with coefficients {QT²: 1, RS²: -1} that gives QT = RS

End of proof.

### 4. Check the mathematics

Engine: SymPy and pipeline checks. LLM call: no.

Acceptance is limited to the checks listed here; formalization and school presentation have separate review status.

Input:

```json
{
  "jgex_input": "p q r = iso_triangle0 p q r; s = midpoint s p q; t = midpoint t p r ? cong r s q t",
  "figure_asset_id": "IMG-1c994300cc53caa15324",
  "givens": [
    "PQ = PR",
    "S is midpoint of PQ",
    "T is midpoint of PR"
  ],
  "goal": "RS = QT"
}
```

Output:

```json
{
  "figure_sha256_verified": true,
  "figure_review": "visually_checked_against_bank_figure",
  "proof_inputs_and_goal_checked": true,
  "independent_replay": {
    "passed": true,
    "checks": {
      "PS_squared_is_PQ_squared_over_4": true,
      "PT_squared_is_PR_squared_over_4": true,
      "RS_QT_squared_difference_follows_equal_sides": true
    },
    "reason": "For midpoints S=Q/2 and T=R/2, RS²−QT²=3(PR²−PQ²)/4=0; segment lengths are nonnegative."
  },
  "symbolic_working": {
    "coordinate_input": {
      "P": "(0,0)",
      "Q": "(qx,qy)",
      "R": "(rx,ry)",
      "S": "(qx/2,qy/2)",
      "T": "(rx/2,ry/2)"
    },
    "RS_squared": "qx**2/4 - qx*rx + qy**2/4 - qy*ry + rx**2 + ry**2",
    "QT_squared": "qx**2 - qx*rx + qy**2 - qy*ry + rx**2/4 + ry**2/4",
    "difference": "-3*qx**2/4 - 3*qy**2/4 + 3*rx**2/4 + 3*ry**2/4",
    "identity_residual": "0",
    "given": "PR = PQ, hence PR^2 - PQ^2 = 0",
    "conclusion": "RS^2 = QT^2; nonnegative lengths imply RS = QT",
    "scope": "Checks this encoded conclusion independently; does not replay Yuclid's individual deductions or validate rendered SAS prose."
  }
}
```

### 5. Render the student answer

Engine: Python render_answer template. LLM call: no.

This prose is assembled by code. In geometry the SAS explanation is a separate handwritten template, not a translation or automatic verification of the raw Newclid trace.

Input:

```json
[
  {
    "input": "S is midpoint of PQ",
    "output": "PS² = PQ²/4",
    "rule_id": "midpoint_S",
    "supporting_premises": [
      "S is midpoint of PQ"
    ],
    "relation": "equality",
    "required_assumptions": [],
    "verification": {
      "passed": true,
      "checker": "exact_symbolic_coordinate_replay"
    },
    "origin": "newclid_proof_plus_independent_replay",
    "reason": "S lies halfway from P to Q.",
    "input_latex": null,
    "output_latex": null
  },
  {
    "input": "T is midpoint of PR",
    "output": "PT² = PR²/4",
    "rule_id": "midpoint_T",
    "supporting_premises": [
      "T is midpoint of PR"
    ],
    "relation": "equality",
    "required_assumptions": [],
    "verification": {
      "passed": true,
      "checker": "exact_symbolic_coordinate_replay"
    },
    "origin": "newclid_proof_plus_independent_replay",
    "reason": "T lies halfway from P to R.",
    "input_latex": null,
    "output_latex": null
  },
  {
    "input": "RS² - QT²",
    "output": "3(PR² - PQ²)/4",
    "rule_id": "midpoint_distance_identity",
    "supporting_premises": [
      "S is midpoint of PQ",
      "T is midpoint of PR"
    ],
    "relation": "equality",
    "required_assumptions": [],
    "verification": {
      "passed": true,
      "checker": "exact_symbolic_coordinate_replay"
    },
    "origin": "newclid_proof_plus_independent_replay",
    "reason": "Expand both squared distances using the midpoint coordinates.",
    "input_latex": null,
    "output_latex": null
  },
  {
    "input": "PR = PQ",
    "output": "RS = QT",
    "rule_id": "equal_sides_nonnegative_lengths",
    "supporting_premises": [
      "PR = PQ",
      "RS² - QT² = 3(PR² - PQ²)/4"
    ],
    "relation": "equality",
    "required_assumptions": [],
    "verification": {
      "passed": true,
      "checker": "exact_symbolic_coordinate_replay"
    },
    "origin": "newclid_proof_plus_independent_replay",
    "reason": "Equal original sides make the squared-distance difference zero; both lengths are nonnegative.",
    "input_latex": null,
    "output_latex": null
  }
]
```

Output:

## PD-MATH-VII-002

20.

In the given diagram, $\triangle PQR$ is an isosceles triangle. S and T are the midpoints of PQ and PR respectively. Prove that $RS = QT$.

**Solution**

Since $S$ and $T$ are midpoints, $PS=\tfrac12 PQ$ and $PT=\tfrac12 PR$. The isosceles condition $PQ=PR$ therefore gives $PS=PT$.

Also, $\angle RPS=\angle QPT$: both are the angle at $P$ between $PQ$ and $PR$.

Thus $\triangle PRS\cong\triangle PQT$ by SAS, with $PR=PQ$, $PS=PT$, and equal included angles. Corresponding sides give $RS=QT$.


### 6. Show the LLM boundary

Engine: No LLM call. LLM call: no.

There is no actual before/after model response in this pipeline. Zero runtime API use excludes the AI used to build code, prepare inputs, or explain this walkthrough in chat.

Input:

```json
{
  "answer_available": true
}
```

Output:

```json
{
  "before_llm_call": {
    "available_input": "The checked proof and rendered answer above",
    "request_sent": null
  },
  "call": {
    "executed": false,
    "reason": "No LLM client or invocation exists on this route"
  },
  "after_llm_call": {
    "response": null,
    "answer_changed_by_llm": false
  },
  "runtime_api_usage": {
    "calls": 0,
    "input_tokens": 0,
    "output_tokens": 0
  },
  "baseline_llm_usage": null,
  "tokens_saved_vs_baseline": null
}
```

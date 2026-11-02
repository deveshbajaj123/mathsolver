# Transfer test: five trigonometry and five geometry questions

This is a small, purposive test, not a random accuracy estimate. All ten are new to the saved production formalizations. Inputs were transcribed in this chat. No solver, rule library, production formalization or checker was changed to make these cases pass.

Trigonometry uses the existing reusable route with new inputs. Geometry tests the Newclid engine directly using supplied predicates; the production geometry adapter remains limited to its original question. Numerical diagrams guide matching and do not prove a universal statement.

Trigonometry checked: 3/5. Geometry engine proved: 3/5. New geometry cases independently checked by existing code: 0/5. Production results are not changed.

| Case | Result | Seconds |
|---|---|---|
| T1 | SOLVED_AND_TRACE_CHECKED | 2.129 |
| T2 | SOLVED_AND_TRACE_CHECKED | 2.438 |
| T3 | SOLVED_AND_TRACE_CHECKED | 1.601 |
| T4 | INCONCLUSIVE | 2.601 |
| T5 | UNSUPPORTED | 2.019 |
| G1 | ENGINE_PROVED_PENDING_INDEPENDENT_CHECK | 12.871 |
| G2 | ENGINE_PROVED_PENDING_INDEPENDENT_CHECK | 9.223 |
| G3 | ENGINE_PROVED_PENDING_INDEPENDENT_CHECK | 11.999 |
| G4 | ERROR | 10.169 |
| G5 | ERROR | 9.05 |
| N1 | COUNTEREXAMPLE | 1.643 |
| N2 | ERROR | 11.067 |

## T1: Sum of tangent and cotangent

Exact input:

```json
{
  "id": "T1",
  "lhs": "tan(A)+cot(A)",
  "rhs": "sec(A)*csc(A)",
  "description": "Sum of tangent and cotangent"
}
```

Output:

```json
{
  "id": "T1",
  "description": "Sum of tangent and cotangent",
  "llm_api_calls": 0,
  "llm_api_tokens": 0,
  "counted_in_production_metrics": false,
  "status": "SOLVED_AND_TRACE_CHECKED",
  "trace": [
    {
      "input": "tan(A) + cot(A)",
      "output": "sin(A)/cos(A) + cos(A)/sin(A)",
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
      "input_latex": "\\tan{\\left(A \\right)} + \\cot{\\left(A \\right)}",
      "output_latex": "\\frac{\\sin{\\left(A \\right)}}{\\cos{\\left(A \\right)}} + \\frac{\\cos{\\left(A \\right)}}{\\sin{\\left(A \\right)}}"
    },
    {
      "input": "sin(A)/cos(A) + cos(A)/sin(A)",
      "output": "(sin(A)**2 + cos(A)**2)/(sin(A)*cos(A))",
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
      "input_latex": "\\frac{\\sin{\\left(A \\right)}}{\\cos{\\left(A \\right)}} + \\frac{\\cos{\\left(A \\right)}}{\\sin{\\left(A \\right)}}",
      "output_latex": "\\frac{\\sin^{2}{\\left(A \\right)} + \\cos^{2}{\\left(A \\right)}}{\\sin{\\left(A \\right)} \\cos{\\left(A \\right)}}"
    },
    {
      "input": "(sin(A)**2 + cos(A)**2)/(sin(A)*cos(A))",
      "output": "1/(sin(A)*cos(A))",
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
      "input_latex": "\\frac{\\sin^{2}{\\left(A \\right)} + \\cos^{2}{\\left(A \\right)}}{\\sin{\\left(A \\right)} \\cos{\\left(A \\right)}}",
      "output_latex": "\\frac{1}{\\sin{\\left(A \\right)} \\cos{\\left(A \\right)}}"
    },
    {
      "input": "1/(sin(A)*cos(A))",
      "output": "csc(A)*sec(A)",
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
      "input_latex": "\\frac{1}{\\sin{\\left(A \\right)} \\cos{\\left(A \\right)}}",
      "output_latex": "\\csc{\\left(A \\right)} \\sec{\\left(A \\right)}"
    }
  ],
  "diagnostics": {
    "starting_side": "LHS",
    "states_explored": 6,
    "elapsed_seconds": 0.141,
    "trace_replayed": true
  },
  "domain_conditions": [
    "C",
    "S"
  ],
  "independently_checked": true,
  "seconds": 2.129
}
```

## T1

tan(A)+cot(A) = sec(A)*csc(A)

**Solution**

Starting with the LHS:

$$\tan{\left(A \right)} + \cot{\left(A \right)}$$

$$= \frac{\sin{\left(A \right)}}{\cos{\left(A \right)}} + \frac{\cos{\left(A \right)}}{\sin{\left(A \right)}}$$

Use the reciprocal and quotient identities.

$$= \frac{\sin^{2}{\left(A \right)} + \cos^{2}{\left(A \right)}}{\sin{\left(A \right)} \cos{\left(A \right)}}$$

Combine and factor the algebraic expression.

$$= \frac{1}{\sin{\left(A \right)} \cos{\left(A \right)}}$$

Use sin² A + cos² A = 1.

$$= \csc{\left(A \right)} \sec{\left(A \right)}$$

Use reciprocal/quotient identities and simplify to obtain the other side.

Hence the identity holds wherever both original sides are defined.



## T2: Product of conjugate expressions

Exact input:

```json
{
  "id": "T2",
  "lhs": "(sec(A)+tan(A))*(sec(A)-tan(A))",
  "rhs": "1",
  "description": "Product of conjugate expressions"
}
```

Output:

```json
{
  "id": "T2",
  "description": "Product of conjugate expressions",
  "llm_api_calls": 0,
  "llm_api_tokens": 0,
  "counted_in_production_metrics": false,
  "status": "SOLVED_AND_TRACE_CHECKED",
  "trace": [
    {
      "input": "(-tan(A) + sec(A))*(tan(A) + sec(A))",
      "output": "-tan(A)**2 + sec(A)**2",
      "rule_id": "algebra_expand",
      "supporting_premises": [
        "original expression"
      ],
      "relation": "equality",
      "required_assumptions": [
        "C != 0"
      ],
      "verification": {
        "passed": true,
        "checker": "exact_sympy_rule_replay"
      },
      "origin": "code_search",
      "reason": "Expand algebraically.",
      "input_latex": "\\left(- \\tan{\\left(A \\right)} + \\sec{\\left(A \\right)}\\right) \\left(\\tan{\\left(A \\right)} + \\sec{\\left(A \\right)}\\right)",
      "output_latex": "- \\tan^{2}{\\left(A \\right)} + \\sec^{2}{\\left(A \\right)}"
    },
    {
      "input": "-tan(A)**2 + sec(A)**2",
      "output": "1",
      "rule_id": "secant_identity",
      "supporting_premises": [
        "original expression"
      ],
      "relation": "equality",
      "required_assumptions": [
        "C != 0"
      ],
      "verification": {
        "passed": true,
        "checker": "exact_sympy_rule_replay"
      },
      "origin": "code_search",
      "reason": "Use sec² A = 1 + tan² A.",
      "input_latex": "- \\tan^{2}{\\left(A \\right)} + \\sec^{2}{\\left(A \\right)}",
      "output_latex": "1"
    }
  ],
  "diagnostics": {
    "starting_side": "LHS",
    "states_explored": 4,
    "elapsed_seconds": 0.11,
    "trace_replayed": true
  },
  "domain_conditions": [
    "C"
  ],
  "independently_checked": true,
  "seconds": 2.438
}
```

## T2

(sec(A)+tan(A))*(sec(A)-tan(A)) = 1

**Solution**

Starting with the LHS:

$$\left(- \tan{\left(A \right)} + \sec{\left(A \right)}\right) \left(\tan{\left(A \right)} + \sec{\left(A \right)}\right)$$

$$= - \tan^{2}{\left(A \right)} + \sec^{2}{\left(A \right)}$$

Expand algebraically.

$$= 1$$

Use sec² A = 1 + tan² A.

Hence the identity holds wherever both original sides are defined.



## T3: Difference of fourth powers

Exact input:

```json
{
  "id": "T3",
  "lhs": "sin(A)**4-cos(A)**4",
  "rhs": "sin(A)**2-cos(A)**2",
  "description": "Difference of fourth powers"
}
```

Output:

```json
{
  "id": "T3",
  "description": "Difference of fourth powers",
  "llm_api_calls": 0,
  "llm_api_tokens": 0,
  "counted_in_production_metrics": false,
  "status": "SOLVED_AND_TRACE_CHECKED",
  "trace": [
    {
      "input": "sin(A)**4 - cos(A)**4",
      "output": "(sin(A) - cos(A))*(sin(A) + cos(A))*(sin(A)**2 + cos(A)**2)",
      "rule_id": "algebra_factor",
      "supporting_premises": [
        "original expression"
      ],
      "relation": "equality",
      "required_assumptions": [],
      "verification": {
        "passed": true,
        "checker": "exact_sympy_rule_replay"
      },
      "origin": "code_search",
      "reason": "Combine and factor the algebraic expression.",
      "input_latex": "\\sin^{4}{\\left(A \\right)} - \\cos^{4}{\\left(A \\right)}",
      "output_latex": "\\left(\\sin{\\left(A \\right)} - \\cos{\\left(A \\right)}\\right) \\left(\\sin{\\left(A \\right)} + \\cos{\\left(A \\right)}\\right) \\left(\\sin^{2}{\\left(A \\right)} + \\cos^{2}{\\left(A \\right)}\\right)"
    },
    {
      "input": "(sin(A) - cos(A))*(sin(A) + cos(A))*(sin(A)**2 + cos(A)**2)",
      "output": "(sin(A) - cos(A))*(sin(A) + cos(A))",
      "rule_id": "pythagorean_sum",
      "supporting_premises": [
        "trig identity"
      ],
      "relation": "equality",
      "required_assumptions": [],
      "verification": {
        "passed": true,
        "checker": "exact_sympy_rule_replay"
      },
      "origin": "code_search",
      "reason": "Use sin² A + cos² A = 1.",
      "input_latex": "\\left(\\sin{\\left(A \\right)} - \\cos{\\left(A \\right)}\\right) \\left(\\sin{\\left(A \\right)} + \\cos{\\left(A \\right)}\\right) \\left(\\sin^{2}{\\left(A \\right)} + \\cos^{2}{\\left(A \\right)}\\right)",
      "output_latex": "\\left(\\sin{\\left(A \\right)} - \\cos{\\left(A \\right)}\\right) \\left(\\sin{\\left(A \\right)} + \\cos{\\left(A \\right)}\\right)"
    },
    {
      "input": "(sin(A) - cos(A))*(sin(A) + cos(A))",
      "output": "sin(A)**2 - cos(A)**2",
      "rule_id": "algebra_finish",
      "supporting_premises": [
        "original expression"
      ],
      "relation": "equality",
      "required_assumptions": [],
      "verification": {
        "passed": true,
        "checker": "exact_sympy_rule_replay"
      },
      "origin": "code_search",
      "reason": "Simplify algebraically to obtain the other side.",
      "input_latex": "\\left(\\sin{\\left(A \\right)} - \\cos{\\left(A \\right)}\\right) \\left(\\sin{\\left(A \\right)} + \\cos{\\left(A \\right)}\\right)",
      "output_latex": "\\sin^{2}{\\left(A \\right)} - \\cos^{2}{\\left(A \\right)}"
    }
  ],
  "diagnostics": {
    "starting_side": "LHS",
    "states_explored": 11,
    "elapsed_seconds": 0.25,
    "trace_replayed": true
  },
  "domain_conditions": [],
  "independently_checked": true,
  "seconds": 1.601
}
```

## T3

sin(A)**4-cos(A)**4 = sin(A)**2-cos(A)**2

**Solution**

Starting with the LHS:

$$\sin^{4}{\left(A \right)} - \cos^{4}{\left(A \right)}$$

$$= \left(\sin{\left(A \right)} - \cos{\left(A \right)}\right) \left(\sin{\left(A \right)} + \cos{\left(A \right)}\right) \left(\sin^{2}{\left(A \right)} + \cos^{2}{\left(A \right)}\right)$$

Combine and factor the algebraic expression.

$$= \left(\sin{\left(A \right)} - \cos{\left(A \right)}\right) \left(\sin{\left(A \right)} + \cos{\left(A \right)}\right)$$

Use sin² A + cos² A = 1.

$$= \sin^{2}{\left(A \right)} - \cos^{2}{\left(A \right)}$$

Simplify algebraically to obtain the other side.

Hence the identity holds wherever both original sides are defined.



## T4: Rational identity with original domain restrictions

Exact input:

```json
{
  "id": "T4",
  "lhs": "(1-cos(A))/(1+cos(A))",
  "rhs": "(csc(A)-cot(A))**2",
  "description": "Rational identity with original domain restrictions"
}
```

Output:

```json
{
  "id": "T4",
  "description": "Rational identity with original domain restrictions",
  "llm_api_calls": 0,
  "llm_api_tokens": 0,
  "counted_in_production_metrics": false,
  "status": "INCONCLUSIVE",
  "trace": [],
  "diagnostics": {
    "states_explored": 21,
    "reason": "Search budget exhausted; no approved derivation found.",
    "elapsed_seconds": 0.797
  },
  "domain_conditions": [],
  "independently_checked": false,
  "seconds": 2.601
}
```


## T5: Double-angle identity outside the documented single-angle grammar

Exact input:

```json
{
  "id": "T5",
  "lhs": "sin(2*A)",
  "rhs": "2*sin(A)*cos(A)",
  "description": "Double-angle identity outside the documented single-angle grammar"
}
```

Output:

```json
{
  "id": "T5",
  "description": "Double-angle identity outside the documented single-angle grammar",
  "llm_api_calls": 0,
  "llm_api_tokens": 0,
  "counted_in_production_metrics": false,
  "status": "UNSUPPORTED",
  "trace": [],
  "diagnostics": {
    "reason": "Only rational trig expressions of one angle are supported."
  },
  "domain_conditions": [],
  "independently_checked": false,
  "seconds": 2.019
}
```


## G1: Perpendicular diagonals bisecting each other imply a rhombus

28. Show that if the diagonals of a quadrilateral bisect each other at right angles, then it is a rhombus.

Exact input:

```json
{
  "id": "G1",
  "bank_id": "PD-MATH-IX-001",
  "description": "Perpendicular diagonals bisecting each other imply a rhombus",
  "points": {
    "a": [
      3.7,
      0
    ],
    "b": [
      0,
      2.3
    ],
    "c": [
      -3.7,
      0
    ],
    "d": [
      0,
      -2.3
    ],
    "o": [
      0,
      0
    ]
  },
  "assumptions": [
    "midp o a c",
    "midp o b d",
    "perp a c b d"
  ],
  "goals": [
    "cong a b b c",
    "cong b c c d",
    "cong c d d a"
  ],
  "translation": "Rhombus conclusion expanded to four equal sides; coordinates are a matching diagram, not proof premises."
}
```

Output:

```json
{
  "id": "G1",
  "description": "Perpendicular diagonals bisecting each other imply a rhombus",
  "llm_api_calls": 0,
  "llm_api_tokens": 0,
  "counted_in_production_metrics": false,
  "stage": "write_proof",
  "status": "ENGINE_PROVED_PENDING_INDEPENDENT_CHECK",
  "solver_goal_checked": true,
  "run_infos": {
    "runtime": 0.39464831352233887,
    "success": true,
    "steps": 35,
    "success_per_goal": {
      "BC = AB succeeded": true,
      "CD = AD succeeded": true,
      "CD = BC succeeded": true
    },
    "agent_stats": {
      "agent_type": "follow_deductions",
      "n_deductions_stored": 34,
      "n_deductions_followed": 34
    }
  },
  "independently_checked": false,
  "independent_checker": "Existing checker only supports PD-MATH-VII-002; it cannot check these cases.",
  "production_adapter": "UNSUPPORTED: no saved formalization, route, general checker or renderer for this bank question.",
  "seconds": 12.871,
  "production_status": "UNSUPPORTED",
  "production_reason": "No audited formalization and reusable derivation route is implemented for this question."
}
```

Raw engine proof (not independently replayed by the existing adapter):

# Problem setup:

## Points

- A(3.7000, 0.0000)
- B(0.0000, 2.3000)
- C(-3.7000, 0.0000)
- D(0.0000, -2.3000)
- O(0.0000, 0.0000)

## Assumptions:

[C0] : O is the midpoint of AC
[C1] : O is the midpoint of BD
[C2] : AC ⟂ BD

## Numerical checks

[N0] : ▲ABO has the same orientation as ▲BCO
[N1] : A ≠ C
[N2] : A ≠ O
[N3] : C ≠ O
[N4] : B ≠ D
[N5] : B ≠ O
[N6] : D ≠ O
[N7] : ▲ABO has the same orientation as ▲AOD
[N8] : ▲ABO has the same orientation as ▲CDO


# Goals

BC = AB : Proved [11]
CD = AD : Proved [23]
CD = BC : Proved [24]


# Proof:

000. | O is the midpoint of AC [C0] =(r56 Properties of midpoint (coll))> A, C, O are collinear [0]
001. | A, C, O are collinear [0], A ≠ C [N1], A ≠ O [N2], C ≠ O [N3] =(r82 Parallel from collinear)> AO ∥ AC [1]
002. | A, C, O are collinear [0], A ≠ C [N1], A ≠ O [N2], C ≠ O [N3] =(r82 Parallel from collinear)> AO ∥ CO [2]
003. | O is the midpoint of BD [C1] =(r56 Properties of midpoint (coll))> B, D, O are collinear [3]
004. | B, D, O are collinear [3], B ≠ D [N4], B ≠ O [N5], D ≠ O [N6] =(r82 Parallel from collinear)> BO ∥ BD [4]
005. | AO ∥ AC [1], AO ∥ CO [2], BO ∥ BD [4], AC ⟂ BD [C2] =(AR Deduction)> ∠(AO,BO) = ∠(BO,CO) [5]
006. | O is the midpoint of AC [C0] =(r51 Midpoint splits in two)> AC:AO = 2/1 [6]
007. | O is the midpoint of AC [C0] =(r51 Midpoint splits in two)> AC:CO = 2/1 [7]
008. | AC:AO = 2/1 [6], AC:CO = 2/1 [7] =(AR Deduction)> AO:BO = CO:BO [8]
009. | ∠(AO,BO) = ∠(BO,CO) [5], AO:BO = CO:BO [8], ▲ABO has the same orientation as ▲BCO [N0] =(r63 SAS Similarity of triangles (Reverse))> ▲ABO ≅ ▲CBO [9]
010. | ▲ABO has the same orientation as ▲BCO [N0], ▲ABO ≅ ▲CBO [9] =(r53 Properties of similar triangles (Reverse))> AB:BC = BO:BO [10]
011. | AB:BC = BO:BO [10] =(AR Deduction)> BC = AB [11]
012. | B, D, O are collinear [3], B ≠ D [N4], B ≠ O [N5], D ≠ O [N6] =(r82 Parallel from collinear)> DO ∥ BO [12]
013. | AO ∥ AC [1], BO ∥ BD [4], DO ∥ BO [12], AC ⟂ BD [C2] =(AR Deduction)> ∠(AO,BO) = ∠(DO,AO) [13]
014. | O is the midpoint of BD [C1] =(r51 Midpoint splits in two)> BD:BO = 2/1 [14]
015. | O is the midpoint of BD [C1] =(r51 Midpoint splits in two)> BD:DO = 2/1 [15]
016. | BD:BO = 2/1 [14], BD:DO = 2/1 [15] =(AR Deduction)> AO:AO = BO:DO [16]
017. | ∠(AO,BO) = ∠(DO,AO) [13], AO:AO = BO:DO [16], ▲ABO has the same orientation as ▲AOD [N7] =(r63 SAS Similarity of triangles (Reverse))> ▲ABO ≅ ▲ADO [17]
018. | ▲ABO has the same orientation as ▲AOD [N7], ▲ABO ≅ ▲ADO [17] =(r53 Properties of similar triangles (Reverse))> AB:AD = BO:DO [18]
019. | AO ∥ CO [2], DO ∥ BO [12] =(AR Deduction)> ∠(AO,BO) = ∠(CO,DO) [19]
020. | AC:AO = 2/1 [6], AC:CO = 2/1 [7], BD:BO = 2/1 [14], BD:DO = 2/1 [15] =(AR Deduction)> AO:BO = CO:DO [20]
021. | ∠(AO,BO) = ∠(CO,DO) [19], AO:BO = CO:DO [20], ▲ABO has the same orientation as ▲CDO [N8] =(r62 SAS Similarity of triangles (Direct))> ▲ABO ≅ ▲CDO [21]
022. | ▲ABO has the same orientation as ▲CDO [N8], ▲ABO ≅ ▲CDO [21] =(r52 Properties of similar triangles (Direct))> AB:BO = CD:DO [22]
023. | AB:AD = BO:DO [18], AB:BO = CD:DO [22] =(AR Deduction)> CD = AD [23]
024. | AB:BC = BO:BO [10], AB:BO = CD:DO [22], BD:BO = 2/1 [14], BD:DO = 2/1 [15] =(AR Deduction)> CD = BC [24]


# Appendix: AR deductions:



005. | Angle Chasing to prove ∠(AO,BO) = ∠(BO,CO):
| Premise AO ∥ AC gives a linear equation with coefficients {Âˆ AC: 1, Âˆ AO: -1}
| Premise AO ∥ CO gives a linear equation with coefficients {Âˆ AO: 1, Âˆ CO: -1}
| Then {Âˆ AC: 2, Âˆ AO: -2} + 1 x {Âˆ AO: 1, Âˆ CO: -1}
|    = {Âˆ AC: 2, Âˆ AO: -1, Âˆ CO: -1}
| Premise BO ∥ BD gives a linear equation with coefficients {Âˆ BD: 1, Âˆ BO: -1}
| Then {Âˆ AC: 2, Âˆ AO: -1, Âˆ CO: -1} + -2 x {Âˆ BD: 1, Âˆ BO: -1}
|    = {Âˆ AC: 2, Âˆ AO: -1, Âˆ CO: -1, Âˆ BD: -2, Âˆ BO: 2}
| Premise AC ⟂ BD gives a linear equation with coefficients {Âˆ AC: 1, Âˆ BD: -1}
| Then {Âˆ AC: 2, Âˆ AO: -1, Âˆ CO: -1, Âˆ BD: -2, Âˆ BO: 2} + -2 x {Âˆ AC: 1, Âˆ BD: -1}
|    = {Âˆ AO: -1, Âˆ CO: -1, Âˆ BO: 2}
We are left with a linear equation with coefficients {Âˆ AO: -1, Âˆ CO: -1, Âˆ BO: 2} that gives ∠(AO,BO) = ∠(BO,CO)



008. | Ratio Chasing to prove AO:BO = CO:BO:
| Premise AC:AO = 2/1 gives a linear equation with coefficients {AC²: 1, AO²: -1}
| Premise AC:CO = 2/1 gives a linear equation with coefficients {AC²: 1, CO²: -1}
| Then {AC²: -1, AO²: 1} + 1 x {AC²: 1, CO²: -1}
|    = {AO²: 1, CO²: -1}
We are left with a linear equation with coefficients {AO²: 1, CO²: -1} that gives AO:BO = CO:BO



011. | Ratio Chasing to prove BC = AB:
| Premise AB:BC = BO:BO gives a linear equation with coefficients {AB²: 1, BC²: -1}
We are left with a linear equation with coefficients {AB²: 1, BC²: -1} that gives BC = AB



013. | Angle Chasing to prove ∠(AO,BO) = ∠(DO,AO):
| Premise AO ∥ AC gives a linear equation with coefficients {Âˆ AC: 1, Âˆ AO: -1}
| Premise BO ∥ BD gives a linear equation with coefficients {Âˆ BD: 1, Âˆ BO: -1}
| Then {Âˆ AC: 2, Âˆ AO: -2} + -2 x {Âˆ BD: 1, Âˆ BO: -1}
|    = {Âˆ AC: 2, Âˆ AO: -2, Âˆ BD: -2, Âˆ BO: 2}
| Premise DO ∥ BO gives a linear equation with coefficients {Âˆ BO: 1, Âˆ DO: -1}
| Then {Âˆ AC: 2, Âˆ AO: -2, Âˆ BD: -2, Âˆ BO: 2} + -1 x {Âˆ BO: 1, Âˆ DO: -1}
|    = {Âˆ AC: 2, Âˆ AO: -2, Âˆ BD: -2, Âˆ BO: 1, Âˆ DO: 1}
| Premise AC ⟂ BD gives a linear equation with coefficients {Âˆ AC: 1, Âˆ BD: -1}
| Then {Âˆ AC: 2, Âˆ AO: -2, Âˆ BD: -2, Âˆ BO: 1, Âˆ DO: 1} + -2 x {Âˆ AC: 1, Âˆ BD: -1}
|    = {Âˆ AO: -2, Âˆ BO: 1, Âˆ DO: 1}
We are left with a linear equation with coefficients {Âˆ AO: -2, Âˆ BO: 1, Âˆ DO: 1} that gives ∠(AO,BO) = ∠(DO,AO)



016. | Ratio Chasing to prove AO:AO = BO:DO:
| Premise BD:BO = 2/1 gives a linear equation with coefficients {BD²: 1, BO²: -1}
| Premise BD:DO = 2/1 gives a linear equation with coefficients {BD²: 1, DO²: -1}
| Then {BD²: 1, BO²: -1} + -1 x {BD²: 1, DO²: -1}
|    = {BO²: -1, DO²: 1}
We are left with a linear equation with coefficients {BO²: -1, DO²: 1} that gives AO:AO = BO:DO



019. | Angle Chasing to prove ∠(AO,BO) = ∠(CO,DO):
| Premise AO ∥ CO gives a linear equation with coefficients {Âˆ AO: 1, Âˆ CO: -1}
| Premise DO ∥ BO gives a linear equation with coefficients {Âˆ BO: 1, Âˆ DO: -1}
| Then {Âˆ AO: -1, Âˆ CO: 1} + 1 x {Âˆ BO: 1, Âˆ DO: -1}
|    = {Âˆ AO: -1, Âˆ CO: 1, Âˆ BO: 1, Âˆ DO: -1}
We are left with a linear equation with coefficients {Âˆ AO: -1, Âˆ CO: 1, Âˆ BO: 1, Âˆ DO: -1} that gives ∠(AO,BO) = ∠(CO,DO)



020. | Ratio Chasing to prove AO:BO = CO:DO:
| Premise AC:AO = 2/1 gives a linear equation with coefficients {AC²: 1, AO²: -1}
| Premise AC:CO = 2/1 gives a linear equation with coefficients {AC²: 1, CO²: -1}
| Then {AC²: -1, AO²: 1} + 1 x {AC²: 1, CO²: -1}
|    = {AO²: 1, CO²: -1}
| Premise BD:BO = 2/1 gives a linear equation with coefficients {BD²: 1, BO²: -1}
| Then {AO²: 1, CO²: -1} + 1 x {BD²: 1, BO²: -1}
|    = {AO²: 1, CO²: -1, BD²: 1, BO²: -1}
| Premise BD:DO = 2/1 gives a linear equation with coefficients {BD²: 1, DO²: -1}
| Then {AO²: 1, CO²: -1, BD²: 1, BO²: -1} + -1 x {BD²: 1, DO²: -1}
|    = {AO²: 1, CO²: -1, BO²: -1, DO²: 1}
We are left with a linear equation with coefficients {AO²: 1, CO²: -1, BO²: -1, DO²: 1} that gives AO:BO = CO:DO



023. | Ratio Chasing to prove CD = AD:
| Premise AB:AD = BO:DO gives a linear equation with coefficients {AB²: 1, AD²: -1, BO²: -1, DO²: 1}
| Premise AB:BO = CD:DO gives a linear equation with coefficients {AB²: 1, BO²: -1, CD²: -1, DO²: 1}
| Then {AB²: -1, AD²: 1, BO²: 1, DO²: -1} + 1 x {AB²: 1, BO²: -1, CD²: -1, DO²: 1}
|    = {AD²: 1, CD²: -1}
We are left with a linear equation with coefficients {AD²: 1, CD²: -1} that gives CD = AD



024. | Ratio Chasing to prove CD = BC:
| Premise AB:BC = BO:BO gives a linear equation with coefficients {AB²: 1, BC²: -1}
| Premise AB:BO = CD:DO gives a linear equation with coefficients {AB²: 1, BO²: -1, CD²: -1, DO²: 1}
| Then {AB²: -1, BC²: 1} + 1 x {AB²: 1, BO²: -1, CD²: -1, DO²: 1}
|    = {BC²: 1, BO²: -1, CD²: -1, DO²: 1}
| Premise BD:BO = 2/1 gives a linear equation with coefficients {BD²: 1, BO²: -1}
| Then {BC²: 1, BO²: -1, CD²: -1, DO²: 1} + -1 x {BD²: 1, BO²: -1}
|    = {BC²: 1, CD²: -1, DO²: 1, BD²: -1}
| Premise BD:DO = 2/1 gives a linear equation with coefficients {BD²: 1, DO²: -1}
| Then {BC²: 1, CD²: -1, DO²: 1, BD²: -1} + 1 x {BD²: 1, DO²: -1}
|    = {BC²: 1, CD²: -1}
We are left with a linear equation with coefficients {BC²: 1, CD²: -1} that gives CD = BC

End of proof.


## G2: Circle on an isosceles triangle's equal side as diameter bisects the base

OR

Prove that the circle drawn with any equal side of an isosceles triangle as diameter, bisects the base.

Exact input:

```json
{
  "id": "G2",
  "bank_id": "PD-MATH-IX-002",
  "description": "Circle on an isosceles triangle's equal side as diameter bisects the base",
  "points": {
    "a": [
      0,
      4.3
    ],
    "b": [
      -2.7,
      0
    ],
    "c": [
      2.7,
      0
    ],
    "d": [
      0,
      0
    ]
  },
  "assumptions": [
    "cong a b a c",
    "coll b d c",
    "perp d a d b",
    "diff b d",
    "ncoll a b c"
  ],
  "goals": [
    "midp d b c"
  ],
  "translation": "D denotes the second intersection with BC. Thales' theorem translates the diameter condition to AD perpendicular BD. This preprocessing was supplied manually."
}
```

Output:

```json
{
  "id": "G2",
  "description": "Circle on an isosceles triangle's equal side as diameter bisects the base",
  "llm_api_calls": 0,
  "llm_api_tokens": 0,
  "counted_in_production_metrics": false,
  "stage": "write_proof",
  "status": "ENGINE_PROVED_PENDING_INDEPENDENT_CHECK",
  "solver_goal_checked": true,
  "run_infos": {
    "runtime": 0.14658546447753906,
    "success": true,
    "steps": 15,
    "success_per_goal": {
      "D is the midpoint of BC succeeded": true
    },
    "agent_stats": {
      "agent_type": "follow_deductions",
      "n_deductions_stored": 14,
      "n_deductions_followed": 14
    }
  },
  "independently_checked": false,
  "independent_checker": "Existing checker only supports PD-MATH-VII-002; it cannot check these cases.",
  "production_adapter": "UNSUPPORTED: no saved formalization, route, general checker or renderer for this bank question.",
  "seconds": 9.223,
  "production_status": "UNSUPPORTED",
  "production_reason": "No audited formalization and reusable derivation route is implemented for this question."
}
```

Raw engine proof (not independently replayed by the existing adapter):

# Problem setup:

## Points

- A(0.0000, 4.3000)
- B(-2.7000, 0.0000)
- C(2.7000, 0.0000)
- D(0.0000, 0.0000)

## Assumptions:

[C0] : B, C, D are collinear
[C1] : AC = AB
[C2] : AD ⟂ BD

## Numerical checks

[N0] : ▲ABC has the same orientation as ▲ABC
[N1] : B ≠ C
[N2] : B ≠ D
[N3] : C ≠ D
[N4] : A, B, C are not collinear


# Goals

D is the midpoint of BC : Proved [7]


# Proof:

000. | AC = AB [C1] =(AR Deduction)> AB:AC = AC:AB [0]
001. | ∠(AB,AC) = ∠(AB,AC) [T0], AB:AC = AC:AB [0], ▲ABC has the same orientation as ▲ABC [N0] =(r63 SAS Similarity of triangles (Reverse))> ▲ABC ≅ ▲ACB [1]
002. | ▲ABC has the same orientation as ▲ABC [N0], ▲ABC ≅ ▲ACB [1] =(r53 Properties of similar triangles (Reverse))> ∠(AB,BC) = ∠(BC,AC) [2]
003. | B, C, D are collinear [C0], B ≠ C [N1], B ≠ D [N2], C ≠ D [N3] =(r82 Parallel from collinear)> BC ∥ BD [3]
004. | ∠(AB,BC) = ∠(BC,AC) [2], BC ∥ BD [3], AD ⟂ BD [C2] =(AR Deduction)> ∠(AB,AD) = ∠(AD,AC) [4]
005. | B, C, D are collinear [C0], ∠(AB,AD) = ∠(AD,AC) [4], A, B, C are not collinear [N4] =(r12 Bisector theorem II)> AB:AC = BD:CD [5]
006. | AC = AB [C1], AB:AC = BD:CD [5] =(AR Deduction)> CD = BD [6]
007. | B, C, D are collinear [C0], CD = BD [6] =(r54 Definition of midpoint)> D is the midpoint of BC [7]


# Appendix: AR deductions:



000. | Ratio Chasing to prove AB:AC = AC:AB:
| Premise AC = AB gives a linear equation with coefficients {AB²: 1, AC²: -1}
We are left with a linear equation with coefficients {AB²: 2, AC²: -2} that gives AB:AC = AC:AB



004. | Angle Chasing to prove ∠(AB,AD) = ∠(AD,AC):
| Premise ∠(AB,BC) = ∠(BC,AC) gives a linear equation with coefficients {Âˆ AB: -1, Âˆ AC: -1, Âˆ BC: 2}
| Premise BC ∥ BD gives a linear equation with coefficients {Âˆ BC: 1, Âˆ BD: -1}
| Then {Âˆ AB: -1, Âˆ AC: -1, Âˆ BC: 2} + -2 x {Âˆ BC: 1, Âˆ BD: -1}
|    = {Âˆ AB: -1, Âˆ AC: -1, Âˆ BD: 2}
| Premise AD ⟂ BD gives a linear equation with coefficients {Âˆ AD: 1, Âˆ BD: -1}
| Then {Âˆ AB: -1, Âˆ AC: -1, Âˆ BD: 2} + 2 x {Âˆ AD: 1, Âˆ BD: -1}
|    = {Âˆ AB: -1, Âˆ AC: -1, Âˆ AD: 2}
We are left with a linear equation with coefficients {Âˆ AB: -1, Âˆ AC: -1, Âˆ AD: 2} that gives ∠(AB,AD) = ∠(AD,AC)



006. | Ratio Chasing to prove CD = BD:
| Premise AC = AB gives a linear equation with coefficients {AB²: 1, AC²: -1}
| Premise AB:AC = BD:CD gives a linear equation with coefficients {AB²: 1, AC²: -1, BD²: -1, CD²: 1}
| Then {AB²: 1, AC²: -1} + -1 x {AB²: 1, AC²: -1, BD²: -1, CD²: 1}
|    = {BD²: 1, CD²: -1}
We are left with a linear equation with coefficients {BD²: 1, CD²: -1} that gives CD = BD

End of proof.


## G3: Midpoints of square sides form another square

35. Show that quadrilateral formed by joining the mid points of the pairs of adjacent sides of a square is also a square.

Exact input:

```json
{
  "id": "G3",
  "bank_id": "PD-MATH-IX-004",
  "description": "Midpoints of square sides form another square",
  "points": {
    "a": [
      0,
      0
    ],
    "b": [
      4.1,
      0
    ],
    "c": [
      4.1,
      4.1
    ],
    "d": [
      0,
      4.1
    ],
    "p": [
      2.05,
      0
    ],
    "q": [
      4.1,
      2.05
    ],
    "r": [
      2.05,
      4.1
    ],
    "s": [
      0,
      2.05
    ]
  },
  "assumptions": [
    "para a b c d",
    "para a d b c",
    "perp a b b c",
    "cong a b b c",
    "midp p a b",
    "midp q b c",
    "midp r c d",
    "midp s d a"
  ],
  "goals": [
    "para p q r s",
    "para q r s p",
    "perp p q q r",
    "cong p q q r",
    "cong q r r s",
    "cong r s s p"
  ],
  "translation": "Square premise and conclusion expanded to parallel/perpendicular/equal-length predicates."
}
```

Output:

```json
{
  "id": "G3",
  "description": "Midpoints of square sides form another square",
  "llm_api_calls": 0,
  "llm_api_tokens": 0,
  "counted_in_production_metrics": false,
  "stage": "write_proof",
  "status": "ENGINE_PROVED_PENDING_INDEPENDENT_CHECK",
  "solver_goal_checked": true,
  "run_infos": {
    "runtime": 1.45389986038208,
    "success": true,
    "steps": 67,
    "success_per_goal": {
      "PQ = QR succeeded": true,
      "PS = RS succeeded": true,
      "QR = RS succeeded": true,
      "PQ ∥ RS succeeded": true,
      "QR ∥ PS succeeded": true,
      "PQ ⟂ QR succeeded": true
    },
    "agent_stats": {
      "agent_type": "follow_deductions",
      "n_deductions_stored": 66,
      "n_deductions_followed": 66
    }
  },
  "independently_checked": false,
  "independent_checker": "Existing checker only supports PD-MATH-VII-002; it cannot check these cases.",
  "production_adapter": "UNSUPPORTED: no saved formalization, route, general checker or renderer for this bank question.",
  "seconds": 11.999,
  "production_status": "UNSUPPORTED",
  "production_reason": "No audited formalization and reusable derivation route is implemented for this question."
}
```

Raw engine proof (not independently replayed by the existing adapter):

# Problem setup:

## Points

- A(0.0000, 0.0000)
- B(4.1000, 0.0000)
- C(4.1000, 4.1000)
- D(0.0000, 4.1000)
- P(2.0500, 0.0000)
- Q(4.1000, 2.0500)
- R(2.0500, 4.1000)
- S(0.0000, 2.0500)

## Assumptions:

[C0] : AB = BC
[C1] : P is the midpoint of AB
[C2] : Q is the midpoint of BC
[C3] : AB ∥ CD
[C4] : AD ∥ BC
[C5] : R is the midpoint of CD
[C6] : AB ⟂ BC
[C7] : S is the midpoint of AD

## Numerical checks

[N0] : ▲ABD has the same orientation as ▲BCD
[N1] : A ≠ B
[N2] : A ≠ P
[N3] : B ≠ P
[N4] : B ≠ C
[N5] : B ≠ Q
[N6] : C ≠ Q
[N7] : C ≠ D
[N8] : C ≠ R
[N9] : D ≠ R
[N10] : P is to the same side of A->B as R is to C->D
[N11] : P, Q, R are not collinear
[N12] : A ≠ D
[N13] : A ≠ S
[N14] : D ≠ S
[N15] : Q is to the same side of B->C as S is to A->D
[N16] : P, Q, S are not collinear
[N17] : Q, R, S are not collinear


# Goals

PQ = QR : Proved [26]
PS = RS : Proved [43]
QR = RS : Proved [42]
PQ ∥ RS : Proved [44]
QR ∥ PS : Proved [45]
PQ ⟂ QR : Proved [46]


# Proof:

000. | P is the midpoint of AB [C1] =(r51 Midpoint splits in two)> AB:BP = 2/1 [0]
001. | Q is the midpoint of BC [C2] =(r51 Midpoint splits in two)> BC:BQ = 2/1 [1]
002. | AB = BC [C0], AB:BP = 2/1 [0], BC:BQ = 2/1 [1] =(AR Deduction)> BP = BQ [2]
003. | BP = BQ [2] =(r13 Isosceles triangle equal angles)> ∠(BP,PQ) = ∠(PQ,BQ) [3]
004. | AB ∥ CD [C3], AD ∥ BC [C4] =(AR Deduction)> ∠(AB,AD) = ∠(CD,BC) [4]
005. | AD ∥ BC [C4] =(AR Deduction)> ∠(AD,BD) = ∠(BC,BD) [5]
006. | ∠(AB,AD) = ∠(CD,BC) [4], ∠(AD,BD) = ∠(BC,BD) [5], ▲ABD has the same orientation as ▲BCD [N0] =(r34 AA Similarity of triangles (Direct))> ▲ABD ≅ ▲CDB [6]
007. | ▲ABD has the same orientation as ▲BCD [N0], ▲ABD ≅ ▲CDB [6] =(r52 Properties of similar triangles (Direct))> AB:AD = CD:BC [7]
008. | ▲ABD has the same orientation as ▲BCD [N0], ▲ABD ≅ ▲CDB [6] =(r52 Properties of similar triangles (Direct))> AD:BC = BD:BD [8]
009. | Q is the midpoint of BC [C2] =(r51 Midpoint splits in two)> BC:CQ = 2/1 [9]
010. | R is the midpoint of CD [C5] =(r51 Midpoint splits in two)> CD:CR = 2/1 [10]
011. | AB = BC [C0], AB:AD = CD:BC [7], AD:BC = BD:BD [8], BC:CQ = 2/1 [9], CD:CR = 2/1 [10] =(AR Deduction)> CQ = CR [11]
012. | CQ = CR [11] =(r13 Isosceles triangle equal angles)> ∠(CQ,QR) = ∠(QR,CR) [12]
013. | P is the midpoint of AB [C1] =(r56 Properties of midpoint (coll))> A, B, P are collinear [13]
014. | A, B, P are collinear [13], A ≠ B [N1], A ≠ P [N2], B ≠ P [N3] =(r82 Parallel from collinear)> AP ∥ AB [14]
015. | A, B, P are collinear [13], A ≠ B [N1], A ≠ P [N2], B ≠ P [N3] =(r82 Parallel from collinear)> BP ∥ AP [15]
016. | Q is the midpoint of BC [C2] =(r56 Properties of midpoint (coll))> B, C, Q are collinear [16]
017. | B, C, Q are collinear [16], B ≠ C [N4], B ≠ Q [N5], C ≠ Q [N6] =(r82 Parallel from collinear)> BQ ∥ BC [17]
018. | B, C, Q are collinear [16], B ≠ C [N4], B ≠ Q [N5], C ≠ Q [N6] =(r82 Parallel from collinear)> CQ ∥ BQ [18]
019. | R is the midpoint of CD [C5] =(r56 Properties of midpoint (coll))> C, D, R are collinear [19]
020. | C, D, R are collinear [19], C ≠ D [N7], C ≠ R [N8], D ≠ R [N9] =(r82 Parallel from collinear)> CR ∥ CD [20]
021. | P is the midpoint of AB [C1] =(r51 Midpoint splits in two)> AB:AP = 2/1 [21]
022. | R is the midpoint of CD [C5] =(r51 Midpoint splits in two)> CD:DR = 2/1 [22]
023. | AB:AP = 2/1 [21], AB:BP = 2/1 [0], CD:CR = 2/1 [10], CD:DR = 2/1 [22] =(AR Deduction)> AP:BP = DR:CR [23]
024. | A, B, P are collinear [13], C, D, R are collinear [19], AP:BP = DR:CR [23], AD ∥ BC [C4], P is to the same side of A->B as R is to C->D [N10] =(r41 Thales theorem III)> PR ∥ BC [24]
025. | ∠(BP,PQ) = ∠(PQ,BQ) [3], ∠(CQ,QR) = ∠(QR,CR) [12], AB ∥ CD [C3], AP ∥ AB [14], BP ∥ AP [15], BQ ∥ BC [17], CQ ∥ BQ [18], CR ∥ CD [20], PR ∥ BC [24], AB ⟂ BC [C6] =(AR Deduction)> ∠(PQ,PR) = ∠(PR,QR) [25]
026. | ∠(PQ,PR) = ∠(PR,QR) [25], P, Q, R are not collinear [N11] =(r14 Equal base angles imply isosceles)> PQ = QR [26]
027. | S is the midpoint of AD [C7] =(r51 Midpoint splits in two)> AD:AS = 2/1 [27]
028. | AB = BC [C0], AD:BC = BD:BD [8], AB:AP = 2/1 [21], AD:AS = 2/1 [27] =(AR Deduction)> AS = AP [28]
029. | AS = AP [28] =(r13 Isosceles triangle equal angles)> ∠(AP,PS) = ∠(PS,AS) [29]
030. | S is the midpoint of AD [C7] =(r56 Properties of midpoint (coll))> A, D, S are collinear [30]
031. | A, D, S are collinear [30], A ≠ D [N12], A ≠ S [N13], D ≠ S [N14] =(r82 Parallel from collinear)> AS ∥ AD [31]
032. | S is the midpoint of AD [C7] =(r51 Midpoint splits in two)> AD:DS = 2/1 [32]
033. | AD:AS = 2/1 [27], AD:DS = 2/1 [32], BC:BQ = 2/1 [1], BC:CQ = 2/1 [9] =(AR Deduction)> AS:BQ = DS:CQ [33]
034. | A, D, S are collinear [30], B, C, Q are collinear [16], AS:BQ = DS:CQ [33], AB ∥ CD [C3], Q is to the same side of B->C as S is to A->D [N15] =(r41 Thales theorem III)> QS ∥ CD [34]
035. | ∠(AP,PS) = ∠(PS,AS) [29], ∠(BP,PQ) = ∠(PQ,BQ) [3], AB ∥ CD [C3], AD ∥ BC [C4], AP ∥ AB [14], AS ∥ AD [31], BP ∥ AP [15], BQ ∥ BC [17], QS ∥ CD [34], AB ⟂ BC [C6] =(AR Deduction)> ∠(PQ,QS) = ∠(QS,PS) [35]
036. | ∠(PQ,QS) = ∠(QS,PS) [35], P, Q, S are not collinear [N16] =(r14 Equal base angles imply isosceles)> PQ = PS [36]
037. | AB = BC [C0], AB:AD = CD:BC [7], AD:BC = BD:BD [8], AD:DS = 2/1 [32], CD:DR = 2/1 [22] =(AR Deduction)> DS = DR [37]
038. | DS = DR [37] =(r13 Isosceles triangle equal angles)> ∠(DR,RS) = ∠(RS,DS) [38]
039. | A, D, S are collinear [30], A ≠ D [N12], A ≠ S [N13], D ≠ S [N14] =(r82 Parallel from collinear)> AS ∥ DS [39]
040. | C, D, R are collinear [19], C ≠ D [N7], C ≠ R [N8], D ≠ R [N9] =(r82 Parallel from collinear)> DR ∥ CR [40]
041. | ∠(CQ,QR) = ∠(QR,CR) [12], ∠(DR,RS) = ∠(RS,DS) [38], AB ∥ CD [C3], AD ∥ BC [C4], AS ∥ AD [31], AS ∥ DS [39], BQ ∥ BC [17], CQ ∥ BQ [18], CR ∥ CD [20], DR ∥ CR [40], QS ∥ CD [34], AB ⟂ BC [C6] =(AR Deduction)> ∠(QR,QS) = ∠(QS,RS) [41]
042. | ∠(QR,QS) = ∠(QS,RS) [41], Q, R, S are not collinear [N17] =(r14 Equal base angles imply isosceles)> QR = RS [42]
043. | PQ = PS [36], PQ = QR [26], QR = RS [42] =(AR Deduction)> PS = RS [43]
044. | ∠(BP,PQ) = ∠(PQ,BQ) [3], ∠(DR,RS) = ∠(RS,DS) [38], AB ∥ CD [C3], AD ∥ BC [C4], AP ∥ AB [14], AS ∥ AD [31], AS ∥ DS [39], BP ∥ AP [15], BQ ∥ BC [17], CR ∥ CD [20], DR ∥ CR [40] =(AR Deduction)> PQ ∥ RS [44]
045. | ∠(AP,PS) = ∠(PS,AS) [29], ∠(CQ,QR) = ∠(QR,CR) [12], AB ∥ CD [C3], AD ∥ BC [C4], AP ∥ AB [14], AS ∥ AD [31], BQ ∥ BC [17], CQ ∥ BQ [18], CR ∥ CD [20] =(AR Deduction)> QR ∥ PS [45]
046. | ∠(BP,PQ) = ∠(PQ,BQ) [3], ∠(CQ,QR) = ∠(QR,CR) [12], AB ∥ CD [C3], AP ∥ AB [14], BP ∥ AP [15], CQ ∥ BQ [18], CR ∥ CD [20] =(AR Deduction)> PQ ⟂ QR [46]


# Appendix: AR deductions:



002. | Ratio Chasing to prove BP = BQ:
| Premise AB = BC gives a linear equation with coefficients {AB²: 1, BC²: -1}
| Premise AB:BP = 2/1 gives a linear equation with coefficients {AB²: 1, BP²: -1}
| Then {AB²: 1, BC²: -1} + -1 x {AB²: 1, BP²: -1}
|    = {BC²: -1, BP²: 1}
| Premise BC:BQ = 2/1 gives a linear equation with coefficients {BC²: 1, BQ²: -1}
| Then {BC²: -1, BP²: 1} + 1 x {BC²: 1, BQ²: -1}
|    = {BP²: 1, BQ²: -1}
We are left with a linear equation with coefficients {BP²: 1, BQ²: -1} that gives BP = BQ



004. | Angle Chasing to prove ∠(AB,AD) = ∠(CD,BC):
| Premise AB ∥ CD gives a linear equation with coefficients {Âˆ AB: 1, Âˆ CD: -1}
| Premise AD ∥ BC gives a linear equation with coefficients {Âˆ AD: 1, Âˆ BC: -1}
| Then {Âˆ AB: -1, Âˆ CD: 1} + 1 x {Âˆ AD: 1, Âˆ BC: -1}
|    = {Âˆ AB: -1, Âˆ CD: 1, Âˆ AD: 1, Âˆ BC: -1}
We are left with a linear equation with coefficients {Âˆ AB: -1, Âˆ CD: 1, Âˆ AD: 1, Âˆ BC: -1} that gives ∠(AB,AD) = ∠(CD,BC)



005. | Angle Chasing to prove ∠(AD,BD) = ∠(BC,BD):
| Premise AD ∥ BC gives a linear equation with coefficients {Âˆ AD: 1, Âˆ BC: -1}
We are left with a linear equation with coefficients {Âˆ AD: -1, Âˆ BC: 1} that gives ∠(AD,BD) = ∠(BC,BD)



011. | Ratio Chasing to prove CQ = CR:
| Premise AB = BC gives a linear equation with coefficients {AB²: 1, BC²: -1}
| Premise AB:AD = CD:BC gives a linear equation with coefficients {AB²: 1, AD²: -1, BC²: 1, CD²: -1}
| Then {AB²: -1, BC²: 1} + 1 x {AB²: 1, AD²: -1, BC²: 1, CD²: -1}
|    = {BC²: 2, AD²: -1, CD²: -1}
| Premise AD:BC = BD:BD gives a linear equation with coefficients {AD²: 1, BC²: -1}
| Then {BC²: 2, AD²: -1, CD²: -1} + 1 x {AD²: 1, BC²: -1}
|    = {BC²: 1, CD²: -1}
| Premise BC:CQ = 2/1 gives a linear equation with coefficients {BC²: 1, CQ²: -1}
| Then {BC²: 1, CD²: -1} + -1 x {BC²: 1, CQ²: -1}
|    = {CD²: -1, CQ²: 1}
| Premise CD:CR = 2/1 gives a linear equation with coefficients {CD²: 1, CR²: -1}
| Then {CD²: -1, CQ²: 1} + 1 x {CD²: 1, CR²: -1}
|    = {CQ²: 1, CR²: -1}
We are left with a linear equation with coefficients {CQ²: 1, CR²: -1} that gives CQ = CR



023. | Ratio Chasing to prove AP:BP = DR:CR:
| Premise AB:AP = 2/1 gives a linear equation with coefficients {AB²: 1, AP²: -1}
| Premise AB:BP = 2/1 gives a linear equation with coefficients {AB²: 1, BP²: -1}
| Then {AB²: -1, AP²: 1} + 1 x {AB²: 1, BP²: -1}
|    = {AP²: 1, BP²: -1}
| Premise CD:CR = 2/1 gives a linear equation with coefficients {CD²: 1, CR²: -1}
| Then {AP²: 1, BP²: -1} + -1 x {CD²: 1, CR²: -1}
|    = {AP²: 1, BP²: -1, CD²: -1, CR²: 1}
| Premise CD:DR = 2/1 gives a linear equation with coefficients {CD²: 1, DR²: -1}
| Then {AP²: 1, BP²: -1, CD²: -1, CR²: 1} + 1 x {CD²: 1, DR²: -1}
|    = {AP²: 1, BP²: -1, CR²: 1, DR²: -1}
We are left with a linear equation with coefficients {AP²: 1, BP²: -1, CR²: 1, DR²: -1} that gives AP:BP = DR:CR



025. | Angle Chasing to prove ∠(PQ,PR) = ∠(PR,QR):
| Premise ∠(BP,PQ) = ∠(PQ,BQ) gives a linear equation with coefficients {Âˆ BP: -1, Âˆ BQ: -1, Âˆ PQ: 2}
| Premise ∠(CQ,QR) = ∠(QR,CR) gives a linear equation with coefficients {Âˆ CQ: -1, Âˆ CR: -1, Âˆ QR: 2}
| Then {Âˆ BP: -1/2, Âˆ BQ: -1/2, Âˆ PQ: 1} + 1/2 x {Âˆ CQ: -1, Âˆ CR: -1, Âˆ QR: 2}
|    = {Âˆ BP: -1/2, Âˆ BQ: -1/2, Âˆ PQ: 1, Âˆ CQ: -1/2, Âˆ CR: -1/2, Âˆ QR: 1}
| Premise AB ∥ CD gives a linear equation with coefficients {Âˆ AB: 1, Âˆ CD: -1}
| Then {Âˆ BP: -1/2, Âˆ BQ: -1/2, Âˆ PQ: 1, Âˆ CQ: -1/2, Âˆ CR: -1/2, Âˆ QR: 1} + -1/2 x {Âˆ AB: 1, Âˆ CD: -1}
|    = {Âˆ BP: -1/2, Âˆ BQ: -1/2, Âˆ PQ: 1, Âˆ CQ: -1/2, Âˆ CR: -1/2, Âˆ QR: 1, Âˆ AB: -1/2, Âˆ CD: 1/2}
| Premise AP ∥ AB gives a linear equation with coefficients {Âˆ AB: 1, Âˆ AP: -1}
| Then {Âˆ BP: -1/2, Âˆ BQ: -1/2, Âˆ PQ: 1, Âˆ CQ: -1/2, Âˆ CR: -1/2, Âˆ QR: 1, Âˆ AB: -1/2, Âˆ CD: 1/2} + -1/2 x {Âˆ AB: 1, Âˆ AP: -1}
|    = {Âˆ BP: -1/2, Âˆ BQ: -1/2, Âˆ PQ: 1, Âˆ CQ: -1/2, Âˆ CR: -1/2, Âˆ QR: 1, Âˆ AB: -1, Âˆ CD: 1/2, Âˆ AP: 1/2}
| Premise BP ∥ AP gives a linear equation with coefficients {Âˆ AP: 1, Âˆ BP: -1}
| Then {Âˆ BP: -1/2, Âˆ BQ: -1/2, Âˆ PQ: 1, Âˆ CQ: -1/2, Âˆ CR: -1/2, Âˆ QR: 1, Âˆ AB: -1, Âˆ CD: 1/2, Âˆ AP: 1/2} + -1/2 x {Âˆ AP: 1, Âˆ BP: -1}
|    = {Âˆ BQ: -1/2, Âˆ PQ: 1, Âˆ CQ: -1/2, Âˆ CR: -1/2, Âˆ QR: 1, Âˆ AB: -1, Âˆ CD: 1/2}
| Premise BQ ∥ BC gives a linear equation with coefficients {Âˆ BC: 1, Âˆ BQ: -1}
| Then {Âˆ BQ: -1/2, Âˆ PQ: 1, Âˆ CQ: -1/2, Âˆ CR: -1/2, Âˆ QR: 1, Âˆ AB: -1, Âˆ CD: 1/2} + -1 x {Âˆ BC: 1, Âˆ BQ: -1}
|    = {Âˆ BQ: 1/2, Âˆ PQ: 1, Âˆ CQ: -1/2, Âˆ CR: -1/2, Âˆ QR: 1, Âˆ AB: -1, Âˆ CD: 1/2, Âˆ BC: -1}
| Premise CQ ∥ BQ gives a linear equation with coefficients {Âˆ BQ: 1, Âˆ CQ: -1}
| Then {Âˆ BQ: 1/2, Âˆ PQ: 1, Âˆ CQ: -1/2, Âˆ CR: -1/2, Âˆ QR: 1, Âˆ AB: -1, Âˆ CD: 1/2, Âˆ BC: -1} + -1/2 x {Âˆ BQ: 1, Âˆ CQ: -1}
|    = {Âˆ PQ: 1, Âˆ CR: -1/2, Âˆ QR: 1, Âˆ AB: -1, Âˆ CD: 1/2, Âˆ BC: -1}
| Premise CR ∥ CD gives a linear equation with coefficients {Âˆ CD: 1, Âˆ CR: -1}
| Then {Âˆ PQ: 1, Âˆ CR: -1/2, Âˆ QR: 1, Âˆ AB: -1, Âˆ CD: 1/2, Âˆ BC: -1} + -1/2 x {Âˆ CD: 1, Âˆ CR: -1}
|    = {Âˆ PQ: 1, Âˆ QR: 1, Âˆ AB: -1, Âˆ BC: -1}
| Premise PR ∥ BC gives a linear equation with coefficients {Âˆ BC: 1, Âˆ PR: -1}
| Then {Âˆ PQ: 1, Âˆ QR: 1, Âˆ AB: -1, Âˆ BC: -1} + 2 x {Âˆ BC: 1, Âˆ PR: -1}
|    = {Âˆ PQ: 1, Âˆ QR: 1, Âˆ AB: -1, Âˆ BC: 1, Âˆ PR: -2}
| Premise AB ⟂ BC gives a linear equation with coefficients {Âˆ AB: 1, Âˆ BC: -1}
| Then {Âˆ PQ: 1, Âˆ QR: 1, Âˆ AB: -1, Âˆ BC: 1, Âˆ PR: -2} + 1 x {Âˆ AB: 1, Âˆ BC: -1}
|    = {Âˆ PQ: 1, Âˆ QR: 1, Âˆ PR: -2}
We are left with a linear equation with coefficients {Âˆ PQ: 1, Âˆ QR: 1, Âˆ PR: -2} that gives ∠(PQ,PR) = ∠(PR,QR)



028. | Ratio Chasing to prove AS = AP:
| Premise AB = BC gives a linear equation with coefficients {AB²: 1, BC²: -1}
| Premise AD:BC = BD:BD gives a linear equation with coefficients {AD²: 1, BC²: -1}
| Then {AB²: 1, BC²: -1} + -1 x {AD²: 1, BC²: -1}
|    = {AB²: 1, AD²: -1}
| Premise AB:AP = 2/1 gives a linear equation with coefficients {AB²: 1, AP²: -1}
| Then {AB²: 1, AD²: -1} + -1 x {AB²: 1, AP²: -1}
|    = {AD²: -1, AP²: 1}
| Premise AD:AS = 2/1 gives a linear equation with coefficients {AD²: 1, AS²: -1}
| Then {AD²: -1, AP²: 1} + 1 x {AD²: 1, AS²: -1}
|    = {AP²: 1, AS²: -1}
We are left with a linear equation with coefficients {AP²: 1, AS²: -1} that gives AS = AP



033. | Ratio Chasing to prove AS:BQ = DS:CQ:
| Premise AD:AS = 2/1 gives a linear equation with coefficients {AD²: 1, AS²: -1}
| Premise AD:DS = 2/1 gives a linear equation with coefficients {AD²: 1, DS²: -1}
| Then {AD²: -1, AS²: 1} + 1 x {AD²: 1, DS²: -1}
|    = {AS²: 1, DS²: -1}
| Premise BC:BQ = 2/1 gives a linear equation with coefficients {BC²: 1, BQ²: -1}
| Then {AS²: 1, DS²: -1} + 1 x {BC²: 1, BQ²: -1}
|    = {AS²: 1, DS²: -1, BC²: 1, BQ²: -1}
| Premise BC:CQ = 2/1 gives a linear equation with coefficients {BC²: 1, CQ²: -1}
| Then {AS²: 1, DS²: -1, BC²: 1, BQ²: -1} + -1 x {BC²: 1, CQ²: -1}
|    = {AS²: 1, DS²: -1, BQ²: -1, CQ²: 1}
We are left with a linear equation with coefficients {AS²: 1, DS²: -1, BQ²: -1, CQ²: 1} that gives AS:BQ = DS:CQ



035. | Angle Chasing to prove ∠(PQ,QS) = ∠(QS,PS):
| Premise ∠(AP,PS) = ∠(PS,AS) gives a linear equation with coefficients {Âˆ AP: -1, Âˆ AS: -1, Âˆ PS: 2}
| Premise ∠(BP,PQ) = ∠(PQ,BQ) gives a linear equation with coefficients {Âˆ BP: -1, Âˆ BQ: -1, Âˆ PQ: 2}
| Then {Âˆ AP: 1/2, Âˆ AS: 1/2, Âˆ PS: -1} + -1/2 x {Âˆ BP: -1, Âˆ BQ: -1, Âˆ PQ: 2}
|    = {Âˆ AP: 1/2, Âˆ AS: 1/2, Âˆ PS: -1, Âˆ BP: 1/2, Âˆ BQ: 1/2, Âˆ PQ: -1}
| Premise AB ∥ CD gives a linear equation with coefficients {Âˆ AB: 1, Âˆ CD: -1}
| Then {Âˆ AP: 1/2, Âˆ AS: 1/2, Âˆ PS: -1, Âˆ BP: 1/2, Âˆ BQ: 1/2, Âˆ PQ: -1} + -2 x {Âˆ AB: 1, Âˆ CD: -1}
|    = {Âˆ AP: 1/2, Âˆ AS: 1/2, Âˆ PS: -1, Âˆ BP: 1/2, Âˆ BQ: 1/2, Âˆ PQ: -1, Âˆ AB: -2, Âˆ CD: 2}
| Premise AD ∥ BC gives a linear equation with coefficients {Âˆ AD: 1, Âˆ BC: -1}
| Then {Âˆ AP: 1/2, Âˆ AS: 1/2, Âˆ PS: -1, Âˆ BP: 1/2, Âˆ BQ: 1/2, Âˆ PQ: -1, Âˆ AB: -2, Âˆ CD: 2} + -1/2 x {Âˆ AD: 1, Âˆ BC: -1}
|    = {Âˆ AP: 1/2, Âˆ AS: 1/2, Âˆ PS: -1, Âˆ BP: 1/2, Âˆ BQ: 1/2, Âˆ PQ: -1, Âˆ AB: -2, Âˆ CD: 2, Âˆ AD: -1/2, Âˆ BC: 1/2}
| Premise AP ∥ AB gives a linear equation with coefficients {Âˆ AB: 1, Âˆ AP: -1}
| Then {Âˆ AP: 1/2, Âˆ AS: 1/2, Âˆ PS: -1, Âˆ BP: 1/2, Âˆ BQ: 1/2, Âˆ PQ: -1, Âˆ AB: -2, Âˆ CD: 2, Âˆ AD: -1/2, Âˆ BC: 1/2} + 1 x {Âˆ AB: 1, Âˆ AP: -1}
|    = {Âˆ AP: -1/2, Âˆ AS: 1/2, Âˆ PS: -1, Âˆ BP: 1/2, Âˆ BQ: 1/2, Âˆ PQ: -1, Âˆ AB: -1, Âˆ CD: 2, Âˆ AD: -1/2, Âˆ BC: 1/2}
| Premise AS ∥ AD gives a linear equation with coefficients {Âˆ AD: 1, Âˆ AS: -1}
| Then {Âˆ AP: -1/2, Âˆ AS: 1/2, Âˆ PS: -1, Âˆ BP: 1/2, Âˆ BQ: 1/2, Âˆ PQ: -1, Âˆ AB: -1, Âˆ CD: 2, Âˆ AD: -1/2, Âˆ BC: 1/2} + 1/2 x {Âˆ AD: 1, Âˆ AS: -1}
|    = {Âˆ AP: -1/2, Âˆ PS: -1, Âˆ BP: 1/2, Âˆ BQ: 1/2, Âˆ PQ: -1, Âˆ AB: -1, Âˆ CD: 2, Âˆ BC: 1/2}
| Premise BP ∥ AP gives a linear equation with coefficients {Âˆ AP: 1, Âˆ BP: -1}
| Then {Âˆ AP: -1/2, Âˆ PS: -1, Âˆ BP: 1/2, Âˆ BQ: 1/2, Âˆ PQ: -1, Âˆ AB: -1, Âˆ CD: 2, Âˆ BC: 1/2} + 1/2 x {Âˆ AP: 1, Âˆ BP: -1}
|    = {Âˆ PS: -1, Âˆ BQ: 1/2, Âˆ PQ: -1, Âˆ AB: -1, Âˆ CD: 2, Âˆ BC: 1/2}
| Premise BQ ∥ BC gives a linear equation with coefficients {Âˆ BC: 1, Âˆ BQ: -1}
| Then {Âˆ PS: -1, Âˆ BQ: 1/2, Âˆ PQ: -1, Âˆ AB: -1, Âˆ CD: 2, Âˆ BC: 1/2} + 1/2 x {Âˆ BC: 1, Âˆ BQ: -1}
|    = {Âˆ PS: -1, Âˆ PQ: -1, Âˆ AB: -1, Âˆ CD: 2, Âˆ BC: 1}
| Premise QS ∥ CD gives a linear equation with coefficients {Âˆ CD: 1, Âˆ QS: -1}
| Then {Âˆ PS: -1, Âˆ PQ: -1, Âˆ AB: -1, Âˆ CD: 2, Âˆ BC: 1} + -2 x {Âˆ CD: 1, Âˆ QS: -1}
|    = {Âˆ PS: -1, Âˆ PQ: -1, Âˆ AB: -1, Âˆ BC: 1, Âˆ QS: 2}
| Premise AB ⟂ BC gives a linear equation with coefficients {Âˆ AB: 1, Âˆ BC: -1}
| Then {Âˆ PS: -1, Âˆ PQ: -1, Âˆ AB: -1, Âˆ BC: 1, Âˆ QS: 2} + 1 x {Âˆ AB: 1, Âˆ BC: -1}
|    = {Âˆ PS: -1, Âˆ PQ: -1, Âˆ QS: 2}
We are left with a linear equation with coefficients {Âˆ PS: -1, Âˆ PQ: -1, Âˆ QS: 2} that gives ∠(PQ,QS) = ∠(QS,PS)



037. | Ratio Chasing to prove DS = DR:
| Premise AB = BC gives a linear equation with coefficients {AB²: 1, BC²: -1}
| Premise AB:AD = CD:BC gives a linear equation with coefficients {AB²: 1, AD²: -1, BC²: 1, CD²: -1}
| Then {AB²: 1, BC²: -1} + -1 x {AB²: 1, AD²: -1, BC²: 1, CD²: -1}
|    = {BC²: -2, AD²: 1, CD²: 1}
| Premise AD:BC = BD:BD gives a linear equation with coefficients {AD²: 1, BC²: -1}
| Then {BC²: -2, AD²: 1, CD²: 1} + -2 x {AD²: 1, BC²: -1}
|    = {AD²: -1, CD²: 1}
| Premise AD:DS = 2/1 gives a linear equation with coefficients {AD²: 1, DS²: -1}
| Then {AD²: -1, CD²: 1} + 1 x {AD²: 1, DS²: -1}
|    = {CD²: 1, DS²: -1}
| Premise CD:DR = 2/1 gives a linear equation with coefficients {CD²: 1, DR²: -1}
| Then {CD²: 1, DS²: -1} + -1 x {CD²: 1, DR²: -1}
|    = {DS²: -1, DR²: 1}
We are left with a linear equation with coefficients {DS²: -1, DR²: 1} that gives DS = DR



041. | Angle Chasing to prove ∠(QR,QS) = ∠(QS,RS):
| Premise ∠(CQ,QR) = ∠(QR,CR) gives a linear equation with coefficients {Âˆ CQ: -1, Âˆ CR: -1, Âˆ QR: 2}
| Premise ∠(DR,RS) = ∠(RS,DS) gives a linear equation with coefficients {Âˆ DR: -1, Âˆ DS: -1, Âˆ RS: 2}
| Then {Âˆ CQ: -1/2, Âˆ CR: -1/2, Âˆ QR: 1} + 1/2 x {Âˆ DR: -1, Âˆ DS: -1, Âˆ RS: 2}
|    = {Âˆ CQ: -1/2, Âˆ CR: -1/2, Âˆ QR: 1, Âˆ DR: -1/2, Âˆ DS: -1/2, Âˆ RS: 1}
| Premise AB ∥ CD gives a linear equation with coefficients {Âˆ AB: 1, Âˆ CD: -1}
| Then {Âˆ CQ: -1/2, Âˆ CR: -1/2, Âˆ QR: 1, Âˆ DR: -1/2, Âˆ DS: -1/2, Âˆ RS: 1} + 1 x {Âˆ AB: 1, Âˆ CD: -1}
|    = {Âˆ CQ: -1/2, Âˆ CR: -1/2, Âˆ QR: 1, Âˆ DR: -1/2, Âˆ DS: -1/2, Âˆ RS: 1, Âˆ AB: 1, Âˆ CD: -1}
| Premise AD ∥ BC gives a linear equation with coefficients {Âˆ AD: 1, Âˆ BC: -1}
| Then {Âˆ CQ: -1/2, Âˆ CR: -1/2, Âˆ QR: 1, Âˆ DR: -1/2, Âˆ DS: -1/2, Âˆ RS: 1, Âˆ AB: 1, Âˆ CD: -1} + 1/2 x {Âˆ AD: 1, Âˆ BC: -1}
|    = {Âˆ CQ: -1/2, Âˆ CR: -1/2, Âˆ QR: 1, Âˆ DR: -1/2, Âˆ DS: -1/2, Âˆ RS: 1, Âˆ AB: 1, Âˆ CD: -1, Âˆ AD: 1/2, Âˆ BC: -1/2}
| Premise AS ∥ AD gives a linear equation with coefficients {Âˆ AD: 1, Âˆ AS: -1}
| Then {Âˆ CQ: -1/2, Âˆ CR: -1/2, Âˆ QR: 1, Âˆ DR: -1/2, Âˆ DS: -1/2, Âˆ RS: 1, Âˆ AB: 1, Âˆ CD: -1, Âˆ AD: 1/2, Âˆ BC: -1/2} + -1/2 x {Âˆ AD: 1, Âˆ AS: -1}
|    = {Âˆ CQ: -1/2, Âˆ CR: -1/2, Âˆ QR: 1, Âˆ DR: -1/2, Âˆ DS: -1/2, Âˆ RS: 1, Âˆ AB: 1, Âˆ CD: -1, Âˆ BC: -1/2, Âˆ AS: 1/2}
| Premise AS ∥ DS gives a linear equation with coefficients {Âˆ AS: 1, Âˆ DS: -1}
| Then {Âˆ CQ: -1/2, Âˆ CR: -1/2, Âˆ QR: 1, Âˆ DR: -1/2, Âˆ DS: -1/2, Âˆ RS: 1, Âˆ AB: 1, Âˆ CD: -1, Âˆ BC: -1/2, Âˆ AS: 1/2} + -1/2 x {Âˆ AS: 1, Âˆ DS: -1}
|    = {Âˆ CQ: -1/2, Âˆ CR: -1/2, Âˆ QR: 1, Âˆ DR: -1/2, Âˆ RS: 1, Âˆ AB: 1, Âˆ CD: -1, Âˆ BC: -1/2}
| Premise BQ ∥ BC gives a linear equation with coefficients {Âˆ BC: 1, Âˆ BQ: -1}
| Then {Âˆ CQ: -1/2, Âˆ CR: -1/2, Âˆ QR: 1, Âˆ DR: -1/2, Âˆ RS: 1, Âˆ AB: 1, Âˆ CD: -1, Âˆ BC: -1/2} + -1/2 x {Âˆ BC: 1, Âˆ BQ: -1}
|    = {Âˆ CQ: -1/2, Âˆ CR: -1/2, Âˆ QR: 1, Âˆ DR: -1/2, Âˆ RS: 1, Âˆ AB: 1, Âˆ CD: -1, Âˆ BC: -1, Âˆ BQ: 1/2}
| Premise CQ ∥ BQ gives a linear equation with coefficients {Âˆ BQ: 1, Âˆ CQ: -1}
| Then {Âˆ CQ: -1/2, Âˆ CR: -1/2, Âˆ QR: 1, Âˆ DR: -1/2, Âˆ RS: 1, Âˆ AB: 1, Âˆ CD: -1, Âˆ BC: -1, Âˆ BQ: 1/2} + -1/2 x {Âˆ BQ: 1, Âˆ CQ: -1}
|    = {Âˆ CR: -1/2, Âˆ QR: 1, Âˆ DR: -1/2, Âˆ RS: 1, Âˆ AB: 1, Âˆ CD: -1, Âˆ BC: -1}
| Premise CR ∥ CD gives a linear equation with coefficients {Âˆ CD: 1, Âˆ CR: -1}
| Then {Âˆ CR: -1/2, Âˆ QR: 1, Âˆ DR: -1/2, Âˆ RS: 1, Âˆ AB: 1, Âˆ CD: -1, Âˆ BC: -1} + -1 x {Âˆ CD: 1, Âˆ CR: -1}
|    = {Âˆ CR: 1/2, Âˆ QR: 1, Âˆ DR: -1/2, Âˆ RS: 1, Âˆ AB: 1, Âˆ CD: -2, Âˆ BC: -1}
| Premise DR ∥ CR gives a linear equation with coefficients {Âˆ CR: 1, Âˆ DR: -1}
| Then {Âˆ CR: 1/2, Âˆ QR: 1, Âˆ DR: -1/2, Âˆ RS: 1, Âˆ AB: 1, Âˆ CD: -2, Âˆ BC: -1} + -1/2 x {Âˆ CR: 1, Âˆ DR: -1}
|    = {Âˆ QR: 1, Âˆ RS: 1, Âˆ AB: 1, Âˆ CD: -2, Âˆ BC: -1}
| Premise QS ∥ CD gives a linear equation with coefficients {Âˆ CD: 1, Âˆ QS: -1}
| Then {Âˆ QR: 1, Âˆ RS: 1, Âˆ AB: 1, Âˆ CD: -2, Âˆ BC: -1} + 2 x {Âˆ CD: 1, Âˆ QS: -1}
|    = {Âˆ QR: 1, Âˆ RS: 1, Âˆ AB: 1, Âˆ BC: -1, Âˆ QS: -2}
| Premise AB ⟂ BC gives a linear equation with coefficients {Âˆ AB: 1, Âˆ BC: -1}
| Then {Âˆ QR: 1, Âˆ RS: 1, Âˆ AB: 1, Âˆ BC: -1, Âˆ QS: -2} + -1 x {Âˆ AB: 1, Âˆ BC: -1}
|    = {Âˆ QR: 1, Âˆ RS: 1, Âˆ QS: -2}
We are left with a linear equation with coefficients {Âˆ QR: 1, Âˆ RS: 1, Âˆ QS: -2} that gives ∠(QR,QS) = ∠(QS,RS)



043. | Ratio Chasing to prove PS = RS:
| Premise PQ = PS gives a linear equation with coefficients {PQ²: 1, PS²: -1}
| Premise PQ = QR gives a linear equation with coefficients {PQ²: 1, QR²: -1}
| Then {PQ²: -1, PS²: 1} + 1 x {PQ²: 1, QR²: -1}
|    = {PS²: 1, QR²: -1}
| Premise QR = RS gives a linear equation with coefficients {QR²: 1, RS²: -1}
| Then {PS²: 1, QR²: -1} + 1 x {QR²: 1, RS²: -1}
|    = {PS²: 1, RS²: -1}
We are left with a linear equation with coefficients {PS²: 1, RS²: -1} that gives PS = RS



044. | Angle Chasing to prove PQ ∥ RS:
| Premise ∠(BP,PQ) = ∠(PQ,BQ) gives a linear equation with coefficients {Âˆ BP: -1, Âˆ BQ: -1, Âˆ PQ: 2}
| Premise ∠(DR,RS) = ∠(RS,DS) gives a linear equation with coefficients {Âˆ DR: -1, Âˆ DS: -1, Âˆ RS: 2}
| Then {Âˆ BP: -1/2, Âˆ BQ: -1/2, Âˆ PQ: 1} + -1/2 x {Âˆ DR: -1, Âˆ DS: -1, Âˆ RS: 2}
|    = {Âˆ BP: -1/2, Âˆ BQ: -1/2, Âˆ PQ: 1, Âˆ DR: 1/2, Âˆ DS: 1/2, Âˆ RS: -1}
| Premise AB ∥ CD gives a linear equation with coefficients {Âˆ AB: 1, Âˆ CD: -1}
| Then {Âˆ BP: -1/2, Âˆ BQ: -1/2, Âˆ PQ: 1, Âˆ DR: 1/2, Âˆ DS: 1/2, Âˆ RS: -1} + 1/2 x {Âˆ AB: 1, Âˆ CD: -1}
|    = {Âˆ BP: -1/2, Âˆ BQ: -1/2, Âˆ PQ: 1, Âˆ DR: 1/2, Âˆ DS: 1/2, Âˆ RS: -1, Âˆ AB: 1/2, Âˆ CD: -1/2}
| Premise AD ∥ BC gives a linear equation with coefficients {Âˆ AD: 1, Âˆ BC: -1}
| Then {Âˆ BP: -1/2, Âˆ BQ: -1/2, Âˆ PQ: 1, Âˆ DR: 1/2, Âˆ DS: 1/2, Âˆ RS: -1, Âˆ AB: 1/2, Âˆ CD: -1/2} + -1/2 x {Âˆ AD: 1, Âˆ BC: -1}
|    = {Âˆ BP: -1/2, Âˆ BQ: -1/2, Âˆ PQ: 1, Âˆ DR: 1/2, Âˆ DS: 1/2, Âˆ RS: -1, Âˆ AB: 1/2, Âˆ CD: -1/2, Âˆ AD: -1/2, Âˆ BC: 1/2}
| Premise AP ∥ AB gives a linear equation with coefficients {Âˆ AB: 1, Âˆ AP: -1}
| Then {Âˆ BP: -1/2, Âˆ BQ: -1/2, Âˆ PQ: 1, Âˆ DR: 1/2, Âˆ DS: 1/2, Âˆ RS: -1, Âˆ AB: 1/2, Âˆ CD: -1/2, Âˆ AD: -1/2, Âˆ BC: 1/2} + -1/2 x {Âˆ AB: 1, Âˆ AP: -1}
|    = {Âˆ BP: -1/2, Âˆ BQ: -1/2, Âˆ PQ: 1, Âˆ DR: 1/2, Âˆ DS: 1/2, Âˆ RS: -1, Âˆ CD: -1/2, Âˆ AD: -1/2, Âˆ BC: 1/2, Âˆ AP: 1/2}
| Premise AS ∥ AD gives a linear equation with coefficients {Âˆ AD: 1, Âˆ AS: -1}
| Then {Âˆ BP: -1/2, Âˆ BQ: -1/2, Âˆ PQ: 1, Âˆ DR: 1/2, Âˆ DS: 1/2, Âˆ RS: -1, Âˆ CD: -1/2, Âˆ AD: -1/2, Âˆ BC: 1/2, Âˆ AP: 1/2} + 1/2 x {Âˆ AD: 1, Âˆ AS: -1}
|    = {Âˆ BP: -1/2, Âˆ BQ: -1/2, Âˆ PQ: 1, Âˆ DR: 1/2, Âˆ DS: 1/2, Âˆ RS: -1, Âˆ CD: -1/2, Âˆ BC: 1/2, Âˆ AP: 1/2, Âˆ AS: -1/2}
| Premise AS ∥ DS gives a linear equation with coefficients {Âˆ AS: 1, Âˆ DS: -1}
| Then {Âˆ BP: -1/2, Âˆ BQ: -1/2, Âˆ PQ: 1, Âˆ DR: 1/2, Âˆ DS: 1/2, Âˆ RS: -1, Âˆ CD: -1/2, Âˆ BC: 1/2, Âˆ AP: 1/2, Âˆ AS: -1/2} + 1/2 x {Âˆ AS: 1, Âˆ DS: -1}
|    = {Âˆ BP: -1/2, Âˆ BQ: -1/2, Âˆ PQ: 1, Âˆ DR: 1/2, Âˆ RS: -1, Âˆ CD: -1/2, Âˆ BC: 1/2, Âˆ AP: 1/2}
| Premise BP ∥ AP gives a linear equation with coefficients {Âˆ AP: 1, Âˆ BP: -1}
| Then {Âˆ BP: -1/2, Âˆ BQ: -1/2, Âˆ PQ: 1, Âˆ DR: 1/2, Âˆ RS: -1, Âˆ CD: -1/2, Âˆ BC: 1/2, Âˆ AP: 1/2} + -1/2 x {Âˆ AP: 1, Âˆ BP: -1}
|    = {Âˆ BQ: -1/2, Âˆ PQ: 1, Âˆ DR: 1/2, Âˆ RS: -1, Âˆ CD: -1/2, Âˆ BC: 1/2}
| Premise BQ ∥ BC gives a linear equation with coefficients {Âˆ BC: 1, Âˆ BQ: -1}
| Then {Âˆ BQ: -1/2, Âˆ PQ: 1, Âˆ DR: 1/2, Âˆ RS: -1, Âˆ CD: -1/2, Âˆ BC: 1/2} + -1/2 x {Âˆ BC: 1, Âˆ BQ: -1}
|    = {Âˆ PQ: 1, Âˆ DR: 1/2, Âˆ RS: -1, Âˆ CD: -1/2}
| Premise CR ∥ CD gives a linear equation with coefficients {Âˆ CD: 1, Âˆ CR: -1}
| Then {Âˆ PQ: 1, Âˆ DR: 1/2, Âˆ RS: -1, Âˆ CD: -1/2} + 1/2 x {Âˆ CD: 1, Âˆ CR: -1}
|    = {Âˆ PQ: 1, Âˆ DR: 1/2, Âˆ RS: -1, Âˆ CR: -1/2}
| Premise DR ∥ CR gives a linear equation with coefficients {Âˆ CR: 1, Âˆ DR: -1}
| Then {Âˆ PQ: 1, Âˆ DR: 1/2, Âˆ RS: -1, Âˆ CR: -1/2} + 1/2 x {Âˆ CR: 1, Âˆ DR: -1}
|    = {Âˆ PQ: 1, Âˆ RS: -1}
We are left with a linear equation with coefficients {Âˆ PQ: 1, Âˆ RS: -1} that gives PQ ∥ RS



045. | Angle Chasing to prove QR ∥ PS:
| Premise ∠(AP,PS) = ∠(PS,AS) gives a linear equation with coefficients {Âˆ AP: -1, Âˆ AS: -1, Âˆ PS: 2}
| Premise ∠(CQ,QR) = ∠(QR,CR) gives a linear equation with coefficients {Âˆ CQ: -1, Âˆ CR: -1, Âˆ QR: 2}
| Then {Âˆ AP: -1/2, Âˆ AS: -1/2, Âˆ PS: 1} + -1/2 x {Âˆ CQ: -1, Âˆ CR: -1, Âˆ QR: 2}
|    = {Âˆ AP: -1/2, Âˆ AS: -1/2, Âˆ PS: 1, Âˆ CQ: 1/2, Âˆ CR: 1/2, Âˆ QR: -1}
| Premise AB ∥ CD gives a linear equation with coefficients {Âˆ AB: 1, Âˆ CD: -1}
| Then {Âˆ AP: -1/2, Âˆ AS: -1/2, Âˆ PS: 1, Âˆ CQ: 1/2, Âˆ CR: 1/2, Âˆ QR: -1} + 1/2 x {Âˆ AB: 1, Âˆ CD: -1}
|    = {Âˆ AP: -1/2, Âˆ AS: -1/2, Âˆ PS: 1, Âˆ CQ: 1/2, Âˆ CR: 1/2, Âˆ QR: -1, Âˆ AB: 1/2, Âˆ CD: -1/2}
| Premise AD ∥ BC gives a linear equation with coefficients {Âˆ AD: 1, Âˆ BC: -1}
| Then {Âˆ AP: -1/2, Âˆ AS: -1/2, Âˆ PS: 1, Âˆ CQ: 1/2, Âˆ CR: 1/2, Âˆ QR: -1, Âˆ AB: 1/2, Âˆ CD: -1/2} + 1/2 x {Âˆ AD: 1, Âˆ BC: -1}
|    = {Âˆ AP: -1/2, Âˆ AS: -1/2, Âˆ PS: 1, Âˆ CQ: 1/2, Âˆ CR: 1/2, Âˆ QR: -1, Âˆ AB: 1/2, Âˆ CD: -1/2, Âˆ AD: 1/2, Âˆ BC: -1/2}
| Premise AP ∥ AB gives a linear equation with coefficients {Âˆ AB: 1, Âˆ AP: -1}
| Then {Âˆ AP: -1/2, Âˆ AS: -1/2, Âˆ PS: 1, Âˆ CQ: 1/2, Âˆ CR: 1/2, Âˆ QR: -1, Âˆ AB: 1/2, Âˆ CD: -1/2, Âˆ AD: 1/2, Âˆ BC: -1/2} + -1/2 x {Âˆ AB: 1, Âˆ AP: -1}
|    = {Âˆ AS: -1/2, Âˆ PS: 1, Âˆ CQ: 1/2, Âˆ CR: 1/2, Âˆ QR: -1, Âˆ CD: -1/2, Âˆ AD: 1/2, Âˆ BC: -1/2}
| Premise AS ∥ AD gives a linear equation with coefficients {Âˆ AD: 1, Âˆ AS: -1}
| Then {Âˆ AS: -1/2, Âˆ PS: 1, Âˆ CQ: 1/2, Âˆ CR: 1/2, Âˆ QR: -1, Âˆ CD: -1/2, Âˆ AD: 1/2, Âˆ BC: -1/2} + -1/2 x {Âˆ AD: 1, Âˆ AS: -1}
|    = {Âˆ PS: 1, Âˆ CQ: 1/2, Âˆ CR: 1/2, Âˆ QR: -1, Âˆ CD: -1/2, Âˆ BC: -1/2}
| Premise BQ ∥ BC gives a linear equation with coefficients {Âˆ BC: 1, Âˆ BQ: -1}
| Then {Âˆ PS: 1, Âˆ CQ: 1/2, Âˆ CR: 1/2, Âˆ QR: -1, Âˆ CD: -1/2, Âˆ BC: -1/2} + 1/2 x {Âˆ BC: 1, Âˆ BQ: -1}
|    = {Âˆ PS: 1, Âˆ CQ: 1/2, Âˆ CR: 1/2, Âˆ QR: -1, Âˆ CD: -1/2, Âˆ BQ: -1/2}
| Premise CQ ∥ BQ gives a linear equation with coefficients {Âˆ BQ: 1, Âˆ CQ: -1}
| Then {Âˆ PS: 1, Âˆ CQ: 1/2, Âˆ CR: 1/2, Âˆ QR: -1, Âˆ CD: -1/2, Âˆ BQ: -1/2} + 1/2 x {Âˆ BQ: 1, Âˆ CQ: -1}
|    = {Âˆ PS: 1, Âˆ CR: 1/2, Âˆ QR: -1, Âˆ CD: -1/2}
| Premise CR ∥ CD gives a linear equation with coefficients {Âˆ CD: 1, Âˆ CR: -1}
| Then {Âˆ PS: 1, Âˆ CR: 1/2, Âˆ QR: -1, Âˆ CD: -1/2} + 1/2 x {Âˆ CD: 1, Âˆ CR: -1}
|    = {Âˆ PS: 1, Âˆ QR: -1}
We are left with a linear equation with coefficients {Âˆ PS: 1, Âˆ QR: -1} that gives QR ∥ PS



046. | Angle Chasing to prove PQ ⟂ QR:
| Premise ∠(BP,PQ) = ∠(PQ,BQ) gives a linear equation with coefficients {Âˆ BP: -1, Âˆ BQ: -1, Âˆ PQ: 2}
| Premise ∠(CQ,QR) = ∠(QR,CR) gives a linear equation with coefficients {Âˆ CQ: -1, Âˆ CR: -1, Âˆ QR: 2}
| Then {Âˆ BP: -1/2, Âˆ BQ: -1/2, Âˆ PQ: 1} + -1/2 x {Âˆ CQ: -1, Âˆ CR: -1, Âˆ QR: 2}
|    = {Âˆ BP: -1/2, Âˆ BQ: -1/2, Âˆ PQ: 1, Âˆ CQ: 1/2, Âˆ CR: 1/2, Âˆ QR: -1}
| Premise AB ∥ CD gives a linear equation with coefficients {Âˆ AB: 1, Âˆ CD: -1}
| Then {Âˆ BP: -1/2, Âˆ BQ: -1/2, Âˆ PQ: 1, Âˆ CQ: 1/2, Âˆ CR: 1/2, Âˆ QR: -1} + 1/2 x {Âˆ AB: 1, Âˆ CD: -1}
|    = {Âˆ BP: -1/2, Âˆ BQ: -1/2, Âˆ PQ: 1, Âˆ CQ: 1/2, Âˆ CR: 1/2, Âˆ QR: -1, Âˆ AB: 1/2, Âˆ CD: -1/2}
| Premise AP ∥ AB gives a linear equation with coefficients {Âˆ AB: 1, Âˆ AP: -1}
| Then {Âˆ BP: -1/2, Âˆ BQ: -1/2, Âˆ PQ: 1, Âˆ CQ: 1/2, Âˆ CR: 1/2, Âˆ QR: -1, Âˆ AB: 1/2, Âˆ CD: -1/2} + -1/2 x {Âˆ AB: 1, Âˆ AP: -1}
|    = {Âˆ BP: -1/2, Âˆ BQ: -1/2, Âˆ PQ: 1, Âˆ CQ: 1/2, Âˆ CR: 1/2, Âˆ QR: -1, Âˆ CD: -1/2, Âˆ AP: 1/2}
| Premise BP ∥ AP gives a linear equation with coefficients {Âˆ AP: 1, Âˆ BP: -1}
| Then {Âˆ BP: -1/2, Âˆ BQ: -1/2, Âˆ PQ: 1, Âˆ CQ: 1/2, Âˆ CR: 1/2, Âˆ QR: -1, Âˆ CD: -1/2, Âˆ AP: 1/2} + -1/2 x {Âˆ AP: 1, Âˆ BP: -1}
|    = {Âˆ BQ: -1/2, Âˆ PQ: 1, Âˆ CQ: 1/2, Âˆ CR: 1/2, Âˆ QR: -1, Âˆ CD: -1/2}
| Premise CQ ∥ BQ gives a linear equation with coefficients {Âˆ BQ: 1, Âˆ CQ: -1}
| Then {Âˆ BQ: -1/2, Âˆ PQ: 1, Âˆ CQ: 1/2, Âˆ CR: 1/2, Âˆ QR: -1, Âˆ CD: -1/2} + 1/2 x {Âˆ BQ: 1, Âˆ CQ: -1}
|    = {Âˆ PQ: 1, Âˆ CR: 1/2, Âˆ QR: -1, Âˆ CD: -1/2}
| Premise CR ∥ CD gives a linear equation with coefficients {Âˆ CD: 1, Âˆ CR: -1}
| Then {Âˆ PQ: 1, Âˆ CR: 1/2, Âˆ QR: -1, Âˆ CD: -1/2} + 1/2 x {Âˆ CD: 1, Âˆ CR: -1}
|    = {Âˆ PQ: 1, Âˆ QR: -1}
We are left with a linear equation with coefficients {Âˆ PQ: 1, Âˆ QR: -1} that gives PQ ⟂ QR

End of proof.


## G4: Right triangle midpoint squared-length sum

(c). In ΔABC, ∠ABC = 90°. If D and E are the mid-points of the sides BC and AB respectively, prove that AD² + CE² = 5 DE². [4]

Exact input:

```json
{
  "id": "G4",
  "bank_id": "PD-MATH-IX-007",
  "description": "Right triangle midpoint squared-length sum",
  "points": {
    "a": [
      0,
      3.9
    ],
    "b": [
      0,
      0
    ],
    "c": [
      5.3,
      0
    ],
    "d": [
      2.65,
      0
    ],
    "e": [
      0,
      1.95
    ]
  },
  "assumptions": [
    "perp a b b c",
    "midp d b c",
    "midp e a b"
  ],
  "goals": [
    "lequation 1 a d * a d 1 c e * c e -5 d e * d e 0"
  ],
  "translation": "AD^2+CE^2-5DE^2=0 is represented with Newclid's length-equation predicate."
}
```

Output:

```json
{
  "id": "G4",
  "description": "Right triangle midpoint squared-length sum",
  "llm_api_calls": 0,
  "llm_api_tokens": 0,
  "counted_in_production_metrics": false,
  "stage": "build_solver",
  "status": "ERROR",
  "error_type": "NotImplementedError",
  "error": "LengthEquationPredicate is not implemented",
  "independently_checked": false,
  "seconds": 10.169,
  "production_status": "UNSUPPORTED",
  "production_reason": "No audited formalization and reusable derivation route is implemented for this question."
}
```


## G5: Rectangle interior point: opposite squared-distance sums

X. (a) If O is any point in the interior of a rectangle ABCD. Prove that \( \mathrm{OA}^2 + \mathrm{OC}^2 = \mathrm{OB}^2 + \mathrm{OD}^2 \) [5]

Exact input:

```json
{
  "id": "G5",
  "bank_id": "PD-MATH-IX-024",
  "description": "Rectangle interior point: opposite squared-distance sums",
  "points": {
    "a": [
      0,
      0
    ],
    "b": [
      5.9,
      0
    ],
    "c": [
      5.9,
      3.2
    ],
    "d": [
      0,
      3.2
    ],
    "o": [
      1.7,
      1.1
    ]
  },
  "assumptions": [
    "para a b c d",
    "para a d b c",
    "perp a b b c"
  ],
  "goals": [
    "lequation 1 o a * o a 1 o c * o c -1 o b * o b -1 o d * o d 0"
  ],
  "translation": "Rectangle expanded into parallelism and a right angle. O is inside the sample diagram; the equality also holds outside, so no stronger location premise is needed."
}
```

Output:

```json
{
  "id": "G5",
  "description": "Rectangle interior point: opposite squared-distance sums",
  "llm_api_calls": 0,
  "llm_api_tokens": 0,
  "counted_in_production_metrics": false,
  "stage": "build_solver",
  "status": "ERROR",
  "error_type": "NotImplementedError",
  "error": "LengthEquationPredicate is not implemented",
  "independently_checked": false,
  "seconds": 9.05,
  "production_status": "UNSUPPORTED",
  "production_reason": "No audited formalization and reusable derivation route is implemented for this question."
}
```


## N1: False trigonometric claim; must not solve

Exact input:

```json
{
  "id": "N1",
  "lhs": "sec(A)**2-tan(A)**2",
  "rhs": "2",
  "description": "False trigonometric claim; must not solve"
}
```

Output:

```json
{
  "id": "N1",
  "description": "False trigonometric claim; must not solve",
  "llm_api_calls": 0,
  "llm_api_tokens": 0,
  "counted_in_production_metrics": false,
  "status": "COUNTEREXAMPLE",
  "trace": [],
  "diagnostics": {
    "counterexample": {
      "angle": "pi/6",
      "lhs": "1",
      "rhs": "2"
    }
  },
  "domain_conditions": [],
  "independently_checked": false,
  "seconds": 1.643
}
```


## N2: Generic triangle falsely claimed to have equal sides

Exact input:

```json
{
  "id": "N2",
  "bank_id": null,
  "description": "Generic triangle falsely claimed to have equal sides",
  "points": {
    "a": [
      0,
      0
    ],
    "b": [
      4.7,
      0
    ],
    "c": [
      1.2,
      3.1
    ]
  },
  "assumptions": [
    "ncoll a b c"
  ],
  "goals": [
    "cong a b a c"
  ],
  "translation": "Negative control: no equal-side assumption."
}
```

Output:

```json
{
  "id": "N2",
  "description": "Generic triangle falsely claimed to have equal sides",
  "llm_api_calls": 0,
  "llm_api_tokens": 0,
  "counted_in_production_metrics": false,
  "stage": "build_solver",
  "status": "ERROR",
  "error_type": "ProofBuildError",
  "error": "Goal cong a b a c is numerically false.",
  "independently_checked": false,
  "seconds": 11.067
}
```


LLM boundary for every worker: request=None; response=None; runtime API calls=0; runtime API tokens=0. Input preparation and this report's interpretation use the surrounding chat and are excluded. No LLM-only baseline was run.
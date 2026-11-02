"""Automatic, bounded search for single-angle rational trig identities.

Run: python automatic_trig_solver.py
Requires SymPy. No model calls and no per-question solution sequences.
The rule profile is illustrative; board/year approval remains separate.
"""
import heapq
import itertools
import json
import time
from functools import lru_cache
from pathlib import Path
import sympy as s

A = s.Symbol('A', real=True)
S, C, T, K, Q, R, Z = s.symbols('S C T K Q R Z')
ATOMS = {s.sin(A): S, s.cos(A): C, s.tan(A): T,
         s.cot(A): K, s.sec(A): Q, s.csc(A): R}
BACK = {v: k for k, v in ATOMS.items()}
TO_SC = {s.sin(A): S, s.cos(A): C, s.tan(A): S/C,
         s.cot(A): C/S, s.sec(A): 1/C, s.csc(A): 1/S}
ENV = {'A': A, 'sin': s.sin, 'cos': s.cos, 'tan': s.tan,
       'cot': s.cot, 'sec': s.sec, 'csc': s.csc}


def supported(e):
    return (not e.free_symbols - {A}
            and not e.atoms(s.Function) - set(ATOMS)
            and all(p.exp.is_Integer for p in e.atoms(s.Pow))
            and not e.has(s.zoo, s.oo, -s.oo, s.nan))


@lru_cache(None)
def algebra(e, operation):
    # Algebra routines see independent symbols, so they cannot silently
    # apply a trig identity or change an angle.
    p = e.xreplace(ATOMS)
    return {'expand': s.expand, 'factor': s.factor,
            'cancel': s.cancel, 'together': s.together}[operation](p).xreplace(BACK)


@lru_cache(None)
def sc(e):
    return s.cancel(e.xreplace(TO_SC))


@lru_cache(None)
def algebra_difference(a, b):
    return s.cancel((a-b).xreplace(ATOMS))


@lru_cache(None)
def reciprocal_difference(a, b):
    # No Pythagorean identity is used in this goal test.
    return s.cancel(sc(a)-sc(b))


@lru_cache(None)
def exact_equal(a, b):
    n, _ = s.fraction(s.cancel(sc(a)-sc(b)))
    return s.groebner([S*S+C*C-1], S, C).reduce(s.expand(n))[1] == 0


def denominator_factors(e):
    """Retain original poles, even if cancel() would remove them."""
    polynomials = []
    for f in e.atoms(s.Function):
        if f.func in (s.tan, s.sec):
            polynomials.append(C)
        elif f.func in (s.cot, s.csc):
            polynomials.append(S)
    for p in e.atoms(s.Pow):
        if p.exp < 0:
            n, _ = s.fraction(sc(p.base))
            polynomials.append(n)
    factors = set()
    for p in polynomials:
        for factor, _ in s.factor_list(p, S, C)[1]:
            factors.add(factor)
    return tuple(sorted(factors, key=str))


@lru_cache(None)
def domain_safe(e, original_factors):
    if not supported(e):
        return False
    original_product = s.prod(original_factors)
    for f in denominator_factors(e):
        if f in original_factors:
            continue
        # A certificate that f cannot vanish on the unit circle while
        # every original denominator remains nonzero. Conservative:
        # failure to obtain this certificate blocks the proposed state.
        basis = s.groebner([S*S+C*C-1, f, Z*original_product-1], S, C, Z)
        if list(basis) != [s.Integer(1)]:
            return False
    return True


def trig_normalize(e):
    return e.xreplace({s.tan(A): s.sin(A)/s.cos(A),
                      s.cot(A): s.cos(A)/s.sin(A),
                      s.sec(A): 1/s.cos(A), s.csc(A): 1/s.sin(A)})


def even_power(e, function, replacement):
    mapping = {}
    for p in e.atoms(s.Pow):
        if p.base == function and p.exp > 0 and p.exp % 2 == 0:
            mapping[p] = replacement**(p.exp//2)
    return e.xreplace(mapping)


# These reusable generators define the entire permitted search space.
RULES = {
    'algebra_expand': ('Expand algebraically.', lambda e: algebra(e, 'expand')),
    'algebra_factor': ('Combine and factor the algebraic expression.', lambda e: algebra(e, 'factor')),
    'algebra_cancel': ('Simplify the algebraic fraction.', lambda e: algebra(e, 'cancel')),
    'algebra_common_denominator': ('Take a common denominator.', lambda e: algebra(e, 'together')),
    'reciprocal_quotient': ('Use the reciprocal and quotient identities.', trig_normalize),
    'pythagorean_sum': ('Use sin² A + cos² A = 1.',
                         lambda e: e.subs(s.sin(A)**2+s.cos(A)**2, 1)),
    'pythagorean_complement_sin': ('Use 1 - sin² A = cos² A.',
                         lambda e: e.subs(1-s.sin(A)**2, s.cos(A)**2)),
    'pythagorean_complement_cos': ('Use 1 - cos² A = sin² A.',
                         lambda e: e.subs(1-s.cos(A)**2, s.sin(A)**2)),
    'pythagorean_even_sin': ('Use sin² A = 1 - cos² A in the even powers.',
                         lambda e: even_power(e, s.sin(A), 1-s.cos(A)**2)),
    'pythagorean_even_cos': ('Use cos² A = 1 - sin² A in the even powers.',
                         lambda e: even_power(e, s.cos(A), 1-s.sin(A)**2)),
    'secant_identity': ('Use sec² A = 1 + tan² A.',
                         lambda e: e.subs(s.sec(A)**2, 1+s.tan(A)**2)),
    'cosecant_identity': ('Use cosec² A = 1 + cot² A.',
                         lambda e: e.subs(s.csc(A)**2, 1+s.cot(A)**2)),
}


@lru_cache(None)
def candidates(e):
    seen = {e}
    result = []
    for rule, (reason, operation) in RULES.items():
        new = operation(e)
        if new not in seen and s.count_ops(new) <= 100 and supported(new):
            seen.add(new)
            result.append((rule, reason, new))
    return tuple(result)


def verified_edge(before, after, rule, domain):
    if rule == 'algebra_finish':
        allowed = algebra_difference(before, after) == 0
    elif rule == 'reciprocal_quotient_finish':
        allowed = reciprocal_difference(before, after) == 0
    elif rule in RULES:
        allowed = RULES[rule][1](before) == after
    else:
        return False
    return allowed and domain_safe(after, domain) and exact_equal(before, after)


@lru_cache(None)
def score(e, goal):
    # This is a search heuristic, not mathematical evidence. A state can
    # temporarily become longer; all edges still need verification.
    delta = algebra_difference(e, goal)
    return float(s.count_ops(e) + s.count_ops(delta)/2)


def find_counterexample(lhs, rhs):
    for angle in (s.pi/6, s.pi/4, s.pi/3, -s.pi/6, 2*s.pi/3):
        left, right = s.simplify(lhs.subs(A, angle)), s.simplify(rhs.subs(A, angle))
        if not (left-right).has(s.zoo, s.oo, s.nan) and s.simplify(left-right) != 0:
            return {'angle': str(angle), 'lhs': str(left), 'rhs': str(right)}
    return None


def solve(lhs, rhs, max_states=400, max_depth=8, seconds=18, extra_domain=()):
    start = time.monotonic()
    if not supported(lhs) or not supported(rhs):
        return {'status': 'UNSUPPORTED', 'reason': 'Only rational trig expressions of one angle are supported.'}
    domain = tuple(sorted(set(denominator_factors(lhs)+denominator_factors(rhs)+tuple(extra_domain)), key=str))
    if not exact_equal(lhs, rhs):
        counterexample = find_counterexample(lhs, rhs)
        return {'status': 'COUNTEREXAMPLE' if counterexample else 'NOT_VERIFIED',
                'counterexample': counterexample}
    queue, serial, visited, parent = [], itertools.count(), set(), {}
    # Search from either side: a school proof may start with LHS or RHS.
    for side, value, goal in [('LHS', lhs, rhs), ('RHS', rhs, lhs)]:
        heapq.heappush(queue, (score(value, goal), next(serial), 0, side, value, goal))
        parent[(side, value)] = None
    explored = 0
    while queue and explored < max_states and time.monotonic()-start < seconds:
        _, _, depth, side, current, goal = heapq.heappop(queue)
        key = side, current
        if key in visited:
            continue
        visited.add(key)
        explored += 1
        finish_rule = None
        if algebra_difference(current, goal) == 0:
            finish_rule, finish_reason = 'algebra_finish', 'Simplify algebraically to obtain the other side.'
        elif reciprocal_difference(current, goal) == 0:
            finish_rule, finish_reason = 'reciprocal_quotient_finish', 'Use reciprocal/quotient identities and simplify to obtain the other side.'
        if finish_rule and verified_edge(current, goal, finish_rule, domain):
            edges = []
            while parent[key] is not None:
                previous_key, rule, reason = parent[key]
                edges.append((previous_key[1], key[1], rule, reason))
                key = previous_key
            edges.reverse()
            if current != goal:
                edges.append((current, goal, finish_rule, finish_reason))
            # Replay every edge after search, independently of parent data.
            replay_ok = all(verified_edge(a, b, r, domain) for a, b, r, _ in edges)
            if not replay_ok:
                raise RuntimeError('Proof replay failed')
            return {'status': 'SOLVED', 'starting_side': side,
                    'original_domain_factors_nonzero': [str(f) for f in domain],
                    'states_explored': explored, 'elapsed_seconds': round(time.monotonic()-start, 3),
                    'trace_replayed': replay_ok,
                    'steps': [{'before': str(a), 'after': str(b), 'rule': r,
                               'reason': reason, 'latex': s.latex(b)} for a, b, r, reason in edges]}
        if depth >= max_depth:
            continue
        for rule, reason, new in candidates(current):
            newkey = side, new
            if newkey in parent or not verified_edge(current, new, rule, domain):
                continue
            parent[newkey] = ((side, current), rule, reason)
            heapq.heappush(queue, (score(new, goal)+depth*2, next(serial), depth+1, side, new, goal))
    return {'status': 'INCONCLUSIVE', 'states_explored': explored,
            'reason': 'Search budget exhausted; no approved derivation found.',
            'elapsed_seconds': round(time.monotonic()-start, 3)}


# Inputs only: no supplied next steps, paths, or per-question tactics.
QUESTIONS = [
    ('PD-MATH-X-001', '(sin(A)+csc(A))**2+(cos(A)+sec(A))**2', '5+sec(A)**2*csc(A)**2'),
    ('PD-MATH-X-002', 'sec(A)**4*(1-sin(A)**4)-2*tan(A)**2', '1'),
    ('PD-MATH-X-004', 'sec(A)**2*csc(A)**2', 'tan(A)**2+cot(A)**2+2'),
    ('PD-MATH-X-005', '(1+sin(A))/(1-sin(A))-(1-sin(A))/(1+sin(A))', '4*tan(A)*sec(A)'),
]


def main():
    results = []
    markdown = ['# Automatically discovered trigonometry solutions', '',
                'The code received only the four question expressions and a shared rule library. No solution sequences or model calls were supplied.', '',
                'Profile: demonstration Class X identities; official board/year mapping is not audited. Expressions are compared on their common original domain. S=sin(A), C=cos(A).', '']
    for identifier, left, right in QUESTIONS:
        # Preserve poles in the input, including removable singularities.
        lhs = s.sympify(left, locals=ENV, evaluate=False)
        rhs = s.sympify(right, locals=ENV, evaluate=False)
        result = {'id': identifier, 'lhs': left, 'rhs': right, **solve(lhs, rhs)}
        results.append(result)
        print(json.dumps({k: v for k, v in result.items() if k != 'steps'}), flush=True)
        markdown += [f'## {identifier}', '', '$$'+s.latex(lhs)+' = '+s.latex(rhs)+'$$', '',
                     '**'+result['status']+'**', '']
        if result['status'] == 'SOLVED':
            initial = lhs if result['starting_side'] == 'LHS' else rhs
            markdown += ['Starting with the '+result['starting_side']+':', '', '$$'+s.latex(initial)+'$$', '']
            for step in result['steps']:
                markdown += ['$$= '+step['latex']+'$$', '', step['reason'], '']
            markdown += ['Hence proved, where the original expressions are defined.', '',
                         'Checked nonzero domain factors: '+', '.join(result['original_domain_factors_nonzero'])+'.', '',
                         f"Search explored {result['states_explored']} states; {len(result['steps'])} steps were replayed successfully.", '']
    bad_lhs = s.sympify(QUESTIONS[1][1], locals=ENV)
    new_pole = s.sympify('sin(A)/sin(A)', locals=ENV, evaluate=False)
    preserved_pole = s.sympify('cos(A)/cos(A)', locals=ENV, evaluate=False)
    controls = {
        'false_claim': solve(bad_lhs, s.Integer(2)),
        'unsupported_double_angle': solve(s.sin(2*A), 2*s.sin(A)*s.cos(A)),
        'invented_rule_rejected': not verified_edge(s.sin(A), s.sin(A), 'DOUBLE_ANGLE', ()),
        'new_zero_denominator_rejected': not verified_edge(s.Integer(1), new_pole, 'algebra_finish', ()),
        'original_removable_pole_preserved': denominator_factors(preserved_pole) == (C,)}
    print(json.dumps({'controls': controls}), flush=True)
    if (controls['false_claim']['status'] != 'COUNTEREXAMPLE'
        or controls['unsupported_double_angle']['status'] != 'UNSUPPORTED'
        or not all(controls[k] for k in ['invented_rule_rejected',
                 'new_zero_denominator_rejected', 'original_removable_pole_preserved'])):
        raise RuntimeError('Control check failed')
    report = {'sympy_version': s.__version__, 'automatic_search': True,
              'llm_calls': 0, 'rule_profile': 'Demonstration; not syllabus certified.',
              'results': results, 'controls': controls,
              'limitations': ['Four related problems do not establish 99% accuracy.',
                              'Bounded search is incomplete and may return INCONCLUSIVE for true identities.',
                              'Only one-angle rational expressions with integer powers are supported.',
                              'Explanations are rule templates, without an LLM prose pass.',
                              'Human review of pedagogical quality and official syllabus mapping remains necessary.']}
    destination = Path(__file__).resolve().parent
    (destination/'automatic_trig_run.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    markdown += ['## Controls', '', '```json', json.dumps(controls, indent=2), '```', '',
                 'This is a limited prototype. The traces need presentation review; this run does not measure 99% accuracy.']
    (destination/'automatic_trig_answers.md').write_text('\n'.join(markdown)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()

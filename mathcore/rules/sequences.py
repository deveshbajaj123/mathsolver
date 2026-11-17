"""Sequence definitions as rules: replacing T_k or S_n by its general formula."""
from __future__ import annotations

from ..equality import Theory
from ..parse import sum_class, sum_formula, term_class, term_formula
from .base import Rule, register

REASONS = {
    ("term", "ap"): "Use the general term $T_k = a + (k-1)d$.",
    ("sum", "ap"): r"Use $S_n = \frac{n}{2}[2a + (n-1)d]$.",
    ("term", "gp"): "Use the general term $T_k = ar^{k-1}$.",
    ("sum", "gp"): r"Use $S_n = \frac{a(r^n - 1)}{r - 1}$.",
}


def _formula_rule(which: str, kind: str):
    cls_of, formula = (term_class, term_formula) if which == "term" else (sum_class, sum_formula)

    def factory(theory: Theory) -> Rule:
        def transform(e):
            for name, k, a, step in theory.sequences:
                if k == kind:
                    e = e.replace(cls_of(name), lambda n, a=a, step=step: formula(kind, a, step, n))
            return e
        return Rule(f"{kind}_{which}_formula", REASONS[(which, kind)], transform, "sequence")
    return factory


for _which in ("term", "sum"):
    for _kind in ("ap", "gp"):
        register(f"{_kind}_{_which}_formula", "sequence")(_formula_rule(_which, _kind))

"""Step 3: named rewrite rules.

A rule is a transform plus the reason a student would write. Rules never decide
correctness: every application is checked by equality.exact_equal and
equality.domain_safe, and replayed again by verify.py.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

import sympy as s

from ..equality import Theory


@dataclass(frozen=True)
class Rule:
    name: str
    reason: str
    apply: Callable[[s.Expr], s.Expr]
    topic: str
    params: dict = field(default_factory=dict, compare=False, hash=False)


# name -> factory(theory, **params) -> Rule; verify.py rebuilds rules from here.
REGISTRY: dict[str, Callable[..., Rule]] = {}


def register(name: str, topic: str):
    def wrap(factory):
        REGISTRY[name] = lambda theory, **params: factory(theory, **params)
        REGISTRY[name].topic = topic
        return factory
    return wrap


def static(name: str, topic: str, reason: str, transform: Callable[[s.Expr], s.Expr]) -> None:
    REGISTRY[name] = lambda theory: Rule(name, reason, transform, topic)
    REGISTRY[name].topic = topic


def build(name: str, theory: Theory, params: dict | None = None) -> Rule:
    return REGISTRY[name](theory, **(params or {}))


def names(topic: str) -> list[str]:
    return [name for name, factory in REGISTRY.items() if factory.topic == topic]

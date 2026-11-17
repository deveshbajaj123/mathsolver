"""Importing this package registers every rule in base.REGISTRY."""
from . import algebra, calculus, indices_logs, inverse_trig, polynomial, sequences, trig, trig_compound  # noqa: F401
from .base import REGISTRY, Rule, build, names  # noqa: F401

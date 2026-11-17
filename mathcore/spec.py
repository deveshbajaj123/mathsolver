"""Step 1: the problem spec, one JSON file per question under specs/.

A spec states what is given and what is asked. It never contains solution steps.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

ASSUMPTIONS = {"real", "positive", "nonnegative", "nonzero", "integer", "complex"}
SEQUENCE_TYPES = {"ap": ("first", "difference"), "gp": ("first", "ratio")}
GOALS = {
    "prove_identity": {"lhs", "rhs"},
    "prove_from_hypotheses": {"lhs", "rhs"},
    "factor_theorem": {"polynomial", "factor", "variable"},
    "show_no_real_roots": {"polynomial", "variable"},
    "find_value": {"variable", "lhs", "rhs"},
    "solve_equation": {"variable", "lhs", "rhs", "low", "high"},
    "general_solution": {"variable", "lhs", "rhs"},
    "one_real_roots": {"variable", "polynomials"},  # at least one of these quadratics has real roots
    "only_solution": {"variable", "lhs", "rhs", "value"},  # the only real solution is variable = value
    "evaluate": {"expr"},
    "first_principles": {"function", "variable"},
    "monotonic": {"function", "variable", "direction"},
    "extremum": {"objective", "variable", "type"},  # optional: "eliminate" (variables), "claims" (lhs/rhs at the optimum)
    "geometry_jgex": {"jgex", "figure_asset_id"},
}
# A goal may state "a, b, c are in AP/GP" instead of lhs/rhs, or list several equalities as parts.
GOAL_FORMS = ("in_ap", "in_gp", "parts")
HYPOTHESES = {
    "equation": {"lhs", "rhs"},
    "in_ap": {"terms"},
    "in_gp": {"terms"},
    "equal_ratios": {"ratios"},
    "equal_roots": {"polynomial", "variable"},
}
METHODS = {None, "factor_theorem", "completing_square", "componendo_dividendo"}


class SpecError(ValueError):
    pass


@dataclass(frozen=True)
class Spec:
    id: str
    goal: dict
    variables: dict = field(default_factory=dict)      # name -> list of assumptions
    hypotheses: list = field(default_factory=list)     # see HYPOTHESES; "kind" defaults to "equation"
    sequences: dict = field(default_factory=dict)      # name -> {"type", "first", "difference" | "ratio"}
    functions: dict = field(default_factory=dict)      # y -> {"of": "x", "derivatives": ["y1", "y2"]}: y depends on x
    definitions: dict = field(default_factory=dict)    # C -> {"of": "x", "expr": "..."}: a named function C(x)
    abstract: list = field(default_factory=list)       # names of unspecified functions, e.g. f in a property of integrals
    points: dict = field(default_factory=dict)        # A -> ["x", "y"]: coordinates in declared variables
    nondegenerate: list = field(default_factory=list)  # [["A", "B", "C"]]: triangles the figure assumes are proper
    figure: list = field(default_factory=list)         # [["midpoint", "D", "B", "C"], ...]: facts checked against the coordinates
    intervals: dict = field(default_factory=dict)      # x -> ["0", "pi/4"]: x lies strictly between the two
    prescribed_method: str | None = None
    quotes: dict = field(default_factory=dict)         # field -> source words
    note: str = ""

    def to_json(self) -> dict:
        return asdict(self)

    def parts(self) -> list["Spec"]:
        """A multi-part goal becomes one spec per equality, sharing everything else."""
        if "parts" not in self.goal:
            return [self]
        base = {k: v for k, v in self.goal.items() if k != "parts"}  # a part may set its own kind
        return [from_json({**self.to_json(), "id": f"{self.id}#{i}", "goal": {**base, **part}})
                for i, part in enumerate(self.goal["parts"], 1)]


def hypothesis_kind(hypothesis: dict) -> str:
    return hypothesis.get("kind", "equation")


def from_json(data: dict) -> Spec:
    unknown = set(data) - set(Spec.__dataclass_fields__)
    if unknown:
        raise SpecError(f"Unknown spec fields: {sorted(unknown)}")
    if "id" not in data or "goal" not in data:
        raise SpecError("Spec needs id and goal")
    spec = Spec(**data)
    kind = spec.goal.get("kind")
    if kind not in GOALS:
        raise SpecError(f"Unknown goal kind {kind!r}")
    forms = [f for f in GOAL_FORMS if f in spec.goal]
    if len(forms) > 1 or (forms and kind not in ("prove_identity", "prove_from_hypotheses")):
        raise SpecError(f"Goal form {forms} not allowed for {kind}")
    if forms == ["parts"]:
        if not spec.goal["parts"] or any(set(p) - {"lhs", "rhs", "in_ap", "in_gp", "kind", "expr", "name"}
                                         for p in spec.goal["parts"]):
            raise SpecError("Each goal part needs lhs/rhs or in_ap/in_gp")
    elif forms:
        if len(spec.goal[forms[0]]) != 3:
            raise SpecError(f"{forms[0]} needs exactly three terms")
    else:
        missing = GOALS[kind] - set(spec.goal)
        if missing:
            raise SpecError(f"Goal {kind} missing {sorted(missing)}")
    for name, assumptions in spec.variables.items():
        if not name.isidentifier() or not set(assumptions) <= ASSUMPTIONS:
            raise SpecError(f"Bad variable {name}: {assumptions}")
    for name, sequence in spec.sequences.items():
        fields = SEQUENCE_TYPES.get(sequence.get("type"))
        if not name.isidentifier() or fields is None or not set(fields) <= set(sequence):
            raise SpecError(f"Bad sequence {name}: {sequence}")
        if name in spec.variables:
            raise SpecError(f"{name} is both a variable and a sequence")
    for hypothesis in spec.hypotheses:
        needed = HYPOTHESES.get(hypothesis_kind(hypothesis))
        if needed is None or not needed <= set(hypothesis):
            raise SpecError(f"Bad hypothesis: {hypothesis}")
    for name, function in spec.functions.items():
        if not name.isidentifier() or "of" not in function or not all(d.isidentifier() for d in function.get("derivatives", [])):
            raise SpecError(f"Bad function {name}: {function}")
    for name, definition in spec.definitions.items():
        if not name.isidentifier() or not {"of", "expr"} <= set(definition):
            raise SpecError(f"Bad definition {name}: {definition}")
    for name, point in spec.points.items():
        if not name.isidentifier() or name in spec.variables or len(point) != 2:
            raise SpecError(f"Bad point {name}: {point}")
    for triangle in spec.nondegenerate:
        if len(triangle) != 3 or not set(triangle) <= set(spec.points):
            raise SpecError(f"Bad nondegenerate triangle {triangle}")
    for name, bounds in spec.intervals.items():
        if name not in spec.variables or len(bounds) != 2:
            raise SpecError(f"Bad interval for {name}: {bounds}")
    from .figure import RELATIONS
    for fact in spec.figure:
        if not fact or fact[0] not in RELATIONS or len(fact) - 1 != RELATIONS[fact[0]][0] \
                or not set(fact[1:]) <= set(spec.points):
            raise SpecError(f"Bad figure fact {fact}")
    if spec.points and not spec.figure and len(spec.points) > 2:
        raise SpecError("A coordinate spec must list the figure facts its coordinates encode (\"figure\")")
    if kind == "prove_from_hypotheses" and not spec.hypotheses:
        raise SpecError("prove_from_hypotheses needs at least one hypothesis")
    if spec.prescribed_method not in METHODS:
        raise SpecError(f"Unknown prescribed method {spec.prescribed_method!r}")
    return spec


def load(path: Path) -> Spec:
    return from_json(json.loads(path.read_text(encoding="utf-8")))


def load_dir(directory: Path) -> dict[str, Spec]:
    specs = {}
    for path in sorted(directory.glob("*.json")):
        spec = load(path)
        if path.stem != spec.id:
            raise SpecError(f"{path.name} holds spec {spec.id}")
        specs[spec.id] = spec
    return specs

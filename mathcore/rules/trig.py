"""Trigonometric rules, generalised from automatic_trig_solver.RULES to every angle
in the expression. Compound, double and half angles are in trig_compound.py."""
from __future__ import annotations

import sympy as s

from ..equality import trig_angles
from .base import static


def each_angle(make_mapping):
    def transform(e: s.Expr) -> s.Expr:
        for angle in trig_angles(e):
            e = make_mapping(e, angle)
        return e
    return transform


def even_power(function, replacement):
    def mapping(e, u):
        powers = {p: replacement(u)**(p.exp//2) for p in e.atoms(s.Pow)
                  if p.base == function(u) and p.exp.is_Integer and p.exp != 0 and p.exp % 2 == 0}
        return e.xreplace(powers)
    return mapping


static("reciprocal_quotient", "trig", "Use the reciprocal and quotient identities.",
       each_angle(lambda e, u: e.xreplace({s.tan(u): s.sin(u)/s.cos(u), s.cot(u): s.cos(u)/s.sin(u),
                                           s.sec(u): 1/s.cos(u), s.csc(u): 1/s.sin(u)})))
static("pythagorean_sum", "trig", "Use sin² A + cos² A = 1.",
       each_angle(lambda e, u: e.subs(s.sin(u)**2 + s.cos(u)**2, 1)))
static("pythagorean_complement_sin", "trig", "Use 1 - sin² A = cos² A.",
       each_angle(lambda e, u: e.subs(1 - s.sin(u)**2, s.cos(u)**2)))
static("pythagorean_complement_cos", "trig", "Use 1 - cos² A = sin² A.",
       each_angle(lambda e, u: e.subs(1 - s.cos(u)**2, s.sin(u)**2)))
static("pythagorean_even_sin", "trig", "Use sin² A = 1 - cos² A in the even powers.",
       each_angle(even_power(s.sin, lambda u: 1 - s.cos(u)**2)))
static("pythagorean_even_cos", "trig", "Use cos² A = 1 - sin² A in the even powers.",
       each_angle(even_power(s.cos, lambda u: 1 - s.sin(u)**2)))
static("secant_identity", "trig", "Use sec² A = 1 + tan² A.",
       each_angle(lambda e, u: e.subs(s.sec(u)**2, 1 + s.tan(u)**2)))
static("cosecant_identity", "trig", "Use cosec² A = 1 + cot² A.",
       each_angle(lambda e, u: e.subs(s.csc(u)**2, 1 + s.cot(u)**2)))

"""Properties and their formulas, e.g., probability and reward operators of PCTL and CSL."""

from stormpy import developer as _developer
from stormpy.developer import logic as _bindings

# Properties and optimization directions are bound with the core library of Storm
Property = _developer.Property
OptimizationDirection = _developer.OptimizationDirection

ComparisonType = _bindings.ComparisonType
BinaryBooleanOperatorType = _bindings.BinaryBooleanOperatorType

# Formulas
Formula = _bindings.Formula
# Path formulas
PathFormula = _bindings.PathFormula
UnaryPathFormula = _bindings.UnaryPathFormula
EventuallyFormula = _bindings.EventuallyFormula
GloballyFormula = _bindings.GloballyFormula
BinaryPathFormula = _bindings.BinaryPathFormula
BoundedUntilFormula = _bindings.BoundedUntilFormula
UntilFormula = _bindings.UntilFormula
ConditionalFormula = _bindings.ConditionalFormula
# Reward path formulas
CumulativeRewardFormula = _bindings.CumulativeRewardFormula
DiscountedCumulativeRewardFormula = _bindings.DiscountedCumulativeRewardFormula
DiscountedTotalRewardFormula = _bindings.DiscountedTotalRewardFormula
InstantaneousRewardFormula = _bindings.InstantaneousRewardFormula
LongRunAverageRewardFormula = _bindings.LongRunAverageRewardFormula
# State formulas
StateFormula = _bindings.StateFormula
AtomicExpressionFormula = _bindings.AtomicExpressionFormula
AtomicLabelFormula = _bindings.AtomicLabelFormula
BooleanLiteralFormula = _bindings.BooleanLiteralFormula
UnaryStateFormula = _bindings.UnaryStateFormula
UnaryBooleanStateFormula = _bindings.UnaryBooleanStateFormula
BinaryStateFormula = _bindings.BinaryStateFormula
BinaryBooleanStateFormula = _bindings.BinaryBooleanStateFormula
# Operator formulas
OperatorFormula = _bindings.OperatorFormula
ProbabilityOperatorFormula = _bindings.ProbabilityOperatorFormula
RewardOperatorFormula = _bindings.RewardOperatorFormula
TimeOperatorFormula = _bindings.TimeOperatorFormula
LongRunAverageOperatorFormula = _bindings.LongRunAverageOperatorFormula
# Multi-objective and game formulas
MultiObjectiveFormula = _bindings.MultiObjectiveFormula
GameFormula = _bindings.GameFormula

__all__ = [
    "Property",
    "OptimizationDirection",
    "ComparisonType",
    "BinaryBooleanOperatorType",
    # Formulas
    "Formula",
    "PathFormula",
    "UnaryPathFormula",
    "EventuallyFormula",
    "GloballyFormula",
    "BinaryPathFormula",
    "BoundedUntilFormula",
    "UntilFormula",
    "ConditionalFormula",
    "CumulativeRewardFormula",
    "DiscountedCumulativeRewardFormula",
    "DiscountedTotalRewardFormula",
    "InstantaneousRewardFormula",
    "LongRunAverageRewardFormula",
    "StateFormula",
    "AtomicExpressionFormula",
    "AtomicLabelFormula",
    "BooleanLiteralFormula",
    "UnaryStateFormula",
    "UnaryBooleanStateFormula",
    "BinaryStateFormula",
    "BinaryBooleanStateFormula",
    "OperatorFormula",
    "ProbabilityOperatorFormula",
    "RewardOperatorFormula",
    "TimeOperatorFormula",
    "LongRunAverageOperatorFormula",
    "MultiObjectiveFormula",
    "GameFormula",
]

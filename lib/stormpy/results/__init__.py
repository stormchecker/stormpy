"""Model checking results, values with sound bounds and aggregation options."""

from stormpy import developer as _bindings

CheckResult = _bindings.CheckResult
QualitativeCheckResult = _bindings.QualitativeCheckResult
QuantitativeCheckResult = _bindings.QuantitativeCheckResult.publish_as("stormpy.results.QuantitativeCheckResult")
ExplicitQualitativeCheckResult = _bindings.ExplicitQualitativeCheckResult.publish_as("stormpy.results.ExplicitQualitativeCheckResult")
ExplicitQuantitativeCheckResult = _bindings.ExplicitQuantitativeCheckResult.publish_as("stormpy.results.ExplicitQuantitativeCheckResult")
SymbolicQualitativeCheckResult = _bindings.SymbolicQualitativeCheckResult.publish_as("stormpy.results.SymbolicQualitativeCheckResult")
SymbolicQuantitativeCheckResult = _bindings.SymbolicQuantitativeCheckResult.publish_as("stormpy.results.SymbolicQuantitativeCheckResult")
HybridQuantitativeCheckResult = _bindings.HybridQuantitativeCheckResult.publish_as("stormpy.results.HybridQuantitativeCheckResult")
ParetoCurveCheckResult = _bindings.ParetoCurveCheckResult.publish_as("stormpy.results.ParetoCurveCheckResult")
ExplicitParetoCurveCheckResult = _bindings.ExplicitParetoCurveCheckResult.publish_as("stormpy.results.ExplicitParetoCurveCheckResult")
SolutionBounds = _bindings.SolutionBounds.publish_as("stormpy.results.SolutionBounds")
AggregatedValue = _bindings.AggregatedValue.publish_as("stormpy.results.AggregatedValue")
FilterType = _bindings.FilterType

from ._bounded_value import BoundedValue

__all__ = [
    "CheckResult",
    "QualitativeCheckResult",
    "QuantitativeCheckResult",
    "ExplicitQualitativeCheckResult",
    "ExplicitQuantitativeCheckResult",
    "SymbolicQualitativeCheckResult",
    "SymbolicQuantitativeCheckResult",
    "HybridQuantitativeCheckResult",
    "ParetoCurveCheckResult",
    "ExplicitParetoCurveCheckResult",
    "SolutionBounds",
    "AggregatedValue",
    "FilterType",
    "BoundedValue",
]

"""Python bindings for the probabilistic model checker Storm.

This module provides the public API for the core functionality of Storm:
parsing symbolic models and properties, building models, model checking and transforming models.
"""

# Number types (needed by the native modules and therefore imported first)
from . import numbers

# The value types are also available directly as stormpy.X (same objects as stormpy.numbers.X).
# Must be imported before the native modules and the core modules, which look up the value types as stormpy.X
from .numbers import Interval, Polynomial, Rational, RationalFunction, RationalFunctionCoefficient, RationalInterval, RawPolynomial

from . import developer
from . import exceptions
from . import expressions, datastructures, models, io, logic
from . import utility
from . import environments

try:
    from ._version import __version__
except ImportError:
    # We're running in a tree that doesn't have a _version.py, so we don't know what our version is.
    __version__ = "unknown"

developer._set_up("")

# Import classes from developer (and republish templated classes under stormpy.X)
SymbolicModelDescription = developer.SymbolicModelDescription
JaniModelType = developer.JaniModelType

DirectEncodingParserOptions = developer.DirectEncodingParserOptions
ExplicitModelParserOptions = developer.ExplicitModelParserOptions
DirectEncodingExporterOptions = developer.DirectEncodingExporterOptions

Environment = developer.Environment
UncertaintyResolutionMode = developer.UncertaintyResolutionMode
ModelCheckerHint = developer.ModelCheckerHint
ExplicitModelCheckerHint = developer.ExplicitModelCheckerHint.publish_as("stormpy.ExplicitModelCheckerHint")

CheckResult = developer.CheckResult
QualitativeCheckResult = developer.QualitativeCheckResult
ExplicitQualitativeCheckResult = developer.ExplicitQualitativeCheckResult.publish_as("stormpy.ExplicitQualitativeCheckResult")
ExplicitQuantitativeCheckResult = developer.ExplicitQuantitativeCheckResult.publish_as("stormpy.ExplicitQuantitativeCheckResult")
SymbolicQualitativeCheckResult = developer.SymbolicQualitativeCheckResult.publish_as("stormpy.SymbolicQualitativeCheckResult")
SymbolicQuantitativeCheckResult = developer.SymbolicQuantitativeCheckResult.publish_as("stormpy.SymbolicQuantitativeCheckResult")
HybridQuantitativeCheckResult = developer.HybridQuantitativeCheckResult.publish_as("stormpy.HybridQuantitativeCheckResult")
ExplicitParetoCurveCheckResult = developer.ExplicitParetoCurveCheckResult.publish_as("stormpy.ExplicitParetoCurveCheckResult")
SolutionBounds = developer.SolutionBounds.publish_as("stormpy.SolutionBounds")
AggregatedValue = developer.AggregatedValue.publish_as("stormpy.AggregatedValue")
FilterType = developer.FilterType
PcaaWeightVectorChecker = developer.PcaaWeightVectorChecker.publish_as("stormpy.PcaaWeightVectorChecker")

BisimulationType = developer.BisimulationType
BisimulationOptions = developer.BisimulationOptions
StateLabelPreservation = developer.StateLabelPreservation
QuotientFormat = developer.QuotientFormat
EliminationLabelBehavior = developer.EliminationLabelBehavior
SubsystemBuilderOptions = developer.SubsystemBuilderOptions
SubsystemBuilderReturnType = developer.SubsystemBuilderReturnType.publish_as("stormpy.SubsystemBuilderReturnType")

# Import public functions
from .core._parsing import instantiate_constants, parse_jani_model, parse_jani_model_from_string, parse_prism_program, parse_properties, parse_property
from .core._building import BuilderOptions, build_model, build_model_from_drn, build_model_from_explicit, build_model_from_umb, build_symbolic_model
from .core._results import BoundedValue
from .core._modelchecking import Engine, create_filter, create_filter_initial_states, filter_initial_states, model_checking
from .core._analysis import (
    compute_prob01_states,
    compute_expected_number_of_visits,
    compute_steady_state_distribution,
    create_weight_vector_checker,
    topological_sort,
)
from .core._transformation import (
    add_uncertainty,
    build_submodel,
    eliminate_non_markovian_chains,
    perform_bisimulation,
    set_state_valuations,
    transform_to_discrete_time_model,
    transform_to_sparse_model,
)
from .core._io import export_to_drn, export_to_umb

__all__ = [
    # Value types (re-exported from stormpy.numbers)
    "Interval",
    "Polynomial",
    "Rational",
    "RationalFunction",
    "RationalFunctionCoefficient",
    "RationalInterval",
    "RawPolynomial",
    # Parsing
    "SymbolicModelDescription",
    "JaniModelType",
    "parse_prism_program",
    "parse_jani_model",
    "parse_jani_model_from_string",
    "parse_properties",
    "parse_property",
    "instantiate_constants",
    # Building
    "BuilderOptions",
    "DirectEncodingParserOptions",
    "ExplicitModelParserOptions",
    "build_model",
    "build_symbolic_model",
    "build_model_from_drn",
    "build_model_from_explicit",
    "build_model_from_umb",
    # Model checking
    "Engine",
    "Environment",
    "UncertaintyResolutionMode",
    "ModelCheckerHint",
    "ExplicitModelCheckerHint",
    "CheckResult",
    "QualitativeCheckResult",
    "ExplicitQualitativeCheckResult",
    "ExplicitQuantitativeCheckResult",
    "SymbolicQualitativeCheckResult",
    "SymbolicQuantitativeCheckResult",
    "HybridQuantitativeCheckResult",
    "ExplicitParetoCurveCheckResult",
    "BoundedValue",
    "SolutionBounds",
    "AggregatedValue",
    "FilterType",
    "model_checking",
    "create_filter_initial_states",
    "filter_initial_states",
    "create_filter",
    # Analysis
    "PcaaWeightVectorChecker",
    "topological_sort",
    "compute_prob01_states",
    "compute_expected_number_of_visits",
    "compute_steady_state_distribution",
    "create_weight_vector_checker",
    # Transformations
    "BisimulationType",
    "BisimulationOptions",
    "StateLabelPreservation",
    "QuotientFormat",
    "EliminationLabelBehavior",
    "SubsystemBuilderOptions",
    "SubsystemBuilderReturnType",
    "perform_bisimulation",
    "transform_to_sparse_model",
    "transform_to_discrete_time_model",
    "eliminate_non_markovian_chains",
    "build_submodel",
    "add_uncertainty",
    "set_state_valuations",
    # Export
    "DirectEncodingExporterOptions",
    "export_to_drn",
    "export_to_umb",
]

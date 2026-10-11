"""Python bindings for the probabilistic model checker Storm.

This module provides the public API for the core functionality of Storm:
parsing symbolic models and properties, building models, model checking and transforming models.
"""

# Value types (needed by the native modules and therefore imported first)
from ._config import Interval, Polynomial, Rational, RationalFunction, RationalFunctionCoefficient, RationalInterval, RawPolynomial

from . import developer
from . import exceptions
from . import logic
from . import storage

try:
    from ._version import __version__
except ImportError:
    # We're running in a tree that doesn't have a _version.py, so we don't know what our version is.
    __version__ = "unknown"

developer._set_up("")

# Re-export frequently used classes of stormpy.storage
from .storage import (
    BitVector,
    DdType,
    ModelType,
    SparseCtmc,
    SparseDtmc,
    SparseMA,
    SparseMdp,
    SparsePomdp,
    SparseSmg,
    SymbolicCtmc,
    SymbolicDtmc,
    SymbolicMA,
    SymbolicMdp,
)

# Import classes from developer (and republish templated classes under stormpy.X)
Property = developer.Property
SymbolicModelDescription = developer.SymbolicModelDescription
JaniModelType = developer.JaniModelType

DirectEncodingParserOptions = developer.DirectEncodingParserOptions
ExplicitModelParserOptions = developer.ExplicitModelParserOptions
DirectEncodingExporterOptions = developer.DirectEncodingExporterOptions

Environment = developer.Environment
EquationSolverType = developer.EquationSolverType
NativeLinearEquationSolverMethod = developer.NativeLinearEquationSolverMethod
MinMaxMethod = developer.MinMaxMethod
MultiObjectiveMethod = developer.MultiObjectiveMethod
SteadyStateDistributionAlgorithm = developer.SteadyStateDistributionAlgorithm
PrecomputationType = developer.PrecomputationType
NextStateHeuristic = developer.NextStateHeuristic
OptimizationDirection = developer.OptimizationDirection
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
PcaaWeightVectorChecker = developer.PcaaWeightVectorChecker.publish_as("stormpy.PcaaWeightVectorChecker")

BisimulationType = developer.BisimulationType
BisimulationOptions = developer.BisimulationOptions
StateLabelPreservation = developer.StateLabelPreservation
QuotientFormat = developer.QuotientFormat
EliminationLabelBehavior = developer.EliminationLabelBehavior
SubsystemBuilderOptions = developer.SubsystemBuilderOptions
SubsystemBuilderReturnType = developer.SubsystemBuilderReturnType.publish_as("stormpy.SubsystemBuilderReturnType")
ConstraintCollector = developer.ConstraintCollector.publish_as("stormpy.ConstraintCollector")

LogLevel = developer.LogLevel

# Import public functions
from .core._parsing import instantiate_constants, parse_jani_model, parse_jani_model_from_string, parse_prism_program, parse_properties
from .core._building import BuilderOptions, build_model, build_model_from_drn, build_model_from_explicit, build_model_from_umb, build_symbolic_model
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
from .core._settings import reset_timeout, set_log_level, set_timeout

__all__ = [
    # Value types
    "Interval",
    "Polynomial",
    "Rational",
    "RationalFunction",
    "RationalFunctionCoefficient",
    "RationalInterval",
    "RawPolynomial",
    # Re-exports from stormpy.storage
    "BitVector",
    "DdType",
    "ModelType",
    "SparseCtmc",
    "SparseDtmc",
    "SparseMA",
    "SparseMdp",
    "SparsePomdp",
    "SparseSmg",
    "SymbolicCtmc",
    "SymbolicDtmc",
    "SymbolicMA",
    "SymbolicMdp",
    # Parsing
    "Property",
    "SymbolicModelDescription",
    "JaniModelType",
    "parse_prism_program",
    "parse_jani_model",
    "parse_jani_model_from_string",
    "parse_properties",
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
    "EquationSolverType",
    "NativeLinearEquationSolverMethod",
    "MinMaxMethod",
    "MultiObjectiveMethod",
    "SteadyStateDistributionAlgorithm",
    "PrecomputationType",
    "NextStateHeuristic",
    "OptimizationDirection",
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
    "model_checking",
    "create_filter_initial_states",
    "filter_initial_states",
    "create_filter",
    # Analysis
    "PcaaWeightVectorChecker",
    "ConstraintCollector",
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
    # Settings
    "LogLevel",
    "set_log_level",
    "set_timeout",
    "reset_timeout",
]

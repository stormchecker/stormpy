"""Python bindings for the probabilistic model checker Storm.

This module provides convenience entry points for the core functionality of Storm:
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
from . import analysis, transformations

try:
    from ._version import __version__
except ImportError:
    # We're running in a tree that doesn't have a _version.py, so we don't know what our version is.
    __version__ = "unknown"

developer._set_up("")

# Model checking configuration and results.
from .environments import Environment

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

from .core._results import BoundedValue
from .core._filters import create_filter, create_filter_initial_states, filter_initial_states

UncertaintyResolutionMode = developer.UncertaintyResolutionMode
ModelCheckerHint = developer.ModelCheckerHint
ExplicitModelCheckerHint = developer.ExplicitModelCheckerHint.publish_as("stormpy.ExplicitModelCheckerHint")


# Import public functions
from .io import instantiate_constants, parse_jani_model, parse_jani_model_from_string, parse_prism_program
from .logic import parse_properties, parse_property
from .analysis import compute_expected_number_of_visits
from .core._building import BuilderOptions, build_model, build_model_from_drn, build_model_from_explicit, build_model_from_umb, build_symbolic_model
from .core._modelchecking import Engine, model_checking
from .transformations import add_uncertainty

__all__ = [
    # Numeric types (canonical namespace: stormpy.numbers)
    "Interval",
    "Polynomial",
    "Rational",
    "RationalFunction",
    "RationalFunctionCoefficient",
    "RationalInterval",
    "RawPolynomial",
    # Parsing shortcuts (canonical namespaces: stormpy.io and stormpy.logic)
    "parse_prism_program",
    "parse_jani_model",
    "parse_jani_model_from_string",
    "parse_properties",
    "parse_property",
    "instantiate_constants",
    # Building
    "BuilderOptions",
    "build_model",
    "build_symbolic_model",
    "build_model_from_drn",
    "build_model_from_explicit",
    "build_model_from_umb",
    # Model checking and results
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
    "SolutionBounds",
    "AggregatedValue",
    "FilterType",
    "BoundedValue",
    "create_filter",
    "create_filter_initial_states",
    "filter_initial_states",
    "model_checking",
    # Analysis shortcut (canonical namespace: stormpy.analysis)
    "compute_expected_number_of_visits",
    # Transformation shortcut (canonical namespace: stormpy.transformations)
    "add_uncertainty",
]

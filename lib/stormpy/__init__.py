"""Python bindings for the probabilistic model checker Storm.

This module provides convenience entry points for the core functionality of Storm:
parsing symbolic models and properties, building models and model checking.
"""

# Number types (needed by the native modules and therefore imported first)
from . import numbers

# The value types are also available directly as stormpy.X (same objects as stormpy.numbers.X).
# Must be imported before the native modules and the core modules, which look up the value types as stormpy.X
from .numbers import Interval, Polynomial, Rational, RationalFunction, RationalFunctionCoefficient, RationalInterval, RawPolynomial

from . import developer
from . import exceptions
from . import expressions, datastructures, models, io, logic
from . import environments
from . import results
from . import analysis, transformations

try:
    from ._version import __version__
except ImportError:
    # We're running in a tree that doesn't have a _version.py, so we don't know what our version is.
    __version__ = "unknown"

developer._set_up("")

from .environments import Environment
from .results import CheckResult
from .core._filters import create_filter, create_filter_initial_states, filter_initial_states

UncertaintyResolutionMode = developer.UncertaintyResolutionMode
ModelCheckerHint = developer.ModelCheckerHint
ExplicitModelCheckerHint = developer.ExplicitModelCheckerHint.publish_as("stormpy.ExplicitModelCheckerHint")


# Import public functions
from .io import instantiate_constants, parse_jani_model, parse_jani_model_from_string, parse_prism_program
from .logic import parse_properties, parse_property
from .core._building import BuilderOptions, build_model, build_model_from_drn, build_model_from_explicit, build_model_from_umb, build_symbolic_model
from .core._modelchecking import Engine, model_checking

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
    "create_filter",
    "create_filter_initial_states",
    "filter_initial_states",
    "model_checking",
]

"""Environments configuring the algorithms of Storm, e.g., the solvers and their precision.

Model checking uses :func:`default` unless an environment is given explicitly.
It enforces sound computations, and exact computations for exact and parametric models.
"""

from stormpy import developer as _developer
from stormpy import Rational, RationalFunction, RationalInterval
from stormpy.core._common import _value_type_of_model

Environment = _developer.Environment
# Parts of the environment
SolverEnvironment = _developer.SolverEnvironment
NativeSolverEnvironment = _developer.NativeSolverEnvironment
MinMaxSolverEnvironment = _developer.MinMaxSolverEnvironment
ModelCheckerEnvironment = _developer.ModelCheckerEnvironment
MultiObjectiveModelCheckerEnvironment = _developer.MultiObjectiveModelCheckerEnvironment
ConditionalModelCheckerEnvironment = _developer.ConditionalModelCheckerEnvironment
ExplorationEnvironment = _developer.ExplorationEnvironment
DdEnvironment = _developer.DdEnvironment
SylvanDdManagerEnvironment = _developer.SylvanDdManagerEnvironment
CuddDdManagerEnvironment = _developer.CuddDdManagerEnvironment

# Settings
EquationSolverType = _developer.EquationSolverType
NativeLinearEquationSolverMethod = _developer.NativeLinearEquationSolverMethod
MinMaxMethod = _developer.MinMaxMethod
MultiObjectiveMethod = _developer.MultiObjectiveMethod
MultiObjectivePrecisionType = _developer.MultiObjectivePrecisionType
MultiObjectiveEncodingType = _developer.MultiObjectiveEncodingType
SteadyStateDistributionAlgorithm = _developer.SteadyStateDistributionAlgorithm
ConditionalAlgorithmSetting = _developer.ConditionalAlgorithmSetting
PrecomputationType = _developer.PrecomputationType
NextStateHeuristic = _developer.NextStateHeuristic
CuddReorderingTechnique = _developer.CuddReorderingTechnique


def sound() -> Environment:
    """
    Create a new environment which enforces sound computations.

    Sound solution methods are selected.

    :return: The environment.
    """
    return _developer.get_sound_environment()


def exact() -> Environment:
    """
    Create a new environment which enforces exact computations.

    Exact solution methods are selected.
    Note that exact computations additionally require a model with exact value type, e.g., ``stormpy.build_model[stormpy.Rational]``.

    :return: The environment.
    """
    return _developer.get_exact_environment()


def default(model) -> Environment:
    """
    Create a new environment suitable for the given model.

    The environment enforces exact computations for models with exact or parametric value types
    (:class:`stormpy.Rational`, :class:`stormpy.RationalInterval`, :class:`stormpy.RationalFunction`) and sound computations otherwise.

    :param model: The model (sparse or symbolic).
    :return: The environment.
    """
    return _default_for_value_type(_value_type_of_model(model))


def _default_for_value_type(value_type: type) -> Environment:
    """Create a new environment suitable for models with the given value type."""
    if value_type in (Rational, RationalInterval, RationalFunction):
        return exact()
    return sound()


__all__ = [
    "default",
    "sound",
    "exact",
    "Environment",
    "SolverEnvironment",
    "NativeSolverEnvironment",
    "MinMaxSolverEnvironment",
    "ModelCheckerEnvironment",
    "MultiObjectiveModelCheckerEnvironment",
    "ConditionalModelCheckerEnvironment",
    "ExplorationEnvironment",
    "DdEnvironment",
    "SylvanDdManagerEnvironment",
    "CuddDdManagerEnvironment",
    "EquationSolverType",
    "NativeLinearEquationSolverMethod",
    "MinMaxMethod",
    "MultiObjectiveMethod",
    "MultiObjectivePrecisionType",
    "MultiObjectiveEncodingType",
    "SteadyStateDistributionAlgorithm",
    "ConditionalAlgorithmSetting",
    "PrecomputationType",
    "NextStateHeuristic",
    "CuddReorderingTechnique",
]

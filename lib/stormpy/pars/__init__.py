"""Parameter synthesis and model instantiation for sparse parametric models.

Create parameter regions, verify properties throughout a region, compute extremal
values, or search for satisfying parameter valuations. Instantiate models with
concrete parameter values using :class:`ModelInstantiator`. Lower-level tools are
in :mod:`stormpy.pars.developer`.
"""

from collections.abc import Iterable, Mapping
from math import isfinite as _isfinite

from . import developer
from .developer import gather_derivatives
from stormpy import Environment, Polynomial, RationalFunction, RationalFunctionCoefficient
from stormpy import developer as _developer
from stormpy import environments as _environments
from stormpy.numbers import Variable
from stormpy.logic import Formula, OptimizationDirection, Property
from stormpy.models import SparseModel
from stormpy.core._common import _formula

ParameterRegion = developer.ParameterRegion
ConstraintCollector = developer.ConstraintCollector
RegionResult = developer.RegionResult
RegionCheckEngine = developer.RegionCheckEngine
FeasibilityMethod = developer.FeasibilityMethod
FeasibilityResult = developer.FeasibilityResult
FeasibilitySynthesisResult = developer.FeasibilitySynthesisResult
ModelInstantiator = developer.ModelInstantiator.publish_as("stormpy.pars.ModelInstantiator")


def parse_region(region_string: str, parameters: Iterable[Variable]) -> ParameterRegion:
    """
    Parse a parameter region from a string.

    :param region_string: Region given as bounds for each parameter, e.g. ``"0.3<=p<=0.5,0.1<=q<=0.4"``.
    :param parameters: Parameters occurring in the region, e.g. ``model.collect_all_parameters()``.
    :return: The parameter region.
    """
    return developer.parse_region(region_string, set(parameters))


def create_region(bounds: Mapping[Variable, tuple[RationalFunctionCoefficient, RationalFunctionCoefficient]]) -> ParameterRegion:
    """
    Create a parameter region from bounds for each parameter.

    :param bounds: Mapping from each parameter to its inclusive tuple representing [lower bound, upper bound].
    :return: The parameter region.
    """
    lower = {parameter: bound[0] for parameter, bound in bounds.items()}
    upper = {parameter: bound[1] for parameter, bound in bounds.items()}
    return ParameterRegion(lower, upper)


def _coefficient_argument(value: RationalFunctionCoefficient | float | int, name: str) -> RationalFunctionCoefficient:
    """Convert numeric arguments to coefficients, interpreting floats as decimals."""
    if isinstance(value, float):
        if not _isfinite(value):
            raise ValueError(f"{name} must be finite.")
        return RationalFunctionCoefficient(repr(value))
    if isinstance(value, int):
        return RationalFunctionCoefficient(value)
    return value


def _region_argument(region: ParameterRegion | None, region_bound: RationalFunctionCoefficient | float | int | None):
    if (region is None) == (region_bound is None):
        raise ValueError("Provide exactly one of region or region_bound.")
    if region is not None:
        return region
    return _coefficient_argument(region_bound, "region_bound")


def verify(
    model: SparseModel,
    property: Property | Formula,
    *,
    region: ParameterRegion | None = None,
    region_bound: RationalFunctionCoefficient | float | int | None = None,
    region_engine: RegionCheckEngine = RegionCheckEngine.PARAMETER_LIFTING,
    environment: Environment | None = None,
) -> bool:
    """
    Verify a bounded probability or reward property for all well-defined valuations in a region.

    Requires a sparse parametric DTMC or MDP with exactly one initial state.
    Provide exactly one of ``region`` or ``region_bound``. The region must cover
    all model parameters. Standard parameter lifting requires a well-defined,
    graph-preserving region. Robust parameter lifting supports DTMCs and can include
    graph-changing valuations.
    Unsupported inputs raise an exception.

    For MDPs, properties have the following semantics:

    ==========================  ======================================
    Property                    Schedulers that must satisfy the bound
    ==========================  ======================================
    ``P>=0.8 [F "target"]``     Every scheduler
    ``Pmin>=0.8 [F "target"]``  Every scheduler
    ``Pmax>=0.8 [F "target"]``  At least one scheduler (PLA only)
    ``P<=0.8 [F "target"]``     Every scheduler
    ``Pmin<=0.8 [F "target"]``  At least one scheduler (PLA only)
    ``Pmax<=0.8 [F "target"]``  Every scheduler
    ==========================  ======================================

    :param model: Parametric sparse DTMC or MDP.
    :param property: Bounded probability or reward property or formula.
    :param region: Explicit parameter region.
    :param region_bound: Use [region_bound, 1-region_bound] for every parameter; must be in [0, 1/2].
        Floats use their decimal representation, e.g. 0.2 means exactly 1/5.
    :param region_engine: Region checking engine. See :class:`RegionCheckEngine` for arithmetic choices and region requirements.
    :param environment: (optional) Environment configuring the analysis.
    :return: Whether every well-defined valuation in the region satisfies the property.
    """
    return developer.verify(
        environment if environment is not None else _environments.default(model),
        model,
        _formula(property),
        _region_argument(region, region_bound),
        region_engine=region_engine,
    )


def check_feasibility(
    model: SparseModel,
    property: Property | Formula,
    *,
    region: ParameterRegion | None = None,
    region_bound: RationalFunctionCoefficient | float | int | None = None,
    method: FeasibilityMethod = FeasibilityMethod.PLA,
    region_engine: RegionCheckEngine = RegionCheckEngine.PARAMETER_LIFTING,
    environment: Environment | None = None,
) -> FeasibilitySynthesisResult:
    """
    Search for a well-defined parameter valuation satisfying a bounded probability or reward property.

    Requires a sparse parametric DTMC or MDP with exactly one initial state.
    Provide exactly one of ``region`` or ``region_bound``. The region must cover
    all model parameters and satisfy the method's and engine's requirements.
    Standard parameter lifting, GD, and SCP require a well-defined, graph-preserving
    region. GD supports DTMCs only. Robust parameter lifting supports DTMCs and
    can include graph-changing valuations. Unsupported inputs raise an exception.

    For MDPs, properties have the following semantics:

    ==========================  ======================================
    Property                    Schedulers that must satisfy the bound
    ==========================  ======================================
    ``P>=0.8 [F "target"]``     Every scheduler
    ``Pmin>=0.8 [F "target"]``  Every scheduler
    ``Pmax>=0.8 [F "target"]``  At least one scheduler (PLA only)
    ``P<=0.8 [F "target"]``     Every scheduler
    ``Pmin<=0.8 [F "target"]``  At least one scheduler (PLA only)
    ``Pmax<=0.8 [F "target"]``  Every scheduler
    ==========================  ======================================

    :param model: Parametric sparse DTMC or MDP.
    :param property: Bounded probability or reward property or formula.
    :param region: Explicit parameter region.
    :param region_bound: Use [region_bound, 1-region_bound] for every parameter; must be in [0, 1/2].
        Floats use their decimal representation, e.g. 0.2 means exactly 1/5.
    :param method: Feasibility method: parameter lifting (PLA), gradient descent (GD), or sequential convex programming (SCP).
    :param region_engine: Region checking engine, used only for PLA and ignored by GD and SCP.
        See :class:`RegionCheckEngine` for arithmetic choices and region requirements.
    :param environment: (optional) Environment configuring the analysis.
    :return: Result with status EXISTS_SAT, ALL_VIOLATED, or UNKNOWN. A witness is present only for EXISTS_SAT.
    """
    return developer.check_feasibility(
        environment if environment is not None else _environments.default(model),
        model,
        _formula(property),
        _region_argument(region, region_bound),
        method,
        region_engine,
    )


def compute_extremal_value(
    model: SparseModel,
    property: Property | Formula,
    *,
    region: ParameterRegion,
    direction: OptimizationDirection,
    precision: RationalFunctionCoefficient | float | int,
    absolute_precision: bool = False,
    engine: RegionCheckEngine = RegionCheckEngine.PARAMETER_LIFTING,
    discrete_variables: Iterable[Variable] = (),
    environment: Environment | None = None,
) -> tuple[RationalFunctionCoefficient | float, dict[Variable, RationalFunctionCoefficient]]:
    """
    Compute an extremal probability or expected reward over a parameter region.

    Requires a sparse parametric DTMC or MDP with exactly one initial state and a
    quantitative property, e.g. ``P=? [F "target"]``. For MDPs, the property's
    min/max determines the scheduler optimization; ``direction`` determines the
    optimization over parameter valuations.

    :param model: Parametric sparse DTMC or MDP.
    :param property: Quantitative probability or reward property or formula.
    :param region: Parameter region satisfying the selected engine's requirements.
    :param direction: Whether to minimize or maximize over parameter valuations.
    :param precision: Required precision.
        Floats must be finite and use their decimal representation, e.g. 1e-6 means exactly 1/1000000.
    :param absolute_precision: Whether precision is absolute (True) or relative (False).
    :param engine: Region checking engine. See :class:`RegionCheckEngine` for arithmetic choices and region requirements.
    :param discrete_variables: Parameters treated as discrete when splitting regions.
    :param environment: (optional) Environment configuring the analysis. Defaults to :func:`stormpy.environments.default`.
    :return: The value at the returned parameter valuation and that valuation. The value
        approximates the extremum within the requested precision and can be infinite for rewards.
    """
    precision = _coefficient_argument(precision, "precision")
    environment = environment if environment is not None else _environments.default(model)
    task = _developer.CheckTask[RationalFunction](_formula(property), True)
    checker = developer.initialize_region_refinement_checker(environment, model, task, engine=engine, discrete_variables=set(discrete_variables))
    return checker.compute_extremal_value(environment, region, direction, RationalFunction(Polynomial(precision)), absolute_precision)


__all__ = [
    "ConstraintCollector",
    "ParameterRegion",
    "parse_region",
    "create_region",
    "verify",
    "check_feasibility",
    "compute_extremal_value",
    "RegionCheckEngine",
    "RegionResult",
    "FeasibilityMethod",
    "FeasibilityResult",
    "FeasibilitySynthesisResult",
    "ModelInstantiator",
    "gather_derivatives",
]

"""Parameter synthesis and model instantiation for sparse parametric models.

Create parameter regions, verify properties throughout a region, or search for
satisfying parameter valuations. Instantiate models with concrete parameter values
using :class:`ModelInstantiator`. Lower-level tools are in :mod:`stormpy.pars.developer`.
"""

from collections.abc import Iterable, Mapping
from math import isfinite as _isfinite

from . import developer
from stormpy import Environment, RationalFunctionCoefficient
from stormpy.numbers import Polynomial, Variable
from stormpy.logic import Formula, Property
from stormpy.models import SparseModel
from stormpy.core._common import _formula

ParameterRegion = developer.ParameterRegion
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

    :param bounds: Mapping from each parameter to its (lower bound, upper bound).
    :return: The parameter region.
    """
    lower = {parameter: bound[0] for parameter, bound in bounds.items()}
    upper = {parameter: bound[1] for parameter, bound in bounds.items()}
    return ParameterRegion(lower, upper)


def _region_argument(region: ParameterRegion | None, region_bound: RationalFunctionCoefficient | float | int | None):
    if (region is None) == (region_bound is None):
        raise ValueError("Provide exactly one of region or region_bound.")
    if region is not None:
        return region
    if isinstance(region_bound, float):
        if not _isfinite(region_bound):
            raise ValueError("region_bound must be finite.")
        return RationalFunctionCoefficient(repr(region_bound))
    if isinstance(region_bound, int):
        return RationalFunctionCoefficient(region_bound)
    return region_bound


def verify(
    model: SparseModel,
    property: Property | Formula,
    region: ParameterRegion | None = None,
    *,
    region_bound: RationalFunctionCoefficient | float | int | None = None,
    engine: RegionCheckEngine = RegionCheckEngine.PARAMETER_LIFTING,
    environment: Environment | None = None,
) -> bool:
    """
    Verify a bounded probability or reward property for all well-defined valuations in a region.

    Requires a sparse parametric DTMC or MDP with exactly one initial state.
    Provide exactly one of ``region`` or ``region_bound``. The region must cover
    all model parameters. Standard parameter lifting requires a well-defined,
    graph-preserving region; endpoints are not removed automatically. Robust
    parameter lifting supports DTMCs and can include graph-changing valuations.
    Unsupported inputs raise an exception.

    :param model: Parametric sparse DTMC or MDP.
    :param property: Bounded probability or reward property or formula.
    :param region: Explicit parameter region.
    :param region_bound: Use [region_bound, 1-region_bound] for every parameter; must be in [0, 1/2].
        Accepts rational coefficients, floats, or integers. Floats use their decimal representation, e.g. 0.2 means exactly 1/5.
    :param engine: Region checking engine.
    :param environment: (optional) Environment configuring the analysis.
    :return: Whether every well-defined valuation in the region satisfies the property.
    """
    return developer.verify(
        environment if environment is not None else Environment(), model, _formula(property), _region_argument(region, region_bound), engine
    )


def check_feasibility(
    model: SparseModel,
    property: Property | Formula,
    region: ParameterRegion | None = None,
    *,
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

    For MDPs, bounds without min/max apply to every scheduler. For example,
    ``Pmax>=0.8 [F "target"]`` asks for some scheduler (PLA only), while
    ``Pmin>=0.8 [F "target"]`` requires every scheduler. SCP requires universal
    scheduler quantification.

    :param model: Parametric sparse DTMC or MDP.
    :param property: Bounded probability or reward property or formula.
    :param region: Explicit parameter region.
    :param region_bound: Use [region_bound, 1-region_bound] for every parameter; must be in [0, 1/2].
        Accepts rational coefficients, floats, or integers. Floats use their decimal representation, e.g. 0.2 means exactly 1/5.
    :param method: Feasibility method: parameter lifting (PLA), gradient descent (GD), or sequential convex programming (SCP).
    :param region_engine: Region checking engine, used only for PLA.
    :param environment: (optional) Environment configuring the analysis.
    :return: Result with status EXISTS_SAT, ALL_VIOLATED, or UNKNOWN. A witness is present only for EXISTS_SAT.
    """
    return developer.check_feasibility(
        environment if environment is not None else Environment(),
        model,
        _formula(property),
        _region_argument(region, region_bound),
        method,
        region_engine,
    )


def gather_derivatives(model: SparseModel, parameter: Variable) -> set[Polynomial]:
    """
    Gather the nonconstant numerators of transition-probability derivatives with respect to a parameter.

    :param model: Parametric sparse model.
    :param parameter: Parameter to differentiate by.
    :return: Set of nonconstant derivative numerators.
    """
    return developer.gather_derivatives(model, parameter)


__all__ = [
    "ParameterRegion",
    "parse_region",
    "create_region",
    "verify",
    "check_feasibility",
    "RegionCheckEngine",
    "RegionResult",
    "FeasibilityMethod",
    "FeasibilityResult",
    "FeasibilitySynthesisResult",
    "ModelInstantiator",
    "gather_derivatives",
]

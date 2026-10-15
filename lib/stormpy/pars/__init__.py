"""API for the analysis of parametric models.

Makes the functionality of ``storm::pars::`` available, e.g., model instantiation, model simplification and region checking via parameter lifting.
"""

from collections.abc import Iterable, Mapping

from . import developer
from stormpy import Environment, RationalFunction, RationalFunctionCoefficient
from stormpy import developer as _core_developer
from stormpy.numbers import Polynomial, Variable
from stormpy.logic import Formula, Property
from stormpy.models import SparseModel
from stormpy.core._common import _formula
from stormpy.exceptions import StormError

# Import classes from developer (and republish templated classes under stormpy.pars.X)
ParameterRegion = developer.ParameterRegion
RegionResult = developer.RegionResult
RegionResultHypothesis = developer.RegionResultHypothesis
RegionModelChecker = developer.RegionModelChecker
RegionRefinementChecker = developer.RegionRefinementChecker
ModelInstantiator = developer.ModelInstantiator.publish_as("stormpy.pars.ModelInstantiator")
SparseInstantiationModelChecker = developer.SparseInstantiationModelChecker.publish_as("stormpy.pars.SparseInstantiationModelChecker")


def _check_task(property: Property | Formula):
    """Create a check task for the given property where only the initial states are relevant."""
    return _core_developer.CheckTask[RationalFunction](_formula(property), only_initial_states_relevant=True)


def _graph_preservation_status(graph_preserving: bool):
    return developer.GraphPreservationStatus.GRAPH_PRESERVING if graph_preserving else developer.GraphPreservationStatus.NONE


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


def create_region_checker(
    model, property: Property | Formula, *, environment: Environment | None = None, allow_model_simplification: bool = True, graph_preserving: bool = True
) -> RegionModelChecker:
    """
    Create a region model checker based on parameter lifting.

    :param model: Parametric sparse model (DTMC or MDP).
    :param property: Property or formula to check.
    :param environment: (optional) Environment configuring the model checking.
    :param allow_model_simplification: Whether the model may be simplified before the analysis.
    :param graph_preserving: Whether the graph structure of the model is preserved for all parameter values in the analyzed regions.
    :return: The region model checker.
    """
    return developer.initialize_region_model_checker(
        environment if environment is not None else Environment(),
        model,
        _check_task(property),
        allow_model_simplification=allow_model_simplification,
        graph_preservation_status=_graph_preservation_status(graph_preserving),
    )


def create_region_refinement_checker(
    model, property: Property | Formula, *, environment: Environment | None = None, allow_model_simplification: bool = True, graph_preserving: bool = True
) -> RegionRefinementChecker:
    """
    Create a region refinement checker based on parameter lifting, e.g., to compute extremal values within a region.

    :param model: Parametric sparse model (DTMC or MDP).
    :param property: Property or formula to check.
    :param environment: (optional) Environment configuring the model checking.
    :param allow_model_simplification: Whether the model may be simplified before the analysis.
    :param graph_preserving: Whether the graph structure of the model is preserved for all parameter values in the analyzed regions.
    :return: The region refinement checker.
    """
    return developer.initialize_region_refinement_checker(
        environment if environment is not None else Environment(),
        model,
        _check_task(property),
        allow_model_simplification=allow_model_simplification,
        graph_preservation_status=_graph_preservation_status(graph_preserving),
    )


def simplify_model(model: SparseModel, property: Property | Formula) -> tuple[SparseModel, Formula]:
    """
    Simplify a parametric model preserving the given property by eliminating states with constant outgoing probabilities.

    :param model: Parametric sparse model (DTMC or MDP).
    :param property: Property or formula to preserve.
    :return: Tuple of simplified model and simplified formula.
    """
    if (model.model_type,) not in developer.SparseParametricModelSimplifier.instantiations:
        raise StormError("Model type {} cannot be simplified.".format(model.model_type))
    simplifier = developer.SparseParametricModelSimplifier(model)
    if not simplifier.simplify(_formula(property)):
        raise StormError("Model could not be simplified")
    return simplifier.simplified_model, simplifier.simplified_formula


def gather_derivatives(model, parameter: Variable) -> set[Polynomial]:
    """
    Gather the derivatives of all transition probabilities with respect to the given parameter.

    Only non-constant derivatives are returned.

    :param model: Parametric sparse model.
    :param parameter: Parameter to derive by.
    :return: Set of numerators of the derivatives.
    """
    return developer.gather_derivatives(model, parameter)


__all__ = [
    # Regions
    "ParameterRegion",
    "parse_region",
    "create_region",
    # Region checking
    "RegionResult",
    "RegionResultHypothesis",
    "RegionModelChecker",
    "RegionRefinementChecker",
    "create_region_checker",
    "create_region_refinement_checker",
    # Instantiation
    "ModelInstantiator",
    "SparseInstantiationModelChecker",
    # Transformations
    "simplify_model",
    "gather_derivatives",
]

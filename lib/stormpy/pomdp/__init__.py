"""API for the analysis of partially observable models (POMDPs).

Makes the functionality of ``storm::pomdp::`` available, e.g., transformations of POMDPs, belief tracking, qualitative analysis and monitor verification.
"""

from collections.abc import Sequence

from . import developer
from stormpy import environments
from stormpy.environments import Environment
from stormpy.expressions import ExpressionManager
from stormpy.logic import Formula, Property
from stormpy.models import SparseDtmc, SparseMdp, SparseModel, SparsePomdp
from stormpy.core._common import _formula
from stormpy.developer.storage import parameters_of_model as _parameters_of_model

# Import classes from developer (and republish templated classes under stormpy.pomdp.X)
PomdpMemory = developer.PomdpMemory
PomdpMemoryPattern = developer.PomdpMemoryPattern
PomdpFscApplicationMode = developer.PomdpFscApplicationMode
ObservationTraceUnfolder = developer.ObservationTraceUnfolder.publish_as("stormpy.pomdp.ObservationTraceUnfolder")
BeliefSupportTracker = developer.BeliefSupportTracker.publish_as("stormpy.pomdp.BeliefSupportTracker")
NondeterministicBeliefTracker = developer.NondeterministicBeliefTracker.publish_as("stormpy.pomdp.NondeterministicBeliefTracker")
SparseBeliefState = developer.SparseBeliefState.publish_as("stormpy.pomdp.SparseBeliefState")
MonitorVerifier = developer.MonitorVerifier.publish_as("stormpy.pomdp.MonitorVerifier")
IterativePolicySearch = developer.IterativePolicySearch.publish_as("stormpy.pomdp.IterativePolicySearch")
WinningRegion = developer.WinningRegion
WinningRegionQueryInterface = developer.WinningRegionQueryInterface.publish_as("stormpy.pomdp.WinningRegionQueryInterface")


def make_canonic(model: SparsePomdp) -> SparsePomdp:
    """
    Make the representation of the POMDP canonic, i.e., order the choices of each state consistently for each observation.

    :param model: POMDP.
    :return: The canonic POMDP.
    """
    return developer.MakePOMDPCanonic(model).transform()


def make_simple(model: SparsePomdp, *, keep_state_valuations: bool = False) -> SparsePomdp:
    """
    Make the POMDP simple (aka alternating), i.e., each state has at most two actions, and if there is nondeterminism, then there is no probabilistic branching.

    :param model: Canonic POMDP.
    :param keep_state_valuations: Whether the state valuations are kept.
    :return: The simple POMDP.
    """
    transformer = developer.BinaryPomdpTransformer[_parameters_of_model(model)]()
    return transformer.transform(model, True, keep_state_valuations=keep_state_valuations).transformed_pomdp


def create_memory(pattern: PomdpMemoryPattern, nr_states: int) -> PomdpMemory:
    """
    Create a memory structure for finite-state controllers.

    :param pattern: Pattern of the memory structure.
    :param nr_states: Number of memory states.
    :return: The memory structure.
    """
    return developer.PomdpMemoryBuilder().build(pattern, nr_states)


def unfold_memory(model: SparsePomdp, memory: PomdpMemory, *, add_memory_labels: bool = False, keep_state_valuations: bool = False) -> SparsePomdp:
    """
    Unfold the memory for a finite-state controller into the POMDP.

    :param model: Canonic POMDP.
    :param memory: Memory structure, see :func:`create_memory`.
    :param add_memory_labels: Whether labels for the memory states are added.
    :param keep_state_valuations: Whether the state valuations are kept.
    :return: POMDP whose states are the product of the states of the original POMDP and the memory states.
    """
    return developer.PomdpMemoryUnfolder(model, memory, add_memory_labels=add_memory_labels, keep_state_valuations=keep_state_valuations).transform()


def apply_unknown_fsc(model: SparsePomdp, mode: PomdpFscApplicationMode = PomdpFscApplicationMode.SIMPLE_LINEAR) -> SparseModel:
    """
    Apply an unknown finite-state controller to the POMDP.

    The choices of the controller become parameters, i.e., the result is a parametric Markov chain.

    :param model: Canonic POMDP.
    :param mode: How the choices of the controller are encoded as parameters.
    :return: The parametric Markov chain.
    """
    return developer.ApplyFiniteSchedulerToPomdp(model).transform(mode)


def create_nondeterministic_belief_tracker(model: SparsePomdp, *, reduction_timeout: int = 0, track_timeout: int = 0) -> NondeterministicBeliefTracker:
    """
    Create a tracker for the beliefs of the POMDP given a trace of observations.

    :param model: POMDP.
    :param reduction_timeout: Timeout in milliseconds for the reduction algorithm, 0 for no timeout.
    :param track_timeout: Timeout in milliseconds for tracking, 0 for no timeout.
    :return: The belief tracker.
    """
    options = developer.NondeterministicBeliefTrackerOptions[_parameters_of_model(model)]()
    options.time_out = reduction_timeout
    options.track_time_out = track_timeout
    return NondeterministicBeliefTracker(model, options)


def create_observation_trace_unfolder(
    model: SparsePomdp, risk: Sequence[object], expression_manager: ExpressionManager, *, use_restart_semantics: bool = True
) -> ObservationTraceUnfolder:
    """
    Create an unfolder which turns observation traces of the POMDP into MDPs.

    :param model: POMDP.
    :param risk: Risk for each state of the POMDP.
    :param expression_manager: Expression manager for the variables of the unfolded MDPs.
    :param use_restart_semantics: Whether restart semantics are used instead of a sink state.
    :return: The observation trace unfolder.
    """
    options = developer.ObservationTraceUnfolderOptions()
    options.use_restart_semantics = use_restart_semantics
    return ObservationTraceUnfolder(model, risk, expression_manager, options)


def create_monitor_verifier(
    mc: SparseDtmc,
    monitor: SparseMdp,
    risk: Sequence[object],
    *,
    expression_manager: ExpressionManager | None = None,
    use_restart_semantics: bool = True,
    accepting_label: str = "accepting",
    step_prefix: str = "step",
    horizon_label: str = "horizon",
) -> MonitorVerifier:
    """
    Create the POMDP for verifying a monitor against a Markov chain.

    :param mc: Markov chain.
    :param monitor: Monitor given as MDP whose actions are labels of the Markov chain.
    :param risk: Risk for each state of the Markov chain.
    :param expression_manager: (optional) Expression manager for the variables of the product.
    :param use_restart_semantics: Whether restart semantics are used instead of a sink state.
    :param accepting_label: Label of the accepting states of the monitor.
    :param step_prefix: Prefix of the labels of the monitor steps.
    :param horizon_label: Label of the monitor states reaching the horizon.
    :return: The monitor verifier containing the product POMDP.
    """
    options = developer.GenerateMonitorVerifierOptions[_parameters_of_model(mc)]()
    options.use_restart_semantics = use_restart_semantics
    options.accepting_label = accepting_label
    options.step_prefix = step_prefix
    options.horizon_label = horizon_label
    generator = developer.GenerateMonitorVerifier(mc, monitor, expression_manager if expression_manager is not None else ExpressionManager(), options)
    generator.set_risk(risk)
    return generator.create_product()


def prepare_for_qualitative_search(model: SparsePomdp, property: Property | Formula) -> SparsePomdp:
    """
    Prepare the POMDP for the qualitative analysis by making all states absorbing from which the target is not reached almost surely.

    :param model: POMDP.
    :param property: Reachability probability property or formula.
    :return: The prepared POMDP.
    """
    return developer.prepare_pomdp_for_qualitative_search(model, _formula(property))


def create_iterative_policy_search(model: SparsePomdp, property: Property | Formula, *, environment: Environment | None = None) -> IterativePolicySearch:
    """
    Create a solver for qualitative reachability queries (almost-sure reachability) on POMDPs.

    A solver runs a single analysis, i.e., either ``compute_winning_region`` or ``analyze_for_initial_states``.
    Create a new solver for each further analysis.

    :param model: POMDP, see also :func:`prepare_for_qualitative_search`.
    :param property: Reachability probability property or formula.
    :param environment: (optional) Environment configuring the solvers. Defaults to :func:`stormpy.environments.default`.
    :return: The solver.
    """
    environment = environment if environment is not None else environments.default(model)
    return developer.create_iterative_policy_search(environment, model, _formula(property), developer.MemlessSearchOptions())


__all__ = [
    # Transformations
    "make_canonic",
    "make_simple",
    "PomdpMemory",
    "PomdpMemoryPattern",
    "create_memory",
    "unfold_memory",
    "PomdpFscApplicationMode",
    "apply_unknown_fsc",
    "ObservationTraceUnfolder",
    "create_observation_trace_unfolder",
    # Belief tracking
    "BeliefSupportTracker",
    "SparseBeliefState",
    "NondeterministicBeliefTracker",
    "create_nondeterministic_belief_tracker",
    # Qualitative analysis
    "IterativePolicySearch",
    "WinningRegion",
    "WinningRegionQueryInterface",
    "prepare_for_qualitative_search",
    "create_iterative_policy_search",
    # Monitor verification
    "MonitorVerifier",
    "create_monitor_verifier",
]

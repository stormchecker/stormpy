"""API for the analysis of partially observable models (POMDPs).

Makes the functionality of ``storm::pomdp::`` available, e.g., transformations of POMDPs, belief tracking, qualitative analysis, quantitative analysis and monitor verification.
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
ExplorationQueueOrder = developer.ExplorationQueueOrder
BeliefBasedModelCheckerStatistics = developer.BeliefBasedModelCheckerStatistics
BeliefBasedModelCheckerResult = developer.BeliefBasedModelCheckerResult.publish_as("stormpy.pomdp.BeliefBasedModelCheckerResult")
ObservationBasedFiniteStateController = developer.ObservationBasedFiniteStateController.publish_as("stormpy.pomdp.ObservationBasedFiniteStateController")


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


def verify_with_belief_unfolding(
    model: SparsePomdp,
    property: Property | Formula,
    *,
    max_exploration_size: int | None = None,
    max_exploration_time: int | None = None,
    use_clipping: bool = False,
    clipping_resolutions: Sequence[int] | None = None,
    cut_zero_gap: bool = False,
    exploration_queue_order: ExplorationQueueOrder = ExplorationQueueOrder.FIFO,
    build_choice_labeling: bool = True,
    generate_policy: bool = False,
    environment: Environment | None = None,
) -> BeliefBasedModelCheckerResult:
    """
    Approximate an unbounded reachability probability or expected reachability reward by unfolding the belief MDP.

    The POMDP is prepared automatically (made canonic, target observations refined, failure states made absorbing).
    The POMDP must have exactly one initial state and the property must be non-nested, without threshold and with an explicit optimization direction.
    The value is a lower bound for maximization and an upper bound for minimization.
    Without clipping and with completed exploration, the value is the value of the belief MDP.

    :param model: POMDP.
    :param property: Unbounded reachability probability or expected reachability reward property or formula, e.g., ``Pmax=? [F "goal"]``.
    :param max_exploration_size: (optional) Maximal number of discovered beliefs. Defaults to no limit.
    :param max_exploration_time: (optional) Maximal exploration time in seconds. Defaults to no limit.
    :param use_clipping: Whether belief clipping is used.
    :param clipping_resolutions: Clipping resolution (positive) for each observation of the POMDP. Required for clipping.
    :param cut_zero_gap: Whether non-target beliefs are cut whose preprocessing bounds coincide. Incompatible with ``generate_policy``.
    :param exploration_queue_order: Order in which discovered beliefs are explored.
    :param build_choice_labeling: Whether choice labels are built for the belief MDP. Requires choice labels in the POMDP.
    :param generate_policy: Whether a finite-state controller is generated, see :attr:`BeliefBasedModelCheckerResult.policy`.
        The controller refers to the prepared POMDP, i.e., actions are ordered as in the canonic POMDP and observations include the refined target observations.
    :param environment: (optional) Environment configuring the solvers. Defaults to :func:`stormpy.environments.default`.
    :return: The result containing the bound, whether the exploration was completed, statistics and the optional policy.
    """
    options = developer.BeliefBasedModelCheckerOptions[_parameters_of_model(model)]()
    options.max_exploration_size = max_exploration_size
    options.max_exploration_time = max_exploration_time
    options.use_clipping = use_clipping
    options.clipping_resolutions = list(clipping_resolutions) if clipping_resolutions is not None else None
    options.cut_zero_gap = cut_zero_gap
    options.exploration_queue_order = exploration_queue_order
    options.build_choice_labeling = build_choice_labeling
    options.generate_policy = generate_policy
    environment = environment if environment is not None else environments.default(model)
    return developer.verify_with_belief_unfolding(environment, model, _formula(property), options)


def verify_with_belief_discretization(
    model: SparsePomdp,
    property: Property | Formula,
    resolution: int = 2,
    *,
    use_dynamic: bool = False,
    cut_zero_gap: bool = False,
    exploration_queue_order: ExplorationQueueOrder = ExplorationQueueOrder.FIFO,
    build_choice_labeling: bool = True,
    environment: Environment | None = None,
) -> BeliefBasedModelCheckerResult:
    """
    Approximate an unbounded reachability probability or expected reachability reward by discretizing the belief space (Freudenthal triangulation).

    The POMDP is prepared as for :func:`verify_with_belief_unfolding`.
    The value is an upper bound for maximization and a lower bound for minimization.
    Completed exploration refers to the discretized MDP and does not imply that the value is exact.

    :param model: POMDP.
    :param property: Unbounded reachability probability or expected reachability reward property or formula, e.g., ``Pmax=? [F "goal"]``.
    :param resolution: Resolution (positive) of the discretization. Higher resolutions give tighter bounds.
    :param use_dynamic: Whether the resolution is selected per belief using dynamic triangulation.
    :param cut_zero_gap: Whether non-target beliefs are cut whose preprocessing bounds coincide.
    :param exploration_queue_order: Order in which discovered beliefs are explored.
    :param build_choice_labeling: Whether choice labels are built for the belief MDP. Requires choice labels in the POMDP.
    :param environment: (optional) Environment configuring the solvers. Defaults to :func:`stormpy.environments.default`.
    :return: The result containing the bound, whether the exploration was completed and statistics.
    """
    options = developer.BeliefBasedModelCheckerOptions[_parameters_of_model(model)]()
    options.cut_zero_gap = cut_zero_gap
    options.exploration_queue_order = exploration_queue_order
    options.build_choice_labeling = build_choice_labeling
    environment = environment if environment is not None else environments.default(model)
    return developer.verify_with_belief_discretization(environment, model, _formula(property), resolution, use_dynamic, options)


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
    # Quantitative analysis
    "ExplorationQueueOrder",
    "BeliefBasedModelCheckerStatistics",
    "BeliefBasedModelCheckerResult",
    "ObservationBasedFiniteStateController",
    "verify_with_belief_unfolding",
    "verify_with_belief_discretization",
    # Monitor verification
    "MonitorVerifier",
    "create_monitor_verifier",
]

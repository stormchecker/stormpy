from ._config import *

from . import _core
from ._core import *
from . import storage
from .storage import *
from .logic import *
from . import exceptions

try:
    from ._version import __version__
except ImportError:
    # We're running in a tree that doesn't have a _version.py, so we don't know what our version is.
    __version__ = "unknown"

_core._set_up("")


def _convert_sparse_model(model, parametric=False):
    """
    Convert (parametric) model in sparse representation into model corresponding to exact model type.
    :param model: Sparse model.
    :param parametric: Flag indicating if the model is parametric.
    :return: Model corresponding to exact model type.
    """
    if parametric:
        assert model.supports_parameters
        if model.model_type == ModelType.DTMC:
            return model._as_sparse_pdtmc()
        elif model.model_type == ModelType.MDP:
            return model._as_sparse_pmdp()
        elif model.model_type == ModelType.POMDP:
            return model._as_sparse_ppomdp()
        elif model.model_type == ModelType.CTMC:
            return model._as_sparse_pctmc()
        elif model.model_type == ModelType.MA:
            return model._as_sparse_pma()
        else:
            raise stormpy.exceptions.StormError("Not supported parametric model constructed")
    else:
        assert not model.supports_parameters
        if model.model_type == ModelType.DTMC:
            return model._as_sparse_dtmc()
        elif model.model_type == ModelType.MDP:
            return model._as_sparse_mdp()
        elif model.model_type == ModelType.POMDP:
            return model._as_sparse_pomdp()
        elif model.model_type == ModelType.CTMC:
            return model._as_sparse_ctmc()
        elif model.model_type == ModelType.MA:
            return model._as_sparse_ma()
        elif model.model_type == ModelType.SMG:
            return model._as_sparse_smg()
        else:
            raise stormpy.exceptions.StormError("Not supported non-parametric model constructed")


def _convert_symbolic_model(model, parametric=False):
    """
    Convert (parametric) model in symbolic representation into model corresponding to exact model type.
    :param model: Symbolic model.
    :param parametric: Flag indicating if the model is parametric.
    :return: Model corresponding to exact model type.
    """
    if parametric:
        assert model.supports_parameters
        if model.model_type == ModelType.DTMC:
            return model._as_symbolic_pdtmc()
        elif model.model_type == ModelType.MDP:
            return model._as_symbolic_pmdp()
        elif model.model_type == ModelType.CTMC:
            return model._as_symbolic_pctmc()
        elif model.model_type == ModelType.MA:
            return model._as_symbolic_pma()
        else:
            raise stormpy.exceptions.StormError("Not supported parametric model constructed")
    else:
        assert not model.supports_parameters
        if model.model_type == ModelType.DTMC:
            return model._as_symbolic_dtmc()
        elif model.model_type == ModelType.MDP:
            return model._as_symbolic_mdp()
        elif model.model_type == ModelType.CTMC:
            return model._as_symbolic_ctmc()
        elif model.model_type == ModelType.MA:
            return model._as_symbolic_ma()
        else:
            raise stormpy.exceptions.StormError("Not supported non-parametric model constructed")


def build_model(symbolic_description, properties=None):
    """
    Build a model in sparse representation from a symbolic description.

    :param symbolic_description: Symbolic model description to translate into a model.
    :param List[Property] properties: List of properties that should be preserved during the translation. If None, then all properties are preserved.
    :return: Model in sparse representation.
    """
    return build_sparse_model(symbolic_description, properties=properties)


def build_parametric_model(symbolic_description, properties=None):
    """
    Build a parametric model in sparse representation from a symbolic description.

    :param symbolic_description: Symbolic model description to translate into a model.
    :param List[Property] properties: List of properties that should be preserved during the translation. If None, then all properties are preserved.
    :return: Parametric model in sparse representation.
    """
    return build_sparse_parametric_model(symbolic_description, properties=properties)


def build_sparse_model(symbolic_description, properties=None):
    """
    Build a model in sparse representation from a symbolic description.

    :param symbolic_description: Symbolic model description to translate into a model.
    :param List[Property] properties: List of properties that should be preserved during the translation. If None, then all properties are preserved.
    :return: Model in sparse representation.
    """
    if not symbolic_description.undefined_constants_are_graph_preserving:
        raise stormpy.exceptions.StormError("Program still contains undefined constants")

    if properties:
        formulae = [(prop.raw_formula if isinstance(prop, Property) else prop) for prop in properties]
        intermediate = _core._build_sparse_model_from_symbolic_description(symbolic_description, formulae)
    else:
        intermediate = _core._build_sparse_model_from_symbolic_description(symbolic_description)
    return _convert_sparse_model(intermediate, parametric=False)


def build_sparse_parametric_model(symbolic_description, properties=None):
    """
    Build a parametric model in sparse representation from a symbolic description.

    :param symbolic_description: Symbolic model description to translate into a model.
    :param List[Property] properties: List of properties that should be preserved during the translation. If None, then all properties are preserved.
    :return: Parametric model in sparse representation.
    """
    if not symbolic_description.undefined_constants_are_graph_preserving:
        raise stormpy.exceptions.StormError("Program still contains undefined constants")

    if properties:
        formulae = [(prop.raw_formula if isinstance(prop, Property) else prop) for prop in properties]
        intermediate = _core._build_sparse_parametric_model_from_symbolic_description(symbolic_description, formulae)
    else:
        intermediate = _core._build_sparse_parametric_model_from_symbolic_description(symbolic_description)
    return _convert_sparse_model(intermediate, parametric=True)


def build_symbolic_model(symbolic_description, properties=None):
    """
    Build a model in symbolic representation from a symbolic description.

    :param symbolic_description: Symbolic model description to translate into a model.
    :param List[Property] properties: List of properties that should be preserved during the translation. If None, then all properties are preserved.
    :return: Model in symbolic representation.
    """
    if not symbolic_description.undefined_constants_are_graph_preserving:
        raise stormpy.exceptions.StormError("Program still contains undefined constants")

    if properties:
        formulae = [(prop.raw_formula if isinstance(prop, Property) else prop) for prop in properties]
        intermediate = _core._build_symbolic_model_from_symbolic_description(symbolic_description, formulae)
    else:
        intermediate = _core._build_symbolic_model_from_symbolic_description(symbolic_description)
    return _convert_symbolic_model(intermediate, parametric=False)


def build_symbolic_parametric_model(symbolic_description, properties=None):
    """
    Build a parametric model in symbolic representation from a symbolic description.

    :param symbolic_description: Symbolic model description to translate into a model.
    :param List[Property] properties: List of properties that should be preserved during the translation. If None, then all properties are preserved.
    :return: Parametric model in symbolic representation.
    """
    if not symbolic_description.undefined_constants_are_graph_preserving:
        raise stormpy.exceptions.StormError("Program still contains undefined constants")

    if properties:
        formulae = [(prop.raw_formula if isinstance(prop, Property) else prop) for prop in properties]
        intermediate = _core._build_symbolic_parametric_model_from_symbolic_description(symbolic_description, formulae)
    else:
        intermediate = _core._build_symbolic_parametric_model_from_symbolic_description(symbolic_description)
    return _convert_symbolic_model(intermediate, parametric=True)


def build_model_from_drn(file, options=DirectEncodingParserOptions()):
    """
    Build a model in sparse representation from the explicit DRN representation.

    :param String file: DRN file containing the model.
    :param DirectEncodingParserOptions: Options for the parser.
    :return: Model in sparse representation.
    """
    intermediate = _core._build_sparse_model_from_drn(file, options)
    return _convert_sparse_model(intermediate, parametric=False)


def build_parametric_model_from_drn(file, options=DirectEncodingParserOptions()):
    """
    Build a parametric model in sparse representation from the explicit DRN representation.

    :param String file: DRN file containing the model.
    :param DirectEncodingParserOptions: Options for the parser.
    :return: Parametric model in sparse representation.
    """
    intermediate = _core._build_sparse_parametric_model_from_drn(file, options)
    return _convert_sparse_model(intermediate, parametric=True)


def build_interval_model_from_drn(file, options=DirectEncodingParserOptions()):
    """
    Build an interval model in sparse representation from the explicit DRN representation.

    :param String file: DRN file containing the model.
    :param DirectEncodingParserOptions: Options for the parser.
    :return: Interval model in sparse representation.
    """
    intermediate = _core._build_sparse_interval_model_from_drn(file, options)
    assert intermediate.supports_uncertainty
    if intermediate.model_type == ModelType.MDP:
        return intermediate._as_sparse_imdp()
    elif intermediate.model_type == ModelType.POMDP:
        return intermediate._as_sparse_ipomdp()
    else:
        raise stormpy.exceptions.StormError("Not supported interval model constructed")


def perform_bisimulation(model, properties, bisimulation_type, graph_preserving=True):
    """
    Perform bisimulation on model.
    :param model: Model.
    :param properties: Properties to preserve during bisimulation.
    :param bisimulation_type: Type of bisimulation (weak or strong).
    :param graph_preserving: Whether the graph structure should be preserved.
    :return: Model after bisimulation.
    """
    return perform_sparse_bisimulation(model, properties, bisimulation_type, graph_preserving)


def perform_sparse_bisimulation(model, properties, bisimulation_type, graph_preserving=True):
    """
    Perform bisimulation on model in sparse representation.
    :param model: Model.
    :param properties: Properties to preserve during bisimulation.
    :param bisimulation_type: Type of bisimulation (weak or strong).
    :param graph_preserving: Whether the graph structure should be preserved.
    :return: Model after bisimulation.
    """
    formulae = [(prop.raw_formula if isinstance(prop, Property) else prop) for prop in properties]
    if model.supports_parameters:
        return _core._perform_parametric_bisimulation(model, formulae, bisimulation_type, graph_preserving)
    else:
        return _core._perform_bisimulation(model, formulae, bisimulation_type, graph_preserving)


def perform_symbolic_bisimulation(model, properties, quotient_format=stormpy.QuotientFormat.DD):
    """
    Perform bisimulation on model in symbolic representation.
    :param model: Model.
    :param properties: Properties to preserve during bisimulation.
    :param quotient_format: Return format of quotient.
    :return: Model after bisimulation.
    """
    formulae = [(prop.raw_formula if isinstance(prop, Property) else prop) for prop in properties]
    bisimulation_type = BisimulationType.STRONG
    if model.supports_parameters:
        return _core._perform_symbolic_parametric_bisimulation(model, formulae, bisimulation_type, quotient_format)
    else:
        return _core._perform_symbolic_bisimulation(model, formulae, bisimulation_type, quotient_format)


def model_checking(model, property, only_initial_states=False, extract_scheduler=False, force_fully_observable=False, environment=Environment()):
    """
    Perform model checking on model for property.
    :param model: Model.
    :param property: Property to check for.
    :param only_initial_states: If True, only results for initial states are computed, otherwise for all states.
    :param extract_scheduler: If True, try to extract a scheduler
    :return: Model checking result.
    :rtype: CheckResult
    """
    if model.is_sparse_model:
        return check_model_sparse(
            model,
            property,
            only_initial_states=only_initial_states,
            extract_scheduler=extract_scheduler,
            force_fully_observable=force_fully_observable,
            environment=environment,
        )
    else:
        assert model.is_symbolic_model
        if extract_scheduler:
            raise stormpy.exceptions.StormError("Model checking based on dd engine does not support extracting schedulers right now.")
        return check_model_dd(model, property, only_initial_states=only_initial_states, environment=environment)


def check_model_sparse(model, property, only_initial_states=False, extract_scheduler=False, force_fully_observable=False, hint=None, environment=Environment()):
    """
    Perform model checking on model for property.
    :param model: Model.
    :param property: Property to check for.
    :param only_initial_states: If True, only results for initial states are computed, otherwise for all states.
    :param extract_scheduler: If True, try to extract a scheduler
    :param hint: If not None, this hint is used by the model checker
    :param force_fully_observable: If True, treat a POMDP as an MDP
    :return: Model checking result.
    :rtype: CheckResult
    """
    if isinstance(property, Property):
        formula = property.raw_formula
    else:
        formula = property

    if model.is_partially_observable:
        if force_fully_observable:
            # Note that casting a model to a fully observable model wont work with python/pybind, so we actually have other access points
            if model.supports_parameters:
                raise NotImplementedError("Model checking of partially observable models is not supported for parametric models.")
            elif model.supports_uncertainty:
                raise NotImplementedError("Model checking of partially observable models is not supported for interval models.")
            elif model.is_exact:
                task = _core.ExactCheckTask(formula, only_initial_states)
                task.set_produce_schedulers(extract_scheduler)
                if hint:
                    task.set_hint(hint)
                return _core._exact_model_checking_fully_observable(model, task, environment=environment)
            else:
                task = _core.CheckTask(formula, only_initial_states)
                task.set_produce_schedulers(extract_scheduler)
                if hint:
                    task.set_hint(hint)
                return _core._model_checking_fully_observable(model, task, environment=environment)
        else:
            raise RuntimeError("Model checking of partially observable models is handled via dedicated methods, unless the force fully-observable is set.")

    if model.supports_parameters:
        task = _core.ParametricCheckTask(formula, only_initial_states)
        task.set_produce_schedulers(extract_scheduler)
        if hint:
            task.set_hint(hint)
        return _core._parametric_model_checking_sparse_engine(model, task, environment=environment)
    else:
        if model.is_exact:
            if formula.is_multi_objective_formula:
                return _core._multi_objective_model_checking_exact(model, formula, environment=environment)
            task = _core.ExactCheckTask(formula, only_initial_states)
            task.set_produce_schedulers(extract_scheduler)
            if hint:
                task.set_hint(hint)
            return _core._exact_model_checking_sparse_engine(model, task, environment=environment)
        else:
            if formula.is_multi_objective_formula:
                return _core._multi_objective_model_checking_double(model, formula, environment=environment)
            task = _core.CheckTask(formula, only_initial_states)
            task.set_produce_schedulers(extract_scheduler)
            if hint:
                task.set_hint(hint)
            return _core._model_checking_sparse_engine(model, task, environment=environment)


def check_model_dd(model, property, only_initial_states=False, environment=Environment()):
    """
    Perform model checking using dd engine.
    :param model: Model.
    :param property: Property to check for.
    :param only_initial_states: If True, only results for initial states are computed, otherwise for all states.
    :return: Model checking result.
    :rtype: CheckResult
    """
    if isinstance(property, Property):
        formula = property.raw_formula
    else:
        formula = property

    if model.supports_parameters:
        task = _core.ParametricCheckTask(formula, only_initial_states)
        return _core._parametric_model_checking_dd_engine(model, task, environment=environment)
    else:
        task = _core.CheckTask(formula, only_initial_states)
        return _core._model_checking_dd_engine(model, task, environment=environment)


def check_model_hybrid(model, property, only_initial_states=False, environment=Environment()):
    """
    Perform model checking using hybrid engine.
    :param model: Model.
    :param property: Property to check for.
    :param only_initial_states: If True, only results for initial states are computed, otherwise for all states.
    :return: Model checking result.
    :rtype: CheckResult
    """
    if isinstance(property, Property):
        formula = property.raw_formula
    else:
        formula = property

    if model.supports_parameters:
        task = _core.ParametricCheckTask(formula, only_initial_states)
        return _core._parametric_model_checking_hybrid_engine(model, task, environment=environment)
    else:
        task = _core.CheckTask(formula, only_initial_states)
        return _core._model_checking_hybrid_engine(model, task, environment=environment)


def transform_to_sparse_model(model):
    """
    Transform model in symbolic representation into model in sparse representation.
    :param model: Symbolic model.
    :return: Sparse model.
    """
    if model.supports_parameters:
        return _core._transform_to_sparse_parametric_model(model)
    else:
        return _core._transform_to_sparse_model(model)


def transform_to_discrete_time_model(model, properties):
    """
    Transform continuous-time model to discrete time model.
    :param model: Continuous-time model.
    :param properties: List of properties to transform as well.
    :return: Tuple (Discrete-time model, converted properties).
    """
    formulae = [(prop.raw_formula if isinstance(prop, Property) else prop) for prop in properties]
    if model.supports_parameters:
        return _core._transform_to_discrete_time_parametric_model(model, formulae)
    else:
        return _core._transform_to_discrete_time_model(model, formulae)


def eliminate_non_markovian_chains(ma, properties, label_behavior):
    """
    Eliminate chains of non-Markovian states if possible.
    :param ma: Markov automaton.
    :param properties: List of properties to transform as well.
    :param label_behavior: Behavior of labels while elimination.
    :return: Tuple (converted MA, converted properties).
    """
    formulae = [(prop.raw_formula if isinstance(prop, Property) else prop) for prop in properties]
    if ma.supports_parameters:
        return _core._eliminate_non_markovian_chains_parametric(ma, formulae, label_behavior)
    else:
        return _core._eliminate_non_markovian_chains(ma, formulae, label_behavior)


def prob01min_states(model, eventually_formula):
    assert type(eventually_formula) == logic.EventuallyFormula
    labelform = eventually_formula.subformula
    labelprop = _core.Property("label-prop", labelform)
    phiStates = BitVector(model.nr_states, True)
    psiStates = model_checking(model, labelprop).get_truth_values()
    return compute_prob01min_states(model, phiStates, psiStates)


def prob01max_states(model, eventually_formula):
    assert type(eventually_formula) == logic.EventuallyFormula
    labelform = eventually_formula.subformula
    labelprop = _core.Property("label-prop", labelform)
    phiStates = BitVector(model.nr_states, True)
    psiStates = model_checking(model, labelprop).get_truth_values()
    return compute_prob01max_states(model, phiStates, psiStates)


def compute_prob01_states(model, phi_states, psi_states):
    """
    Compute prob01 states for properties of the form phi_states until psi_states

    :param SparseDTMC model:
    :param BitVector phi_states:
    :param BitVector psi_states: Target states
    """
    if model.model_type != ModelType.DTMC:
        raise stormpy.exceptions.StormError("Prob 01 is only defined for DTMCs -- model must be a DTMC")

    if model.supports_parameters:
        return _core._compute_prob01states_rationalfunc(model, phi_states, psi_states)
    else:
        return _core._compute_prob01states_double(model, phi_states, psi_states)


def compute_prob01min_states(model, phi_states, psi_states):
    if model.model_type == ModelType.DTMC:
        return compute_prob01_states(model, phi_states, psi_states)
    if model.supports_parameters:
        return _core._compute_prob01states_min_rationalfunc(model, phi_states, psi_states)
    else:
        return _core._compute_prob01states_min_double(model, phi_states, psi_states)


def compute_prob01max_states(model, phi_states, psi_states):
    if model.model_type == ModelType.DTMC:
        return compute_prob01_states(model, phi_states, psi_states)
    if model.supports_parameters:
        return _core._compute_prob01states_max_rationalfunc(model, phi_states, psi_states)
    else:
        return _core._compute_prob01states_max_double(model, phi_states, psi_states)


def topological_sort(model, forward=True, initial=[]):
    """

    :param model: A sparse model
    :param forward: A flag whether the sorting should be forward or backwards
    :param initial: a list of states
    :return: A topological sort of the states
    """
    matrix = model.transition_matrix if forward else model.backward_transition_matrix
    if isinstance(model, storage._storage._SparseParametricModel):
        return storage._storage._topological_sort_rf(matrix, initial)
    elif isinstance(model, storage._storage._SparseModel):
        return storage._storage._topological_sort_double(matrix, initial)
    else:
        raise stormpy.exceptions.StormError("Unknown kind of model.")


def get_reachable_states(model, initial_states, constraint_states, target_states, maximal_steps=None, choice_filter=None):
    """
    Get the states that are reachable in a sparse model

    :param model: A model
    :param initial_states: Which states should be definitively reachable
    :param constraint_states:
    :param target_states: Which states should be considered absorbing
    :param maximal_steps: The maximal depth to explore
    :param choice_filter:
    :return:
    """
    if model.supports_parameters:
        return _core._get_reachable_states_rf(model, initial_states, constraint_states, target_states, maximal_steps, choice_filter)
    if model.is_exact:
        return _core._get_reachable_states_exact(model, initial_states, constraint_states, target_states, maximal_steps, choice_filter)
    return _core._get_reachable_states_double(model, initial_states, constraint_states, target_states, maximal_steps, choice_filter)


def compute_expected_number_of_visits(environment, model):
    """
    Compute the number of expected visits. Model must be deterministic.

    :param environment: An model checking environment
    :param model: A DTMC or CTMC
    :return: A vector with the expected number of visits
    """
    if model.supports_parameters:
        raise NotImplementedError("Expected number of visits is not implemented for parametric models")
    if model.is_exact:
        return _core._compute_expected_number_of_visits_exact(environment, model)
    return _core._compute_expected_number_of_visits_double(environment, model)


def compute_steady_state_distribution(environment, model):
    """
    Compute the steady-state (aka stationary) distribution. Model must be deterministic.

    :param environment: A model checking environment
    :param model: A DTMC or CTMC
    :return: A vector with the steady-state distribution
    """
    if model.supports_parameters:
        raise NotImplementedError("Steady-state distribution is not implemented for parametric models")
    if model.is_exact:
        return _core._compute_steady_state_distribution_exact(environment, model)
    return _core._compute_steady_state_distribution_double(environment, model)


def construct_submodel(model, states, actions, keep_unreachable_states=True, options=SubsystemBuilderOptions()):
    """

    :param model: The model
    :param states: Which states should be preserved
    :param actions: Which actions should be preserved
    :param keep_unreachable_states: If False, run a reachability analysis.
    :param options: An options object of type SubsystemBuilderOptions
    :return: A model with fewer states/actions
    """
    if model.supports_parameters:
        return _core._construct_subsystem_RatFunc(model, states, actions, keep_unreachable_states, options)
    if model.is_exact:
        return _core._construct_subsystem_Exact(model, states, actions, keep_unreachable_states, options)
    return _core._construct_subsystem_Double(model, states, actions, keep_unreachable_states, options)


def eliminate_ECs(matrix, subsystem, possible_ecs, add_sink_row_states, add_self_loop_at_sink_states=False):
    """
    For each such EC (that is not contained in another EC), we add a new state and redirect all incoming and outgoing
             transitions of the EC to (and from) this state.

    :param matrix:
    :param subsystem: BitVector with states many entries. Only states in the given subsystem are kept. Transitions leading to a state outside of the subsystem will be
             removed (but the corresponding row is kept, possibly yielding empty rows).
             The ECs are then identified on the subsystem.
    :param possible_ecs: BitVector with rows many entries. Only ECs for which possible_ecs is true for all choices are considered.
             Furthermore, the rows that contain a transition leading outside of the subsystem are not considered for an EC.
    :param add_sink_row_states: BitVector with states many entries. If add_sink_row_states is true for at least one state of an eliminated EC, a row is added to the new state (representing the choice to stay at the EC forever).
    :param add_self_loop_at_sink_states: if true, such rows get a selfloop (with value 1). Otherwise, the row remains empty.
    :return: A container with various information.
    """
    assert matrix.nr_columns == subsystem.size(), "subsystem vector should have an entry for every state."
    assert matrix.nr_rows == possible_ecs.size(), "possible_ecs vector should have an entry for every row."
    assert matrix.nr_columns == add_sink_row_states.size(), "add_sink_row_states vector should have an entry for every state."

    return _core._eliminate_end_components_double(matrix, subsystem, possible_ecs, add_sink_row_states, add_self_loop_at_sink_states)


def parse_properties(properties, context=None, filters=None):
    """

    :param properties: A string with the pctl properties
    :param context: A symbolic model that gives meaning to variables and constants.
    :param filters: filters, if applicable.
    :return: A list of properties
    """
    if context is None:
        return _core.parse_properties_without_context(properties, filters)
    elif type(context) == _core.SymbolicModelDescription:
        if context.is_prism_program:
            return _core.parse_properties_for_prism_program(properties, context.as_prism_program(), filters)
        else:
            return _core.parse_properties_for_jani_program(properties, context.as_jani_model(), filters)
    elif type(context) == storage.PrismProgram:
        return _core.parse_properties_for_prism_program(properties, context, filters)
    elif type(context) == storage.JaniModel:
        return _core.parse_properties_for_jani_model(properties, context, filters)
    else:
        raise stormpy.exceptions.StormError("Unclear context. Please pass a symbolic model description")


def export_to_drn(model, file, options=DirectEncodingOptions()):
    """
    Export a model to DRN format
    :param model: The model
    :param file: A path
    :param options: DirectEncodingOptions
    :return:
    """
    if model.supports_parameters:
        return _core._export_parametric_to_drn(model, file, options)
    if model.supports_uncertainty:
        return _core._export_to_drn_interval(model, file, options)
    if model.is_exact:
        return _core._export_exact_to_drn(model, file, options)
    return _core._export_to_drn(model, file, options)

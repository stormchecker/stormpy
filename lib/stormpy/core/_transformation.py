"""Transformations of models, e.g. bisimulation minimization or the construction of submodels."""

from __future__ import annotations

from collections.abc import Iterable

from stormpy import developer
from stormpy.developer import storage
from stormpy.core._common import _formulas, _value_type_of_model
from stormpy import Rational
from stormpy.developer import (
    AddUncertainty,
    BisimulationOptions,
    BisimulationType,
    DdBisimulationOptions,
    EliminationLabelBehavior,
    Property,
    QuotientFormat,
    SubsystemBuilderOptions,
    SubsystemBuilderReturnType,
)
from stormpy.exceptions import StormError


def perform_bisimulation(
    model,
    properties: Property | Iterable[Property],
    *,
    bisimulation_type: BisimulationType = BisimulationType.STRONG,
    options: BisimulationOptions | None = None,
    quotient_format: QuotientFormat = QuotientFormat.DD,
):
    """
    Minimize a model via bisimulation while preserving the given properties.

    :param model: The model (sparse or symbolic).
    :param properties: Property or properties which are preserved by the minimization.
    :param bisimulation_type: Type of bisimulation (strong or weak).
    :param options: (optional) Further options for the bisimulation of sparse models.
        If given, its bisimulation type takes precedence over the bisimulation_type argument.
    :param quotient_format: Format of the quotient for symbolic models (DD for a symbolic quotient, SPARSE for a sparse quotient).
    :return: The minimized model.
    """
    formulas = _formulas(properties)
    if model.is_sparse_model:
        if options is None:
            options = BisimulationOptions()
            options.bisimulation_type = bisimulation_type
        return developer.perform_bisimulation_minimization(model, formulas, options)
    if options is not None:
        raise StormError("Bisimulation options are only supported for sparse models.")
    quotient = developer.perform_bisimulation_minimization(
        model, formulas, bisimulation_type=bisimulation_type, quotient_format=quotient_format, bisimulation_options=DdBisimulationOptions()
    )
    return quotient


def transform_to_sparse_model(model, properties: Property | Iterable[Property] | None = None):
    """
    Transform a model in symbolic representation into a model in sparse representation.

    :param model: Symbolic model.
    :param properties: (optional) Property or properties which should be preserved. If None, all labels and reward models are preserved.
    :return: The model in sparse representation.
    """
    return developer.transform_symbolic_to_sparse_model(model, _formulas(properties))


def transform_to_discrete_time_model(model, properties: Property | Iterable[Property]) -> tuple:
    """
    Transform a continuous-time model (CTMC or MA) into a discrete-time model (DTMC or MDP).

    Formulas which are not preserved by the transformation are dropped (with a warning).

    :param model: Sparse continuous-time model.
    :param properties: Property or properties which are transformed accordingly.
    :return: Tuple of the discrete-time model and the transformed formulas.
    """
    discrete_model, formulas = developer.transform_continuous_to_discrete_time_sparse_model(model, _formulas(properties))
    return discrete_model, formulas


def eliminate_non_markovian_chains(model, properties: Property | Iterable[Property], label_behavior: EliminationLabelBehavior) -> tuple:
    """
    Eliminate chains of non-Markovian states in a Markov automaton if possible.

    Formulas which are not preserved by the elimination are dropped (with a warning).

    :param model: Sparse Markov automaton.
    :param properties: Property or properties which are transformed accordingly.
    :param label_behavior: How labels of eliminated states are handled.
    :return: Tuple of the resulting model (an MA or a CTMC) and the transformed formulas.
    """
    result, formulas = developer.eliminate_non_markovian_chains(model, _formulas(properties), label_behavior)
    return result, formulas


def build_submodel(
    model,
    states: storage.BitVector,
    actions: storage.BitVector,
    *,
    keep_unreachable_states: bool = True,
    options: SubsystemBuilderOptions | None = None,
) -> SubsystemBuilderReturnType:
    """
    Build the submodel restricted to the given states and actions.

    :param model: Sparse model.
    :param states: States which are kept.
    :param actions: Actions (choices) which are kept.
    :param keep_unreachable_states: If False, states which become unreachable are removed as well.
    :param options: (optional) Options for building the submodel.
    :return: Result containing the submodel (attribute ``model``) and the mappings to the original model.
    """
    return developer.build_subsystem(
        model, states, actions, keep_unreachable_states=keep_unreachable_states, options=options if options is not None else SubsystemBuilderOptions()
    )


def add_uncertainty(model, additive_uncertainty: float | Rational, *, minimal_value: float | Rational | None = None, max_successors: int | None = None):
    """
    Transform a model into an interval model by adding uncertainty to all transition probabilities.

    Each probability p becomes the interval [max(minimal_value, p - additive_uncertainty), min(1, p + additive_uncertainty)].

    :param model: Sparse model with float or Rational values.
    :param additive_uncertainty: Uncertainty added to each probability.
    :param minimal_value: (optional) Lower bound of each interval. Defaults to 0.0001.
    :param max_successors: (optional) Only states with at most this many successors are made uncertain.
    :return: The interval model (with Interval or RationalInterval values).
    """
    value_type = _value_type_of_model(model)
    if value_type not in (float, Rational):
        raise StormError("Uncertainty can only be added to models with float or Rational values.")
    transformer = AddUncertainty[value_type](model)
    if minimal_value is None:
        minimal_value = 0.0001 if value_type is float else Rational("1/10000")
    return transformer.transform(additive_uncertainty, minimal_value, max_successors)


def set_state_valuations(model, valuations: storage.Valuations):
    """
    Create a copy of the model with the given state valuations.

    :param model: Sparse DTMC or MDP.
    :param valuations: The new state valuations.
    :return: Copy of the model with the new state valuations.
    """
    if model.model_type not in [storage.ModelType.DTMC, storage.ModelType.MDP]:
        raise StormError(f"Only DTMCs and MDPs are supported, got {model.model_type}.")
    components = storage.SparseModelComponents(
        transition_matrix=model.transition_matrix, state_labeling=model.labeling, reward_models=model.reward_models, rate_transitions=False
    )
    components.state_valuations = valuations
    if model.has_choice_labeling():
        components.choice_labeling = model.choice_labeling
    if model.has_choice_origins():
        components.choice_origins = model.choice_origins
    return type(model)(components)

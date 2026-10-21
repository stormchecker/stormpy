"""Model checking of properties on sparse and symbolic models."""

from __future__ import annotations

from enum import Enum

from stormpy import developer, environments
from stormpy.core._common import _formula, _value_type_of_model
from stormpy import Interval, Rational, RationalInterval
from stormpy.developer import (
    CheckResult,
    CheckTask,
    Environment,
    ModelCheckerHint,
    Property,
    UncertaintyResolutionMode,
)
from stormpy.exceptions import StormError


class Engine(Enum):
    """Engine used for building models and model checking."""

    SPARSE = "sparse"
    """Explicit (sparse) engine. Requires a sparse model."""
    DD = "dd"
    """Symbolic engine based on decision diagrams. Requires a symbolic model."""
    HYBRID = "hybrid"
    """Hybrid engine combining decision diagrams and explicit numerical computations. Requires a symbolic model."""


def model_checking(
    model,
    property: Property,
    *,
    only_initial_states: bool = False,
    extract_scheduler: bool = False,
    force_fully_observable: bool = False,
    hint: ModelCheckerHint | None = None,
    uncertainty_resolution_mode: UncertaintyResolutionMode | None = None,
    engine: Engine | None = None,
    environment: Environment | None = None,
) -> CheckResult:
    """
    Model check a property on a model.

    Supports sparse and symbolic models, parametric models, interval models and multi-objective properties.

    :param model: The model (sparse or symbolic).
    :param property: The property (or formula) to check.
    :param only_initial_states: If True, only the results for the initial states are computed. Otherwise, the results for all states are computed.
    :param extract_scheduler: If True, an optimal scheduler is extracted (if supported). Only supported by the sparse engine.
    :param force_fully_observable: If True, a POMDP is treated as a fully observable MDP. Must be set for POMDPs.
    :param hint: (optional) Hint that may speed up the computation. Only supported by the sparse engine.
    :param uncertainty_resolution_mode: How uncertainty is resolved. Required for interval models, not allowed otherwise.
    :param engine: (optional) Engine to use. Defaults to the sparse engine for sparse models and the DD engine for symbolic models.
    :param environment: (optional) Environment configuring the solvers. Defaults to :func:`stormpy.environments.default`.
    :return: The model checking result, e.g. an :class:`stormpy.results.ExplicitQuantitativeCheckResult`. Use ``result[state]`` to get the value for a state together with its sound bounds as a :class:`stormpy.results.BoundedValue`, or ``result.get_value(state)`` to get the value only.
    """
    formula = _formula(property)
    environment = environment if environment is not None else environments.default(model)
    if engine is None:
        engine = Engine.SPARSE if model.is_sparse_model else Engine.DD
    if engine == Engine.SPARSE:
        if not model.is_sparse_model:
            raise StormError("The sparse engine requires a sparse model.")
    else:
        if not model.is_symbolic_model:
            raise StormError(f"The {engine.value} engine requires a symbolic model.")
        if extract_scheduler or hint is not None:
            raise StormError(f"The {engine.value} engine does not support extracting schedulers or hints.")

    value_type = _value_type_of_model(model)
    is_interval = value_type in (Interval, RationalInterval)
    if is_interval != (uncertainty_resolution_mode is not None):
        raise StormError("The uncertainty resolution mode must be given if and only if the model is an interval model.")
    if model.is_partially_observable and not force_fully_observable:
        raise StormError("Model checking of partially observable models is handled via stormpy.pomdp, unless force_fully_observable is set.")

    if formula.is_multi_objective_formula:
        if engine != Engine.SPARSE or model.supports_parameters or is_interval:
            raise StormError("Multi-objective model checking is only supported for non-parametric sparse models.")
        return developer.perform_multi_objective_model_checking(environment, model, formula, produce_scheduler=extract_scheduler)

    if is_interval:
        # Interval models are checked with tasks over the underlying number type
        value_type = Rational if value_type is RationalInterval else float
    task = CheckTask[value_type](formula, only_initial_states)
    task.set_produce_schedulers(extract_scheduler)
    if hint is not None:
        task.set_hint(hint)
    if uncertainty_resolution_mode is not None:
        task.set_uncertainty_resolution_mode(uncertainty_resolution_mode)

    if engine == Engine.SPARSE:
        return developer.verify_with_sparse_engine(environment, model, task)
    if engine == Engine.DD:
        return developer.verify_with_dd_engine(environment, model, task)
    return developer.verify_with_hybrid_engine(environment, model, task)

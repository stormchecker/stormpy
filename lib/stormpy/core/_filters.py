"""Filters for sparse, symbolic and hybrid model checking results."""

from __future__ import annotations

from stormpy.core._common import _result_value_type_of_model
from stormpy.developer import storage
from stormpy.developer import CheckResult, QualitativeCheckResult, SymbolicQualitativeCheckResult, ExplicitQualitativeCheckResult
from stormpy.exceptions import StormError


def create_filter_initial_states(model) -> QualitativeCheckResult:
    """
    Create a filter selecting the initial states of the model.

    The filter can be applied to a model checking result via ``result.filter(filter)``.

    :param model: The model (sparse or symbolic).
    :return: Qualitative check result containing the initial states.
    """
    if model.is_sparse_model:
        return ExplicitQualitativeCheckResult[_result_value_type_of_model(model)](model.initial_states_as_bitvector)
    return SymbolicQualitativeCheckResult[storage.DdType.Sylvan](model.reachable_states, model.initial_states)


def filter_initial_states(result: CheckResult, model) -> CheckResult:
    """
    Restrict the model checking result to the initial states of the model.

    :param result: Model checking result (explicit, symbolic or hybrid).
    :param model: The model (sparse or symbolic) the result was computed for.
    :return: The filtered result (the same object as ``result``).
    """
    result.filter(create_filter_initial_states(model))
    return result


def create_filter(model, expression: storage.Expression) -> SymbolicQualitativeCheckResult:
    """
    Create a filter selecting the states of a symbolic model satisfying the given expression.

    The filter can be applied to a model checking result via ``result.filter(filter)``.

    :param model: The symbolic model.
    :param expression: Boolean expression over the model variables.
    :return: Qualitative check result containing the states satisfying the expression.
    """
    if not model.is_symbolic_model:
        raise StormError("Filters from expressions are only supported for symbolic models.")
    return SymbolicQualitativeCheckResult[storage.DdType.Sylvan](model.reachable_states, model.get_states(expression))

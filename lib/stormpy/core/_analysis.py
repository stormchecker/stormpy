"""Qualitative and quantitative analysis of sparse models."""

from __future__ import annotations

from collections.abc import Iterable

from stormpy import developer
from stormpy.developer import storage
from stormpy.core._common import _formula, _value_type_of_model
from stormpy.core._modelchecking import model_checking
from stormpy.developer import CheckResult, CheckTask, Environment, OptimizationDirection, PcaaWeightVectorChecker, Property
from stormpy.exceptions import StormError


def topological_sort(model, *, forward: bool = True, initial: Iterable[int] | None = None) -> list[int]:
    """
    Sort the states of a sparse model topologically.

    :param model: Sparse model.
    :param forward: If True, the states are sorted along the transitions. Otherwise, the states are sorted along the backward transitions.
    :param initial: (optional) States from which the sorting starts.
    :return: List of states in topological order.
    """
    if not model.is_sparse_model:
        raise StormError("Topological sorting is only supported for sparse models.")
    matrix = model.transition_matrix if forward else model.backward_transition_matrix
    return storage.get_topological_sort(matrix, list(initial) if initial is not None else [])


def compute_prob01_states(model, property: Property) -> tuple[storage.BitVector, storage.BitVector]:
    """
    Compute the states satisfying a reachability or until property with probability 0 and with probability 1.

    The property has the form ``F psi`` or ``phi U psi`` (unbounded), optionally within a probability operator, e.g. ``Pmax=? [F "goal"]``.
    The computation is purely graph-based.
    For nondeterministic models, the probability operator must specify the optimization direction, e.g. ``Pmax=? [F "goal"]``.

    :param model: Sparse model.
    :param property: Property (or formula) describing the reachability or until objective.
    :return: Tuple (prob0, prob1) of the states with probability 0 and with probability 1.
    """
    if not model.is_sparse_model:
        raise StormError("Prob0/1 computation is only supported for sparse models.")
    formula = _formula(property)
    optimality_type = None
    if formula.is_probability_operator_formula:
        if formula.has_optimality_type:
            optimality_type = formula.optimality_type
        formula = formula.subformula
    # Compute phi and psi states
    if formula.is_eventually_formula:
        phi_states = storage.BitVector(model.nr_states, True)
        psi_formula = formula.subformula
    elif formula.is_until_formula:
        phi_states = model_checking(model, formula.left_subformula).get_truth_values_vector()
        psi_formula = formula.right_subformula
    else:
        raise StormError(f"Prob0/1 computation is only supported for unbounded reachability (F psi) or until (phi U psi) formulas, got '{formula}'.")
    psi_states = model_checking(model, psi_formula).get_truth_values_vector()

    if not model.is_nondeterministic_model:
        return developer.perform_prob01(model, phi_states, psi_states)
    if optimality_type is None:
        raise StormError("Nondeterministic models require an optimization direction via Pmin/Pmax in the property.")
    if optimality_type == OptimizationDirection.MAXIMIZE:
        return developer.perform_prob01_max(model, phi_states, psi_states)
    else:
        return developer.perform_prob01_min(model, phi_states, psi_states)


def compute_expected_number_of_visits(model, *, environment: Environment | None = None) -> CheckResult:
    """
    Compute the expected number of visits of each state, starting from the initial states.

    :param model: Sparse deterministic model (DTMC or CTMC). Parametric models are not supported.
    :param environment: (optional) Environment configuring the solvers.
    :return: Quantitative result containing the expected number of visits for each state.
    """
    if model.supports_parameters:
        raise StormError("The expected number of visits is not supported for parametric models.")
    return developer.compute_expected_visiting_times_with_sparse_engine(environment if environment is not None else Environment(), model)


def compute_steady_state_distribution(model, *, environment: Environment | None = None) -> CheckResult:
    """
    Compute the steady-state (aka stationary) distribution.

    :param model: Sparse deterministic model (DTMC or CTMC). Parametric models are not supported.
    :param environment: (optional) Environment configuring the solvers.
    :return: Quantitative result containing the steady-state probability for each state.
    """
    if model.supports_parameters:
        raise StormError("The steady-state distribution is not supported for parametric models.")
    return developer.compute_steady_state_distribution_with_sparse_engine(environment if environment is not None else Environment(), model)


def create_weight_vector_checker(
    model, property: Property, *, produce_scheduler: bool = False, environment: Environment | None = None
) -> tuple[PcaaWeightVectorChecker, storage.SparseModelMemoryProductReverseData | None]:
    """
    Create a checker for weighted sums of the objectives of a multi-objective property.

    The checker optimizes the weighted sum for a given weight vector via ``checker.check(env, weights)``.

    :param model: Sparse MDP (with float or Rational values).
    :param property: Multi-objective property (or formula).
    :param produce_scheduler: If True, the checker can compute optimal schedulers.
    :param environment: (optional) Environment configuring the preprocessing.
    :return: Tuple of the checker and the data mapping schedulers of the checker back to the original model (None if not required).
    """
    if model.supports_parameters or model.supports_uncertainty:
        raise StormError("Parametric and interval models are not supported.")
    return developer.create_weight_vector_checker(environment if environment is not None else Environment(), model, _formula(property), produce_scheduler)

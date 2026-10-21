"""Graph and numerical analyses of probabilistic models.

Includes maximal end components, shortest paths, qualitative reachability,
expected visiting times and steady-state distributions.
"""

from __future__ import annotations

import stormpy as _stormpy
from stormpy.developer import storage as _storage, utility as _utility
from stormpy.core._analysis import topological_sort, compute_prob01_states, compute_expected_number_of_visits, compute_steady_state_distribution

MaximalEndComponent = _storage.MaximalEndComponent
MaximalEndComponentDecomposition = _storage.MaximalEndComponentDecomposition.publish_as("stormpy.analysis.MaximalEndComponentDecomposition")
Path = _utility.Path.publish_as("stormpy.analysis.Path")


def get_maximal_end_components(model: "_stormpy.models.SparseModel") -> MaximalEndComponentDecomposition:
    """Compute the maximal end components of a nondeterministic sparse model.

    :param model: Sparse MDP, POMDP, Markov automaton or stochastic game.
    :return: An iterable decomposition into maximal end components.
    """
    return MaximalEndComponentDecomposition(model)


def shortest_path(
    model: _stormpy.models.SparseModel,
    target: int | str | list[int] | _stormpy.datastructures.BitVector,
    *,
    k: int = 1,
) -> tuple[list[int], float | _stormpy.Rational]:
    """Compute the k-th most probable path from an initial state to a target.

    Paths stop when they first reach a target and may contain loops. They are
    ranked by decreasing probability, rather than by the number of transitions.

    :param model: Sparse DTMC with floating-point or rational probabilities.
    :param target: Target state ID, list of state IDs, bitvector or state label.
    :param k: One-based path rank; defaults to the most probable path.
    :return: Tuple (states, probability), with states ordered from initial state to target.
    :raises ValueError: If k is not positive.
    """
    if not isinstance(k, int):
        raise TypeError("k must be an integer.")
    if k < 1:
        raise ValueError("k must be positive (path ranks start at 1).")
    if not model.is_sparse_model or model.model_type != _stormpy.models.ModelType.DTMC:
        raise _stormpy.exceptions.StormError("Shortest paths are only supported for sparse DTMCs.")
    generator = _utility.ShortestPathsGenerator(model, target)
    states = generator.get_path_as_list(k)
    states.reverse()
    return states, generator.get_distance(k)


__all__ = [
    "MaximalEndComponent",
    "MaximalEndComponentDecomposition",
    "Path",
    "get_maximal_end_components",
    "shortest_path",
    "topological_sort",
    "compute_prob01_states",
    "compute_expected_number_of_visits",
    "compute_steady_state_distribution",
]

"""Graph and numerical analyses of probabilistic models.

Includes maximal end components, shortest paths, qualitative reachability,
expected visiting times and steady-state distributions.
"""

import stormpy as _stormpy
from stormpy.developer import storage as _storage, utility as _utility
from stormpy.core._analysis import topological_sort, compute_prob01_states, compute_expected_number_of_visits, compute_steady_state_distribution

MaximalEndComponent = _storage.MaximalEndComponent
MaximalEndComponentDecomposition = _storage.MaximalEndComponentDecomposition.publish_as("stormpy.analysis.MaximalEndComponentDecomposition")
ShortestPathsGenerator = _utility.ShortestPathsGenerator.publish_as("stormpy.analysis.ShortestPathsGenerator")
Path = _utility.Path.publish_as("stormpy.analysis.Path")
MatrixFormat = _utility.MatrixFormat


def get_maximal_end_components(model: "_stormpy.models.SparseModel") -> MaximalEndComponentDecomposition:
    """Compute the maximal end components of a nondeterministic sparse model.

    :param model: Sparse MDP, POMDP, Markov automaton or stochastic game.
    :return: An iterable decomposition into maximal end components.
    """
    return MaximalEndComponentDecomposition(model)


__all__ = [
    "MaximalEndComponent",
    "MaximalEndComponentDecomposition",
    "ShortestPathsGenerator",
    "Path",
    "MatrixFormat",
    "get_maximal_end_components",
    "topological_sort",
    "compute_prob01_states",
    "compute_expected_number_of_visits",
    "compute_steady_state_distribution",
]

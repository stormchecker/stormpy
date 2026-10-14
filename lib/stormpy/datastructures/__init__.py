"""Matrices, labels, schedulers, valuations, memory structures and JSON containers."""

import stormpy as _stormpy
from stormpy.developer import storage as _bindings

BitVector = _bindings.BitVector
SparseMatrixEntry = _bindings.SparseMatrixEntry.publish_as("stormpy.datastructures.SparseMatrixEntry")
SparseMatrixBuilder = _bindings.SparseMatrixBuilder.publish_as("stormpy.datastructures.SparseMatrixBuilder")
SparseMatrix = _bindings.SparseMatrix.publish_as("stormpy.datastructures.SparseMatrix")
SparseMatrixRows = _bindings.SparseMatrixRows.publish_as("stormpy.datastructures.SparseMatrixRows")
StateLabeling = _bindings.StateLabeling
ChoiceLabeling = _bindings.ChoiceLabeling
Scheduler = _bindings.Scheduler.publish_as("stormpy.datastructures.Scheduler")
SchedulerChoice = _bindings.SchedulerChoice.publish_as("stormpy.datastructures.SchedulerChoice")
Distribution = _bindings.Distribution.publish_as("stormpy.datastructures.Distribution")
Valuations = _bindings.Valuations
ValuationClassDescription = _bindings.ValuationClassDescription
ValuationDescriptionBuilder = _bindings.ValuationDescriptionBuilder
ValuationTransformer = _bindings.ValuationTransformer
SimpleValuation = _bindings.SimpleValuation
MemoryStructure = _bindings.MemoryStructure
MemoryStructureBuilder = _bindings.MemoryStructureBuilder.publish_as("stormpy.datastructures.MemoryStructureBuilder")
ChoiceOrigins = _bindings.ChoiceOrigins
JaniChoiceOrigins = _bindings.JaniChoiceOrigins
PrismChoiceOrigins = _bindings.PrismChoiceOrigins
MaximalEndComponent = _bindings.MaximalEndComponent
MaximalEndComponentDecomposition = _bindings.MaximalEndComponentDecomposition.publish_as("stormpy.datastructures.MaximalEndComponentDecomposition")
JsonContainer = _bindings.JsonContainer.publish_as("stormpy.datastructures.JsonContainer")

__all__ = [
    "BitVector",
    "SparseMatrixEntry",
    "SparseMatrixBuilder",
    "SparseMatrix",
    "SparseMatrixRows",
    "StateLabeling",
    "ChoiceLabeling",
    "Scheduler",
    "SchedulerChoice",
    "Distribution",
    "Valuations",
    "ValuationClassDescription",
    "ValuationDescriptionBuilder",
    "ValuationTransformer",
    "SimpleValuation",
    "MemoryStructure",
    "MemoryStructureBuilder",
    "ChoiceOrigins",
    "JaniChoiceOrigins",
    "PrismChoiceOrigins",
    "MaximalEndComponent",
    "MaximalEndComponentDecomposition",
    "JsonContainer",
    "build_sparse_matrix",
    "get_maximal_end_components",
]

from . import _json, _scheduler, _valuations
from ._matrix import build_sparse_matrix


def get_maximal_end_components(model: "_stormpy.models.SparseModel") -> "MaximalEndComponentDecomposition":
    """Compute the maximal end components of a nondeterministic sparse model.

    :param model: Sparse MDP, POMDP, Markov automaton or stochastic game.
    :return: An iterable decomposition into maximal end components.
    """
    return MaximalEndComponentDecomposition(model)

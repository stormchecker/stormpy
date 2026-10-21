"""Model transformations and their options, policies and mapping results.

Includes bisimulation minimization, submodel construction, representation changes
and the addition of uncertainty.
"""

from stormpy import developer as _bindings
from stormpy.core._transformation import (
    perform_bisimulation,
    transform_to_sparse_model,
    transform_to_discrete_time_model,
    eliminate_non_markovian_chains,
    build_submodel,
    add_uncertainty,
    set_state_valuations,
)

BisimulationType = _bindings.BisimulationType
BisimulationOptions = _bindings.BisimulationOptions
StateLabelPreservation = _bindings.StateLabelPreservation
QuotientFormat = _bindings.QuotientFormat
EliminationLabelBehavior = _bindings.EliminationLabelBehavior
SubsystemBuilderOptions = _bindings.SubsystemBuilderOptions
SubsystemBuilderReturnType = _bindings.SubsystemBuilderReturnType.publish_as("stormpy.transformations.SubsystemBuilderReturnType")

__all__ = [
    "BisimulationType",
    "BisimulationOptions",
    "StateLabelPreservation",
    "QuotientFormat",
    "EliminationLabelBehavior",
    "SubsystemBuilderOptions",
    "SubsystemBuilderReturnType",
    "perform_bisimulation",
    "transform_to_sparse_model",
    "transform_to_discrete_time_model",
    "eliminate_non_markovian_chains",
    "build_submodel",
    "add_uncertainty",
    "set_state_valuations",
]

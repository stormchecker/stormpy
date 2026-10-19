"""Raw pybind11 bindings for storm-pomdp.

This module is only meant for developers.
Use :mod:`stormpy.pomdp` for the public API.

The naming of functions and classes of the bindings mirrors the corresponding ``storm::pomdp`` C++ functions and classes.
"""

from stormpy.info import _config

if not _config.STORM_WITH_POMDP:
    raise ImportError("No support for POMDPs was built in Storm.")

from . import _pomdp

# Mirror _pomdp's entire namespace (including private underscored classes) directly onto this package.
for _name, _value in vars(_pomdp).items():
    if not _name.startswith("__"):
        globals()[_name] = _value
del _name, _value

from stormpy._template import _TemplateClass, _deduce_default, _deduce_from_object
from stormpy.developer.storage import parameters_of_model as _parameters_of_model

_deduce_from_pomdp = _deduce_from_object(_parameters_of_model, keyword="pomdp")

# Define templated classes
# Transformations
MakePOMDPCanonic = _TemplateClass(
    "stormpy.pomdp.developer.MakePOMDPCanonic",
    _pomdp,
    parameters=("ValueType",),
    deduce=_deduce_from_pomdp,
)

PomdpMemoryUnfolder = _TemplateClass(
    "stormpy.pomdp.developer.PomdpMemoryUnfolder",
    _pomdp,
    parameters=("ValueType",),
    deduce=_deduce_from_pomdp,
)

BinaryPomdpTransformer = _TemplateClass(
    "stormpy.pomdp.developer.BinaryPomdpTransformer",
    _pomdp,
    parameters=("ValueType",),
    deduce=_deduce_default(float),
)

PomdpTransformationResult = _TemplateClass(
    "stormpy.pomdp.developer.PomdpTransformationResult",
    _pomdp,
    parameters=("ValueType",),
)

ApplyFiniteSchedulerToPomdp = _TemplateClass(
    "stormpy.pomdp.developer.ApplyFiniteSchedulerToPomdp",
    _pomdp,
    parameters=("ValueType",),
    deduce=_deduce_from_pomdp,
)

ObservationTraceUnfolder = _TemplateClass(
    "stormpy.pomdp.developer.ObservationTraceUnfolder",
    _pomdp,
    parameters=("ValueType",),
    deduce=_deduce_from_object(_parameters_of_model, keyword="model"),
)


# Belief tracking
BeliefSupportTracker = _TemplateClass(
    "stormpy.pomdp.developer.BeliefSupportTracker",
    _pomdp,
    parameters=("ValueType",),
    deduce=_deduce_from_pomdp,
)

SparseBeliefState = _TemplateClass(
    "stormpy.pomdp.developer.SparseBeliefState",
    _pomdp,
    parameters=("ValueType",),
)

NondeterministicBeliefTrackerOptions = _TemplateClass(
    "stormpy.pomdp.developer.NondeterministicBeliefTrackerOptions",
    _pomdp,
    parameters=("ValueType",),
    deduce=_deduce_default(float),
)

NondeterministicBeliefTracker = _TemplateClass(
    "stormpy.pomdp.developer.NondeterministicBeliefTracker",
    _pomdp,
    parameters=("ValueType",),
    deduce=_deduce_from_pomdp,
)


# Qualitative analysis
IterativePolicySearch = _TemplateClass(
    "stormpy.pomdp.developer.IterativePolicySearch",
    _pomdp,
    parameters=("ValueType",),
)

WinningRegionQueryInterface = _TemplateClass(
    "stormpy.pomdp.developer.WinningRegionQueryInterface",
    _pomdp,
    parameters=("ValueType",),
    deduce=_deduce_from_pomdp,
)


# Quantitative analysis
BeliefBasedModelCheckerOptions = _TemplateClass(
    "stormpy.pomdp.developer.BeliefBasedModelCheckerOptions",
    _pomdp,
    parameters=("ValueType",),
    deduce=_deduce_default(float),
)

BeliefBasedModelCheckerResult = _TemplateClass(
    "stormpy.pomdp.developer.BeliefBasedModelCheckerResult",
    _pomdp,
    parameters=("ValueType",),
)

ObservationBasedFiniteStateController = _TemplateClass(
    "stormpy.pomdp.developer.ObservationBasedFiniteStateController",
    _pomdp,
    parameters=("ValueType",),
)


# Monitor verification
MonitorVerifier = _TemplateClass(
    "stormpy.pomdp.developer.MonitorVerifier",
    _pomdp,
    parameters=("ValueType",),
    deduce=_deduce_from_object(_parameters_of_model, keyword="product"),
)

GenerateMonitorVerifierOptions = _TemplateClass(
    "stormpy.pomdp.developer.GenerateMonitorVerifierOptions",
    _pomdp,
    parameters=("ValueType",),
    deduce=_deduce_default(float),
)

GenerateMonitorVerifier = _TemplateClass(
    "stormpy.pomdp.developer.GenerateMonitorVerifier",
    _pomdp,
    parameters=("ValueType",),
    deduce=_deduce_from_object(_parameters_of_model, keyword="mc"),
)

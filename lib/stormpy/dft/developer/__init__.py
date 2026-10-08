"""Raw pybind11 bindings for storm-dft.

This module is only meant for developers.
Use :mod:`stormpy.dft` for the public API.

The naming of functions and classes of the bindings mirrors the corresponding ``storm::dft`` C++ functions and classes.
"""

from stormpy.info import _config
from stormpy import Property
from stormpy.exceptions import StormError
import warnings

if not _config.STORM_WITH_DFT:
    raise ImportError("No support for DFTs was built in Storm.")

from . import _dft

# Mirror _dft's entire namespace (including private underscored classes) directly onto this package.
for _name, _value in vars(_dft).items():
    if not _name.startswith("__"):
        globals()[_name] = _value
del _name, _value

from stormpy._template import _TemplateClass, _deduce_from_first_argument, _deduce_from_object

# Define templated classes
DFT = _TemplateClass(
    "stormpy.dft.developer.DFT",
    _dft,
    parameters=("ValueType",),
    deduce=_deduce_from_first_argument(keyword="dft"),
)

DFTElement = _TemplateClass(
    "stormpy.dft.developer.DFTElement",
    _dft,
    parameters=("ValueType",),
)

DFTBE = _TemplateClass(
    "stormpy.dft.developer.DFTBE",
    _dft,
    parameters=("ValueType",),
)

DFTDependency = _TemplateClass(
    "stormpy.dft.developer.DFTDependency",
    _dft,
    parameters=("ValueType",),
)

DFTState = _TemplateClass(
    "stormpy.dft.developer.DFTState",
    _dft,
    parameters=("ValueType",),
)

DFTTraceSimulator = _TemplateClass(
    "stormpy.dft.developer.DFTTraceSimulator",
    _dft,
    parameters=("ValueType",),
    deduce=_deduce_from_first_argument(DFT, keyword="dft"),
)

ExplicitDFTModelBuilder = _TemplateClass(
    "stormpy.dft.developer.ExplicitDFTModelBuilder",
    _dft,
    parameters=("ValueType",),
    deduce=_deduce_from_object(DFT.parameters_of, position=1, keyword="dft"),
)

_deduce_dft_parameters = _deduce_from_first_argument(DFT, keyword="dft")


def _deduce_dft_instantiator(family, args, kwargs):
    return (*_deduce_dft_parameters(family, args, kwargs), float)


DftInstantiator = _TemplateClass(
    "stormpy.dft.developer.DftInstantiator",
    _dft,
    parameters=("SourceValueType", "TargetValueType"),
    deduce=_deduce_dft_instantiator,
)


# Add additional functions
def compute_relevant_events(properties, *args, **kwargs):
    return _dft.compute_relevant_events([(prop.raw_formula if isinstance(prop, Property) else prop) for prop in properties], *args, **kwargs)

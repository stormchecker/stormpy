from stormpy.info import _config

if not _config.STORM_WITH_DFT:
    raise ImportError("No support for DFTs was built in Storm.")

from . import _dft
from ._dft import *
from .modules import modules_json
from stormpy._template import TemplateClass, deduce_from_first_argument as _deduce_from_first_argument

_dft._set_up()


DFT = TemplateClass(
    "stormpy.dft.DFT",
    _dft,
    parameters=("ValueType",),
    deduce=_deduce_from_first_argument(keyword="dft"),
)

DFTElement = TemplateClass(
    "stormpy.dft.DFTElement",
    _dft,
    parameters=("ValueType",),
)

DFTBE = TemplateClass(
    "stormpy.dft.DFTBE",
    _dft,
    parameters=("ValueType",),
)

DFTDependency = TemplateClass(
    "stormpy.dft.DFTDependency",
    _dft,
    parameters=("ValueType",),
)

DFTState = TemplateClass(
    "stormpy.dft.DFTState",
    _dft,
    parameters=("ValueType",),
)

DFTSimulator = TemplateClass(
    "stormpy.dft.DFTSimulator",
    _dft,
    parameters=("ValueType",),
    deduce=_deduce_from_first_argument(DFT, keyword="dft"),
)

ExplicitDFTModelBuilder = TemplateClass(
    "stormpy.dft.ExplicitDFTModelBuilder",
    _dft,
    parameters=("ValueType",),
    deduce=_deduce_from_first_argument(DFT, keyword="dft"),
)

_deduce_dft_parameters = _deduce_from_first_argument(DFT, keyword="dft")


def _deduce_dft_instantiator(family, args, kwargs):
    return (*_deduce_dft_parameters(family, args, kwargs), float)


DFTInstantiator = TemplateClass(
    "stormpy.dft.DFTInstantiator",
    _dft,
    parameters=("SourceValueType", "TargetValueType"),
    deduce=_deduce_dft_instantiator,
)


def prepare_for_analysis(ft):
    compute_dependency_conflicts(ft, use_smt=False)
    return transform_dft(ft, unique_constant_be=True, binary_fdeps=True, exponential_distributions=True)

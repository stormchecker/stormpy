from stormpy.info import _config

if not _config.STORM_WITH_DFT:
    raise ImportError("No support for DFTs was built in Storm.")

from . import _dft
from ._dft import *
from .modules import modules_json
from stormpy._template import TemplateClass

_dft._set_up()

DFT = TemplateClass("DFT", _dft)

DFTElement = TemplateClass("DFTElement", _dft)

DFTBE = TemplateClass("DFTBE", _dft)

DFTDependency = TemplateClass("DFTDependency", _dft)

DFTState = TemplateClass("DFTState", _dft)

DFTSimulator = TemplateClass("DFTSimulator", _dft, deduce_from=DFT)

ExplicitDFTModelBuilder = TemplateClass("ExplicitDFTModelBuilder", _dft, deduce_from=DFT)

DFTInstantiator = TemplateClass("DFTInstantiator", _dft)


def prepare_for_analysis(ft):
    compute_dependency_conflicts(ft, use_smt=False)
    return transform_dft(ft, unique_constant_be=True, binary_fdeps=True, exponential_distributions=True)

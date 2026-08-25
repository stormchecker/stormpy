from stormpy.info import _config

if not _config.STORM_WITH_PARS:
    raise ImportError("No support for parametric analysis was built in Storm.")

from . import _pars
from ._pars import *

from stormpy import ModelType
from stormpy._template import TemplateClass

_pars._set_up()


ModelInstantiator = TemplateClass("ModelInstantiator", _pars)

ModelInstantiationChecker = TemplateClass("ModelInstantiationChecker", _pars)


def simplify_model(model, formula):
    """
    Simplify parametric model preserving the given formula by eliminating states with constant outgoing probabilities.
    :param model: Model.
    :param formula: Formula.
    :return: Tuple of simplified model and simplified formula.
    """
    if model.model_type == ModelType.DTMC:
        simplifier = _pars._SparseParametricDtmcSimplifier(model)
    elif model.model_type == ModelType.MDP:
        simplifier = _pars._SparseParametricMdpSimplifier(model)
    else:
        raise stormpy.exceptions.StormError("Model type {} cannot be simplified.".format(model.model_type))
    if not simplifier.simplify(formula):
        raise stormpy.exceptions.StormError("Model could not be simplified")
    return simplifier.simplified_model, simplifier.simplified_formula

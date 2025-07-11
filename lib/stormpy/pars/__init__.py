from stormpy import _config

if not _config.storm_with_pars:
    raise ImportError("No support for parametric analysis was built in Storm.")

from . import pars
from .pars import *

from stormpy import ModelType, StormError

pars._set_up()


class ModelInstantiator:
    """
    Class for instantiating models.
    """

    def __init__(self, model):
        """
        Constructor.
        :param model: Model.
        """
        if model.model_type == ModelType.MDP:
            self._instantiator = PMdpInstantiator(model)
        elif model.model_type == ModelType.DTMC:
            self._instantiator = PDtmcInstantiator(model)
        elif model.model_type == ModelType.CTMC:
            self._instantiator = PCtmcInstantiator(model)
        elif model.model_type == ModelType.MA:
            self._instantiator = PMaInstantiator(model)
        else:
            raise StormError("Model type {} not supported".format(model.model_type))

    def instantiate(self, valuation):
        """
        Instantiate model with given valuation.
        :param valuation: Valuation from parameter to value.
        :return: Instantiated model.
        """
        return self._instantiator.instantiate(valuation)


def simplify_model(model, formula):
    """
    Simplify parametric model preserving the given formula by eliminating states with constant outgoing probabilities.
    :param model: Model.
    :param formula: Formula.
    :return: Tuple of simplified model and simplified formula.
    """
    if model.model_type == ModelType.DTMC:
        simplifier = pars._SparseParametricDtmcSimplifier(model)
    elif model.model_type == ModelType.MDP:
        simplifier = pars._SparseParametricMdpSimplifier(model)
    else:
        raise StormError("Model type {} cannot be simplified.".format(model.model_type))
    if not simplifier.simplify(formula):
        raise StormError("Model could not be simplified")
    return simplifier.simplified_model, simplifier.simplified_formula

from collections.abc import Mapping as _Mapping

from stormpy.info import _config

if not _config.STORM_WITH_PARS:
    raise ImportError("No support for parametric analysis was built in Storm.")

from . import _pars
from ._pars import *

from stormpy import ModelType
from stormpy._template import TemplateClass, TemplateParameter as _TemplateParameter

_pars._set_up()


def _deduce_model_and_double(_family: TemplateClass, args: tuple[object, ...], kwargs: _Mapping[str, object]) -> object:
    if args:
        model = args[0]
    else:
        try:
            model = kwargs["model"]
        except KeyError:
            raise TypeError("Cannot deduce template parameters without the model argument") from None
    return model.model_type, float


ModelInstantiator = TemplateClass(
    "stormpy.pars.ModelInstantiator",
    _pars,
    parameters=(_TemplateParameter("ModelType", kind="value"), "ValueType"),
    deduce=_deduce_model_and_double,
)

ModelInstantiationChecker = TemplateClass(
    "stormpy.pars.ModelInstantiationChecker",
    _pars,
    parameters=(_TemplateParameter("ModelType", kind="value"), "ResultType"),
    deduce=_deduce_model_and_double,
)


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

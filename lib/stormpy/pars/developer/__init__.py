"""Raw pybind11 bindings for storm-pars.

This module is only meant for developers.
Use :mod:`stormpy.pars` for the public API.

The naming of functions and classes of the bindings mirrors the corresponding ``storm::pars`` C++ functions and classes.
"""

from collections.abc import Mapping as _Mapping

from stormpy.info import _config

if not _config.STORM_WITH_PARS:
    raise ImportError("No support for parametric analysis was built in Storm.")

from . import _pars

# Mirror _pars's entire namespace (including private underscored classes) directly onto this package.
for _name, _value in vars(_pars).items():
    if not _name.startswith("__"):
        globals()[_name] = _value
del _name, _value

from stormpy._template import _TemplateClass, _TemplateParameter


def _model_argument(args: tuple[object, ...], kwargs: _Mapping[str, object], position: int) -> object:
    if len(args) > position:
        return args[position]
    try:
        return kwargs["model"]
    except KeyError:
        raise TypeError("Cannot deduce template parameters without the model argument") from None


def _deduce_model(_family: _TemplateClass, args: tuple[object, ...], kwargs: _Mapping[str, object]) -> object:
    return (_model_argument(args, kwargs, 0).model_type,)


def _deduce_model_and_double(_family: _TemplateClass, args: tuple[object, ...], kwargs: _Mapping[str, object]) -> object:
    return _model_argument(args, kwargs, 0).model_type, float


def _deduce_checker_model_and_double(_family: _TemplateClass, args: tuple[object, ...], kwargs: _Mapping[str, object]) -> object:
    return _model_argument(args, kwargs, 1).model_type, float


# Define templated classes
ModelInstantiator = _TemplateClass(
    "stormpy.pars.developer.ModelInstantiator",
    _pars,
    parameters=(_TemplateParameter("ModelType", kind="value"), "ValueType"),
    deduce=_deduce_model_and_double,
)

SparseInstantiationModelChecker = _TemplateClass(
    "stormpy.pars.developer.SparseInstantiationModelChecker",
    _pars,
    parameters=(_TemplateParameter("ModelType", kind="value"), "ResultType"),
    deduce=_deduce_checker_model_and_double,
)

SparseParametricModelSimplifier = _TemplateClass(
    "stormpy.pars.developer.SparseParametricModelSimplifier",
    _pars,
    parameters=(_TemplateParameter("ModelType", kind="value"),),
    deduce=_deduce_model,
)

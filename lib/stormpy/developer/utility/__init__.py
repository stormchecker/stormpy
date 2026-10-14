"""Raw bindings for Storm utilities, such as shortest paths and the Kwek-Mehlhorn algorithm.

This module is intended for developers. Use :mod:`stormpy.utility` for the documented public API.
"""

from . import _utility

# Include private native classes and overloads in the developer namespace.
for _name, _value in vars(_utility).items():
    if not _name.startswith("__"):
        globals()[_name] = _value
del _name, _value
from stormpy._template import _TemplateClass, _deduce_default, _deduce_from_object
from stormpy.developer import storage as _storage_bindings


# src/utility/shortestPaths.cpp
def _parameters_of_model_or_matrix(model_or_matrix: object) -> object:
    if hasattr(model_or_matrix, "transition_matrix"):
        return _storage_bindings.parameters_of_model(model_or_matrix)
    return _storage_bindings.SparseMatrix.parameters_of(model_or_matrix)


Path = _TemplateClass("stormpy.developer.utility.Path", _utility, parameters=("ValueType",), deduce=_deduce_default(float))
ShortestPathsGenerator = _TemplateClass(
    "stormpy.developer.utility.ShortestPathsGenerator",
    _utility,
    parameters=("ValueType",),
    deduce=_deduce_from_object(_parameters_of_model_or_matrix, keyword=("model", "transition_matrix", "maybe_transition_matrix")),
)

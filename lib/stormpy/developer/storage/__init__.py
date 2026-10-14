"""Raw bindings for Storm storage, model descriptions, models and expressions.

This module is intended for developers. Use :mod:`stormpy.models`,
:mod:`stormpy.datastructures`, :mod:`stormpy.expressions` and :mod:`stormpy.io`
for the documented public API.
"""

from . import _storage

# Include private native classes and overloads in the developer namespace.
for _name, _value in vars(_storage).items():
    if not _name.startswith("__"):
        globals()[_name] = _value
del _name, _value
from stormpy._template import (
    _TemplateClass,
    _TemplateFunction,
    _TemplateParameter,
    _deduce_default,
    _deduce_from_object,
)

# src/storage/json.cpp
JsonContainer = _TemplateClass("stormpy.developer.storage.JsonContainer", _storage, parameters=("ValueType",), deduce=_deduce_default(float))

# src/storage/matrix.cpp
SparseMatrixEntry = _TemplateClass("stormpy.developer.storage.SparseMatrixEntry", _storage, parameters=("ValueType",), deduce=_deduce_default(float))
SparseMatrixBuilder = _TemplateClass("stormpy.developer.storage.SparseMatrixBuilder", _storage, parameters=("ValueType",), deduce=_deduce_default(float))
SparseMatrix = _TemplateClass("stormpy.developer.storage.SparseMatrix", _storage, parameters=("ValueType",), deduce=_deduce_default(float))
SparseMatrixRows = _TemplateClass("stormpy.developer.storage.SparseMatrixRows", _storage, parameters=("ValueType",), deduce=_deduce_default(float))

# src/storage/state.cpp
SparseModelStates = _TemplateClass("stormpy.developer.storage.SparseModelStates", _storage, parameters=("ValueType",), deduce=_deduce_default(float))
SparseModelState = _TemplateClass("stormpy.developer.storage.SparseModelState", _storage, parameters=("ValueType",), deduce=_deduce_default(float))
SparseModelActions = _TemplateClass("stormpy.developer.storage.SparseModelActions", _storage, parameters=("ValueType",), deduce=_deduce_default(float))
SparseModelAction = _TemplateClass("stormpy.developer.storage.SparseModelAction", _storage, parameters=("ValueType",), deduce=_deduce_default(float))

# src/storage/scheduler.cpp
Scheduler = _TemplateClass("stormpy.developer.storage.Scheduler", _storage, parameters=("ValueType",), deduce=_deduce_default(float))
SchedulerChoice = _TemplateClass("stormpy.developer.storage.SchedulerChoice", _storage, parameters=("ValueType",), deduce=_deduce_default(float))

# src/storage/distribution.cpp
Distribution = _TemplateClass("stormpy.developer.storage.Distribution", _storage, parameters=("ValueType",), deduce=_deduce_default(float))

# src/storage/geometry.cpp
Polytope = _TemplateClass("stormpy.developer.storage.Polytope", _storage, parameters=("ValueType",), deduce=_deduce_default(float))

# src/storage/dd.cpp
DdMetaVariable = _TemplateClass("stormpy.developer.storage.DdMetaVariable", _storage, parameters=(_TemplateParameter("DdType", kind="value"),))
DdManager = _TemplateClass("stormpy.developer.storage.DdManager", _storage, parameters=(_TemplateParameter("DdType", kind="value"),))
Dd = _TemplateClass("stormpy.developer.storage.Dd", _storage, parameters=(_TemplateParameter("DdType", kind="value"),))
Bdd = _TemplateClass("stormpy.developer.storage.Bdd", _storage, parameters=(_TemplateParameter("DdType", kind="value"),))
Add = _TemplateClass(
    "stormpy.developer.storage.Add",
    _storage,
    parameters=(_TemplateParameter("DdType", kind="value"), "ValueType"),
)
AddIterator = _TemplateClass(
    "stormpy.developer.storage.AddIterator",
    _storage,
    parameters=(_TemplateParameter("DdType", kind="value"), "ValueType"),
)

# src/storage/model_components.cpp
SparseModelComponents = _TemplateClass(
    "stormpy.developer.storage.SparseModelComponents",
    _storage,
    parameters=("ValueType",),
    deduce=_deduce_from_object(SparseMatrix.parameters_of, keyword="transition_matrix", default=(float,)),
)


# src/storage/model.cpp
def parameters_of_model(model):
    """Return the value-type parameter of a sparse model or model components."""

    return SparseMatrix.parameters_of(model.transition_matrix)


SparseModel = _TemplateClass("stormpy.developer.storage.SparseModel", _storage, parameters=("ValueType",), deduce=_deduce_default(float))
SparseDtmc = _TemplateClass(
    "stormpy.developer.storage.SparseDtmc",
    _storage,
    parameters=("ValueType",),
    deduce=_deduce_from_object(parameters_of_model, keyword=("components", "other_model")),
)
SparseMdp = _TemplateClass(
    "stormpy.developer.storage.SparseMdp",
    _storage,
    parameters=("ValueType",),
    deduce=_deduce_from_object(parameters_of_model, keyword=("components", "other_model")),
)
SparsePomdp = _TemplateClass(
    "stormpy.developer.storage.SparsePomdp",
    _storage,
    parameters=("ValueType",),
    deduce=_deduce_from_object(parameters_of_model, keyword=("components", "other_model")),
)
SparseCtmc = _TemplateClass(
    "stormpy.developer.storage.SparseCtmc",
    _storage,
    parameters=("ValueType",),
    deduce=_deduce_from_object(parameters_of_model, keyword=("components", "other_model")),
)
SparseMA = _TemplateClass(
    "stormpy.developer.storage.SparseMA",
    _storage,
    parameters=("ValueType",),
    deduce=_deduce_from_object(parameters_of_model, keyword=("components", "other_model")),
)
SparseSmg = _TemplateClass(
    "stormpy.developer.storage.SparseSmg",
    _storage,
    parameters=("ValueType",),
    deduce=_deduce_from_object(parameters_of_model, keyword=("components", "other_model")),
)
SparseRewardModel = _TemplateClass("stormpy.developer.storage.SparseRewardModel", _storage, parameters=("ValueType",), deduce=_deduce_default(float))
SymbolicModel = _TemplateClass("stormpy.developer.storage.SymbolicModel", _storage, parameters=(_TemplateParameter("DdType", kind="value"), "ValueType"))
SymbolicDtmc = _TemplateClass("stormpy.developer.storage.SymbolicDtmc", _storage, parameters=(_TemplateParameter("DdType", kind="value"), "ValueType"))
SymbolicMdp = _TemplateClass("stormpy.developer.storage.SymbolicMdp", _storage, parameters=(_TemplateParameter("DdType", kind="value"), "ValueType"))
SymbolicCtmc = _TemplateClass("stormpy.developer.storage.SymbolicCtmc", _storage, parameters=(_TemplateParameter("DdType", kind="value"), "ValueType"))
SymbolicMA = _TemplateClass("stormpy.developer.storage.SymbolicMA", _storage, parameters=(_TemplateParameter("DdType", kind="value"), "ValueType"))
SymbolicRewardModel = _TemplateClass(
    "stormpy.developer.storage.SymbolicRewardModel", _storage, parameters=(_TemplateParameter("DdType", kind="value"), "ValueType")
)

# src/storage/decomposition.cpp
MaximalEndComponentDecomposition = _TemplateClass(
    "stormpy.developer.storage.MaximalEndComponentDecomposition",
    _storage,
    parameters=("ValueType",),
    deduce=_deduce_from_object(parameters_of_model, keyword="model"),
)

# src/storage/memorystructure.cpp
MemoryStructureBuilder = _TemplateClass(
    "stormpy.developer.storage.MemoryStructureBuilder",
    _storage,
    parameters=("ValueType",),
    deduce=_deduce_from_object(parameters_of_model, keyword="model", position=1),
)
MemoryStructureProduct = _TemplateClass("stormpy.developer.storage.MemoryStructureProduct", _storage, parameters=("ValueType",), deduce=_deduce_default(float))

# Storm Scheduler::toValueType<NewValueType>, with overloads for source value types.
to_value_type = _TemplateFunction("stormpy.developer.storage.to_value_type", _storage, parameters=("NewValueType",))

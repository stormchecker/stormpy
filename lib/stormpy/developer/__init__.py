"""Raw pybind11 bindings for the core library of Storm.

This module is only meant for developers.
Use :mod:`stormpy` for the public API.

The naming of functions and classes of the bindings mirrors the corresponding ``storm::`` C++ functions and classes.
"""

from . import storage
from . import utility
from . import _core

# Mirror _core's entire namespace (including private underscored classes) directly onto this package.
for _name, _value in vars(_core).items():
    if not _name.startswith("__"):
        globals()[_name] = _value
del _name, _value

from stormpy._template import _TemplateClass, _TemplateFunction, _TemplateParameter, _deduce_default, _deduce_from_object

_deduce_from_model = _deduce_from_object(storage.parameters_of_model, keyword=("model", "original_model"))

# Define templated classes
ExplicitModelBuilderOptions = _TemplateClass("stormpy.developer.ExplicitModelBuilderOptions", _core, parameters=("ValueType",), deduce=_deduce_default(float))
ExplicitModelBuilder = _TemplateClass("stormpy.developer.ExplicitModelBuilder", _core, parameters=("ValueType",))

SMTMinimalLabelSetGeneratorStats = _TemplateClass(
    "stormpy.developer.SMTMinimalLabelSetGeneratorStats", _core, parameters=("ValueType",), deduce=_deduce_default(float)
)
SMTMinimalLabelSetGeneratorOptions = _TemplateClass(
    "stormpy.developer.SMTMinimalLabelSetGeneratorOptions", _core, parameters=("ValueType",), deduce=_deduce_default(float)
)
SMTMinimalLabelSetGenerator = _TemplateClass("stormpy.developer.SMTMinimalLabelSetGenerator", _core, parameters=("ValueType",))
SMTMinimalLabelSetGeneratorCexInput = _TemplateClass("stormpy.developer.SMTMinimalLabelSetGeneratorCexInput", _core, parameters=("ValueType",))

Choice = _TemplateClass("stormpy.developer.Choice", _core, parameters=("ValueType",))
ActionMask = _TemplateClass("stormpy.developer.ActionMask", _core, parameters=("ValueType",))
StateValuationFunctionMask = _TemplateClass("stormpy.developer.StateValuationFunctionMask", _core, parameters=("ValueType",), deduce=_deduce_default(float))

CheckTask = _TemplateClass("stormpy.developer.CheckTask", _core, parameters=("ValueType",), deduce=_deduce_default(float))
ExplicitModelCheckerHint = _TemplateClass("stormpy.developer.ExplicitModelCheckerHint", _core, parameters=("ValueType",), deduce=_deduce_default(float))

PcaaWeightVectorChecker = _TemplateClass("stormpy.developer.PcaaWeightVectorChecker", _core, parameters=("ValueType",))

ExplicitQualitativeCheckResult = _TemplateClass(
    "stormpy.developer.ExplicitQualitativeCheckResult", _core, parameters=("ValueType",), deduce=_deduce_default(float)
)
SymbolicQualitativeCheckResult = _TemplateClass(
    "stormpy.developer.SymbolicQualitativeCheckResult",
    _core,
    parameters=(_TemplateParameter("DdType", kind="value"),),
    deduce=_deduce_default(storage.DdType.Sylvan),
)
QuantitativeCheckResult = _TemplateClass("stormpy.developer.QuantitativeCheckResult", _core, parameters=("ValueType",))
ExplicitQuantitativeCheckResult = _TemplateClass(
    "stormpy.developer.ExplicitQuantitativeCheckResult", _core, parameters=("ValueType",), deduce=_deduce_default(float)
)
SymbolicQuantitativeCheckResult = _TemplateClass(
    "stormpy.developer.SymbolicQuantitativeCheckResult", _core, parameters=(_TemplateParameter("DdType", kind="value"), "ValueType")
)
HybridQuantitativeCheckResult = _TemplateClass(
    "stormpy.developer.HybridQuantitativeCheckResult", _core, parameters=(_TemplateParameter("DdType", kind="value"), "ValueType")
)
ParetoCurveCheckResult = _TemplateClass("stormpy.developer.ParetoCurveCheckResult", _core, parameters=("ValueType",))
ExplicitParetoCurveCheckResult = _TemplateClass("stormpy.developer.ExplicitParetoCurveCheckResult", _core, parameters=("ValueType",))

DiscreteTimeSparseModelSimulator = _TemplateClass(
    "stormpy.developer.DiscreteTimeSparseModelSimulator", _core, parameters=("ValueType",), deduce=_deduce_from_model
)
DiscreteTimePrismProgramSimulator = _TemplateClass(
    "stormpy.developer.DiscreteTimePrismProgramSimulator", _core, parameters=("ValueType",), deduce=_deduce_default(float)
)

SubsystemBuilderReturnType = _TemplateClass("stormpy.developer.SubsystemBuilderReturnType", _core, parameters=("ValueType",))
EndComponentEliminatorReturnType = _TemplateClass("stormpy.developer.EndComponentEliminatorReturnType", _core, parameters=("ValueType",))
EndComponentEliminator = _TemplateClass("stormpy.developer.EndComponentEliminator", _core, parameters=("ValueType",))
AddUncertainty = _TemplateClass("stormpy.developer.AddUncertainty", _core, parameters=("ValueType",), deduce=_deduce_from_model)

# Define templated functions (value type cannot be deduced from the arguments)
build_sparse_model = _TemplateFunction("stormpy.developer.build_sparse_model", _core, parameters=("ValueType",), deduce=_deduce_default(float))
build_symbolic_model = _TemplateFunction("stormpy.developer.build_symbolic_model", _core, parameters=("ValueType",), deduce=_deduce_default(float))
make_explicit_model_builder = _TemplateFunction(
    "stormpy.developer.make_explicit_model_builder", _core, parameters=("ValueType",), deduce=_deduce_default(float)
)
build_explicit_drn_model = _TemplateFunction("stormpy.developer.build_explicit_drn_model", _core, parameters=("ValueType",), deduce=_deduce_default(float))

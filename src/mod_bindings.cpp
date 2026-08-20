#include "src/module_bindings.h"

namespace {

pybind11::module_ createModule(pybind11::module_ const& parent, char const* name, char const* doc) {
    pybind11::object moduleType = pybind11::module_::import("types").attr("ModuleType");
    pybind11::module_ result = moduleType(name, doc).cast<pybind11::module_>();
    result.attr("__package__") = std::string(name).substr(0, std::string(name).rfind('.'));
    result.attr("__loader__") = pybind11::none();
    result.attr("__spec__") = pybind11::module_::import("importlib.machinery").attr("ModuleSpec")(name, pybind11::none());
    if (pybind11::hasattr(parent, "__file__")) {
        result.attr("__file__") = parent.attr("__file__");
        result.attr("__spec__").attr("origin") = parent.attr("__file__");
    }
    pybind11::module_::import("sys").attr("modules")[pybind11::str(name)] = result;
    return result;
}

void bindAll(pybind11::module_ const& core, pybind11::module_ const& storage, pybind11::module_ const& logic, pybind11::module_ const& utility,
             py::Phase phase) {
    py::module utilityBindings(utility, phase);
    py::module storageBindings(storage, phase);
    py::module logicBindings(logic, phase);
    py::module coreBindings(core, phase);

    stormpy::bindings::bindUtility(utilityBindings);
    stormpy::bindings::bindStorage(storageBindings);
    stormpy::bindings::bindLogic(logicBindings);
    stormpy::bindings::bindCore(coreBindings);
}

}  // namespace

PYBIND11_MODULE(_bindings, m) {
    m.doc() = "Native Storm bindings";

#ifdef STORMPY_DISABLE_SIGNATURE_DOC
    pybind11::options options;
    options.disable_function_signatures();
#endif

    pybind11::module_ core = createModule(m, "stormpy._core", "Core Storm APIs");
    pybind11::module_ storage = createModule(m, "stormpy.storage._storage", "Data structures in Storm");
    pybind11::module_ logic = createModule(m, "stormpy.logic._logic", "Logic module for Storm");
    pybind11::module_ utility = createModule(m, "stormpy.utility._utility", "Utilities for Storm");

    m.attr("_core") = core;
    m.attr("_storage") = storage;
    m.attr("_logic") = logic;
    m.attr("_utility") = utility;

    bindAll(core, storage, logic, utility, py::Phase::Declare);
    bindAll(core, storage, logic, utility, py::Phase::Define);
}

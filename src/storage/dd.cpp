#include "dd.h"

#include <storm/storage/dd/Add.h>
#include <storm/storage/dd/Bdd.h>
#include <storm/storage/dd/Dd.h>
#include <storm/storage/dd/DdManager.h>
#include <storm/storage/dd/DdMetaVariable.h>

#include "src/binding_type_index.h"
#include "src/helpers.h"

template<storm::dd::DdType DdType>
py::classh<storm::dd::Dd<DdType>> define_dd(py::module& m) {
    auto const index = stormpy::bindings::typeIndex<DdType>();
    auto ddMetaVariable = stormpy::bindings::bindTemplateClass<storm::dd::DdMetaVariable<DdType>>(m, "DdMetaVariable", index, "DD meta variable");
    ddMetaVariable.def("compute_indices", &storm::dd::DdMetaVariable<DdType>::getIndices, py::arg("sorted") = true);
    ddMetaVariable.def_property_readonly("name", &storm::dd::DdMetaVariable<DdType>::getName);
    ddMetaVariable.def_property_readonly("lowest_value", &storm::dd::DdMetaVariable<DdType>::getLow);
    ddMetaVariable.def_property_readonly("type", &storm::dd::DdMetaVariable<DdType>::getType);
    ddMetaVariable.def("__str__", &storm::dd::DdMetaVariable<DdType>::getName);

    auto ddManager = stormpy::bindings::bindTemplateClass<storm::dd::DdManager<DdType>>(m, "DdManager", index, "DD manager");
    ddManager.def(
        "get_meta_variable", [](storm::dd::DdManager<DdType> const& manager, storm::expressions::Variable const& var) { return manager.getMetaVariable(var); },
        py::arg("expression_variable"));

    auto dd = stormpy::bindings::bindTemplateClass<storm::dd::Dd<DdType>>(m, "Dd", index, "Dd");
    dd.def_property_readonly("node_count", &storm::dd::Dd<DdType>::getNodeCount, "get node count");
    dd.def_property_readonly("dd_manager", &storm::dd::Dd<DdType>::getDdManager, "get the manager");
    dd.def_property_readonly("meta_variables", [](storm::dd::Dd<DdType> const& dd) { return dd.getContainedMetaVariables(); }, "the contained meta variables");

    stormpy::bindings::bindTemplateClass<storm::dd::Bdd<DdType>>(m, "Bdd", index, "Bdd", dd)
        .def("to_expression", &storm::dd::Bdd<DdType>::toExpression, py::arg("expression_manager"));

    return dd;
}

template<storm::dd::DdType DdType, typename ValueType>
void define_dd_typed(py::module& m, py::classh<storm::dd::Dd<DdType>> const& dd) {
    auto const index = stormpy::bindings::typeIndex<DdType, ValueType>();
    auto add = stormpy::bindings::bindTemplateClass<storm::dd::Add<DdType, ValueType>>(m, "Add", index, "Add", dd);
    add.def(
        "__iter__", [](const storm::dd::Add<DdType, ValueType>& s) { return py::make_iterator(s.begin(), s.end()); },
        py::keep_alive<0, 1>() /* Essential: keep object alive while iterator exists */);

    auto addIterator = stormpy::bindings::bindTemplateClass<storm::dd::AddIterator<DdType, ValueType>>(m, "AddIterator", index, "AddIterator");
    addIterator.def("get", [](const storm::dd::AddIterator<DdType, ValueType>& it) { return *it; });
}

void define_dd_nt(py::module& m) {
    m.attr("DdType") = py::module::import("stormpy._core").attr("DdType");
    py::native_enum<storm::dd::MetaVariableType>(m, "DdMetaVariableType", "enum.Enum")
        .value("INT", storm::dd::MetaVariableType::Int)
        .value("BOOL", storm::dd::MetaVariableType::Bool)
        .value("BITVECTOR", storm::dd::MetaVariableType::BitVector)
        .finalize();
}

template py::classh<storm::dd::Dd<storm::dd::DdType::Sylvan>> define_dd<storm::dd::DdType::Sylvan>(py::module& m);
template void define_dd_typed<storm::dd::DdType::Sylvan, double>(py::module&, py::classh<storm::dd::Dd<storm::dd::DdType::Sylvan>> const&);

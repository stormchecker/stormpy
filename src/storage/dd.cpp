#include "dd.h"
#include "src/helpers.h"
#include "storm/storage/dd/Add.h"
#include "storm/storage/dd/Bdd.h"
#include "storm/storage/dd/Dd.h"
#include "storm/storage/dd/DdManager.h"
#include "storm/storage/dd/DdMetaVariable.h"

template<storm::dd::DdType DdType>
void define_dd(py::module& m, std::string const& libstring) {
    py::class_<storm::dd::DdMetaVariable<DdType>> ddMetaVariable(m, (std::string("DdMetaVariable_") + libstring).c_str());
    ddMetaVariable.def("compute_indices", &storm::dd::DdMetaVariable<DdType>::getIndices, py::arg("sorted") = true);
    ddMetaVariable.def_property_readonly("name", &storm::dd::DdMetaVariable<DdType>::getName);
    ddMetaVariable.def_property_readonly("lowest_value", &storm::dd::DdMetaVariable<DdType>::getLow);
    ddMetaVariable.def_property_readonly("type", &storm::dd::DdMetaVariable<DdType>::getType);
    ddMetaVariable.def("__str__", &storm::dd::DdMetaVariable<DdType>::getName);

    py::class_<storm::dd::DdManager<DdType>, std::shared_ptr<storm::dd::DdManager<DdType>>> ddManager(m, (std::string("DdManager_") + libstring).c_str());
    ddManager.def(
        "get_meta_variable", [](storm::dd::DdManager<DdType> const& manager, storm::expressions::Variable const& var) { return manager.getMetaVariable(var); },
        py::arg("expression_variable"));

    py::class_<storm::dd::Dd<DdType>> dd(m, (std::string("Dd_") + libstring).c_str(), "Dd");
    dd.def_property_readonly("node_count", &storm::dd::Dd<DdType>::getNodeCount, "get node count");
    dd.def_property_readonly("dd_manager", &storm::dd::Dd<DdType>::getDdManager, "get the manager");
    dd.def_property_readonly("meta_variables", [](storm::dd::Dd<DdType> const& dd) { return dd.getContainedMetaVariables(); }, "the contained meta variables");

    py::class_<storm::dd::Bdd<DdType>> bdd(m, (std::string("Bdd_") + libstring).c_str(), "Bdd", dd);
    bdd.def("to_expression", &storm::dd::Bdd<DdType>::toExpression, py::arg("expression_manager"));

    py::class_<storm::dd::Add<DdType, double>> add(m, (std::string("Add_") + libstring + "_Double").c_str(), "Add", dd);
    add.def(
        "__iter__", [](const storm::dd::Add<DdType, double>& s) { return py::make_iterator(s.begin(), s.end()); },
        py::keep_alive<0, 1>() /* Essential: keep object alive while iterator exists */);

    py::class_<storm::dd::AddIterator<DdType, double>> addIterator(m, (std::string("AddIterator_") + libstring + "_Double").c_str(), "AddIterator");
    addIterator.def("get", [](const storm::dd::AddIterator<DdType, double>& it) { return *it; });
}

void define_dd_nt(py::module& m) {
    py::enum_<storm::dd::MetaVariableType>(m, "DdMetaVariableType")
        .value("Int", storm::dd::MetaVariableType::Int)
        .value("Bool", storm::dd::MetaVariableType::Bool)
        .value("Bitvector", storm::dd::MetaVariableType::BitVector);
}

template void define_dd<storm::dd::DdType::Sylvan>(py::module& m, std::string const& libstring);
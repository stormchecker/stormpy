#include "dft.h"

#include <storm-dft/settings/modules/DftIOSettings.h>
#include <storm-dft/settings/modules/FaultTreeSettings.h>
#include <storm-dft/storage/DFT.h>
#include <storm-dft/storage/DftSymmetries.h>
#include <storm-dft/utility/DftModularizer.h>
#include <storm-dft/utility/SymmetryFinder.h>
#include <storm/adapters/RationalFunctionAdapter.h>
#include <storm/settings/SettingsManager.h>

#include "src/binding_type_index.h"
#include "src/helpers.h"

template<typename ValueType>
using DFT = storm::dft::storage::DFT<ValueType>;
template<typename ValueType>
using DFTElement = storm::dft::storage::elements::DFTElement<ValueType>;

// requires pycarl.Variable
std::set<storm::RationalFunctionVariable> getParameters(DFT<storm::RationalFunction> const& dft) {
    return storm::dft::storage::getParameters(dft);
}

void define_dft(py::module& m) {
    m.def(
        "_set_up",
        []() {
            storm::settings::addModule<storm::dft::settings::modules::FaultTreeSettings>();
            storm::settings::addModule<storm::dft::settings::modules::DftIOSettings>();
        },
        "Initialize Storm-dft");

    m.def("get_parameters", &getParameters, "Collect parameters in parametric DFT", py::arg("dft"));
}

template<typename ValueType>
void define_dft_typed(py::module& m) {
    // DFT class
    auto dft =
        stormpy::bindings::bindTemplateClass<DFT<ValueType>, py::smart_holder>(m, "DFT", stormpy::bindings::typeIndex<ValueType>(), "Dynamic Fault Tree");
    dft.def(py::init<DFT<ValueType> const&>(), "Copy a Dynamic Fault Tree", py::arg("dft"))
        .def("nr_elements", &DFT<ValueType>::nrElements, "Total number of elements")
        .def("nr_be", &DFT<ValueType>::nrBasicElements, "Number of basic elements")
        .def("nr_dynamic", &DFT<ValueType>::nrDynamicElements, "Number of dynamic elements")
        .def("can_have_nondeterminism", &DFT<ValueType>::canHaveNondeterminism, "Whether the model can contain non-deterministic choices")
        .def("__str__", &DFT<ValueType>::getInfoString)
        .def("str_long", &DFT<ValueType>::getElementsString)
        .def_property_readonly(
            "top_level_element", [](DFT<ValueType>& dft) { return dft.getElement(dft.getTopLevelIndex()); }, "Get top level element")
        .def("get_element", &DFT<ValueType>::getElement, "Get DFT element at index", py::arg("index"))
        .def(
            "get_element_by_name", [](DFT<ValueType>& dft, std::string const& name) { return dft.getElement(dft.getIndex(name)); }, "Get DFT element by name",
            py::arg("name"))
        .def(
            "modules",
            [](DFT<ValueType> const& dft) {
                storm::dft::utility::DftModularizer<ValueType> modularizer;
                return modularizer.computeModules(dft);
            },
            "Compute independent modules of DFT")
        .def(
            "symmetries", [](DFT<ValueType>& dft) { return storm::dft::utility::SymmetryFinder<ValueType>::findSymmetries(dft); }, "Compute symmetries in DFT")
        .def("state_generation_info", &DFT<ValueType>::buildStateGenerationInfo, "Build state generation information",
             py::arg("symmetries") = storm::dft::storage::DftSymmetries())
        .def("set_relevant_events", &DFT<ValueType>::setRelevantEvents, py::arg("relevant_events"), py::arg("allow_dc_for_revelant"));
}

void define_symmetries(py::module& m) {
    py::classh<storm::dft::storage::DftSymmetries>(m, "DftSymmetries", "Symmetries in DFT")
        .def(py::init<>(), "Constructor for empty symmetry")
        .def("__len__", &storm::dft::storage::DftSymmetries::nrSymmetries)
        .def(
            "__iter__", [](storm::dft::storage::DftSymmetries const& symmetries) { return py::make_iterator(symmetries.begin(), symmetries.end()); },
            py::keep_alive<0, 1>() /* Essential: keep object alive while iterator exists */)
        .def("get_group", &storm::dft::storage::DftSymmetries::getSymmetryGroup, "Get symmetry group", py::arg("index"))
        .def("__str__", &streamToString<storm::dft::storage::DftSymmetries>);
}

template void define_dft_typed<double>(py::module& m);
template void define_dft_typed<storm::RationalFunction>(py::module& m);

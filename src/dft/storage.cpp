#include "storage.h"

#include <storm-dft/storage/DFT.h>
#include <storm-dft/storage/DFTState.h>
#include <storm-dft/storage/DftModule.h>
#include <storm-dft/storage/DftSymmetries.h>
#include <storm-dft/storage/FailableElements.h>
#include <storm-dft/storage/elements/DFTDependency.h>
#include <storm-dft/utility/DftModularizer.h>
#include <storm-dft/utility/RelevantEvents.h>
#include <storm-dft/utility/SymmetryFinder.h>
#include <storm/adapters/RationalFunctionAdapter.h>

#include "src/binding_type_index.h"
#include "src/helpers.h"

template<typename ValueType>
using DFT = storm::dft::storage::DFT<ValueType>;
template<typename ValueType>
using DFTState = storm::dft::storage::DFTState<ValueType>;
typedef storm::dft::storage::FailableElements Failable;
typedef storm::dft::storage::FailableElements::const_iterator FailableIter;
using DftIndependentModule = storm::dft::storage::DftIndependentModule;

// requires pycarl.Variable
std::set<storm::RationalFunctionVariable> getParameters(DFT<storm::RationalFunction> const& dft) {
    return storm::dft::storage::getParameters(dft);
}

void define_dft(py::module& m) {
    m.def("get_parameters", &getParameters, "Collect parameters in parametric DFT", py::arg("dft"));
}

template<typename ValueType>
void define_dft_typed(py::module& m) {
    // DFT class
    auto dft = stormpy::bindings::bindTemplateClass<DFT<ValueType>>(m, "DFT", stormpy::bindings::typeIndex<ValueType>(), "Dynamic Fault Tree");
    dft.def(py::init<DFT<ValueType> const&>(), "Copy a Dynamic Fault Tree", py::arg("dft"))
        .def("nr_elements", &DFT<ValueType>::nrElements, "Total number of elements")
        .def("nr_basic_elements", &DFT<ValueType>::nrBasicElements, "Number of basic elements")
        .def("nr_dynamic_elements", &DFT<ValueType>::nrDynamicElements, "Number of dynamic elements")
        .def("can_have_nondeterminism", &DFT<ValueType>::canHaveNondeterminism, "Whether the model can contain non-deterministic choices")
        .def("__str__", &DFT<ValueType>::getInfoString)
        .def("get_elements_string", &DFT<ValueType>::getElementsString)
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
        .def("build_state_generation_info", &DFT<ValueType>::buildStateGenerationInfo, "Build state generation information", py::arg("symmetries"))
        .def("set_relevant_events", &DFT<ValueType>::setRelevantEvents, py::arg("relevant_events"), py::arg("allow_dc_for_relevant"));
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

template<typename ValueType>
void define_dft_state(py::module& m) {
    // DFT state
    auto state = stormpy::bindings::bindTemplateClass<DFTState<ValueType>>(m, "DFTState", stormpy::bindings::typeIndex<ValueType>(), "DFT state");
    state.def("is_operational", &DFTState<ValueType>::isOperational, "Is element operational", py::arg("id"))
        .def(
            "has_failed", [](DFTState<ValueType> const& state, size_t id) { return state.hasFailed(id); }, "Is element failed", py::arg("id"))
        .def(
            "is_failsafe", [](DFTState<ValueType> const& state, size_t id) { return state.isFailsafe(id); }, "Is element fail-safe", py::arg("id"))
        .def("dont_care", &DFTState<ValueType>::dontCare, "Is element Don't Care", py::arg("id"))
        .def("is_invalid", &DFTState<ValueType>::isInvalid, "Is state invalid")
        .def("get_failable_elements", &DFTState<ValueType>::getFailableElements, "Get failable elements")
        .def("spare_uses", &DFTState<ValueType>::uses, "Child currently used by a SPARE", py::arg("spare_id"))
        .def("__str__", [](DFTState<ValueType> const& state) { return streamToString<storm::storage::BitVector>(state.status()); })
        .def(
            "to_string",
            [](std::shared_ptr<DFTState<ValueType>> const& state, storm::dft::storage::DFT<ValueType> const& dft) { return dft.getStateString(state); },
            "Print status", py::arg("dft"));
}

void define_failable_elements(py::module& m) {
    // Helper iterator for access from python
    // We need to manually create the bindings (and not use make_iterator) as we need access to the iterator (and not only the value).
    struct FailableIterator {
        FailableIterator(Failable const& failable, py::object ref) : failable(failable), ref(ref), it(failable.begin()) {}

        FailableIter next() {
            if (it == failable.end()) {
                throw py::stop_iteration();
            } else {
                FailableIter res(it);
                ++it;
                return res;
            }
        }

        Failable const& failable;
        py::object ref;  // keep a reference
        FailableIter it;
    };

    py::classh<Failable>(m, "FailableElements", "Failable elements in DFT state")
        .def("__iter__", [](py::object s) { return FailableIterator(s.cast<Failable const&>(), s); }, py::keep_alive<0, 1>());

    py::classh<FailableIterator>(m, "FailableIterator")
        .def(
            "__iter__", [](FailableIterator& it) -> FailableIterator& { return it; }, py::keep_alive<0, 1>())
        .def("__next__", &FailableIterator::next, py::keep_alive<0, 1>());

    py::classh<FailableIter>(m, "FailableElement", "Failable element")
        .def("is_due_dependency", &FailableIter::isFailureDueToDependency, "Is failure due to dependency")
        .def("as_be", &FailableIter::asBE<double>, py::arg("dft"), "Get BE which fails")
        .def("as_be", &FailableIter::asBE<storm::RationalFunction>, py::arg("dft"), "Get BE which fails")
        .def("as_be_double", &FailableIter::asBE<double>, py::arg("dft"), "Get BE which fails in a double-valued DFT")
        .def("as_be_ratfunc", &FailableIter::asBE<storm::RationalFunction>, py::arg("dft"), "Get BE which fails in a rational-function-valued DFT")
        .def("as_dependency", &FailableIter::asDependency<double>, py::arg("dft"), "Get dependency which is triggered")
        .def("as_dependency", &FailableIter::asDependency<storm::RationalFunction>, py::arg("dft"), "Get dependency which is triggered")
        .def("as_dependency_double", &FailableIter::asDependency<double>, py::arg("dft"), "Get dependency which is triggered in a double-valued DFT")
        .def("as_dependency_ratfunc", &FailableIter::asDependency<storm::RationalFunction>, py::arg("dft"),
             "Get dependency which is triggered in a rational-function-valued DFT");
}

void define_module(py::module& m) {
    py::classh<DftIndependentModule>(m, "DftIndependentModule", "Independent module in DFT")
        .def("is_static", &DftIndependentModule::isStatic, "Whether the module contains only static elements (except in submodules)")
        .def("is_fully_static", &DftIndependentModule::isFullyStatic, "Whether the module contains only static elements (also in submodules)")
        .def("is_single_be", &DftIndependentModule::isSingleBE, "Whether the module consists of a single BE (trivial module)")
        .def("get_representative", &DftIndependentModule::getRepresentative, "Get module representative")
        .def("get_elements", &DftIndependentModule::getElements, "Get elements of module (excluding submodules)")
        .def("get_submodules", &DftIndependentModule::getSubModules, "Get submodules")
        .def("get_subtree", &DftIndependentModule::getSubtree<double>, "Get subtree formed by module", py::arg("dft"))
        .def("get_subtree", &DftIndependentModule::getSubtree<storm::RationalFunction>, "Get subtree formed by module", py::arg("dft"));
}

template void define_dft_typed<double>(py::module& m);
template void define_dft_typed<storm::RationalFunction>(py::module& m);
template void define_dft_state<double>(py::module& m);
template void define_dft_state<storm::RationalFunction>(py::module& m);

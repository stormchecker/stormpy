#include "dft_state.h"
#include "src/helpers.h"
#include "storm-dft/storage/DFTState.h"
#include "storm-dft/storage/FailableElements.h"
#include "storm/adapters/RationalFunctionAdapter.h"

template<typename ValueType>
using DFTState = storm::dft::storage::DFTState<ValueType>;
typedef storm::dft::storage::FailableElements Failable;
typedef storm::dft::storage::FailableElements::const_iterator FailableIter;

template<typename ValueType>
void define_dft_state(py::module& m, std::string const& vt_suffix) {
    // DFT state
    py::class_<DFTState<ValueType>, std::shared_ptr<DFTState<ValueType>>>(m, ("DFTState" + vt_suffix).c_str(), "DFT state")
        .def("operational", &DFTState<ValueType>::isOperational, "Is element operational", py::arg("id"))
        .def(
            "failed", [](DFTState<ValueType> const& state, size_t id) { return state.hasFailed(id); }, "Is element failed", py::arg("id"))
        .def(
            "failsafe", [](DFTState<ValueType> const& state, size_t id) { return state.isFailsafe(id); }, "Is element fail-safe", py::arg("id"))
        .def("dontcare", &DFTState<ValueType>::dontCare, "Is element Don't Care", py::arg("id"))
        .def("invalid", &DFTState<ValueType>::isInvalid, "Is state invalid")
        .def("failable", &DFTState<ValueType>::getFailableElements, "Get failable elements")
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

    py::class_<Failable, std::shared_ptr<Failable>>(m, "FailableElements", "Failable elements in DFT state")
        .def("__iter__", [](py::object s) { return FailableIterator(s.cast<Failable const&>(), s); }, py::keep_alive<0, 1>());

    py::class_<FailableIterator>(m, "FailableIterator")
        .def(
            "__iter__", [](FailableIterator& it) -> FailableIterator& { return it; }, py::keep_alive<0, 1>())
        .def("__next__", &FailableIterator::next, py::keep_alive<0, 1>());

    py::class_<FailableIter, std::shared_ptr<FailableIter>>(m, "FailableElement", "Failable element")
        .def("is_due_dependency", &FailableIter::isFailureDueToDependency, "Is failure due to dependency")
        .def("as_be_double", &FailableIter::asBE<double>, py::arg("dft"), "Get BE which fails")
        .def("as_be_ratfunc", &FailableIter::asBE<storm::RationalFunction>, py::arg("dft"), "Get BE which fails")
        .def("as_dependency_double", &FailableIter::asDependency<double>, py::arg("dft"), "Get dependency which is triggered")
        .def("as_dependency_ratfunc", &FailableIter::asDependency<storm::RationalFunction>, py::arg("dft"), "Get dependency which is triggered");
}

template void define_dft_state<double>(py::module& m, std::string const& vt_suffix);
template void define_dft_state<storm::RationalFunction>(py::module& m, std::string const& vt_suffix);

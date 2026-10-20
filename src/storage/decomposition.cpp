#include "decomposition.h"

#include <storm/adapters/IntervalAdapter.h>
#include <storm/storage/decomposition/MaximalEndComponent.h>
#include <storm/storage/decomposition/MaximalEndComponentDecomposition.h>

#include "src/binding_type_index.h"

using MEC = storm::storage::MaximalEndComponent;
template<typename ValueType>
using MECDecomposition = storm::storage::MaximalEndComponentDecomposition<ValueType>;

void define_maximal_end_components(py::module& m) {
    py::classh<MEC>(m, "MaximalEndComponent", "Maximal end component")

        .def_property_readonly("size", &MEC::size, "Number of states in MEC")
        .def(
            "__iter__", [](MEC const& mec) { return py::make_iterator(mec.begin(), mec.end()); },
            py::keep_alive<0, 1>() /* Essential: keep object alive while iterator exists */);
}

template<typename ValueType>
void define_maximal_end_component_decomposition(py::module& m) {
    stormpy::bindings::bindTemplateClass<MECDecomposition<ValueType>>(m, "MaximalEndComponentDecomposition", stormpy::bindings::typeIndex<ValueType>(),
                                                                      "Decomposition of maximal end components")
        .def(py::init<storm::models::sparse::NondeterministicModel<ValueType> const&>(), py::arg("model"), "Create MECs from model")
        .def_property_readonly("size", &MECDecomposition<ValueType>::size, "Number of MECs in the decomposition")
        .def(
            "__iter__", [](MECDecomposition<ValueType> const& mecs) { return py::make_iterator(mecs.begin(), mecs.end()); },
            py::keep_alive<0, 1>() /* Essential: keep object alive while iterator exists */);
}

template void define_maximal_end_component_decomposition<double>(py::module& m);
template void define_maximal_end_component_decomposition<storm::RationalNumber>(py::module& m);
template void define_maximal_end_component_decomposition<storm::Interval>(py::module& m);
template void define_maximal_end_component_decomposition<storm::RationalInterval>(py::module& m);
template void define_maximal_end_component_decomposition<storm::RationalFunction>(py::module& m);

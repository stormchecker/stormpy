#include "dft.h"

#include <storm-dft/transformations/DftInstantiator.h>
#include <storm/adapters/RationalFunctionAdapter.h>

#include "src/binding_type_index.h"
#include "src/helpers.h"

using DFTInstantiator = storm::dft::transformations::DftInstantiator<storm::RationalFunction, double>;

void define_transformations(py::module& m) {
    auto instantiator = stormpy::bindings::bindTemplateClass<DFTInstantiator, std::shared_ptr<DFTInstantiator>>(
        m, "DFTInstantiator", stormpy::bindings::typeIndex<storm::RationalFunction, double>(), "Instantiator for parametric DFT");
    instantiator.def(py::init<storm::dft::storage::DFT<storm::RationalFunction> const&>(), "Initialize with parametric DFT", py::arg("dft"))
        .def("instantiate", &DFTInstantiator::instantiate, "Instantiate parametric DFT and obtain concrete DFT", py::arg("valuation"));
}

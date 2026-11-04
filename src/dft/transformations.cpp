#include "transformations.h"

#include <storm-dft/storage/DFT.h>
#include <storm-dft/transformations/DftInstantiator.h>
#include <storm/adapters/RationalFunctionAdapter.h>

#include "src/binding_type_index.h"
#include "src/helpers.h"

namespace stormpy::dft {

using DFTInstantiator = storm::dft::transformations::DftInstantiator<storm::RationalFunction, double>;

void define_transformations(py::module& m) {
    auto instantiator = stormpy::bindings::bindTemplateClass<DFTInstantiator>(
        m, "DftInstantiator", stormpy::bindings::typeIndex<storm::RationalFunction, double>(), "Instantiator for parametric DFT");
    instantiator
        .def(py::init<storm::dft::storage::DFT<storm::RationalFunction> const&>(), "Initialize with parametric DFT", py::arg("dft"), py::keep_alive<1, 2>())
        .def("instantiate", &DFTInstantiator::instantiate, "Instantiate parametric DFT and obtain concrete DFT", py::arg("valuation"));
}

}  // namespace stormpy::dft

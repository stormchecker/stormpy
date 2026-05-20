#include "dft.h"
#include "src/helpers.h"

#include "storm-dft/transformations/DftInstantiator.h"
#include "storm/adapters/RationalFunctionAdapter.h"

using DFTInstantiator = storm::dft::transformations::DftInstantiator<storm::RationalFunction, double>;

void define_transformations(py::module& m) {
    py::class_<DFTInstantiator, std::shared_ptr<DFTInstantiator>>(m, "DFTInstantiator", "Instantiator for parametric DFT")
        .def(py::init<storm::dft::storage::DFT<storm::RationalFunction> const&>(), "Initialize with parametric DFT", py::arg("dft"))
        .def("instantiate", &DFTInstantiator::instantiate, "Instantiate parametric DFT and obtain concrete DFT", py::arg("valuation"));
}

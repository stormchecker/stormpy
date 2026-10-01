#include "dft.h"

#include <storm-dft/storage/DFT.h>
#include <storm-dft/storage/DftModule.h>

using DftIndependentModule = storm::dft::storage::DftIndependentModule;

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

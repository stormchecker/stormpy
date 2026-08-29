#include "dft_elements.h"

#include <storm-dft/storage/elements/DFTElements.h>
#include <storm/adapters/RationalFunctionAdapter.h>

template<typename ValueType>
using DFTElement = storm::dft::storage::elements::DFTElement<ValueType>;
template<typename ValueType>
using BE = storm::dft::storage::elements::DFTBE<ValueType>;
template<typename ValueType>
using Dependency = storm::dft::storage::elements::DFTDependency<ValueType>;

void define_dft_elements(py::module& m) {
    // DFT element type
    py::native_enum<storm::dft::storage::elements::DFTElementType>(m, "DFTElementType", "enum.Enum")
        .value("BE", storm::dft::storage::elements::DFTElementType::BE)
        .value("AND", storm::dft::storage::elements::DFTElementType::AND)
        .value("OR", storm::dft::storage::elements::DFTElementType::OR)
        .value("VOT", storm::dft::storage::elements::DFTElementType::VOT)
        .value("PAND", storm::dft::storage::elements::DFTElementType::PAND)
        .value("POR", storm::dft::storage::elements::DFTElementType::POR)
        .value("SPARE", storm::dft::storage::elements::DFTElementType::SPARE)
        .value("PDEP", storm::dft::storage::elements::DFTElementType::PDEP)
        .value("SEQ", storm::dft::storage::elements::DFTElementType::SEQ)
        .value("MUTEX", storm::dft::storage::elements::DFTElementType::MUTEX)
        .finalize();
    m.attr("DFTElementType").attr("friendly_name") =
        py::cpp_function([](storm::dft::storage::elements::DFTElementType type) { return storm::dft::storage::elements::toString(type); },
                         py::name("friendly_name"), py::is_method(m.attr("DFTElementType")));
}

template<typename ValueType>
void define_dft_elements_typed(py::module& m, std::string const& vt_suffix) {
    // DFT elements
    py::classh<DFTElement<ValueType>> element(m, ("DFTElement" + vt_suffix).c_str(), "DFT element");
    element.def_property_readonly("id", &DFTElement<ValueType>::id, "Id")
        .def_property_readonly("name", &DFTElement<ValueType>::name, "Name")
        .def_property_readonly("type", &DFTElement<ValueType>::type, "Type")
        .def("__str__", &DFTElement<ValueType>::toString);

    py::classh<BE<ValueType>>(m, ("DFTBE" + vt_suffix).c_str(), "Basic Event", element).def("__str__", &BE<ValueType>::toString);

    py::classh<Dependency<ValueType>>(m, ("DFTDependency" + vt_suffix).c_str(), "Dependency", element)
        .def_property_readonly("trigger", &Dependency<ValueType>::triggerEvent, "Trigger event")
        .def_property_readonly("dependent_events", &Dependency<ValueType>::dependentEvents, "Dependent events")
        .def("__str__", &Dependency<ValueType>::toString);
}

template void define_dft_elements_typed<double>(py::module& m, std::string const& vt_suffix);
template void define_dft_elements_typed<storm::RationalFunction>(py::module& m, std::string const& vt_suffix);

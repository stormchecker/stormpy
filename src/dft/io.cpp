#include "io.h"
#include "src/helpers.h"

// Define python bindings
void define_input(py::module& m) {
    // Load DFT input
    m.def("load_dft_galileo_file", &storm::dft::api::loadDFTGalileoFile<double>, "Load DFT from Galileo file", py::arg("path"));
    m.def("load_parametric_dft_galileo_file", &storm::dft::api::loadDFTGalileoFile<storm::RationalFunction>, "Load parametric DFT from Galileo file",
          py::arg("path"));
    // Parse Jani model
    m.def("load_dft_json_file", &storm::dft::api::loadDFTJsonFile<double>, "Load DFT from JSON file", py::arg("path"));
    m.def("load_dft_json_string", &storm::dft::api::loadDFTJsonString<double>, "Load DFT from JSON string", py::arg("json_string"));
    m.def("load_parametric_dft_json_file", &storm::dft::api::loadDFTJsonFile<storm::RationalFunction>, "Load parametric DFT from JSON file", py::arg("path"));
    m.def("load_parametric_dft_json_string", &storm::dft::api::loadDFTJsonString<storm::RationalFunction>, "Load parametric DFT from JSON string",
          py::arg("json_string"));
}

void define_output(py::module& m) {
    // Export DFT
    m.def("export_dft_json_file", &storm::dft::api::exportDFTToJsonFile<double>, "Export DFT to JSON file", py::arg("dft"), py::arg("path"));
    m.def("export_dft_json_string", &storm::dft::api::exportDFTToJsonString<double>, "Export DFT to JSON string", py::arg("dft"));
    m.def("export_parametric_dft_json_file", &storm::dft::api::exportDFTToJsonFile<storm::RationalFunction>, "Export parametric DFT to JSON file",
          py::arg("dft"), py::arg("path"));
    m.def("export_parametric_dft_json_string", &storm::dft::api::exportDFTToJsonString<storm::RationalFunction>, "Export parametric DFT to JSON string",
          py::arg("dft"));
}

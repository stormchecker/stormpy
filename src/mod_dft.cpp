#include <storm/adapters/RationalFunctionForward.h>

#include "src/common.h"
#include "src/dft/api.h"
#include "src/dft/builder.h"
#include "src/dft/environment.h"
#include "src/dft/simulator.h"
#include "src/dft/storage.h"
#include "src/dft/storage_elements.h"
#include "src/dft/transformations.h"
#include "src/dft/utility.h"

PYBIND11_MODULE(_dft, m) {
    m.doc() = "Functionality for DFT analysis";

#ifdef STORMPY_DISABLE_SIGNATURE_DOC
    py::options options;
    options.disable_function_signatures();
#endif

    define_api_io_input(m);
    define_api_io_output(m);
    define_api_analysis(m);
    define_api_analysis_typed<double>(m);
    define_api_analysis_typed<storm::RationalFunction>(m);
    define_api_transformation_typed<double>(m);
    define_api_transformation_typed<storm::RationalFunction>(m);
    define_builder(m);
    define_builder_typed<double>(m);
    define_builder_typed<storm::RationalFunction>(m);
    define_dft_environment(m);
    define_simulator(m);
    define_simulator_typed<double>(m);
    define_simulator_typed<storm::RationalFunction>(m);
    define_symmetries(m);
    define_dft(m);
    define_dft_typed<double>(m);
    define_dft_typed<storm::RationalFunction>(m);
    define_dft_state<double>(m);
    define_dft_state<storm::RationalFunction>(m);
    define_failable_elements(m);
    define_module(m);
    define_storage_elements(m);
    define_storage_elements_typed<double>(m);
    define_storage_elements_typed<storm::RationalFunction>(m);
    define_transformations(m);
    define_relevant_events(m);
}

#include "common.h"

#include "dft/analysis.h"
#include "dft/dft.h"
#include "dft/dft_elements.h"
#include "dft/dft_state.h"
#include "dft/io.h"
#include "dft/module.h"
#include "dft/simulator.h"
#include "dft/transformations.h"

PYBIND11_MODULE(_dft, m) {
    m.doc() = "Functionality for DFT analysis";

#ifdef STORMPY_DISABLE_SIGNATURE_DOC
    py::options options;
    options.disable_function_signatures();
#endif

    define_symmetries(m);  // Must be before define_analysis_typed
    define_analysis(m);
    define_analysis_typed<double>(m, "_double");
    define_analysis_typed<storm::RationalFunction>(m, "_ratfunc");
    define_dft(m);
    define_dft_typed<double>(m, "_double");
    define_dft_typed<storm::RationalFunction>(m, "_ratfunc");
    define_dft_elements(m);
    define_dft_elements_typed<double>(m, "_double");
    define_dft_elements_typed<storm::RationalFunction>(m, "_ratfunc");
    define_dft_state<double>(m, "_double");
    define_dft_state<storm::RationalFunction>(m, "_ratfunc");
    define_failable_elements(m);
    define_input(m);
    define_module(m);
    define_output(m);
    define_simulator(m);
    define_simulator_typed<double>(m, "_double");
    define_simulator_typed<storm::RationalFunction>(m, "_ratfunc");
    define_transformations(m);
}

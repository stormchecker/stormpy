#include "common.h"

#include "pars/model_instantiator.h"
#include "pars/pars.h"
#include "pars/pla.h"

PYBIND11_MODULE(_pars, m) {
    m.doc() = "Functionality for parametric analysis";

#ifdef STORMPY_DISABLE_SIGNATURE_DOC
    py::options options;
    options.disable_function_signatures();
#endif

    define_pars(m);
    define_pla(m);
    define_model_instantiator(m);
    define_model_instantiation_checker(m);
}

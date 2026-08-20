#include "src/common.h"
#include "src/pars/model_instantiator.h"
#include "src/pars/pars.h"
#include "src/pars/pla.h"

namespace {

void bindPars(py::module& m) {
    define_pars(m);
    define_pla(m);
    define_model_instantiator<double>(m);
    define_model_instantiator<storm::RationalFunction>(m);
    define_model_instantiation_checker<double>(m);
    define_model_instantiation_checker<storm::RationalNumber>(m);
}

}  // namespace

PYBIND11_MODULE(_pars, m) {
    m.doc() = "Functionality for parametric analysis";

#ifdef STORMPY_DISABLE_SIGNATURE_DOC
    py::options options;
    options.disable_function_signatures();
#endif

    py::bindModule(m, bindPars);
}

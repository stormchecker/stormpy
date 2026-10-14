#include <storm/adapters/RationalNumberAdapter.h>

#include "src/common.h"
#include "src/utility/chrono.h"
#include "src/utility/kwekMehlhorn.h"
#include "src/utility/shortestPaths.h"

PYBIND11_MODULE(_utility, m) {
    m.doc() = "Utilities for Storm";

#ifdef STORMPY_DISABLE_SIGNATURE_DOC
    py::options options;
    options.disable_function_signatures();
#endif

    define_ksp(m);
    define_ksp_typed<double>(m);
    define_ksp_typed<storm::RationalNumber>(m);
    define_chrono(m);
    define_kwek_mehlhorn<storm::RationalNumber>(m);
}

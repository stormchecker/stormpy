#include <storm/adapters/RationalNumberAdapter.h>

#include "src/common.h"
#include "src/utility/chrono.h"
#include "src/utility/json.h"
#include "src/utility/kwekMehlhorn.h"
#include "src/utility/shortestPaths.h"
#include "src/utility/smtsolver.h"

PYBIND11_MODULE(_utility, m) {
    m.doc() = "Utilities for Storm";

#ifdef STORMPY_DISABLE_SIGNATURE_DOC
    py::options options;
    options.disable_function_signatures();
#endif

    define_ksp(m);
    define_smt(m);
    define_chrono(m);
    define_json<double>(m, "Double");
    define_json<storm::RationalNumber>(m, "Rational");
    define_kwek_mehlhorn<storm::RationalNumber>(m, "");
}

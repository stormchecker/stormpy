#include <storm/adapters/RationalNumberAdapter.h>

#include "src/module_bindings.h"
#include "src/utility/chrono.h"
#include "src/utility/json.h"
#include "src/utility/kwekMehlhorn.h"
#include "src/utility/shortestPaths.h"
#include "src/utility/smtsolver.h"

namespace stormpy::bindings {

void bindUtility(py::module& m) {
    define_ksp(m);
    define_smt(m);
    define_chrono(m);
    define_json<double>(m, "Double");
    define_json<storm::RationalNumber>(m, "Rational");
    define_kwek_mehlhorn<storm::RationalNumber>(m, "");
}

}  // namespace stormpy::bindings

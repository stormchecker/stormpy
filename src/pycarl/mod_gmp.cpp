#include "src/common.h"
#include "src/pycarl/typed_core/factorization.h"
#include "src/pycarl/typed_core/factorizedpolynomial.h"
#include "src/pycarl/typed_core/factorizedrationalfunction.h"
#include "src/pycarl/typed_core/integer.h"
#include "src/pycarl/typed_core/interval.h"
#include "src/pycarl/typed_core/polynomial.h"
#include "src/pycarl/typed_core/rational.h"
#include "src/pycarl/typed_core/rationalfunction.h"
#include "src/pycarl/typed_core/term.h"
#include "src/pycarl/types.h"

namespace {

void bindGmp(py::module& m) {
    define_gmp_integer(m);
    define_gmp_rational(m);
    define_term(m);
    define_polynomial(m);
    define_factorizationcache(m);
    define_factorization(m);
    define_factorizedpolynomial(m);
    define_rationalfunction(m);
    define_factorizedrationalfunction(m);

    define_interval<Rational>(m);
}

}  // namespace

PYBIND11_MODULE(_gmp, m) {
    m.attr("__name__") = "stormpy.pycarl.gmp";
    m.doc() = "pycarl core gmp-typed data and functions";

    py::bindModule(m, bindGmp);
}

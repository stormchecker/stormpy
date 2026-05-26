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

PYBIND11_MODULE(_cln, m) {
    m.attr("__name__") = "stormpy.pycarl.cln";

    m.doc() = "pycarl core cln-typed data and functions";

    define_cln_integer(m);
    define_cln_rational(m);
    define_term(m);
    define_polynomial(m);
    define_factorizationcache(m);
    define_factorization(m);
    define_factorizedpolynomial(m);
    define_rationalfunction(m);
    define_factorizedrationalfunction(m);

    define_interval<Rational>(m);
}

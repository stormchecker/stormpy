#include "common.h"
#include "types.h"

#include "typed_core/integer.h"
#include "typed_core/rational.h"
#include "typed_core/term.h"
#include "typed_core/polynomial.h"
#include "typed_core/rationalfunction.h"
#include "typed_core/factorization.h"
#include "typed_core/factorizedpolynomial.h"
#include "typed_core/factorizedrationalfunction.h"
#include "typed_core/interval.h"

PYBIND11_MODULE(gmp, m) {
    m.attr("__name__") = "stormpy.pycarl.gmp";
    m.doc() = "pycarl core gmp-typed data and functions";

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

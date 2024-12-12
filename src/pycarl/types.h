#include "pycarl/definitions.h"

#include <carl/core/Monomial.h>
#include <carl/core/Term.h>
#include <carl/core/MultivariatePolynomial.h>
#include <carl/core/PolynomialFactorizationPair.h>
#include <carl/core/FactorizedPolynomial.h>
#include <carl/core/RationalFunction.h>
#include <carl/interval/Interval.h>

#ifdef PYCARL_USE_CLN
#include "types/cln_types.h"
#else
#include "types/gmp_types.h"
#endif

typedef carl::Monomial Monomial;
typedef carl::Term<Rational> Term;
typedef carl::MultivariatePolynomial<Rational> Polynomial;
typedef carl::Factorization<Polynomial> Factorization;
typedef carl::FactorizedPolynomial<Polynomial> FactorizedPolynomial;
typedef carl::RationalFunction<Polynomial, true> RationalFunction;
typedef carl::RationalFunction<FactorizedPolynomial, true> FactorizedRationalFunction;
typedef carl::PolynomialFactorizationPair<Polynomial> FactorizationPair;

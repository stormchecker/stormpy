from . import _gmp
from ._gmp import *


def numerator(x):
    if type(x) == _gmp.RationalFunction or type(x) == _gmp.Rational or type(x) == _gmp.FactorizedRationalFunction:
        return x.numerator
    else:
        return x


def denominator(x):
    if type(x) == _gmp.RationalFunction or type(x) == _gmp.Rational or type(x) == _gmp.FactorizedRationalFunction:
        return x.denominator
    else:
        return 1


def expand(x):
    if type(x) == _gmp.FactorizedRationalFunction:
        return x.rational_function()
    if type(x) == _gmp.FactorizedPolynomial:
        return x.polynomial()
    return x


factorization_cache = _gmp._FactorizationCache()


def create_factorized_polynomial(polynomial):
    return _gmp.FactorizedPolynomial(polynomial, factorization_cache)

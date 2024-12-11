from . import gmp
from .gmp import *


def numerator(x):
    if type(x) == gmp.RationalFunction or type(x) == gmp.Rational or type(x) == gmp.FactorizedRationalFunction:
        return x.numerator
    else:
        return x


def denominator(x):
    if type(x) == gmp.RationalFunction or type(x) == gmp.Rational or type(x) == gmp.FactorizedRationalFunction:
        return x.denominator
    else:
        return 1


def expand(x):
    if type(x) == gmp.FactorizedRationalFunction:
        return x.rational_function()
    if type(x) == gmp.FactorizedPolynomial:
        return x.polynomial()
    return x


factorization_cache = gmp._FactorizationCache()


def create_factorized_polynomial(polynomial):
    return gmp.FactorizedPolynomial(polynomial, factorization_cache)

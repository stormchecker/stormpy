from stormpy.pycarl import _config

if not _config.CARL_WITH_CLN:
    raise ImportError("CLN is not available in the configured carl library! Did you configure carl with -DUSE_CLN_NUMBERS=ON?")
from . import cln
from .cln import *


def numerator(x):
    if type(x) == cln.RationalFunction or type(x) == cln.Rational or type(x) == cln.FactorizedRationalFunction:
        return x.numerator
    else:
        return x


def denominator(x):
    if type(x) == cln.RationalFunction or type(x) == cln.Rational or type(x) == cln.FactorizedRationalFunction:
        return x.denominator
    else:
        return 1


def expand(x):
    if type(x) == cln.FactorizedRationalFunction:
        return x.rational_function()
    if type(x) == cln.FactorizedPolynomial:
        return x.polynomial()
    return x


factorization_cache = cln._FactorizationCache()


def create_factorized_polynomial(polynomial):
    return cln.FactorizedPolynomial(polynomial, factorization_cache)

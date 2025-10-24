from stormpy.pycarl import _config

if not _config.CARL_WITH_CLN:
    raise ImportError("CLN is not available in the configured carl library! Did you configure carl with -DUSE_CLN_NUMBERS=ON?")
from . import _cln
from ._cln import *


def numerator(x):
    if type(x) == _cln.RationalFunction or type(x) == _cln.Rational or type(x) == _cln.FactorizedRationalFunction:
        return x.numerator
    else:
        return x


def denominator(x):
    if type(x) == _cln.RationalFunction or type(x) == _cln.Rational or type(x) == _cln.FactorizedRationalFunction:
        return x.denominator
    else:
        return 1


def expand(x):
    if type(x) == _cln.FactorizedRationalFunction:
        return x.rational_function()
    if type(x) == _cln.FactorizedPolynomial:
        return x.polynomial()
    return x


factorization_cache = _cln._FactorizationCache()


def create_factorized_polynomial(polynomial):
    return _cln.FactorizedPolynomial(polynomial, factorization_cache)

from . import _pycarl_core
from ._pycarl_core import *
from . import infinity
from stormpy.pycarl import _config

inf = infinity.Infinity()


def carl_version():
    """
    Get Carl version.
    :return: Version of Carl.
    """
    return _config.CARL_VERSION


def has_cln():
    """
    Check if pycarl has support for CLN.
    :return: True iff CLN is supported.
    """
    return _config.CARL_WITH_CLN


def clear_pools():
    """
    Clear all pools.
    """
    # clear_monomial_pool()
    clear_variable_pool()

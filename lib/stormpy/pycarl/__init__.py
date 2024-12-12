import sys

if sys.version_info[0] == 2:
    raise ImportError("Python 2.x is not supported for pycarl.")

from . import pycarl_core
from .pycarl_core import *
from . import infinity
from stormpy.pycarl import _config

__version__ = "unknown"
try:
    from ._version import __version__
except ImportError:
    # We're running in a tree that doesn't have a _version.py, so we don't know what our version is.
    pass

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


def has_parser():
    """
    Check if pycarl has parsing support.
    :return: True iff parsing is supported.
    """
    return _config.CARL_WITH_PARSER


def print_info():
    """
    Print information about pycarl.
    """
    print("Pycarl version {}".format(__version__))
    print("Using carl in version {}".format(carl_version()))
    print("Support for CLN: {}".format(has_cln()))
    print("Support for parsing: {}".format(has_parser()))


def clear_pools():
    """
    Clear all pools.
    """
    # clear_monomial_pool()
    clear_variable_pool()

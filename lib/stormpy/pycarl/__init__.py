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


def carl_parser_directory() -> str | None:
    """
    Return the carl-parser directory which is used by stormpy, or None if carl parser is not available.

    :return: Carl-parser directory.
    """
    return _config.CARL_PARSER_DIRECTORY


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
    print("Support for CLN: {}".format(has_cln()))
    print("Support for parsing: {}".format(has_parser()))


def clear_pools():
    """
    Clear all pools.
    """
    # clear_monomial_pool()
    clear_variable_pool()

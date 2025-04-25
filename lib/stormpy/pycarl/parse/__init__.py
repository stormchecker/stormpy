from stormpy.pycarl import _config

if not _config.CARL_WITH_PARSER:
    raise ImportError("Parser is not available in the configured carl library! Did you configure carl with '-DBUILD_ADDONS=ON -DBUILD_ADDON_PARSER=ON'?")

from . import parse
from .parse import *


class ParserError(Exception):
    """
    Error which is meant to be raised when the parser throws an error.
    """

    def __init__(self, message):
        self.message = message


def deserialize(input, package):
    """

    :param input:
    :return:
    """
    error = None
    try:
        res = package.parse.parse._deserialize(input)
    except RuntimeError as e:
        error = str(e)
    # ugly save and rethrow yields improved error messages in pytest.
    if error:
        raise ParserError(error + " when parsing '" + input + "'")
    res_type = res.get_type()
    if res_type == parse._ParserReturnType.Rational:
        return res.as_rational()
    elif res_type == parse._ParserReturnType.Variable:
        return res.as_variable()
    elif res_type == parse._ParserReturnType.Monomial:
        return res.as_monomial()
    elif res_type == parse._ParserReturnType.Term:
        return res.as_term()
    elif res_type == parse._ParserReturnType.Polynomial:
        return res.as_polynomial()
    elif res_type == parse._ParserReturnType.RationalFunction:
        return res.as_rational_function()
    elif res_type == parse._ParserReturnType.Constraint:
        return res.as_constraint()
    elif res_type == parse._ParserReturnType.Formula:
        return res.as_formula()
    assert False, "Internal error."

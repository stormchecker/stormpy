import os
from lark import Lark, UnexpectedInput

from stormpy.pycarl.parse.transformer import CarlParserTransformer

_grammar_path = os.path.join(os.path.dirname(__file__), "lark_grammar.lark")
_parser = Lark.open(_grammar_path, parser="earley", lexer="dynamic", transformer=None)


class ParserError(Exception):
    def __init__(self, message):
        self.message = message


def deserialize(input, package):
    try:
        tree = _parser.parse(input)
        transformer = CarlParserTransformer(package)
        return transformer.transform(tree)
    except UnexpectedInput as e:
        raise ParserError(str(e) + " when parsing '" + input + "'")
    except Exception as e:
        msg = str(e) if str(e) else type(e).__name__
        raise ParserError(msg + " when parsing '" + input + "'")

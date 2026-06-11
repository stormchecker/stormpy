try:
    from lark import Lark, UnexpectedInput

    _lark_available = True
except ImportError:
    _lark_available = False

if _lark_available:
    import os
    from stormpy.pycarl.parse.transformer import CarlParserTransformer

    _grammar_path = os.path.join(os.path.dirname(__file__), "lark_grammar.lark")
    _parser = Lark.open(_grammar_path, parser="earley", lexer="dynamic", transformer=None)


class ParserError(Exception):
    def __init__(self, message):
        self.message = message


def deserialize(text, package):
    if not _lark_available:
        raise ParserError("stormpy.pycarl.parse requires the 'lark' package. Install it with: pip install lark")
    try:
        tree = _parser.parse(text)
        transformer = CarlParserTransformer(package)
        return transformer.transform(tree)
    except UnexpectedInput as e:
        raise ParserError(str(e) + " when parsing '" + text + "'")
    except Exception as e:
        msg = str(e) if str(e) else type(e).__name__
        raise ParserError(msg + " when parsing '" + text + "'")

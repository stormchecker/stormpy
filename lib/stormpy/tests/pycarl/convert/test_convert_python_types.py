import pytest
from stormpy import pycarl

parameters = [(pycarl.gmp, pycarl.convert.gmp_converter)]
names = ["gmp_converter"]

if pycarl.has_cln():
    parameters.append((pycarl.cln, pycarl.convert.cln_converter))
    names.append("cln_converter")


@pytest.mark.parametrize("convert_package,converter", parameters, ids=names)
class TestConvertExplicit:
    def test_convert_int(self, convert_package, converter):
        original = -2
        assert isinstance(original, int)
        converted = converter.convert_integer(original)
        assert isinstance(converted, convert_package.Integer)

    def test_convert_float(self, convert_package, converter):
        original = 43.12
        assert isinstance(original, float)
        converted = converter.convert_rational(original)
        assert isinstance(converted, convert_package.Rational)

from stormpy import pycarl

from configurations import PackageSelector, pycarl_parser


@pycarl_parser
class TestPycarlParse(PackageSelector):
    def test_parse_number(self, package):
        num = pycarl.parse.deserialize("2", package)
        assert num == package.Rational(2)
        num = pycarl.parse.deserialize("-2", package)
        assert num == package.Rational(-2)
        num = pycarl.parse.deserialize("(- 2)", package)
        assert num == package.Rational(-2)

    def test_parse_polynomial(self, package):
        pol = pycarl.parse.deserialize("(+ y 1)", package)
        assert str(pol) == "y+1"

    def test_parse_rational_function(self, package):
        rf = pycarl.parse.deserialize("(/ (+ x 1) (+ y 1))", package)
        x = pycarl.variable_with_name("x")
        y = pycarl.variable_with_name("y")
        assert package.numerator(rf) == package.Polynomial(x) + 1

    def test_parse_constraint(self, package):
        constraint = pycarl.parse.deserialize("(< x 0)", package)
        assert str(constraint) == "x<0"
        constraint = pycarl.parse.deserialize("(< x 1)", package)
        x = pycarl.variable_with_name("x")
        assert constraint.lhs == x - package.Rational(1)
        constraint = pycarl.parse.deserialize("(<= (* (- 1) x) 0)", package)
        assert constraint.lhs == -package.Polynomial(x)

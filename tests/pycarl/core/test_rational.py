from stormpy import pycarl
import math
from configurations import PackageSelector


class TestRational(PackageSelector):
    def test_create(self, package):
        r1 = package.Rational(package.Integer(1), package.Integer(2))
        assert package.numerator(r1) == 1
        assert package.denominator(r1) == 2

    def test_parse(self, package):
        r1 = package.Rational("1/2")
        assert package.numerator(r1) == 1
        assert package.denominator(r1) == 2
        r2 = package.Rational("1090843549285935/1125899906842624")
        assert package.numerator(r2) == package.Integer("1090843549285935")
        assert package.denominator(r2) == package.Integer("1125899906842624")

    def test_addition(self, package):
        r1 = package.Rational(package.Integer(2), package.Integer(5))
        r2 = package.Rational(package.Integer(3), package.Integer(10))
        res = r1 + r2
        assert isinstance(res, package.Rational)
        assert res == package.Rational("7/10")

    def test_subtraction(self, package):
        r1 = package.Rational(package.Integer(2), package.Integer(5))
        r2 = package.Rational(package.Integer(3), package.Integer(10))
        res = r1 - r2
        assert isinstance(res, package.Rational)
        assert res == package.Rational("1/10")

    def test_multiplication(self, package):
        r1 = package.Rational(package.Integer(2), package.Integer(5))
        r2 = package.Rational(package.Integer(3), package.Integer(10))
        res = r1 * r2
        assert isinstance(res, package.Rational)
        assert res == package.Rational("3/25")

    def test_division(self, package):
        r1 = package.Rational(package.Integer(2), package.Integer(5))
        r2 = package.Rational(package.Integer(3), package.Integer(10))
        res = r1 / r2
        assert isinstance(res, package.Rational)
        assert res == package.Rational("4/3")

    def test_eq(self, package):
        r3 = package.Rational("3/1")
        assert r3 == package.Integer(3)
        assert r3 == 3
        assert r3 != package.Integer(1)
        assert r3 != 2
        r2 = package.Rational("1/2")
        assert r3 != r2

    def test_comparison_infinity(self, package):
        r4 = package.Rational("1/2")
        assert pycarl.inf > r4
        assert r4 < pycarl.inf
        assert r4 > -pycarl.inf
        assert -pycarl.inf < r4

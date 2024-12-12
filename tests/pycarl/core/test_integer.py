from stormpy import pycarl
from configurations import PackageSelector


class TestInteger(PackageSelector):
    def test_construction(self, package):
        i3 = package.Integer("3")
        assert str(i3) == "3"
        i4 = package.Integer(4)
        assert str(i4) == "4"

    def test_eq(self, package):
        i3 = package.Integer(3)
        assert i3 == 3
        i3b = package.Integer(3)
        assert i3 == i3b
        in3 = package.Integer(-3)
        assert in3 == -3

    def test_addition(self, package):
        i1 = package.Integer(3)
        i2 = package.Integer(2)
        res = i1 + i2
        assert isinstance(res, package.Integer)
        assert res == 5
        assert i1 + 4 == 7
        assert i1 + -3 == 0

    def test_subtraction(self, package):
        i1 = package.Integer(4)
        i2 = package.Integer(-3)
        res = i1 - i2
        assert isinstance(res, package.Integer)
        assert res == 7

    def test_multiplication(self, package):
        i1 = package.Integer(5)
        i2 = package.Integer(6)
        res = i1 * i2
        assert isinstance(res, package.Integer)
        assert res == 30

    def test_division(self, package):
        i1 = package.Integer(10)
        i2 = package.Integer(2)
        res = i1 / i2
        assert isinstance(res, package.Rational)
        assert res == 5

    def test_neg(self, package):
        i3 = package.Integer(3)
        in3 = -i3
        assert in3 == -3
        inn3 = -in3
        assert i3 == inn3

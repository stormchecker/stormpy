from stormpy import pycarl
from configurations import PackageSelector


class TestPolynomial(PackageSelector):
    def test_init(self, package):
        pycarl.clear_pools()
        var = pycarl.Variable("x")
        pol = package.Polynomial(var)
        assert str(pol) == "x"

    def test_addition(self, package):
        pycarl.clear_pools()
        var1 = pycarl.Variable("x")
        var2 = pycarl.Variable("y")
        pol1 = var1 * var1 + package.Integer(2)
        pol2 = var2 + package.Integer(1)
        res = pol1 + pol2
        assert isinstance(res, package.Polynomial)
        polOrig = package.Polynomial(var1 * var1)
        polOrig += var2 + package.Integer(3)
        assert res == polOrig

    def test_subtraction(self, package):
        pycarl.clear_pools()
        var1 = pycarl.Variable("x")
        pol1 = package.Polynomial(5) * var1 * var1 + 2
        pol2 = package.Polynomial(var1 * var1) + 1
        res = pol1 - pol2
        assert isinstance(res, package.Polynomial)
        polOrig = package.Polynomial(4) * var1 * var1 + 1
        assert res == polOrig

    def test_multiplication(self, package):
        pycarl.clear_pools()
        var1 = pycarl.Variable("x")
        var2 = pycarl.Variable("y")
        pol1 = var1 * var1 + package.Integer(2)
        pol2 = var2 + package.Integer(1)
        res = pol1 * pol2
        assert isinstance(res, package.Polynomial)
        polOrig = package.Polynomial(var1 * var1 * var2) + var1 * var1 + package.Integer(2) * var2 + 2
        assert res == polOrig

    def test_division(self, package):
        pycarl.clear_pools()
        var1 = pycarl.Variable("x")
        var2 = pycarl.Variable("y")
        pol1 = package.Polynomial(var1 * var1 * var2) + package.Integer(2) * var2
        pol2 = package.Integer(3) * var2
        res = pol1 / pol2
        assert isinstance(res, package.RationalFunction)
        polOrig = package.Polynomial(var1 * var1)
        polOrig += package.Integer(2)
        assert res == package.RationalFunction(polOrig, package.Polynomial(3))

    def test_constant(self, package):
        pycarl.clear_pools()
        var1 = pycarl.Variable("x")
        var2 = pycarl.Variable("y")
        pol = package.Polynomial(var1 * var1 * var2) + package.Integer(2) * var2 + package.Integer(4)
        assert pol.constant_part() == 4
        pol = package.Polynomial(package.Rational(-8 / 3))
        assert pol.is_constant()
        print(type(pol))
        assert pol.constant_part() == package.Rational(-8 / 3)
        pol = package.Polynomial(1)
        assert pol.is_constant()
        print(type(pol))
        assert pol.constant_part() == 1

    def test_eq(self, package):
        pycarl.clear_pools()
        var = pycarl.Variable("x")
        pol1 = package.Integer(2) * var + package.Integer(3) * var * var
        assert not pol1 == package.Rational(1)
        pol2 = var + package.Integer(1) - var
        assert pol2 == package.Rational(1)
        assert pol2 == package.Integer(1)

    def test_substitute(self, package):
        pycarl.clear_pools()
        x = pycarl.Variable("x")
        y = pycarl.Variable("y")
        pol1 = package.Polynomial(1) - x
        sub = {x: -package.Polynomial(y) + 1}
        assert pol1.substitute(sub) == package.Polynomial(y)

        z = pycarl.Variable("z")
        sub2 = {z: package.Polynomial(3)}
        assert pol1.substitute(sub2) == pol1

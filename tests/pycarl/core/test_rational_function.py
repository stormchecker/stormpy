from stormpy import pycarl
from configurations import PackageSelector


class TestRationalFunction(PackageSelector):
    def test_init(self, package):
        pycarl.clear_pools()
        var = pycarl.Variable("x")
        num = package.Polynomial(2) * var * var + var
        denom = package.Polynomial(var)
        ratfunc = package.RationalFunction(num, denom)
        assert str(ratfunc) == "(2*x+1)/(1)"

    def test_addition(self, package):
        pycarl.clear_pools()
        var1 = pycarl.Variable("x")
        var2 = pycarl.Variable("y")
        pol1 = var1 * var1 + package.Integer(2)
        pol2 = var2 + package.Integer(1)
        ratfunc1 = package.RationalFunction(pol1, pol2)
        ratfunc2 = package.RationalFunction(package.Polynomial(2), package.Polynomial(1))
        res = ratfunc1 + ratfunc2
        assert isinstance(res, package.RationalFunction)
        polOrig = package.Polynomial(var1 * var1) + package.Integer(2) * var2 + package.Integer(4)
        assert res == package.RationalFunction(polOrig, pol2)

    def test_subtraction(self, package):
        pycarl.clear_pools()
        var1 = pycarl.Variable("x")
        var2 = pycarl.Variable("y")
        pol1 = var1 * var1 + package.Integer(2)
        pol2 = var2 + package.Integer(1)
        ratfunc1 = package.RationalFunction(pol1, pol2)
        ratfunc2 = package.RationalFunction(package.Polynomial(2), package.Polynomial(1))
        res = ratfunc1 - ratfunc2
        assert isinstance(res, package.RationalFunction)
        polOrig = package.Polynomial(var1 * var1) - package.Integer(2) * var2
        assert res == package.RationalFunction(polOrig, pol2)

    def test_multiplication(self, package):
        pycarl.clear_pools()
        var1 = pycarl.Variable("x")
        var2 = pycarl.Variable("y")
        pol1 = var1 * var1 + package.Integer(2)
        pol2 = var2 + package.Integer(1)
        ratfunc1 = package.RationalFunction(pol1, pol2)
        ratfunc2 = package.RationalFunction(package.Polynomial(2), package.Polynomial(1))
        res = ratfunc1 * ratfunc2
        assert isinstance(res, package.RationalFunction)
        polOrig = package.Polynomial(2) * var1 * var1 + package.Integer(4)
        assert res == package.RationalFunction(polOrig, pol2)

    def test_division(self, package):
        pycarl.clear_pools()
        var1 = pycarl.Variable("x")
        var2 = pycarl.Variable("y")
        pol1 = var1 * var1 + package.Integer(2)
        pol2 = package.Polynomial(var2)
        ratfunc1 = package.RationalFunction(pol1, pol2)
        ratfunc2 = package.RationalFunction(package.Polynomial(3), pol2)
        res = ratfunc1 / ratfunc2
        assert isinstance(res, package.RationalFunction)
        assert res == package.RationalFunction(pol1, package.Polynomial(3))
        res = var1 / package.Rational("4/3")
        assert isinstance(res, package.RationalFunction)
        expected_res = package.Polynomial(package.Rational("3/4") * var1)
        assert res == expected_res

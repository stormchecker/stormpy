from stormpy import pycarl
from configurations import PackageSelector


class TestFactorizedPolynomial(PackageSelector):
    def test_init(self, package):
        pol1 = package.FactorizedPolynomial(32)
        assert pol1 == 32
        assert str(pol1) == "32"

    def test_cache(self, package):
        pycarl.clear_pools()
        x = pycarl.Variable("x")
        p1 = package.create_factorized_polynomial(x * x + package.Integer(3))
        p1.cache()

    def test_coefficient(self, package):
        pycarl.clear_pools()
        var1 = pycarl.Variable("a")
        pol1 = package.create_factorized_polynomial(package.Polynomial(5) * (var1 + package.Integer(1)))
        pol2 = package.create_factorized_polynomial(package.Polynomial(3) * var1)
        res = pol1 * pol2
        assert res.coefficient == 15
        res.coefficient = package.Rational(-3)
        assert res.coefficient == -3

    def test_factorization(self, package):
        pycarl.clear_pools()
        var1 = pycarl.Variable("a")
        var2 = pycarl.Variable("b")
        pol1 = package.create_factorized_polynomial(package.Polynomial(5) * (var1 + package.Integer(1)))
        pol2 = package.create_factorized_polynomial(package.Polynomial(var1) + 1)
        pol3 = package.create_factorized_polynomial(package.Polynomial(3) * var2)
        res = pol1 * pol2 * pol3
        factorization = res.factorization()

        assert res.coefficient == 15
        assert res.constant_part() == 0
        res1 = package.create_factorized_polynomial(package.Polynomial(var1) + 1)
        res2 = package.create_factorized_polynomial(package.Polynomial(var2))
        for factor in factorization:
            assert (factor[0] == res1 and factor[1] == 2) or (factor[0] == res2 and factor[1] == 1)
        assert len(factorization) == 2

    def test_derivation(self, package):
        pycarl.clear_pools()
        x = pycarl.Variable("x")
        c = package.FactorizedPolynomial(3)
        derivation = c.derive(x)
        assert derivation == package.Rational(0)

        p1 = package.create_factorized_polynomial(x * x + package.Integer(3))
        p2 = package.create_factorized_polynomial(x + package.Integer(1))

        pol = p1 * p2
        derivation = pol.derive(x)
        expected = package.create_factorized_polynomial(package.Integer(3) * x * x + package.Integer(2) * x + package.Integer(3))
        assert derivation == expected

        derivation = p1.derive(x)
        p3 = package.Polynomial(package.Integer(2) * x)
        expected = package.create_factorized_polynomial(p3)
        assert derivation == expected

    def test_constant(self, package):
        pycarl.clear_pools()
        var1 = pycarl.Variable("x")
        var2 = pycarl.Variable("y")
        pol = package.create_factorized_polynomial(package.Polynomial(var1 * var1 * var2) + package.Integer(2) * var2 + package.Integer(4))
        assert pol.constant_part() == 4
        pol = package.FactorizedPolynomial(package.Rational(-8 / 3))
        assert pol.is_constant()
        print(type(pol))
        assert pol.constant_part() == package.Rational(-8 / 3)
        pol = package.FactorizedPolynomial(1)
        assert pol.is_constant()
        print(type(pol))
        assert pol.constant_part() == 1

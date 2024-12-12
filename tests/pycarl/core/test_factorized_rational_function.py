from stormpy import pycarl
from configurations import PackageSelector


class TestFactorizedRationalFunction(PackageSelector):
    def test_init(self, package):
        pol1 = package.FactorizedPolynomial(32)
        pol2 = package.FactorizedPolynomial(2)
        rat = package.FactorizedRationalFunction(pol1, pol2)
        assert rat.numerator == 16
        assert rat.denominator == 1

    def test_derivation(self, package):
        x = pycarl.Variable("x")
        p1 = package.create_factorized_polynomial(x * x + package.Integer(3))
        p2 = package.create_factorized_polynomial(x + package.Integer(1))

        rat = package.FactorizedRationalFunction(p1, p2)
        derivation = rat.derive(x)

        pe1 = package.create_factorized_polynomial(package.Integer(2) * x + x * x - 3)
        pe2 = package.create_factorized_polynomial((x + package.Integer(1)) * (x + package.Integer(1)))
        expected = package.FactorizedRationalFunction(pe1, pe2)
        assert derivation == expected

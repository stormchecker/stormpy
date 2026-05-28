from stormpy import pycarl
import math
import fractions
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

    def test_from_fraction(self, package):
        # zero
        assert package.Rational(fractions.Fraction(0)) == package.Rational(0)

        # one and minus one
        assert package.Rational(fractions.Fraction(1)) == package.Rational(1)
        assert package.Rational(fractions.Fraction(-1)) == package.Rational(-1)

        # small positive
        r = package.Rational(fractions.Fraction(1, 2))
        assert package.numerator(r) == 1
        assert package.denominator(r) == 2

        # small negative
        assert package.Rational(fractions.Fraction(-7, 3)) == package.Rational("-7/3")

        # denominator 1 (integer-valued)
        assert package.Rational(fractions.Fraction(42)) == package.Rational(42)

        # fractions.Fraction reduces automatically, verify we preserve the reduced form
        r = package.Rational(fractions.Fraction(6, 4))  # reduces to 3/2
        assert package.numerator(r) == 3
        assert package.denominator(r) == 2

        # fits in 32 bits
        assert package.Rational(fractions.Fraction(2**31 - 1, 2**31)) == package.Rational(str(2**31 - 1) + "/" + str(2**31))

        # fits in 64 bits but not 32
        assert package.Rational(fractions.Fraction(2**63 - 1, 2**63)) == package.Rational(str(2**63 - 1) + "/" + str(2**63))

        # just beyond 64 bits
        n, d = 2**65 + 1, 2**65 + 3
        r = package.Rational(fractions.Fraction(n, d))
        assert package.numerator(r) == package.Integer(str(n))
        assert package.denominator(r) == package.Integer(str(d))

        # large (beyond 128 bits), negative numerator
        n, d = -(10**40 + 7), 10**40 + 9
        r = package.Rational(fractions.Fraction(n, d))
        assert package.numerator(r) == package.Integer(str(n))
        assert package.denominator(r) == package.Integer(str(d))

        # cross-check: round-trip via float for a simple fraction
        assert abs(float(package.Rational(fractions.Fraction(1, 3))) - 1/3) < 1e-15

    def test_comparison_infinity(self, package):
        r4 = package.Rational("1/2")
        assert pycarl.inf > r4
        assert r4 < pycarl.inf
        assert r4 > -pycarl.inf
        assert -pycarl.inf < r4

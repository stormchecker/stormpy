from stormpy import pycarl
from configurations import PackageSelector


class TestTerm(PackageSelector):
    def test_init(self, package):
        pycarl.clear_pools()
        var = pycarl.Variable("x")
        rational = package.Rational(0.25)
        monomial = pycarl.create_monomial(var, 1)
        term = package.Term(rational, monomial)
        assert term.coeff == package.Rational(0.25)
        assert term.monomial == monomial
        assert str(term) == "1/4*x"
        assert term.tdeg == 1

    def test_constant(self, package):
        pycarl.clear_pools()
        rational = package.Rational(0.25)
        term = package.Term(rational)
        assert term.monomial is None
        assert term.is_constant()
        assert term.tdeg == 0

    def test_eq(self, package):
        pycarl.clear_pools()
        var = pycarl.Variable("x")
        term1 = package.Integer(4) * var
        term1 *= var
        term2 = package.Term(2, pycarl.create_monomial(var, 2))
        assert term1 / 2 == term2

    def test_multiplication(self, package):
        pycarl.clear_pools()
        var = pycarl.Variable("x")
        term1 = package.Integer(2) * var * var
        term2 = package.Integer(3) * var

        term3 = term1 * term2
        termOrig = package.Term(6, var * var * var)
        assert term3 == termOrig

    def test_singleton_bug(self, package):
        var = pycarl.Variable("x")
        assert str(package.Term(var)) == "x"
        # Ensures bug is fixed where second call would yield '1' instead of 'x'
        assert str(package.Term(var)) == "x"

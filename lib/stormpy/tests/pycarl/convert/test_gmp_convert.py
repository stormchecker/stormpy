from stormpy import pycarl


class TestGmpConvert:
    def test_convert_int(self):
        original = 43
        assert isinstance(original, int)
        converted = pycarl.convert.convert_to_gmp(original)
        assert isinstance(converted, pycarl.gmp.Integer)

    def test_convert_integer(self):
        original = pycarl.gmp.Integer(23)
        assert isinstance(original, pycarl.gmp.Integer)
        converted = pycarl.convert.convert_to_gmp(original)
        assert isinstance(converted, pycarl.gmp.Integer)

    def test_convert_float(self):
        original = -3.4
        assert isinstance(original, float)
        converted = pycarl.convert.convert_to_gmp(original)
        assert isinstance(converted, pycarl.gmp.Rational)

    def test_convert_rational(self):
        original = pycarl.gmp.Rational(pycarl.gmp.Integer(12), pycarl.gmp.Integer(-4))
        assert isinstance(original, pycarl.gmp.Rational)
        converted = pycarl.convert.convert_to_gmp(original)
        assert isinstance(converted, pycarl.gmp.Rational)

    def test_convert_term(self):
        pycarl.clear_pools()
        var = pycarl.Variable("n")
        rational = pycarl.gmp.Integer(-1) / pycarl.gmp.Integer(6)
        monomial = pycarl.create_monomial(var, 3)
        original = pycarl.gmp.Term(rational, monomial)
        assert isinstance(original, pycarl.gmp.Term)
        converted = pycarl.convert.convert_to_gmp(original)
        assert isinstance(converted, pycarl.gmp.Term)

    def test_convert_polynomial(self):
        pycarl.clear_pools()
        var1 = pycarl.Variable("n")
        var2 = pycarl.Variable("o")
        original = pycarl.gmp.Polynomial(5) * var2 * var1 + var2 * var2 + pycarl.gmp.Integer(3)
        assert isinstance(original, pycarl.gmp.Polynomial)
        converted = pycarl.convert.convert_to_gmp(original)
        assert isinstance(converted, pycarl.gmp.Polynomial)

    def test_convert_rational_function(self):
        pycarl.clear_pools()
        var1 = pycarl.Variable("x")
        var2 = pycarl.Variable("y")
        pol1 = var1 * var2 + pycarl.gmp.Integer(42)
        pol2 = var1 + pycarl.gmp.Integer(-1)
        original = pycarl.gmp.RationalFunction(pol1, pol2)
        assert isinstance(original, pycarl.gmp.RationalFunction)
        converted = pycarl.convert.convert_to_gmp(original)
        assert isinstance(converted, pycarl.gmp.RationalFunction)

    def test_convert_factorized_polynomial(self):
        pycarl.clear_pools()
        var1 = pycarl.Variable("a")
        var2 = pycarl.Variable("b")
        pol1 = pycarl.gmp.create_factorized_polynomial(pycarl.gmp.Polynomial(4) * (var2 + pycarl.gmp.Integer(-2)))
        pol2 = pycarl.gmp.create_factorized_polynomial(pycarl.gmp.Polynomial(var1) - 3)
        pol3 = pycarl.gmp.create_factorized_polynomial(pycarl.gmp.Polynomial(2) * var2)
        original = pol1 * pol2 * pol3
        assert isinstance(original, pycarl.gmp.FactorizedPolynomial)
        converted = pycarl.convert.convert_to_gmp(original)
        assert isinstance(converted, pycarl.gmp.FactorizedPolynomial)
        assert len(converted.factorization()) == len(original.factorization())

    def test_convert_factorized_rational_function(self):
        pycarl.clear_pools()
        var1 = pycarl.Variable("a")
        var2 = pycarl.Variable("b")
        pol1 = pycarl.gmp.create_factorized_polynomial(pycarl.gmp.Polynomial(55) * (var1 + pycarl.gmp.Integer(20)))
        pol2 = pycarl.gmp.create_factorized_polynomial(pycarl.gmp.Polynomial(var2) - 2)
        pol3 = pycarl.gmp.create_factorized_polynomial(pycarl.gmp.Polynomial(562) * var2)
        original = pycarl.gmp.FactorizedRationalFunction(pol1 * pol2, pol2 * pol3)
        assert isinstance(original, pycarl.gmp.FactorizedRationalFunction)
        converted = pycarl.convert.convert_to_gmp(original)
        assert isinstance(converted, pycarl.gmp.FactorizedRationalFunction)
        assert len(converted.numerator.factorization()) == len(original.numerator.factorization())
        assert len(converted.denominator.factorization()) == len(original.denominator.factorization())

    def test_convert_constraint(self):
        pycarl.clear_pools()
        var1 = pycarl.Variable("a")
        pol1 = pycarl.gmp.Polynomial(2) * var1 * var1 + var1 + pycarl.gmp.Integer(4)
        original = pycarl.gmp.formula.Constraint(pol1, pycarl.formula.Relation.GREATER)
        assert isinstance(original, pycarl.gmp.formula.Constraint)
        converted = pycarl.convert.convert_to_gmp(original)
        assert isinstance(converted, pycarl.gmp.formula.Constraint)
        assert converted.relation == original.relation

class TestCore:
    def test_init(self):
        import stormpy

    def test_pycarl(self):
        import stormpy

        rational = stormpy.Rational(0.25)
        assert str(rational) == "1/4"
        pol1 = stormpy.FactorizedPolynomial(32)
        pol2 = stormpy.FactorizedPolynomial(2)
        rat = stormpy.FactorizedRationalFunction(pol1, pol2)
        assert str(rat) == "16"

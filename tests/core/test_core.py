class TestCore:
    def test_init(self):
        import stormpy

    def test_pycarl(self):
        import stormpy

        rational = stormpy.Rational(0.25)
        assert str(rational) == "1/4"
        pol1 = stormpy.Polynomial(32)
        pol2 = stormpy.Polynomial(2)
        rat = stormpy.RationalFunction(pol1, pol2)
        assert str(rat) == "16"

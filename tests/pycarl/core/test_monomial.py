from stormpy import pycarl


class TestCore:
    def test_init(self):
        var = pycarl.Variable("x")
        exp = 1
        monom = pycarl.create_monomial(var, exp)

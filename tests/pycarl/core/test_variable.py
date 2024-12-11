from stormpy import pycarl
import pickle


class TestVariable:
    def test_init(self):
        pycarl.clear_pools()
        var = pycarl.Variable("x")
        assert var.name == "x"
        assert not var.is_no_variable

    def test_eq(self):
        pycarl.clear_pools()
        var1 = pycarl.Variable("x")
        var2 = pycarl.variable_with_name("x")
        assert var1 == var2
        var3 = pycarl.Variable("y")
        assert var1 != var3

    def test_product(self):
        pycarl.clear_pools()
        x = pycarl.Variable("x")
        y = pycarl.Variable("y")
        product = x * y

    def test_pickle(self):
        pycarl.clear_pools()
        var1 = pycarl.Variable("x")
        ser = pickle.dumps(var1)
        var2 = pickle.loads(ser)
        assert var1 == var2
        var3 = pycarl.Variable("y")
        ser = pickle.dumps(var3)
        var4 = pickle.loads(ser)
        assert var3 == var4
        assert var4 != var2

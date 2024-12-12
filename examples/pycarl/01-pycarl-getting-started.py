from stormpy import pycarl
from stormpy.pycarl import gmp


def pycarl_example_getting_started_01():
    pycarl.clear_variable_pool()
    x = pycarl.Variable("x")
    y = pycarl.Variable("y")
    pol1 = x * x + pycarl.gmp.Integer(2)
    pol2 = y + pycarl.gmp.Integer(1)
    result = pol1 * pol2
    print("({}) * ({}) = {}".format(pol1, pol2, result))


if __name__ == "__main__":
    pycarl_example_getting_started_01()

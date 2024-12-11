from stormpy import pycarl
from configurations import PackageSelector, cln


class TestMonomialPool(PackageSelector):
    def test_clear(self, package):
        pycarl.clear_pools()
        var = pycarl.Variable("i")
        pol = package.Polynomial(var)

        pycarl.clear_pools()
        var = pycarl.Variable("i")
        pol = package.Polynomial(var)

        pycarl.clear_pools()
        var = pycarl.Variable("i")
        pol = package.Polynomial(var)


@cln
def test_clear_cln():
    pycarl.clear_pools()
    var = pycarl.Variable("i")
    pol = pycarl.cln.Polynomial(var)

    pycarl.clear_pools()
    var = pycarl.Variable("i")
    pol = pycarl.gmp.Polynomial(var)

    pycarl.clear_pools()
    var = pycarl.Variable("i")
    pol = pycarl.cln.Polynomial(var)

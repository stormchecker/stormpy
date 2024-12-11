from stormpy import pycarl
from stormpy.pycarl.formula import Relation
from configurations import PackageSelector


class TestConstraint(PackageSelector):
    def test_init_bool(self, package):
        constraint = package.formula.Constraint(True)
        assert constraint.relation == Relation.EQ
        assert constraint.lhs == 0

    def test_init_var(self, package):
        pycarl.clear_pools()
        var = pycarl.Variable("x")
        bound = package.Rational(3)
        constraint = package.formula.Constraint(var, Relation.GREATER, bound)
        assert constraint.relation == Relation.LESS

    def test_init_pol(self, package):
        pycarl.clear_pools()
        var = pycarl.Variable("x")
        pol = var * var + package.Integer(2)
        constraint = package.formula.Constraint(pol, Relation.LEQ)
        assert constraint.relation == Relation.LESS

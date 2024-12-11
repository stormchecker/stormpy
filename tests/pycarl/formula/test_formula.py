from stormpy import pycarl
from stormpy.pycarl.formula import Relation, FormulaType

from configurations import PackageSelector


class TestFormula(PackageSelector):
    def test_init_constraint(self, package):
        pycarl.clear_pools()
        x = pycarl.Variable("x")
        constraint = package.formula.Constraint(x, Relation.GREATER, package.Rational(3))
        formula = package.formula.Formula(constraint)

    def test_negation(self, package):
        pycarl.clear_pools()
        x = pycarl.Variable("x")
        constraint = package.formula.Constraint(x, Relation.GREATER, package.Rational(3))
        formula = package.formula.Formula(constraint)
        neg_formula = ~constraint
        assert neg_formula.type == FormulaType.CONSTRAINT
        assert str(~neg_formula) == str(formula)

    def test_conjunction(self, package):
        pycarl.clear_pools()
        x = pycarl.Variable("x")
        y = pycarl.Variable("y")
        constraint1 = package.formula.Constraint(x, Relation.GREATER, package.Rational(3))
        formula1 = package.formula.Formula(constraint1)
        constraint2 = package.formula.Constraint(y, Relation.EQ, package.Rational(2))
        formula2 = package.formula.Formula(constraint2)
        and_formula = formula1 & formula2
        assert and_formula.type == FormulaType.AND
        assert len(and_formula) == 2
        subformulas = and_formula.get_subformulas()
        assert len(subformulas) == 2
        assert str(subformulas[0]) == str(formula1)
        assert str(subformulas[1]) == str(formula2)

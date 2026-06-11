import pytest

from stormpy import pycarl
from configurations import PackageSelector, pycarl_parser


@pycarl_parser
class TestPycarlParse(PackageSelector):
    def test_parse_bool(self, package):
        formula = pycarl.parse.deserialize("true", package)
        assert isinstance(formula, package.formula.Formula)
        assert formula.type is pycarl.formula.FormulaType.TRUE

        formula = pycarl.parse.deserialize("false", package)
        assert isinstance(formula, package.formula.Formula)
        assert formula.type is pycarl.formula.FormulaType.FALSE

        pycarl.clear_pools()
        formula = pycarl.parse.deserialize("(and A B)", package)
        assert isinstance(formula, package.formula.Formula)
        assert formula.type is pycarl.formula.FormulaType.AND
        sub = formula.get_subformulas()
        assert len(sub) == 2

        pycarl.clear_pools()
        formula = pycarl.parse.deserialize("(xor A B)", package)
        assert isinstance(formula, package.formula.Formula)
        assert formula.type is pycarl.formula.FormulaType.XOR
        assert len(formula) == 2

    def test_parse_number(self, package):
        num = pycarl.parse.deserialize("2", package)
        assert isinstance(num, package.Rational)
        assert num == package.Rational(2)

        num = pycarl.parse.deserialize("-2", package)
        assert isinstance(num, package.Rational)
        assert num == package.Rational(-2)

        num = pycarl.parse.deserialize("(- 2.5)", package)
        assert isinstance(num, package.Rational)
        assert num == package.Rational("-2.5")

        num = pycarl.parse.deserialize("3.14", package)
        assert isinstance(num, package.Rational)
        assert num == package.Rational("3.14")

        num = pycarl.parse.deserialize("#xff", package)
        assert isinstance(num, package.Rational)
        assert num == package.Rational(255)

        num = pycarl.parse.deserialize("#b1010", package)
        assert isinstance(num, package.Rational)
        assert num == package.Rational(10)

    def test_parse_real_variable(self, package):
        pycarl.clear_pools()
        var = pycarl.parse.deserialize("x", package)
        assert isinstance(var, pycarl.Variable)
        assert var.name == "x"

    def test_parse_term(self, package):
        pol = pycarl.parse.deserialize("(* 2 x)", package)
        assert isinstance(pol, package.Term)
        x = pycarl.variable_with_name("x")
        assert pol == package.Term(x) * 2

    def test_parse_monomial(self, package):
        pol = pycarl.parse.deserialize("(* x y z)", package)
        assert isinstance(pol, pycarl.Monomial)
        x = pycarl.variable_with_name("x")
        y = pycarl.variable_with_name("y")
        z = pycarl.variable_with_name("z")
        assert pol == x * y * z

    def test_parse_polynomial(self, package):
        pycarl.clear_pools()
        pol = pycarl.parse.deserialize("(+ y 1)", package)
        assert isinstance(pol, package.Polynomial)
        y = pycarl.variable_with_name("y")
        assert pol == y + package.Rational(1)

        pol = pycarl.parse.deserialize("(- x 1)", package)
        assert isinstance(pol, package.Polynomial)
        x = pycarl.variable_with_name("x")
        assert pol == x - package.Rational(1)

        pol = pycarl.parse.deserialize("(+ x y z)", package)
        assert isinstance(pol, package.Polynomial)
        z = pycarl.variable_with_name("z")
        assert pol == package.Term(x) + y + z

        pol = pycarl.parse.deserialize("(- 10 x y)", package)
        assert isinstance(pol, package.Polynomial)
        assert pol == package.Rational(10) - x - y

        pol = pycarl.parse.deserialize("(+ (* 2 x) y)", package)
        assert isinstance(pol, package.Polynomial)
        assert pol == package.Rational(2) * x + y

    def test_parse_rational_function(self, package):
        pycarl.clear_pools()
        rf = pycarl.parse.deserialize("(/ 1 x)", package)
        assert isinstance(rf, package.RationalFunction)
        assert rf.numerator == package.Rational(1)
        x = pycarl.variable_with_name("x")
        assert rf.denominator == package.Polynomial(x)

        rf = pycarl.parse.deserialize("(/ (+ x 1) (+ y 1))", package)
        y = pycarl.variable_with_name("y")
        assert isinstance(rf, package.RationalFunction)
        assert package.numerator(rf) == package.Polynomial(x) + 1
        assert package.denominator(rf) == package.Polynomial(y) + 1

    def test_parse_constraint(self, package):
        pycarl.clear_pools()
        constraint = pycarl.parse.deserialize("(< x 0)", package)
        assert isinstance(constraint, package.formula.Constraint)
        assert str(constraint) == "x<0"
        assert constraint.relation is pycarl.formula.Relation.LESS

        constraint = pycarl.parse.deserialize("(< x 1)", package)
        x = pycarl.variable_with_name("x")
        assert isinstance(constraint, package.formula.Constraint)
        assert constraint.lhs == x - package.Rational(1)
        assert constraint.relation is pycarl.formula.Relation.LESS

        constraint = pycarl.parse.deserialize("(<= (* (- 1) x) 0)", package)
        assert isinstance(constraint, package.formula.Constraint)
        assert constraint.lhs == -package.Polynomial(x)
        assert constraint.relation is pycarl.formula.Relation.LEQ

        constraint = pycarl.parse.deserialize("(= x 0)", package)
        assert isinstance(constraint, package.formula.Constraint)
        assert constraint.relation is pycarl.formula.Relation.EQ
        assert constraint.lhs == package.Polynomial(x)

        constraint = pycarl.parse.deserialize("(!= x 0)", package)
        assert isinstance(constraint, package.formula.Constraint)
        assert constraint.relation is pycarl.formula.Relation.NEQ
        assert constraint.lhs == package.Polynomial(x)

        constraint = pycarl.parse.deserialize("(> x 0)", package)
        assert isinstance(constraint, package.formula.Constraint)
        # Rewritten as -x < 0
        assert constraint.relation is pycarl.formula.Relation.LESS
        assert constraint.lhs == -package.Polynomial(x)

        constraint = pycarl.parse.deserialize("(>= x 0)", package)
        assert isinstance(constraint, package.formula.Constraint)
        # Rewritten as -x <= 0
        assert constraint.relation is pycarl.formula.Relation.LEQ
        assert constraint.lhs == -package.Polynomial(x)

        constraint = pycarl.parse.deserialize("(!= x 3)", package)
        assert isinstance(constraint, package.formula.Constraint)
        assert constraint.relation is pycarl.formula.Relation.NEQ
        assert constraint.lhs == package.Polynomial(x) - 3

    def test_parse_formula(self, package):
        pycarl.clear_pools()
        formula = pycarl.parse.deserialize("(and (< x 0) (> y 0))", package)
        assert isinstance(formula, package.formula.Formula)
        assert formula.type is pycarl.formula.FormulaType.AND
        assert len(formula) == 2

        formula = pycarl.parse.deserialize("(or (< x 0) (> y 0))", package)
        assert isinstance(formula, package.formula.Formula)
        assert formula.type is pycarl.formula.FormulaType.OR
        assert len(formula) == 2

        formula = pycarl.parse.deserialize("(xor (< x 0) (> y 0))", package)
        assert isinstance(formula, package.formula.Formula)
        assert formula.type is pycarl.formula.FormulaType.XOR
        assert len(formula) == 2

        formula = pycarl.parse.deserialize("(=> (< x 0) (> y 0))", package)
        assert isinstance(formula, package.formula.Formula)
        assert formula.type is pycarl.formula.FormulaType.IMPLIES

        formula = pycarl.parse.deserialize("(ite (< x 0) (> y 0) (= z 0))", package)
        assert isinstance(formula, package.formula.Formula)
        assert formula.type is pycarl.formula.FormulaType.ITE
        assert len(formula) == 3

        formula = pycarl.parse.deserialize("(= (< x 0) (> y 0))", package)
        assert isinstance(formula, package.formula.Formula)
        assert formula.type is pycarl.formula.FormulaType.IFF

        formula = pycarl.parse.deserialize("(not (< x 0))", package)
        assert isinstance(formula, package.formula.Formula)
        assert formula.type is pycarl.formula.FormulaType.CONSTRAINT
        # Rewritten as -x <= 0
        constraint = formula.get_constraint()
        assert constraint.relation is pycarl.formula.Relation.LEQ
        x = pycarl.variable_with_name("x")
        assert constraint.lhs == -package.Polynomial(x)

        formula = pycarl.parse.deserialize("(and (< x 0))", package)
        assert isinstance(formula, package.formula.Formula)
        assert formula.type is pycarl.formula.FormulaType.CONSTRAINT
        assert formula.get_constraint().relation is pycarl.formula.Relation.LESS

        formula = pycarl.parse.deserialize("(or (< x 0))", package)
        assert isinstance(formula, package.formula.Formula)
        assert formula.type is pycarl.formula.FormulaType.CONSTRAINT
        assert formula.get_constraint().relation is pycarl.formula.Relation.LESS

    def test_nested_formulas(self, package):
        pycarl.clear_pools()
        formula = pycarl.parse.deserialize("(and (or (< x 0) (> y 0)) (= z 0))", package)
        assert isinstance(formula, package.formula.Formula)
        assert formula.type is pycarl.formula.FormulaType.AND
        assert len(formula) == 2
        sub = formula.get_subformulas()
        assert sub[0].type is pycarl.formula.FormulaType.OR
        assert sub[1].type is pycarl.formula.FormulaType.CONSTRAINT

        formula = pycarl.parse.deserialize("(not (and (< x 0) (> y 0)))", package)
        assert isinstance(formula, package.formula.Formula)
        assert formula.type is pycarl.formula.FormulaType.NOT
        sub = formula.get_negation_subformula()
        assert sub.type is pycarl.formula.FormulaType.AND

        formula = pycarl.parse.deserialize("(=> (< x 0) (> y 0) (= z 0))", package)
        assert isinstance(formula, package.formula.Formula)
        assert formula.type is pycarl.formula.FormulaType.IMPLIES
        premise = formula.get_implication_premise()
        conclusion = formula.get_implication_conclusion()
        assert premise.type is pycarl.formula.FormulaType.IMPLIES
        assert conclusion.type is pycarl.formula.FormulaType.CONSTRAINT

    def test_parse_errors(self, package):
        with pytest.raises(pycarl.parse.ParserError):
            pycarl.parse.deserialize("(< x 0", package)

        with pytest.raises(pycarl.parse.ParserError):
            pycarl.parse.deserialize("garbage input !!!", package)

        with pytest.raises(pycarl.parse.ParserError):
            pycarl.parse.deserialize("(+ x", package)

        with pytest.raises(pycarl.parse.ParserError):
            pycarl.parse.deserialize("((< x 0))", package)

        with pytest.raises(pycarl.parse.ParserError):
            pycarl.parse.deserialize("(ite (< x 0) (> y 0))", package)

        with pytest.raises(pycarl.parse.ParserError):
            pycarl.parse.deserialize("(=> (< x 0))", package)

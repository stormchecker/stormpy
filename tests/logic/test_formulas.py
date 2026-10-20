import pytest
import stormpy
from helpers.helper import get_example_path


class TestFormulas:
    def test_probability_formula(self):
        formula_str = 'P=? [F "one"]'
        prop = stormpy.parse_property(formula_str)
        formula = prop.get_raw_formula()
        assert type(formula) == stormpy.logic.ProbabilityOperatorFormula
        assert str(formula) == formula_str

    def test_reward_formula(self):
        formula_str = 'R=? [F "one"]'
        prop = stormpy.parse_property(formula_str)
        formula = prop.get_raw_formula()
        assert type(formula) == stormpy.logic.RewardOperatorFormula
        assert str(formula) == 'R=? [F "one"]'

    def test_formula_list(self):
        formulas = []
        prop = '=? [F "one"]'
        form = stormpy.parse_property("P" + prop)
        formulas.append(form.get_raw_formula())
        form = stormpy.parse_property("R" + prop)
        formulas.append(form.get_raw_formula())
        assert len(formulas) == 2
        assert str(formulas[0]) == "P" + prop
        assert str(formulas[1]) == "R" + prop

    def test_jani_formula(self):
        _, properties = stormpy.parse_jani_model(get_example_path("dtmc", "die.jani"))
        assert len(properties) == 2
        prop = properties[0]
        assert isinstance(prop, stormpy.logic.Property)
        assert prop.get_name() == "Probability to throw a six"
        prop = properties[1]
        assert isinstance(prop, stormpy.logic.Property)
        assert prop.get_name() == "Expected number of coin flips"

    @pytest.mark.parametrize("operator", ["P", "R"])
    def test_clone_property(self, operator):
        formula = stormpy.parse_property(f'{operator}<=0.5 [F "one"]').get_raw_formula()
        manager = stormpy.expressions.ExpressionManager()
        constant = manager.declare_rational_variable("threshold")
        formula.set_bound(stormpy.logic.ComparisonType.LEQ, constant.get_expression())
        prop = stormpy.logic.Property("named-property", formula, {constant}, "Property comment")

        cloned = prop.clone()
        assert isinstance(cloned, stormpy.logic.Property)
        assert cloned is not prop
        assert cloned.get_name() == prop.get_name()
        assert cloned.get_comment() == prop.get_comment()
        assert cloned.get_undefined_constants() == prop.get_undefined_constants()
        assert str(cloned) == str(prop)

        cloned_formula = cloned.get_raw_formula()
        assert cloned_formula is not formula
        assert cloned_formula.subformula is not formula.subformula
        cloned_formula.remove_bound()
        assert not cloned_formula.has_bound
        assert formula.has_bound
        assert str(formula.threshold_expr) == "threshold"

    def test_bounds(self):
        prop = 'P=? [F "one"]'
        formula = stormpy.parse_property(prop).get_raw_formula()
        assert not formula.has_bound
        prop = 'P<0.4 [F "one"]'
        formula = stormpy.parse_property(prop).get_raw_formula()
        assert formula.has_bound
        assert formula.threshold == stormpy.Rational("0.4")
        assert formula.comparison_type == stormpy.logic.ComparisonType.LESS

    def test_set_bounds(self):
        prop = 'P<0.4 [F "one"]'
        formula = stormpy.parse_property(prop).get_raw_formula()
        expression_manager = stormpy.expressions.ExpressionManager()
        rational = stormpy.Rational("0.2")
        expression = expression_manager.rational(rational)
        formula.set_bound(stormpy.logic.ComparisonType.GEQ, expression)
        assert formula.threshold == stormpy.Rational("0.2")
        assert formula.comparison_type == stormpy.logic.ComparisonType.GEQ
        assert str(formula) == 'P>=1/5 [F "one"]'

    def test_subformula(self):
        prop = 'P=? [F "one"]'
        formula = stormpy.parse_property(prop).get_raw_formula()
        assert type(formula) == stormpy.logic.ProbabilityOperatorFormula
        pathform = formula.subformula
        assert type(pathform) == stormpy.logic.EventuallyFormula
        labelform = pathform.subformula
        assert type(labelform) == stormpy.logic.AtomicLabelFormula
        prop = stormpy.logic.Property("label-formula", labelform, set())
        assert prop.get_raw_formula() == labelform

    def test_game_formula(self):
        formula_str = '<<0>> Pmax=? [F "goal"]'
        prop = stormpy.parse_property(formula_str)
        formula = prop.get_raw_formula()
        assert type(formula) == stormpy.logic.GameFormula
        assert str(formula) == formula_str
        formula = formula.subformula
        assert type(formula) == stormpy.logic.ProbabilityOperatorFormula
        assert str(formula) == 'Pmax=? [F "goal"]'

    def test_discounted_total_reward_formula(self):
        formula_str = 'R{"reward"}max=? [Cdiscount=0.9]'
        prop = stormpy.parse_property(formula_str)
        formula = prop.get_raw_formula()
        assert type(formula) == stormpy.logic.RewardOperatorFormula
        subformula = formula.subformula
        assert type(subformula) == stormpy.logic.DiscountedTotalRewardFormula
        assert subformula.is_discounted_total_reward_formula
        assert subformula.discount_factor_double == pytest.approx(0.9)
        assert subformula.discount_factor_rational == stormpy.Rational("0.9")

    def test_discounted_cumulative_reward_formula(self):
        formula_str = 'R{"reward"}max=? [C<=10 discount=0.9]'
        prop = stormpy.parse_property(formula_str)
        formula = prop.get_raw_formula()
        subformula = formula.subformula
        assert type(subformula) == stormpy.logic.DiscountedCumulativeRewardFormula
        assert subformula.is_discounted_cumulative_reward_formula
        assert subformula.discount_factor_double == pytest.approx(0.9)
        assert subformula.discount_factor_rational == stormpy.Rational("0.9")
        assert not subformula.is_discounted_total_reward_formula

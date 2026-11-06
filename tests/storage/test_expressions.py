import stormpy

import sys


class TestExpressions:
    def test_expression_manager(self):
        manager = stormpy.expressions.ExpressionManager()

    def test_create_variable(self):
        manager = stormpy.expressions.ExpressionManager()
        v1 = manager.declare_boolean_variable("b1")
        assert v1.has_boolean_type()
        v2 = manager.declare_integer_variable("v1")
        assert v2.has_integer_type()
        assert manager.has_variable("b1")
        assert not manager.has_variable("b2")

    def test_boolean_expression(self):
        manager = stormpy.expressions.ExpressionManager()
        expression = manager.boolean(True)
        assert expression.is_literal()
        assert expression.evaluate_as_bool
        assert not expression.contains_variables()
        assert expression.has_boolean_type()
        assert not expression.has_integer_type()
        assert not expression.has_rational_type()

    def test_integer_expression(self):
        manager = stormpy.expressions.ExpressionManager()
        expression = manager.integer(2)
        assert expression.is_literal()
        assert not expression.contains_variables()
        assert not expression.has_boolean_type()
        assert expression.has_integer_type()
        assert not expression.has_rational_type()
        assert expression.evaluate_as_int() == 2

    def test_rational_expression(self):
        manager = stormpy.expressions.ExpressionManager()
        expression = manager.rational(stormpy.Rational(0.2))
        assert expression.is_literal()
        assert not expression.contains_variables()
        assert not expression.has_boolean_type()
        assert not expression.has_integer_type()
        assert expression.has_rational_type()
        assert expression.evaluate_as_double() == 0.2

    def test_expression_parser(self):
        manager = stormpy.expressions.ExpressionManager()
        ep = stormpy.expressions.ExpressionParser(manager)
        ep.set_identifier_mapping(dict())
        ex_true = ep.parse_from_string("true")
        assert str(ex_true) == "true"
        ex_one = ep.parse_from_string("1.0")
        assert str(ex_one) == "1"
        assert ex_one.has_rational_type()

    def test_expression_parser_keeps_manager_alive(self):
        manager = stormpy.expressions.ExpressionManager()
        refs = sys.getrefcount(manager)
        ep = stormpy.expressions.ExpressionParser(manager)
        assert sys.getrefcount(manager) == refs + 1
        del ep
        assert sys.getrefcount(manager) == refs

import stormpy
from helpers.helper import get_example_path
import pytest


class TestValuationTransformer:
    def test_transform_die(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        options = stormpy.BuilderOptions()
        options.set_build_state_valuations()
        options.set_build_choice_labels(True)
        model = stormpy.build_sparse_model_with_options(program, options)
        assert model.has_state_valuations
        vt = stormpy.ValuationTransformer(model.state_valuations)
        manager = program.expression_manager
        vt.add_expression(
            manager.create_boolean_variable("s_exceeds_three"), stormpy.Expression.Geq(manager.get_variable("s").get_expression(), manager.create_integer(4))
        )
        vt.add_expression(
            manager.create_integer_variable("sum"),
            stormpy.Expression.Plus(manager.get_variable("d").get_expression(), manager.get_variable("s").get_expression()),
        )
        new_sv = vt.build(True)
        assert new_sv.get_nr_of_entities() == model.state_valuations.get_nr_of_entities()
        new_model = stormpy.set_state_valuations(model, new_sv)
        assert new_model.nr_states == model.nr_states


class TestValuationsExtendedTypes:
    def test_string_variable(self):
        manager = stormpy.ExpressionManager()
        var_s = manager.create_string_variable(name="s")
        assert var_s.has_string_type()

        builder = stormpy.ValuationDescriptionBuilder(manager)
        builder.add_string_variable(var_s)
        desc = builder.build_class_description()

        vals = stormpy.Valuations(desc, manager, 3)
        vals.write_value(0, var_s, "hello")
        vals.write_value(1, var_s, "world")
        vals.write_value(2, var_s, "")

        assert vals.get_value(0, var_s) == "hello"
        assert vals.get_value(1, var_s) == "world"
        assert vals.get_value(2, var_s) == ""
        assert vals.get_values_states(var_s) == ["hello", "world", ""]

    def test_bigint_value(self):
        manager = stormpy.ExpressionManager()
        var_big = manager.create_integer_variable(name="big")
        assert var_big.has_integer_type()

        # bounds far beyond int64 range, requiring the arbitrary-precision overload
        lower = stormpy.pycarl.gmp.Integer(str(-(10**30)))
        upper = stormpy.pycarl.gmp.Integer(str(10**30))
        builder = stormpy.ValuationDescriptionBuilder(manager)
        builder.add_integer_variable(var_big, lower, upper)
        desc = builder.build_class_description()

        vals = stormpy.Valuations(desc, manager, 2)
        value = stormpy.pycarl.gmp.Integer(str(10**25))
        vals.write_integer_bigint_value(0, var_big, value)

        result = vals.get_integer_bigint_value(0, var_big)
        assert result == value
        assert isinstance(result, stormpy.pycarl.gmp.Integer)

    def test_bigint_value_wrong_variable_type_raises(self):
        manager = stormpy.ExpressionManager()
        var_b = manager.create_boolean_variable(name="b")
        builder = stormpy.ValuationDescriptionBuilder(manager)
        builder.add_boolean_variable(var_b)
        desc = builder.build_class_description()
        vals = stormpy.Valuations(desc, manager, 1)
        vals.write_value(0, var_b, True)

        with pytest.raises(ValueError):
            vals.get_integer_bigint_value(0, var_b)
        with pytest.raises(ValueError):
            vals.write_integer_bigint_value(0, var_b, stormpy.pycarl.gmp.Integer(1))

    def test_double_encoding_of_rational_variable(self):
        # "double" is not a distinct variable type: it is an alternative, approximate 64-bit
        # storage encoding for a rational-typed variable (see storm's own
        # ValuationsTest.cpp, which declares such variables via declareRationalVariable and
        # only chooses addDoubleVariable vs. addRationalVariable on the builder).
        manager = stormpy.ExpressionManager()
        var_r = manager.create_rational_variable(name="r")
        assert var_r.has_rational_type()

        builder = stormpy.ValuationDescriptionBuilder(manager)
        builder.add_double_variable(var_r)
        desc = builder.build_class_description()

        vals = stormpy.Valuations(desc, manager, 2)
        vals.write_double_value(0, var_r, 1.0 / 3.0)
        vals.write_double_value(1, var_r, -2.5)

        assert vals.get_double_value(0, var_r) == pytest.approx(1.0 / 3.0)
        assert vals.get_double_values_states(var_r) == pytest.approx([1.0 / 3.0, -2.5])

    def test_double_encoding_wrong_variable_type_raises(self):
        manager = stormpy.ExpressionManager()
        var_b = manager.create_boolean_variable(name="b")
        builder = stormpy.ValuationDescriptionBuilder(manager)
        builder.add_boolean_variable(var_b)
        desc = builder.build_class_description()
        vals = stormpy.Valuations(desc, manager, 1)
        vals.write_value(0, var_b, True)

        with pytest.raises(ValueError):
            vals.get_double_value(0, var_b)
        with pytest.raises(ValueError):
            vals.write_double_value(0, var_b, 1.0)

    def test_double_encoded_variable_rejects_mismatched_read(self):
        # Regression test: reading a double-encoded rational variable through the normal
        # get_value/getRationalValue path used to crash the whole process with SIGABRT
        # (storm's ValuationsStorage::read() asserted instead of throwing on this type
        # mismatch). It must now raise a catchable exception instead.
        manager = stormpy.ExpressionManager()
        var_r = manager.create_rational_variable(name="r")
        builder = stormpy.ValuationDescriptionBuilder(manager)
        builder.add_double_variable(var_r)
        desc = builder.build_class_description()
        vals = stormpy.Valuations(desc, manager, 1)
        vals.write_double_value(0, var_r, 0.5)

        with pytest.raises(RuntimeError):
            vals.get_value(0, var_r)

    def test_mixed_types_in_one_valuation_class(self):
        manager = stormpy.ExpressionManager()
        var_b = manager.create_boolean_variable(name="b")
        var_i = manager.create_integer_variable(name="i")
        var_r = manager.create_rational_variable(name="r")
        var_s = manager.create_string_variable(name="s")
        var_big = manager.create_integer_variable(name="big")

        builder = stormpy.ValuationDescriptionBuilder(manager)
        builder.add_boolean_variable(var_b)
        builder.add_integer_variable(var_i, 0, 10)
        builder.add_rational_variable(var_r, 64)
        builder.add_string_variable(var_s)
        builder.add_integer_variable(var_big, stormpy.pycarl.gmp.Integer(str(-(10**30))), stormpy.pycarl.gmp.Integer(str(10**30)))
        desc = builder.build_class_description()

        vals = stormpy.Valuations(desc, manager, 1)
        vals.write_value(0, var_b, True)
        vals.write_value(0, var_i, 7)
        vals.write_value(0, var_r, stormpy.Rational("3/4"))
        vals.write_value(0, var_s, "hello")
        vals.write_integer_bigint_value(0, var_big, stormpy.pycarl.gmp.Integer(str(10**25)))

        assert vals.get_value(0, var_b) is True
        assert vals.get_value(0, var_i) == 7
        assert vals.get_value(0, var_r) == stormpy.Rational("3/4")
        assert vals.get_value(0, var_s) == "hello"
        assert vals.get_integer_bigint_value(0, var_big) == stormpy.pycarl.gmp.Integer(str(10**25))
        assert len(vals.get_all_variables()) == 5

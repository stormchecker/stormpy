import stormpy
from helpers.helper import get_example_path
import pytest


class TestStateValuationTransformer:
    def test_transform_die(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        options = stormpy.BuilderOptions()
        options.set_build_state_valuations()
        options.set_build_choice_labels(True)
        model = stormpy.build_sparse_model_with_options(program, options)
        assert model.has_state_valuations
        svt = stormpy.StateValuationTransformer(model.state_valuations)
        manager = program.expression_manager
        svt.add_boolean_expression(
            manager.create_boolean_variable("s_exceeds_three"), stormpy.Expression.Geq(manager.get_variable("s").get_expression(), manager.create_integer(4))
        )
        svt.add_integer_expression(
            manager.create_integer_variable("sum"),
            stormpy.Expression.Plus(manager.get_variable("d").get_expression(), manager.get_variable("s").get_expression()),
        )
        new_sv = svt.build(True)
        assert new_sv.get_nr_of_states() == model.state_valuations.get_nr_of_states()
        new_model = stormpy.set_state_valuations(model, new_sv)
        assert new_model.nr_states == model.nr_states

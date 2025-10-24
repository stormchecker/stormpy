import stormpy
from helpers.helper import get_example_path
import pytest


class TestPrism:

    def test_prism_to_jani_states(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        orig_properties = stormpy.parse_properties_for_prism_program("P=? [F s=7]", program)
        assert len(orig_properties) == 1
        jani_model, new_properties = program.to_jani(orig_properties)
        assert len(new_properties) == len(orig_properties)

    def test_prism_to_jani_labels(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        orig_properties = stormpy.parse_properties_for_prism_program('P=? [F "two"]', program)
        assert len(orig_properties) == 1
        jani_model, new_properties = program.to_jani(orig_properties)
        assert len(new_properties) == len(orig_properties)

    def test_prism_to_jani_repetitive(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        orig_properties = stormpy.parse_properties_for_prism_program('P=? [F "two"]', program)
        jani_model, new_properties = program.to_jani(orig_properties)
        assert len(new_properties) == len(orig_properties)
        orig_properties = stormpy.parse_properties_for_prism_program("P=? [F s=7]", program)
        jani_model, new_properties = program.to_jani(orig_properties, suffix="2")
        assert len(new_properties) == len(orig_properties)

    def test_prism_variables(selfs):
        program = stormpy.parse_prism_program(get_example_path("mdp", "leader3.nm"))
        assert program.nr_modules == 3
        assert program.model_type == stormpy.PrismModelType.MDP
        assert not program.has_undefined_constants
        assert len(program.constants) == 1
        assert len(program.global_boolean_variables) == 0
        assert len(program.global_integer_variables) == 0
        assert len(program.get_variables()) == 16
        assert len(program.variables) == 16
        assert len(program.get_variables(False)) == 15
        for module in program.modules:
            assert len(module.integer_variables) == 5
            assert len(module.boolean_variables) == 0

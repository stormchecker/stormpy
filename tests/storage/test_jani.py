import stormpy
from helpers.helper import get_example_path
import pytest


class TestJani:
    def test_information_collection(self):
        model, properties = stormpy.parse_jani_model(get_example_path("dtmc", "brp.jani"))
        information = stormpy.developer.storage.collect_model_information(model)
        assert information.nr_automata == 5
        assert information.nr_edges == 31
        assert information.nr_variables == 18

    def test_variables(self):
        model, properties = stormpy.parse_jani_model(get_example_path("dtmc", "brp.jani"))
        var_s = model.global_variables.get_variable_by_name("s")
        assert var_s.type.is_bounded_type
        assert var_s.type.lower_bound.evaluate_as_int() == 0
        assert var_s.type.upper_bound.evaluate_as_int() == 6

    def test_flatten_composition(self):
        model, properties = stormpy.parse_jani_model(get_example_path("dtmc", "brp.jani"))
        assert len(model.automata) > 1
        assert len(model.flatten_composition().automata) == 1
        # Flattening declares a new variable in the expression manager, so use a fresh model
        model, properties = stormpy.parse_jani_model(get_example_path("dtmc", "brp.jani"))
        assert len(model.flatten_composition(smt_solver_factory=stormpy.developer.Z3SmtSolverFactory()).automata) == 1

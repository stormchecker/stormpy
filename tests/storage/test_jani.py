import gc
import sys
import typing

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

    def test_location_assignments(self):
        model, properties = stormpy.parse_jani_model(get_example_path("dtmc", "brp.jani"))
        location = model.automata[0].locations[0]
        assert location.assignments is not None
        assert len(list(location.assignments)) >= 0

    def test_flatten_composition(self):
        model, properties = stormpy.parse_jani_model(get_example_path("dtmc", "brp.jani"))
        assert len(model.automata) > 1
        assert len(model.flatten_composition().automata) == 1
        # Flattening declares a new variable in the expression manager, so use a fresh model
        model, properties = stormpy.parse_jani_model(get_example_path("dtmc", "brp.jani"))
        assert len(model.flatten_composition(smt_solver_factory=stormpy.developer.Z3SmtSolverFactory()).automata) == 1

    def test_export_annotations(self):
        hints = typing.get_type_hints(stormpy.io.export_jani_to_file)
        assert stormpy.logic.Property in typing.get_args(typing.get_args(hints["properties"])[0])

    def test_variables_lifetime(self):
        model, properties = stormpy.parse_jani_model(get_example_path("dtmc", "brp.jani"))
        refs = sys.getrefcount(model)
        expander = stormpy.developer.storage.JaniLocationExpander(model)
        assert sys.getrefcount(model) == refs + 1
        del expander
        assert sys.getrefcount(model) == refs
        variables = model.global_variables
        var_s = variables.get_variable_by_name("s")
        del model, properties, variables
        gc.collect()
        assert var_s.type.upper_bound.evaluate_as_int() == 6

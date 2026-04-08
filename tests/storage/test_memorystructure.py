import stormpy
from helpers.helper import get_example_path
import pytest


class TestMemoryStructure:

    def _build_memory_structure(self, model, goalstates):
        builder = stormpy.storage.MemoryStructureBuilder(2, model, False)
        builder.set_transition(0, 0, ~goalstates)
        builder.set_transition(0, 1, goalstates)
        builder.set_transition(1, 1, stormpy.BitVector(model.nr_states, True))
        memorystructure = builder.build()
        return memorystructure

    def test_memory_structure_builder(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        formulas = stormpy.parse_properties_for_prism_program('P=? [ F "one" ]', program)
        model = stormpy.build_model(program, formulas)
        goalstates = model.labeling.get_states("one")
        memorystructure = self._build_memory_structure(model, goalstates)
        assert memorystructure.nr_states == 2

    def test_product_memorystructure(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        formulas = stormpy.parse_properties_for_prism_program('P=? [ F "one"|"two" ]', program)
        model = stormpy.build_model(program, formulas)
        goalstates = model.labeling.get_states("one")
        memorystructure_one = self._build_memory_structure(model, goalstates)
        goalstates = model.labeling.get_states("two")
        memorystructure_two = self._build_memory_structure(model, goalstates)
        product_memorystructure = memorystructure_one.product(memorystructure_two)
        assert product_memorystructure.nr_states == 4

    def test_product_model(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        formulas = stormpy.parse_properties_for_prism_program('P=? [ F "one" ]', program)
        model = stormpy.build_model(program, formulas)
        goalstates = model.labeling.get_states("one")
        memorystructure_one = self._build_memory_structure(model, goalstates)
        product_type = memorystructure_one.product_model(model)
        product_model = product_type.build()
        assert product_model.model_type == stormpy.ModelType.DTMC
        assert product_model.nr_states == 14

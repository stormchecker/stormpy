import os
import math

import stormpy

from helpers.helper import get_example_path
from configurations import gspn, xml


@gspn
class TestGSPNJani:
    def test_simple_pnml(self):
        gspn = stormpy.gspn.load_gspn_file(get_example_path("gspn", "gspn_simple.pnml"))
        assert gspn.get_name() == "simple_gspn"
        assert gspn.get_number_of_places() == 4
        assert gspn.get_number_of_immediate_transitions() == 3
        assert gspn.get_number_of_timed_transitions() == 2

    @xml
    def test_custom_property(self):
        gspn = stormpy.gspn.load_gspn_file(get_example_path("gspn", "philosophers_4.pnpro"))
        assert gspn.get_name() == "Philosophers4"
        assert gspn.get_number_of_timed_transitions() == 12
        assert gspn.get_number_of_immediate_transitions() == 0
        assert gspn.get_number_of_places() == 16

        # Build jani program
        jani_program, _ = stormpy.gspn.build_jani_model(gspn)

        # Set properties
        prop = stormpy.parse_property("P=? [F<=10 eating1=1]", jani_program)

        # Build model
        model = stormpy.build_model(jani_program, prop)

        # Model checking
        initial_state = model.initial_states[0]
        assert initial_state == 0
        result = stormpy.model_checking(model, prop)
        assert math.isclose(result[initial_state], 0.4372171069840004)

    @xml
    def test_standard_properties(self):
        gspn = stormpy.gspn.load_gspn_file(get_example_path("gspn", "philosophers_4.pnpro"))
        assert gspn.get_name() == "Philosophers4"
        assert gspn.get_number_of_timed_transitions() == 12
        assert gspn.get_number_of_immediate_transitions() == 0
        assert gspn.get_number_of_places() == 16

        # Build jani program with standard properties
        jani_program, properties = stormpy.gspn.build_jani_model(gspn, add_deadlock_properties=True)

        # Instantiate constants
        jani_program, properties = stormpy.instantiate_constants(jani_program, "TIME_BOUND=1", properties)

        # Build model
        # Leads to incorrect result
        # model = stormpy.build_model(jani_program, properties)
        model = stormpy.build_model(jani_program)

        # Model checking
        initial_state = model.initial_states[0]
        assert initial_state == 0
        result = stormpy.model_checking(model, properties[0])
        assert math.isclose(result[initial_state], 1.0)
        result = stormpy.model_checking(model, properties[1])
        assert math.isclose(result[initial_state], 0.09123940783)
        result = stormpy.model_checking(model, properties[2])
        assert math.isclose(result[initial_state], 5.445544554455446)

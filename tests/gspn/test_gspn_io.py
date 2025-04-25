import os
import math

import stormpy

from helpers.helper import get_example_path
from configurations import gspn, xml


@gspn
class TestGSPNJani:
    @xml
    def test_custom_property(self):
        gspn_parser = stormpy.gspn.GSPNParser()
        gspn = gspn_parser.parse(get_example_path("gspn", "philosophers_4.pnpro"))
        assert gspn.get_name() == "Philosophers4"
        assert gspn.get_number_of_timed_transitions() == 12
        assert gspn.get_number_of_immediate_transitions() == 0
        assert gspn.get_number_of_places() == 16

        # Build jani program
        jani_builder = stormpy.gspn.GSPNToJaniBuilder(gspn)
        jani_program = jani_builder.build()

        # Set properties
        properties = stormpy.parse_properties_for_jani_model("P=? [F<=10 eating1=1]", jani_program)

        # Build model
        model = stormpy.build_model(jani_program, properties)

        # Model checking
        initial_state = model.initial_states[0]
        assert initial_state == 0
        result = stormpy.model_checking(model, properties[0])
        assert math.isclose(result.at(initial_state), 0.4372171069840004)

    @xml
    def test_standard_properties(self):
        gspn_parser = stormpy.gspn.GSPNParser()
        gspn = gspn_parser.parse(get_example_path("gspn", "philosophers_4.pnpro"))
        assert gspn.get_name() == "Philosophers4"
        assert gspn.get_number_of_timed_transitions() == 12
        assert gspn.get_number_of_immediate_transitions() == 0
        assert gspn.get_number_of_places() == 16

        # Build jani program
        jani_builder = stormpy.gspn.GSPNToJaniBuilder(gspn)
        jani_program = jani_builder.build()

        # Use standard properties
        properties = jani_builder.create_deadlock_properties(jani_program)

        # Instantiate constants
        jani_program, properties = stormpy.preprocess_symbolic_input(jani_program, properties, "TIME_BOUND=1")
        jani_program = jani_program.as_jani_model()

        # Build model
        # Leads to incorrect result
        # model = stormpy.build_model(jani_program, properties)
        model = stormpy.build_model(jani_program)

        # Model checking
        initial_state = model.initial_states[0]
        assert initial_state == 0
        result = stormpy.model_checking(model, properties[0])
        assert math.isclose(result.at(initial_state), 1.0)
        result = stormpy.model_checking(model, properties[1])
        assert math.isclose(result.at(initial_state), 0.09123940783)
        result = stormpy.model_checking(model, properties[2])
        assert math.isclose(result.at(initial_state), 5.445544554455446)

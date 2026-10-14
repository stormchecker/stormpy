import stormpy
from helpers.helper import get_example_path


class TestJson:

    def test_json_container(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        simulator = stormpy.developer.DiscreteTimePrismProgramSimulator(program, stormpy.BuilderOptions())
        simulator.reset_to_initial()
        state = simulator.get_state_as_json()
        assert isinstance(state, stormpy.datastructures.JsonContainer[float])
        assert int(state["s"]) == 0
        assert state == simulator.get_state_as_json()
        assert hash(state) == hash(simulator.get_state_as_json())

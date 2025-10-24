import stormpy
import stormpy.simulator
from helpers.helper import get_example_path


class TestSparseSimulator:
    path = stormpy.examples.files.prism_dtmc_die
    prism_program = stormpy.parse_prism_program(path)

    model = stormpy.build_model(prism_program)
    simulator = stormpy.simulator.create_simulator(model, seed=42)
    final_outcomes = dict()
    for n in range(7):
        while not simulator.is_done():
            observation, reward, labels = simulator.step()
        assert len(labels) == 2
        assert "done" in labels
        if observation not in final_outcomes:
            final_outcomes[observation] = 1
        else:
            final_outcomes[observation] += 1
        simulator.restart()


class TestPrismSimulator:

    def test_negative_values(self):
        prism_program = stormpy.parse_prism_program(get_example_path("dtmc", "negativevals.pm"))
        prism_program = stormpy.preprocess_symbolic_input(prism_program, [], "")[0].as_prism_program()

        simulator = stormpy.simulator.create_simulator(prism_program, seed=42)
        simulator.set_action_mode(stormpy.simulator.SimulatorActionMode.GLOBAL_NAMES)
        state, rew, labels = simulator.restart()
        assert state["s"] == -1
        assert int(state["s"]) == -1

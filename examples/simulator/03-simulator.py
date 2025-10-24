import stormpy
import stormpy.simulator

import stormpy.examples
import stormpy.examples.files

"""
Simulator for programs
"""


def example_simulator_03():
    path = stormpy.examples.files.prism_mdp_firewire
    prism_program = stormpy.parse_prism_program(path)
    prism_program = stormpy.preprocess_symbolic_input(prism_program, [], "delay=10,fast=0.8")[0].as_prism_program()

    simulator = stormpy.simulator.create_simulator(prism_program, seed=42)
    simulator.set_action_mode(stormpy.simulator.SimulatorActionMode.GLOBAL_NAMES)
    final_outcomes = dict()
    for n in range(5):
        while not simulator.is_done():
            actions = simulator.available_actions()
            observation, reward, labels = simulator.step(actions[0])
        if observation not in final_outcomes:
            final_outcomes[observation] = 1
        else:
            final_outcomes[observation] += 1
        simulator.restart()


if __name__ == "__main__":
    example_simulator_03()

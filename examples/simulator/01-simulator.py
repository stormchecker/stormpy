import stormpy
import stormpy.simulator

import stormpy.examples
import stormpy.examples.files

"""
Simulator for deterministic models
"""


def example_simulator_01():
    path = stormpy.examples.files.prism_dtmc_die
    prism_program = stormpy.parse_prism_program(path)

    model = stormpy.build_model(prism_program)
    simulator = stormpy.simulator.create_simulator(model, seed=42)
    final_outcomes = dict()
    for n in range(1000):
        while not simulator.is_done():
            observation, reward, labels = simulator.step()
        print(labels)
        if observation not in final_outcomes:
            final_outcomes[observation] = 1
        else:
            final_outcomes[observation] += 1
        simulator.restart()

    options = stormpy.BuilderOptions([])
    options.set_build_state_valuations()
    options.set_build_all_reward_models()
    model = stormpy.build_sparse_model_with_options(prism_program, options)
    simulator = stormpy.simulator.create_simulator(model, seed=42)
    simulator.set_observation_mode(stormpy.simulator.SimulatorObservationMode.PROGRAM_LEVEL)
    final_outcomes = dict()
    print(simulator.get_reward_names())
    for n in range(1000):
        while not simulator.is_done():
            observation, reward, labels = simulator.step()
        if observation not in final_outcomes:
            final_outcomes[observation] = 1
        else:
            final_outcomes[observation] += 1
        simulator.restart()
    print(", ".join([f"{str(k)}: {v}" for k, v in final_outcomes.items()]))


if __name__ == "__main__":
    example_simulator_01()

import random

import stormpy
import stormpy.simulator

import stormpy.examples
import stormpy.examples.files

"""
Simulator for nondeterministic models
"""


def example_simulator_02():
    path = stormpy.examples.files.prism_mdp_maze
    prism_program = stormpy.parse_prism_program(path)

    model = stormpy.build_model(prism_program)
    simulator = stormpy.simulator.create_simulator(model, seed=42)
    # 5 paths of at most 20 steps.
    paths = []
    for m in range(5):
        path = []
        state, reward, labels = simulator.restart()
        path = [f"{state}"]
        for n in range(20):
            actions = simulator.available_actions()
            select_action = random.randint(0, len(actions) - 1)
            # print(f"Randomly select action nr: {select_action} from actions {actions}")
            path.append(f"--act={actions[select_action]}-->")
            state, reward, labels = simulator.step(actions[select_action])
            # print(state)
            path.append(f"{state}")
            if simulator.is_done():
                # print("Trapped!")
                break
        paths.append(path)
    for path in paths:
        print(" ".join(path))

    options = stormpy.BuilderOptions()
    options.set_build_state_valuations()
    options.set_build_choice_labels(True)
    model = stormpy.build_sparse_model_with_options(prism_program, options)
    print(model)
    simulator = stormpy.simulator.create_simulator(model, seed=42)
    simulator.set_observation_mode(stormpy.simulator.SimulatorObservationMode.PROGRAM_LEVEL)
    simulator.set_action_mode(stormpy.simulator.SimulatorActionMode.GLOBAL_NAMES)
    # 5 paths of at most 20 steps.
    paths = []
    for m in range(5):
        path = []
        state, reward, labels = simulator.restart()
        path = [f"{state}"]
        for n in range(20):
            actions = simulator.available_actions()
            select_action = random.randint(0, len(actions) - 1)
            # print(f"Randomly select action nr: {select_action} from actions {actions}")
            path.append(f"--act={actions[select_action]}-->")
            state, reward, labels = simulator.step(actions[select_action])
            # print(state)
            path.append(f"{state}")
            if simulator.is_done():
                # print("Trapped!")
                break
        paths.append(path)
    for path in paths:
        print(" ".join(path))


if __name__ == "__main__":
    example_simulator_02()

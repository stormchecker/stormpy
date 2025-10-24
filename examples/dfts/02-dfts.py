import stormpy
import stormpy.dft
from stormpy.dft.simulator import DftSimulator

import stormpy.examples
import stormpy.examples.files


def print_status(simulator):
    dft_state, states = simulator.status()
    print(dft_state)
    for element, status in states.items():
        print("\t{} ({}): {}".format(element.name, element.type, status))


def example_dft_simulator_02():
    # Load DFT from Galileo
    path = stormpy.examples.files.dft_galileo_hecs
    dft = stormpy.dft.load_dft_galileo_file(path)
    print("DFT with {} elements, {} BEs and {} dynamic elements.".format(dft.nr_elements(), dft.nr_be(), dft.nr_dynamic()))

    # Create simulator
    simulator = DftSimulator(dft, seed=42)
    print_status(simulator)

    choices = ["n15", "n118", "n134", "n23", "n7"]

    for choice in choices:
        candidates = simulator.next_failures()
        print("Failable BEs: {}".format(", ".join(candidates)))
        print("Let {} fail".format(choice))
        res = simulator.let_fail(choice)
        print("Simulation was {}".format(res))
        print_status(simulator)

    # Analyze DFT via simulation
    timebound = 5
    no_runs = 1000
    print("Perform {} simulation runs for timebound {}".format(no_runs, timebound))
    no_failed = simulator.simulate_traces(timebound, no_runs)
    print("Result for time bound {}: {}".format(timebound, no_failed / no_runs))


if __name__ == "__main__":
    example_dft_simulator_02()

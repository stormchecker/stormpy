import stormpy

import stormpy.examples
import stormpy.examples.files


def example_shortest_paths():
    path = stormpy.examples.files.prism_dtmc_die
    prism_program = stormpy.parse_prism_program(path)
    model = stormpy.build_model(prism_program)

    state_id = 8
    for k in range(1, 4):
        states, probability = stormpy.analysis.shortest_path(model, state_id, k=k)
        print(f"{k}-shortest path to state #{state_id}: {states}, with probability {probability}")


if __name__ == "__main__":
    example_shortest_paths()

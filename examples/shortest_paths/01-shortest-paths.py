import stormpy
from stormpy.utility import ShortestPathsGenerator

import stormpy.examples
import stormpy.examples.files


def example_shortest_paths():
    path = stormpy.examples.files.prism_dtmc_die
    prism_program = stormpy.parse_prism_program(path)
    model = stormpy.build_model(prism_program)

    state_id = 8
    spg = ShortestPathsGenerator(model, state_id)

    # TODO: it's unintuitive to return the paths reversed, change that
    # the reason for being reversed in the first place is that the algorithm traverses them in that order
    print("Note: Paths are traversed in reverse (from target back to the initial state).")

    for k in range(1, 4):
        path = spg.get_path_as_list(k)
        distance = spg.get_distance(k)
        print("{}-shortest path to state #{}: {}, with distance {}".format(k, state_id, path, distance))


if __name__ == "__main__":
    example_shortest_paths()

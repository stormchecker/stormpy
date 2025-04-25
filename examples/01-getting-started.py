import stormpy

import stormpy.examples
import stormpy.examples.files


def example_getting_started_01():
    path = stormpy.examples.files.prism_dtmc_die
    prism_program = stormpy.parse_prism_program(path)

    model = stormpy.build_model(prism_program)
    print("Number of states: {}".format(model.nr_states))
    print("Number of transitions: {}".format(model.nr_transitions))
    print("Labels: {}".format(model.labeling.get_labels()))


if __name__ == "__main__":
    example_getting_started_01()

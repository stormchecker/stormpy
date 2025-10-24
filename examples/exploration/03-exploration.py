import stormpy

import stormpy.examples
import stormpy.examples.files


def example_exploration_03():
    """
    Topological sort

    :return:
    """
    path = stormpy.examples.files.prism_dtmc_die
    prism_program = stormpy.parse_prism_program(path)

    formula_str = "P=? [F s=7 & d=2]"
    properties = stormpy.parse_properties_for_prism_program(formula_str, prism_program)
    model = stormpy.build_model(prism_program, properties)

    sorted = stormpy.topological_sort(model)
    print(sorted)
    sorted = stormpy.topological_sort(model, forward=False)
    print(sorted)


if __name__ == "__main__":
    example_exploration_03()

import stormpy

import stormpy.examples
import stormpy.examples.files


def example_getting_started_02():
    path = stormpy.examples.files.prism_dtmc_die
    prism_program = stormpy.parse_prism_program(path)

    model = stormpy.build_model(prism_program)
    print("Number of states: {}".format(model.nr_states))
    print("Number of transitions: {}".format(model.nr_transitions))
    print("Labels in the model: {}".format(model.labeling.get_labels()))

    formula_str = "P=? [F s=2]"
    prop = stormpy.parse_property(formula_str, prism_program)
    model_for_formula = stormpy.build_model(prism_program, prop)
    print("Number of states: {}".format(model_for_formula.nr_states))
    print("Number of transitions: {}".format(model_for_formula.nr_transitions))
    print("Labels in the model: {}".format(model_for_formula.labeling.get_labels()))

    formula_str_2 = "P=? [F s=7 & d=2]"
    prop_2 = stormpy.parse_property(formula_str_2, prism_program)
    model_for_formula_2 = stormpy.build_model(prism_program, prop_2)
    print("Number of states: {}".format(model_for_formula_2.nr_states))
    print("Number of transitions: {}".format(model_for_formula_2.nr_transitions))
    print("Labels in the model: {}".format(model_for_formula_2.labeling.get_labels()))


if __name__ == "__main__":
    example_getting_started_02()

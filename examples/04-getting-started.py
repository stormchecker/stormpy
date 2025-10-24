import stormpy

import stormpy.examples
import stormpy.examples.files


def example_getting_started_04():
    path = stormpy.examples.files.prism_dtmc_die
    prism_program = stormpy.parse_prism_program(path)

    formula_str = "P=? [F s=7 & d=2]"
    properties = stormpy.parse_properties(formula_str, prism_program)
    model = stormpy.build_model(prism_program, properties)

    print(model.model_type)

    for state in model.states:
        if state.id in model.initial_states:
            print(state)
        for action in state.actions:
            for transition in action.transitions:
                print("From state {}, with probability {}, go to state {}".format(state, transition.value(), transition.column))


if __name__ == "__main__":
    example_getting_started_04()

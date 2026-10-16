import stormpy

import stormpy.examples
import stormpy.examples.files


def example_analysis_04():
    path = stormpy.examples.files.prism_dtmc_die
    prism_program = stormpy.parse_prism_program(path)

    formula_str = "P=? [F s=7 & d=2]"
    prop = stormpy.parse_property(formula_str, prism_program)

    options = stormpy.BuilderOptions(prop)
    options.set_build_state_valuations()
    model = stormpy.build_model(prism_program, options=options)

    result = stormpy.model_checking(model, prop)

    # Print the model checking result for all states

    print("Model checking results:")
    for i in range(len(model.states)):
        print("\tstate #{}\t {}:\t {}".format(i, model.state_valuations.to_string(i), result[i]))


if __name__ == "__main__":
    example_analysis_04()

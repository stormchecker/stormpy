import stormpy

import stormpy.examples
import stormpy.examples.files


def example_analysis_04():
    path = stormpy.examples.files.prism_dtmc_die
    prism_program = stormpy.parse_prism_program(path)

    formula_str = "P=? [F s=7 & d=2]"
    properties = stormpy.parse_properties(formula_str, prism_program)

    options = stormpy.BuilderOptions([p.raw_formula for p in properties])
    options.set_build_state_valuations()
    model = stormpy.build_sparse_model_with_options(prism_program, options)

    result = stormpy.model_checking(model, properties[0])

    # Print the model checking result for all states

    print("Model checking results:")
    for i in range(len(model.states)):
        print("\tstate #{}\t {}:\t {}".format(i, model.state_valuations.get_string(i), result.at(i)))


if __name__ == "__main__":
    example_analysis_04()

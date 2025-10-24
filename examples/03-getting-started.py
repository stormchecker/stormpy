import stormpy

import stormpy.examples
import stormpy.examples.files


def example_getting_started_03():
    path = stormpy.examples.files.prism_dtmc_die
    prism_program = stormpy.parse_prism_program(path)

    formula_str = "P=? [F s=7 & d=2]"
    properties = stormpy.parse_properties(formula_str, prism_program)
    model = stormpy.build_model(prism_program, properties)
    result = stormpy.model_checking(model, properties[0])
    print(result)
    assert result.result_for_all_states
    for x in result.get_values():
        print(x)
    initial_state = model.initial_states[0]
    print(result.at(initial_state))


if __name__ == "__main__":
    example_getting_started_03()

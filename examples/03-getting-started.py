import stormpy

import stormpy.examples
import stormpy.examples.files


def example_getting_started_03():
    path = stormpy.examples.files.prism_dtmc_die
    prism_program = stormpy.parse_prism_program(path)

    formula_str = "P=? [F s=7 & d=2]"
    prop = stormpy.parse_property(formula_str, prism_program)
    model = stormpy.build_model(prism_program, prop)
    result = stormpy.model_checking(model, prop)
    print(result)
    assert result.is_result_for_all_states()
    for state in model.states:
        print(result[state])
    initial_state = model.initial_states[0]
    print(result[initial_state])


if __name__ == "__main__":
    example_getting_started_03()

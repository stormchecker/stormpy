import time

import stormpy
import stormpy.pars

import stormpy.examples
import stormpy.examples.files


def example_parametric_models_03():
    path = stormpy.examples.files.prism_dtmc_brp
    prism_program = stormpy.parse_prism_program(path)

    formula_str = 'P=? [F "target"]'
    properties = stormpy.parse_properties_for_prism_program(formula_str, prism_program)
    model = stormpy.build_parametric_model(prism_program, properties)

    print(model.model_type)
    start = time.time()
    t = 0
    for state in model.states:
        if state.id in model.initial_states:
            print(state)
        for action in state.actions:
            for transition in action.transitions:
                if transition.value().constant_part() == 1:
                    t += 1
                    # print("From state {}, with probability {}, go to state {}".format(state, transition.value(), transition.column))
    print(time.time() - start)
    print(t)

    t2 = 0
    start = time.time()
    for row_group in range(model.nr_states):
        for row in range(model.transition_matrix.get_row_group_start(row_group), model.transition_matrix.get_row_group_end(row_group)):
            for entry in model.transition_matrix.get_row(row):
                if entry.value().constant_part() == 1:
                    t2 += 1
    print(time.time() - start)
    print(t2)

    states_and_transitions = []
    for row_group in range(model.nr_states):
        states_and_transitions.append([])
        for row in range(model.transition_matrix.get_row_group_start(row_group), model.transition_matrix.get_row_group_end(row_group)):
            for entry in model.transition_matrix.get_row(row):
                states_and_transitions[-1].append((entry.value(), entry.column))
    t3 = 0
    start = time.time()
    for s in states_and_transitions:
        for v, c in s:
            if v.constant_part() == 1:
                t3 += 1
    print(time.time() - start)
    print(t3)


if __name__ == "__main__":
    example_parametric_models_03()

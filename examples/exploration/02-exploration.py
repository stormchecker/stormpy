import stormpy

import stormpy.examples
import stormpy.examples.files


def example_exploration_02():
    """
    Example to exploration of POMDPs.
    :return:
    """
    program = stormpy.parse_prism_program(stormpy.examples.files.prism_pomdp_maze)
    prop = 'R=? [F "goal"]'
    properties = stormpy.parse_properties(prop, program)
    model = stormpy.build_model(program, properties)
    print(model.model_type)
    # Internally, POMDPs are just MDPs with additional observation information.
    # Thus, data structure exploration for MDPs can be applied as before.
    initial_state = model.initial_states[0]

    for state in model.states:
        if state.id in model.initial_states:
            print(state)
        for action in state.actions:
            for transition in action.transitions:
                print("From state {} by action {}, with probability {}, go to state {}".format(state, action, transition.value(), transition.column))

    print(model.nr_observations)

    for state in model.states:
        print("State {} has observation id {}".format(state.id, model.observations[state.id]))


if __name__ == "__main__":
    example_exploration_02()

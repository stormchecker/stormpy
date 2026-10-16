import stormpy

import stormpy.examples
import stormpy.examples.files


def example_exploration_01():
    """
    Example to exploration of MDPs.
    :return:
    """
    program = stormpy.parse_prism_program(stormpy.examples.files.prism_pomdp_maze)
    prop = 'R=? [F "goal"]'
    formula = stormpy.parse_property(prop, program)
    model = stormpy.build_model(program, formula)
    print(model.model_type)

    for state in model.states:
        if state.id in model.initial_states:
            print(state)
        for action in state.actions:
            for transition in action.transitions:
                print("From state {} by action {}, with probability {}, go to state {}".format(state, action, transition.value, transition.column))


if __name__ == "__main__":
    example_exploration_01()

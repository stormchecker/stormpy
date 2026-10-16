import stormpy

import stormpy.examples
import stormpy.examples.files


def example_schedulers_01():
    path = stormpy.examples.files.prism_mdp_coin_2_2
    formula_str = 'Pmin=? [F "finished" & "all_coins_equal_1"]'

    program = stormpy.parse_prism_program(path)
    formula = stormpy.parse_property(formula_str, program)

    options = stormpy.BuilderOptions(build_full=True)
    model = stormpy.build_model(program, options=options)

    initial_state = model.initial_states[0]
    assert initial_state == 0
    result = stormpy.model_checking(model, formula, extract_scheduler=True)
    assert result.has_scheduler
    scheduler = result.get_scheduler()
    print(scheduler)
    assert scheduler.memoryless
    assert scheduler.deterministic

    for state in model.states:
        choice = scheduler.get_choice(state)
        action_index = choice.get_deterministic_choice()
        action = state.actions[action_index]
        print("In state {} ({}) choose action {} ({})".format(state, ", ".join(state.labels), action, ", ".join(action.labels)))
        print(state.valuations)

    dtmc = model.apply_scheduler(scheduler)
    print(dtmc)


if __name__ == "__main__":
    example_schedulers_01()

import stormpy

import stormpy.examples
import stormpy.examples.files


def example_schedulers_02():
    path = stormpy.examples.files.prism_ma_simple
    formula_str = "Tmin=? [ F s=4 ]"

    program = stormpy.parse_prism_program(path)
    formula = stormpy.parse_property(formula_str, program)
    options = stormpy.BuilderOptions(formula)
    options.set_build_choice_labels()
    options.set_build_choice_origins()
    ma = stormpy.build_model(program, options=options)
    assert ma.model_type == stormpy.models.ModelType.MA

    # Convert MA to MDP
    mdp, mdp_formulas = stormpy.transformations.transform_to_discrete_time_model(ma, formula)
    assert mdp.model_type == stormpy.models.ModelType.MDP
    initial_state = mdp.initial_states[0]
    assert initial_state == 0

    result = stormpy.model_checking(mdp, mdp_formulas[0], extract_scheduler=True)
    assert result.has_scheduler
    scheduler = result.get_scheduler()
    print(scheduler)
    assert scheduler.memoryless
    assert scheduler.deterministic

    for state in mdp.states:
        choice = scheduler.get_choice(state)
        action_index = choice.get_deterministic_choice()
        action = state.actions[action_index]
        print("In state {} ({}) choose action {} ({})".format(state, ", ".join(state.labels), action, ", ".join(action.labels)))


if __name__ == "__main__":
    example_schedulers_02()

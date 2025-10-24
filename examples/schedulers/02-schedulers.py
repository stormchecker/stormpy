import stormpy

import stormpy.examples
import stormpy.examples.files


def example_schedulers_02():
    path = stormpy.examples.files.prism_ma_simple
    formula_str = "Tmin=? [ F s=4 ]"

    program = stormpy.parse_prism_program(path, False, True)
    formulas = stormpy.parse_properties_for_prism_program(formula_str, program)
    options = stormpy.BuilderOptions([f.raw_formula for f in formulas])
    options.set_build_choice_labels()
    options.set_build_with_choice_origins()
    ma = stormpy.build_sparse_model_with_options(program, options)
    assert ma.model_type == stormpy.ModelType.MA

    # Convert MA to MDP
    mdp, mdp_formulas = stormpy.transform_to_discrete_time_model(ma, formulas)
    assert mdp.model_type == stormpy.ModelType.MDP
    initial_state = mdp.initial_states[0]
    assert initial_state == 0

    result = stormpy.model_checking(mdp, mdp_formulas[0], extract_scheduler=True)
    assert result.has_scheduler
    scheduler = result.scheduler
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

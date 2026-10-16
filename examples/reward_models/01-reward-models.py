import stormpy

import stormpy.examples
import stormpy.examples.files


def example_reward_models_01():
    program = stormpy.parse_prism_program(stormpy.examples.files.prism_dtmc_die)
    prop = 'R=? [F "done"]'
    formula = stormpy.parse_property(prop, program)
    model = stormpy.build_model(program, formula)
    assert len(model.reward_models) == 1
    initial_state = model.initial_states[0]
    result = stormpy.model_checking(model, formula)
    print("Result: {}".format(round(result[initial_state], 6)))

    reward_model_name = list(model.reward_models.keys())[0]
    print(reward_model_name)
    assert reward_model_name == "coin_flips"
    assert not model.reward_models[reward_model_name].has_state_rewards
    assert model.reward_models[reward_model_name].has_state_action_rewards
    for reward in model.reward_models[reward_model_name].state_action_rewards:
        print(reward)
    assert not model.reward_models[reward_model_name].has_transition_rewards

    model = stormpy.build_model_from_drn[stormpy.RationalFunction](stormpy.examples.files.drn_pdtmc_die)
    assert len(model.reward_models) == 1
    assert reward_model_name == "coin_flips"


if __name__ == "__main__":
    example_reward_models_01()

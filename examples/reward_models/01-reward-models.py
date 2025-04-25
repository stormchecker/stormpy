import stormpy

import stormpy.examples
import stormpy.examples.files


def example_reward_models_01():
    program = stormpy.parse_prism_program(stormpy.examples.files.prism_dtmc_die)
    prop = 'R=? [F "done"]'
    properties = stormpy.parse_properties_for_prism_program(prop, program, None)
    model = stormpy.build_model(program, properties)
    assert len(model.reward_models) == 1
    initial_state = model.initial_states[0]
    result = stormpy.model_checking(model, properties[0])
    print("Result: {}".format(round(result.at(initial_state), 6)))

    reward_model_name = list(model.reward_models.keys())[0]
    print(reward_model_name)
    assert reward_model_name == "coin_flips"
    assert not model.reward_models[reward_model_name].has_state_rewards
    assert model.reward_models[reward_model_name].has_state_action_rewards
    for reward in model.reward_models[reward_model_name].state_action_rewards:
        print(reward)
    assert not model.reward_models[reward_model_name].has_transition_rewards

    model = stormpy.build_parametric_model_from_drn(stormpy.examples.files.drn_pdtmc_die)
    assert len(model.reward_models) == 1
    assert reward_model_name == "coin_flips"


if __name__ == "__main__":
    example_reward_models_01()

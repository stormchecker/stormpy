import json

import stormpy

import stormpy.examples
import stormpy.examples.files

"""
Building with a fixed (permissive) policy
"""


def example_building_models_04():
    path = stormpy.examples.files.prism_mdp_firewire
    prism_program = stormpy.parse_prism_program(path)
    prism_program = stormpy.preprocess_symbolic_input(prism_program, [], "delay=10,fast=0.8")[0].as_prism_program()
    options = stormpy.BuilderOptions()
    options.set_build_state_valuations()
    options.set_build_all_reward_models(True)
    options.set_build_choice_labels(True)

    def permissive_policy(state_valuation, action_index):
        """
        Whether for the given state and action, the action should be allowed in the model.

        :param state_valuation:
        :param action_index:
        :return: True or False
        """
        action_name = prism_program.get_action_name(action_index)
        print(f"{state_valuation.to_json()}, {action_name}")
        # conditions on the action
        cond1 = action_name.startswith("snd")
        # conditions on the state (efficient)
        cond2 = state_valuation.get_value(prism_program.get_module("node2").get_integer_variable("x2").expression_variable) < 20
        # conditions on the json repr of the state (inefficient, string handling, etc)
        cond3 = json.loads(str(state_valuation.to_json()))["x1"] < 40
        return cond1 or (cond2 and cond3)

    constructor = stormpy.make_sparse_model_builder(prism_program, options, stormpy.StateValuationFunctionActionMaskDouble(permissive_policy))
    model = constructor.build()
    print(model)


if __name__ == "__main__":
    example_building_models_04()

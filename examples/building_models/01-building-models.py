import stormpy
import stormpy.pomdp

import stormpy.examples
import stormpy.examples.files


def example_building_models_01():
    path = stormpy.examples.files.drn_ctmc_dft
    model = stormpy.build_model_from_drn(path)
    print(model.model_type)
    print("Number of states: {}".format(model.nr_states))

    # And the parametric
    path = stormpy.examples.files.drn_pdtmc_die
    model = stormpy.build_parametric_model_from_drn(path)
    print(model.model_type)
    print("Number of states: {}".format(model.nr_states))

    path = stormpy.examples.files.jani_dtmc_die
    jani_program, properties = stormpy.parse_jani_model(path)
    model = stormpy.build_model(jani_program)
    print(model.model_type)
    print("Number of states: {}".format(model.nr_states))

    # POMDPs should be constructed with choice labels
    path = stormpy.examples.files.drn_pomdp_maze
    opts = stormpy.DirectEncodingParserOptions()
    opts.build_choice_labels = True
    pomdp = stormpy.build_model_from_drn(stormpy.examples.files.drn_pomdp_maze, opts)
    # POMDPs need to be in a canonic representation
    pomdp = stormpy.pomdp.make_canonic(pomdp)


if __name__ == "__main__":
    example_building_models_01()

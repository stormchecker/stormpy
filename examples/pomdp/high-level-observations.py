import stormpy
import stormpy.info
import stormpy.pomdp

import stormpy.examples
import stormpy.examples.files


def example_pomdp_highlevel_observations():
    path = stormpy.examples.files.prism_pomdp_maze
    prism_program = stormpy.parse_prism_program(path)
    formula_str = 'P=? [!"bad" U "goal"]'
    prop = stormpy.parse_property(formula_str, prism_program)
    # construct the POMDP
    options = stormpy.BuilderOptions(prop)
    options.set_build_observation_valuations()
    options.set_build_choice_labels()
    pomdp = stormpy.build_model(prism_program, options=options)
    # make its representation canonic.
    pomdp = stormpy.pomdp.make_canonic(pomdp)

    assert pomdp.has_observation_valuations
    assert pomdp.observation_valuations.to_json(0)["o"] == 5


if __name__ == "__main__":
    example_pomdp_highlevel_observations()

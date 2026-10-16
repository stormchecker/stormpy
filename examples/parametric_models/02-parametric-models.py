import stormpy
import stormpy.info
import stormpy.pars

if stormpy.info.storm_ratfunc_use_cln():
    from stormpy.numbers.developer.cln import formula
else:
    from stormpy.numbers.developer.gmp import formula

import stormpy.examples
import stormpy.examples.files


def example_parametric_models_02():
    path = stormpy.examples.files.prism_pdtmc_die
    prism_program = stormpy.parse_prism_program(path)

    formula_str = "P=? [F s=7 & d=2]"
    prop = stormpy.parse_property(formula_str, prism_program)
    model = stormpy.build_model[stormpy.RationalFunction](prism_program, prop)

    initial_state = model.initial_states[0]
    result = stormpy.model_checking(model, prop)
    print("Result: {}".format(result[initial_state]))

    collector = stormpy.ConstraintCollector(model)
    print("Well formed constraints:")
    for constraint in collector.get_wellformed_constraints():
        print(constraint)
    print("Graph preserving constraints:")
    for constraint in collector.get_graph_preserving_constraints():
        print(constraint)


if __name__ == "__main__":
    example_parametric_models_02()

import stormpy
import stormpy.pars
from stormpy import pycarl

import stormpy.examples
import stormpy.examples.files


def example_parametric_models_04():
    path = stormpy.examples.files.prism_pdtmc_die
    prism_program = stormpy.parse_prism_program(path)

    formula_str = "P=? [F s=7 & d=2]"
    properties = stormpy.parse_properties(formula_str, prism_program)
    model = stormpy.build_parametric_model(prism_program, properties)

    # Modify
    i = 0
    for state in model.states:
        if state.id in model.initial_states:
            print(state)
        for action in state.actions:
            for transition in action.transitions:
                if len(transition.value().gather_variables()) > 0:

                    new_var = pycarl.Variable("p{}".format(i))
                    i += 1
                    new_pol = stormpy.Polynomial(new_var)
                    pol_in_right_format = stormpy.FactorizedPolynomial(new_pol, transition.value().numerator.cache())

                    new_factorized_ratfunc = stormpy.FactorizedRationalFunction(pol_in_right_format)
                    transition.set_value(new_factorized_ratfunc)

    # Display
    for state in model.states:
        if state.id in model.initial_states:
            print(state)
        for action in state.actions:
            for transition in action.transitions:
                print("From state {}, with probability {}, go to state {}".format(state, transition.value(), transition.column))


if __name__ == "__main__":
    example_parametric_models_04()

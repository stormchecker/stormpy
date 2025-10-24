import stormpy
import stormpy.info
import stormpy.pars
from stormpy import pycarl

if stormpy.info.storm_ratfunc_use_cln():
    from stormpy.pycarl import cln as pc
else:
    from stormpy.pycarl import gmp as pc

import stormpy.examples
import stormpy.examples.files


def example_building_models_02():

    def make_factorized_rf(var, cache):
        num = pc.FactorizedPolynomial(pc.Polynomial(var), cache)
        denom = pc.FactorizedPolynomial(pc.Rational(1))
        return pc.FactorizedRationalFunction(num, denom)

        # And the parametric

    path = stormpy.examples.files.drn_pdtmc_die
    model = stormpy.build_parametric_model_from_drn(path)

    parameters = model.collect_probability_parameters()
    bar_parameters = dict()
    for p in parameters:
        # Ensure that variables with that name are not recognized by pycarl.
        assert pycarl.variable_with_name(p.name + "_bar").is_no_variable
        bar_parameters[p] = pycarl.Variable(p.name + "_bar")

    substitutions = dict([[pc.Polynomial(1) - p, bar_parameters[p]] for p in parameters])
    print(substitutions)

    matrix = model.transition_matrix
    for e in matrix:
        val = e.value()
        if val.is_constant():
            continue
        val_pol = val.numerator.polynomial()
        cache = val.numerator.cache()
        for sub, repl in substitutions.items():
            if val_pol - sub == 0:
                print("Found substitution")
                e.set_value(make_factorized_rf(repl, cache))
                break  # Assume only one substitution per entry
    print(matrix)


if __name__ == "__main__":
    example_building_models_02()

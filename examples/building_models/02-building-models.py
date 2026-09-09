import stormpy
import stormpy.info
import stormpy.pars
from stormpy import pycarl

import stormpy.examples
import stormpy.examples.files


def example_building_models_02():
    def make_factorized_rf(var, cache):
        num = stormpy.Polynomial(stormpy.RawPolynomial(var), cache)
        denom = stormpy.Polynomial(stormpy.RationalFunctionCoefficient(1))
        return stormpy.RationalFunction(num, denom)

        # And the parametric

    path = stormpy.examples.files.drn_pdtmc_die
    model = stormpy.build_parametric_model_from_drn(path)

    parameters = model.collect_all_parameters()
    bar_parameters = dict()
    for p in parameters:
        # Ensure that variables with that name are not recognized by pycarl.
        assert pycarl.variable_with_name(p.name + "_bar").is_no_variable
        bar_parameters[p] = pycarl.Variable(p.name + "_bar")

    substitutions = dict([[stormpy.RawPolynomial(1) - p, bar_parameters[p]] for p in parameters])
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

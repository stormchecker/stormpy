import math

import stormpy
import stormpy.pars
import stormpy.examples.files


def example_parameter_synthesis():
    program = stormpy.parse_prism_program(stormpy.examples.files.prism_pdtmc_die)
    property = stormpy.parse_property("P<=0.5 [F s=7 & d=2]", program)
    model = stormpy.build_model[stormpy.RationalFunction](program, property)
    region = stormpy.pars.parse_region("0.2<=p<=0.8,0.2<=q<=0.8", model.collect_all_parameters())

    print("Property holds throughout the region:", stormpy.pars.verify(model, property, region=region))
    instantiator = stormpy.pars.ModelInstantiator(model)
    probability_formula = property.get_raw_formula().clone()
    probability_formula.remove_bound()
    methods = [stormpy.pars.FeasibilityMethod.PLA, stormpy.pars.FeasibilityMethod.GD, stormpy.pars.FeasibilityMethod.SCP]
    for method in methods:
        result = stormpy.pars.check_feasibility(model, property, region=region, method=method)
        print(method.name, "feasibility:", result.status)
        assert result.status == stormpy.pars.RegionResult.EXISTS_SAT
        assert result.witness is not None
        print("Parameter valuation:", result.witness.valuation)
        print("Value at the initial state:", result.witness.value)
        instantiated_model = instantiator.instantiate(result.witness.valuation)
        checked = stormpy.model_checking(instantiated_model, probability_formula, only_initial_states=True)
        probability = checked[instantiated_model.initial_states[0]].value
        print(method.name, "probability on the instantiated model:", probability)
        assert math.isclose(probability, result.witness.value, rel_tol=1e-6)
        assert probability <= 0.5

    lower = stormpy.numbers.RationalFunctionCoefficient("1/5")
    upper = stormpy.numbers.RationalFunctionCoefficient("3/5")
    smaller_region = stormpy.pars.create_region({parameter: (lower, upper) for parameter in model.collect_all_parameters()})
    assert stormpy.pars.verify(model, property, region=smaller_region)

    stronger_property = stormpy.parse_property("P>=0.9 [F s=7 & d=2]", program)
    infeasible = stormpy.pars.check_feasibility(model, stronger_property, region=region, method=stormpy.pars.FeasibilityMethod.PLA)
    print("Feasibility of the stronger property:", infeasible.status)
    assert infeasible.status == stormpy.pars.RegionResult.ALL_VIOLATED
    assert infeasible.witness is None

    # Alternatively, give every parameter the bounds [1/5, 4/5].
    print("Verification with uniform bounds:", stormpy.pars.verify(model, property, region_bound=0.2))


if __name__ == "__main__":
    example_parameter_synthesis()

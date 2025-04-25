import stormpy

from stormpy import pycarl

import stormpy.examples
import stormpy.examples.files

import stormpy._config as config


def example_parametric_models_01():
    # Check support for parameters
    if not config.storm_with_pars:
        print("Support parameters is missing. Try building storm-pars.")
        return

    import stormpy.pars

    path = stormpy.examples.files.prism_pdtmc_die
    prism_program = stormpy.parse_prism_program(path)

    formula_str = "P=? [F s=7 & d=2]"
    properties = stormpy.parse_properties_for_prism_program(formula_str, prism_program)
    model = stormpy.build_parametric_model(prism_program, properties)
    print("Model supports parameters: {}".format(model.supports_parameters))
    parameters = model.collect_probability_parameters()
    assert len(parameters) == 2

    instantiator = stormpy.pars.PDtmcInstantiator(model)
    point = dict()
    for x in parameters:
        print(x.name)
        point[x] = stormpy.RationalRF(0.4)
    instantiated_model = instantiator.instantiate(point)
    result = stormpy.model_checking(instantiated_model, properties[0])
    print(result)


if __name__ == "__main__":
    example_parametric_models_01()

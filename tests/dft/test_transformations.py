import math

import stormpy
from helpers.helper import get_example_path
from configurations import dft


@dft
class TestTransformations:
    def test_instantiate_dft(self):
        stormpy.numbers.clear_pools()
        dft = stormpy.dft.load_dft_galileo_file[stormpy.RationalFunction](get_example_path("dft", "symmetry_param.dft"))
        assert dft.nr_elements() == 7
        assert dft.nr_basic_elements() == 4

        instantiator_type = stormpy.dft.DftInstantiator[stormpy.RationalFunction, float]
        instantiator = stormpy.dft.DftInstantiator(dft)
        assert type(instantiator) is instantiator_type
        assert instantiator_type is stormpy.dft.developer._DftInstantiator_RationalFunction_Double
        x = stormpy.numbers.variable_with_name("x")
        y = stormpy.numbers.variable_with_name("y")
        valuation = {x: stormpy.numbers.RationalFunctionCoefficient("5"), y: stormpy.numbers.RationalFunctionCoefficient("0.01")}
        inst_dft = instantiator.instantiate(valuation)
        assert inst_dft.nr_elements() == 7
        assert inst_dft.nr_basic_elements() == 4
        elem = inst_dft.get_element_by_name("C")
        assert str(elem) == "{C} BE(exp 5, 0.05)"
        elem = inst_dft.get_element_by_name("D")
        assert str(elem) == "{D} BE(exp 0.01, 0)"

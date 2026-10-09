import math

import stormpy
from stormpy import pycarl
from stormpy.tests.helpers.helper import get_example_path
from stormpy.tests.configurations import dft


@dft
class TestTransformations:
    def test_instantiate_dft(self):
        pycarl.clear_pools()
        dft = stormpy.dft.load_parametric_dft_galileo_file(get_example_path("dft", "symmetry_param.dft"))
        assert dft.nr_elements() == 7
        assert dft.nr_basic_elements() == 4

        instantiator_type = stormpy.dft.DftInstantiator[stormpy.RationalFunction, float]
        instantiator = stormpy.dft.DftInstantiator(dft)
        assert type(instantiator) is instantiator_type
        assert instantiator_type is stormpy.dft.developer._DftInstantiator_RationalFunction_Double
        x = pycarl.variable_with_name("x")
        y = pycarl.variable_with_name("y")
        valuation = {x: stormpy.RationalFunctionCoefficient("5"), y: stormpy.RationalFunctionCoefficient("0.01")}
        inst_dft = instantiator.instantiate(valuation)
        assert inst_dft.nr_elements() == 7
        assert inst_dft.nr_basic_elements() == 4
        elem = inst_dft.get_element_by_name("C")
        assert str(elem) == "{C} BE(exp 5, 0.05)"
        elem = inst_dft.get_element_by_name("D")
        assert str(elem) == "{D} BE(exp 0.01, 0)"

import stormpy
from helpers.helper import get_example_path
from stormpy import pycarl

import math
from configurations import dft


@dft
class TestTransformations:

    def test_instantiate_dft(self):
        pycarl.clear_pools()
        dft = stormpy.dft.load_parametric_dft_galileo_file(get_example_path("dft", "symmetry_param.dft"))
        assert dft.nr_elements() == 7
        assert dft.nr_be() == 4

        instantiator = stormpy.dft.DFTInstantiator(dft)
        x = pycarl.variable_with_name("x")
        y = pycarl.variable_with_name("y")
        valuation = {x: stormpy.RationalRF("5"), y: stormpy.RationalRF("0.01")}
        inst_dft = instantiator.instantiate(valuation)
        assert inst_dft.nr_elements() == 7
        assert inst_dft.nr_be() == 4
        elem = inst_dft.get_element_by_name("C")
        assert str(elem) == "{C} BE(exp 5, 0.05)"
        elem = inst_dft.get_element_by_name("D")
        assert str(elem) == "{D} BE(exp 0.01, 0)"

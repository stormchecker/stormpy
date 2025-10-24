import os
import pytest

import stormpy
from helpers.helper import get_example_path

from configurations import dft


@dft
class TestDft:
    def test_parametric_dft(self):
        from stormpy import pycarl

        pycarl.clear_pools()
        dft = stormpy.dft.load_parametric_dft_galileo_file(get_example_path("dft", "symmetry_param.dft"))
        assert dft.nr_elements() == 7
        assert dft.nr_be() == 4
        assert dft.nr_dynamic() == 0
        assert type(dft) is stormpy.dft.DFT_ratfunc
        parameters = stormpy.dft.get_parameters(dft)
        param_names = [x.name for x in parameters]
        assert "x" in param_names
        assert "y" in param_names


@dft
class TestDftElement:
    def test_element(self):
        dft = stormpy.dft.load_dft_json_file(get_example_path("dft", "and.json"))
        tle = dft.top_level_element
        assert dft.nr_elements() == 3
        assert dft.nr_be() == 2
        assert dft.nr_dynamic() == 0
        assert tle.id == 2
        assert tle.name == "A"
        b = dft.get_element(0)
        assert b.id == 0
        assert b.name == "B"
        c = dft.get_element_by_name("C")
        assert c.id == 1
        assert c.name == "C"
        # Invalid name should raise exception
        with pytest.raises(RuntimeError) as exception:
            d = dft.get_element_by_name("D")
        assert "InvalidArgumentException" in str(exception.value)


@dft
class TestDftSymmetries:
    def test_symmetries_none(self):
        symmetries = stormpy.dft.DftSymmetries()
        assert len(symmetries) == 0

    def test_symmetries_small(self):
        dft = stormpy.dft.load_dft_json_file(get_example_path("dft", "and.json"))
        symmetries = dft.symmetries()
        assert len(symmetries) == 1
        for index in symmetries:
            group = symmetries.get_group(index)
            assert len(group) == 1
            for syms in group:
                assert len(syms) == 2
                for elem in syms:
                    assert elem == 0 or elem == 1

    def test_symmetries(self):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "rc.dft"))
        symmetries = dft.symmetries()
        assert len(symmetries) == 1
        for index in symmetries:
            group = symmetries.get_group(index)
            assert len(group) == 3
            i = 4
            for syms in group:
                assert len(syms) == 2
                for elem in syms:
                    assert elem == i or elem == i + 3
                i += 1

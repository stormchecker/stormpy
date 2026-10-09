import math
import os
import pytest

import stormpy
from stormpy.tests.helpers.helper import get_example_path
from stormpy.tests.configurations import dft


@dft
class TestDft:
    def test_generic_dft_type(self):
        dft = stormpy.dft.load_dft_json_file(get_example_path("dft", "and.json"))

        concrete_type = stormpy.dft.DFT[float]
        assert type(dft) is concrete_type
        assert concrete_type is stormpy.dft.developer._DFT_Double

        metadata = stormpy.dft.DFT.metadata
        assert metadata.canonical_name == "stormpy.dft.DFT"
        assert tuple(parameter.name for parameter in metadata.parameters) == ("ValueType",)
        assert metadata.instantiations[0].native_name == "stormpy.dft.developer._dft._DFT_Double"
        assert repr(stormpy.dft.DFT) == "<template class stormpy.dft.DFT>"

        explicit_copy = stormpy.dft.DFT[float](dft)
        inferred_copy = stormpy.dft.DFT(dft)
        keyword_inferred_copy = stormpy.dft.DFT(dft=dft)
        assert type(explicit_copy) is concrete_type
        assert type(inferred_copy) is concrete_type
        assert type(keyword_inferred_copy) is concrete_type

        builder = stormpy.dft.developer.ExplicitDFTModelBuilder(stormpy.dft.DftEnvironment(), dft, stormpy.dft.developer.DftSymmetries())
        assert type(builder) is stormpy.dft.developer.ExplicitDFTModelBuilder[float]

    def test_parametric_dft(self):
        from stormpy import pycarl

        pycarl.clear_pools()
        env = stormpy.dft.DftEnvironment()
        generic_dft = stormpy.dft.load_parametric_dft_json_file(get_example_path("dft", "and.json"))
        assert type(generic_dft) is stormpy.dft.DFT[stormpy.RationalFunction]
        assert stormpy.dft.DFT[stormpy.RationalFunction] is stormpy.dft.developer._DFT_RationalFunction

        builder = stormpy.dft.developer.ExplicitDFTModelBuilder(env, generic_dft, stormpy.dft.developer.DftSymmetries())
        assert type(builder) is stormpy.dft.developer.ExplicitDFTModelBuilder[stormpy.RationalFunction]

        model = stormpy.dft.build_model(env, generic_dft)
        assert model.supports_parameters

        dft = stormpy.dft.load_parametric_dft_galileo_file(get_example_path("dft", "symmetry_param.dft"))
        assert dft.nr_elements() == 7
        assert dft.nr_basic_elements() == 4
        assert dft.nr_dynamic_elements() == 0
        parameters = dft.get_parameters()
        param_names = [x.name for x in parameters]
        assert "x" in param_names
        assert "y" in param_names


@dft
class TestDftElement:
    def test_element(self):
        dft = stormpy.dft.load_dft_json_file(get_example_path("dft", "and.json"))
        tle = dft.top_level_element
        assert dft.nr_elements() == 3
        assert dft.nr_basic_elements() == 2
        assert dft.nr_dynamic_elements() == 0
        assert tle.id == 2
        assert tle.name == "A"
        assert tle.type == stormpy.dft.DFTElementType.AND
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

    def test_element_type_spare(self):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "hecs.dft"))
        spare = dft.get_element_by_name("n137")
        assert spare.type == stormpy.dft.DFTElementType.SPARE


@dft
class TestDftSymmetries:
    def test_symmetries_none(self):
        symmetries = stormpy.dft.developer.DftSymmetries()
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

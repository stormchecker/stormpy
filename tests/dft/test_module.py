import os

import stormpy
from helpers.helper import get_example_path
from configurations import dft


@dft
class TestModule:
    def test_module(self):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "hecs.dft"))
        assert dft.nr_elements() == 23
        assert dft.nr_basic_elements() == 13
        assert dft.nr_dynamic_elements() == 2
        module = stormpy.dft.modules(dft)
        assert module.representative.name == "n0"
        assert len(module.elements) == 1
        assert len(module.submodules) == 4
        for submodule in module.submodules:
            assert submodule.representative.name in ["n116", "n137", "n120", "n21"]
            assert len(submodule.elements) in [1, 7]
            assert len(submodule.submodules) in [0, 2, 3, 7]

    def test_module_json(self):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "hecs.dft"))
        json = stormpy.dft.modules_json(dft)
        assert json["representative"]["name"] == "n0"
        assert len(json["elements"]) == 1
        assert len(json["submodules"]) == 4
        for submodule in json["submodules"]:
            assert submodule["representative"]["name"] in ["n116", "n137", "n120", "n21"]
            assert len(submodule["elements"]) in [1, 7]
            assert len(submodule["submodules"]) in [0, 2, 3, 7]

    def test_subtree(self):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "hecs.dft"))
        module = stormpy.dft.modules(dft)
        assert module.is_static
        assert not module.is_fully_static
        assert not module.is_single_be

        trivial = next(submodule for submodule in module.submodules if submodule.representative.name == "n116")
        assert trivial.is_static
        assert trivial.is_fully_static
        assert trivial.is_single_be
        subtree = trivial.subtree()
        assert subtree.nr_elements() == 1
        assert subtree.top_level_element.name == "n116"

    def test_module_recursive_consistency(self):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "hecs.dft"))
        module = stormpy.dft.modules(dft)
        json = stormpy.dft.modules_json(dft)

        def assert_consistent(module, json):
            assert module.representative.name == json["representative"]["name"]
            assert len(module.elements) == len(json["elements"])
            assert len(module.submodules) == len(json["submodules"])
            submodules_by_name = {submodule.representative.name: submodule for submodule in module.submodules}
            json_by_name = {subjson["representative"]["name"]: subjson for subjson in json["submodules"]}
            assert set(submodules_by_name) == set(json_by_name)
            for name, submodule in submodules_by_name.items():
                assert_consistent(submodule, json_by_name[name])

        assert_consistent(module, json)
        assert any(len(submodule.submodules) > 0 for submodule in module.submodules)

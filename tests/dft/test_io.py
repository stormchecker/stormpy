import os

import stormpy
from helpers.helper import get_example_path
from configurations import dft


@dft
class TestDftLoad:
    def test_load_dft_galileo_file(self):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "hecs.dft"))
        assert dft.nr_elements() == 23
        assert dft.nr_basic_elements() == 13
        assert dft.nr_dynamic_elements() == 2
        assert not dft.can_have_nondeterminism()

    def test_load_dft_json_file(self):
        dft = stormpy.dft.load_dft_json_file(get_example_path("dft", "and.json"))
        assert dft.nr_elements() == 3
        assert dft.nr_basic_elements() == 2
        assert dft.nr_dynamic_elements() == 0
        assert not dft.can_have_nondeterminism()

    def test_load_dft_json_string(self):
        # Build json string
        json_node_a = '{"data": {"id":"0", "name":"A", "type":"be", "rate":"1", "dorm":"1", "label":"A (1)"}, "group":"nodes", "classes":"be"}'
        json_node_b = '{"data": {"id":"1", "name":"B", "type":"be", "rate":"1", "dorm":"1", "label":"B (1)"}, "group":"nodes", "classes":"be"}'
        json_node_c = '{"data": {"id":"6", "name":"Z", "type":"pand", "children":["0", "1"], "label":"Z"}, "group":"nodes", "classes":"pand"}'
        json_string = '{"toplevel": "6", "parameters": {}, "nodes": [' + json_node_a + "," + json_node_b + "," + json_node_c + "]}"
        # Load
        dft = stormpy.dft.load_dft_json_string(json_string)
        assert dft.nr_elements() == 3
        assert dft.nr_basic_elements() == 2
        assert dft.nr_dynamic_elements() == 1
        assert not dft.can_have_nondeterminism()

    def test_load_parametric_dft_json_string(self):
        json_node_a = '{"data": {"id":"0", "name":"A", "type":"be", "rate":"x", "dorm":"1", "label":"A (x)"}, "group":"nodes", "classes":"be"}'
        json_node_b = '{"data": {"id":"1", "name":"B", "type":"be", "rate":"1", "dorm":"1", "label":"B (1)"}, "group":"nodes", "classes":"be"}'
        json_node_c = '{"data": {"id":"6", "name":"Z", "type":"and", "children":["0", "1"], "label":"Z"}, "group":"nodes", "classes":"and"}'
        json_string = '{"toplevel": "6", "parameters": ["x"], "nodes": [' + json_node_a + "," + json_node_b + "," + json_node_c + "]}"
        # Load
        dft = stormpy.dft.load_parametric_dft_json_string(json_string)
        assert type(dft) is stormpy.dft.DFT[stormpy.RationalFunction]
        assert dft.nr_elements() == 3
        assert dft.nr_basic_elements() == 2
        assert dft.nr_dynamic_elements() == 0
        assert not dft.can_have_nondeterminism()
        parameter_names = {parameter.name for parameter in dft.get_parameters()}
        assert parameter_names == {"x"}


@dft
class TestDftExport:
    def test_export_dft_json_string(self):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "hecs.dft"))
        assert dft.nr_elements() == 23
        assert dft.nr_basic_elements() == 13
        assert dft.nr_dynamic_elements() == 2
        json_string = stormpy.dft.export_dft_json_string(dft)
        dft2 = stormpy.dft.load_dft_json_string(json_string)
        assert dft2.nr_elements() == 23
        assert dft2.nr_basic_elements() == 13
        assert dft2.nr_dynamic_elements() == 2

    def test_export_dft_json_file(self, tmpdir):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "hecs.dft"))
        assert dft.nr_elements() == 23
        assert dft.nr_basic_elements() == 13
        assert dft.nr_dynamic_elements() == 2
        export_file = os.path.join(str(tmpdir), "hecs.json")
        stormpy.dft.export_dft_json_file(dft, export_file)
        dft2 = stormpy.dft.load_dft_json_file(export_file)
        assert dft2.nr_elements() == 23
        assert dft2.nr_basic_elements() == 13
        assert dft2.nr_dynamic_elements() == 2

    def test_export_parametric_dft_json_string(self):
        dft = stormpy.dft.load_parametric_dft_galileo_file(get_example_path("dft", "symmetry_param.dft"))
        parameter_names = {parameter.name for parameter in dft.get_parameters()}
        assert parameter_names == {"x", "y"}

        json_string = stormpy.dft.export_dft_json_string(dft)
        dft2 = stormpy.dft.load_parametric_dft_json_string(json_string)

        assert type(dft2) is stormpy.dft.DFT[stormpy.RationalFunction]
        assert dft2.nr_elements() == dft.nr_elements()
        assert dft2.nr_basic_elements() == dft.nr_basic_elements()
        assert dft2.nr_dynamic_elements() == dft.nr_dynamic_elements()
        assert {parameter.name for parameter in dft2.get_parameters()} == parameter_names

    def test_export_parametric_dft_json_file(self, tmpdir):
        dft = stormpy.dft.load_parametric_dft_galileo_file(get_example_path("dft", "symmetry_param.dft"))
        parameter_names = {parameter.name for parameter in dft.get_parameters()}
        assert parameter_names == {"x", "y"}

        export_file = os.path.join(str(tmpdir), "symmetry_param.json")
        stormpy.dft.export_dft_json_file(dft, export_file)
        dft2 = stormpy.dft.load_parametric_dft_json_file(export_file)

        assert type(dft2) is stormpy.dft.DFT[stormpy.RationalFunction]
        assert dft2.nr_elements() == dft.nr_elements()
        assert dft2.nr_basic_elements() == dft.nr_basic_elements()
        assert dft2.nr_dynamic_elements() == dft.nr_dynamic_elements()
        assert {parameter.name for parameter in dft2.get_parameters()} == parameter_names

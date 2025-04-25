import os

import stormpy
from helpers.helper import get_example_path

from configurations import dft


@dft
class TestDftLoad:
    def test_load_dft_galileo_file(self):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "hecs.dft"))
        assert dft.nr_elements() == 23
        assert dft.nr_be() == 13
        assert dft.nr_dynamic() == 2
        assert not dft.can_have_nondeterminism()

    def test_load_dft_json_file(self):
        dft = stormpy.dft.load_dft_json_file(get_example_path("dft", "and.json"))
        assert dft.nr_elements() == 3
        assert dft.nr_be() == 2
        assert dft.nr_dynamic() == 0
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
        assert dft.nr_be() == 2
        assert dft.nr_dynamic() == 1
        assert not dft.can_have_nondeterminism()


@dft
class TestDftExport:
    def test_export_dft_json_string(self):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "hecs.dft"))
        assert dft.nr_elements() == 23
        assert dft.nr_be() == 13
        assert dft.nr_dynamic() == 2
        json_string = stormpy.dft.export_dft_json_string(dft)
        dft2 = stormpy.dft.load_dft_json_string(json_string)
        assert dft2.nr_elements() == 23
        assert dft2.nr_be() == 13
        assert dft2.nr_dynamic() == 2

    def test_export_dft_json_file(self, tmpdir):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "hecs.dft"))
        assert dft.nr_elements() == 23
        assert dft.nr_be() == 13
        assert dft.nr_dynamic() == 2
        export_file = os.path.join(str(tmpdir), "hecs.json")
        stormpy.dft.export_dft_json_file(dft, export_file)
        dft2 = stormpy.dft.load_dft_json_file(export_file)
        assert dft2.nr_elements() == 23
        assert dft2.nr_be() == 13
        assert dft2.nr_dynamic() == 2

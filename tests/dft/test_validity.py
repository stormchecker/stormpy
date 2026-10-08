import pytest

import stormpy
from helpers.helper import get_example_path
from configurations import dft


@dft
class TestCheckDftValidity:
    def test_check_dft_valid(self):
        dft = stormpy.dft.load_dft_json_file(get_example_path("dft", "and.json"))
        assert stormpy.dft.check_dft_validity(dft)

    def test_check_dft_invalid(self):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "rc2.dft"))
        with pytest.raises(stormpy.exceptions.StormError):
            stormpy.dft.check_dft_validity(dft)

    def test_check_dft_validity_warns(self):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "rc2.dft"))
        dft = stormpy.dft.prepare_for_analysis(dft)
        with pytest.warns(stormpy.dft.StormWarning):
            valid = stormpy.dft.check_dft_validity(dft)
        assert valid is False

    def test_analyze_dft_invalid_raises(self):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "rc2.dft"))
        formulas = stormpy.parse_properties('T=? [ F "failed" ]')
        with pytest.raises(stormpy.exceptions.StormError):
            stormpy.dft.analyze_dft(stormpy.dft.DftEnvironment(), dft, formulas)

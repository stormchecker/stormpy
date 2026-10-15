"""Pars-specific tests for the public parametric API (stormpy.pars).

Generic checks of all public APIs (names exist, documentation) are in tests/test_public_apis.py.
"""

import stormpy
from configurations import pars


@pars
class TestPublicParsApi:
    def test_internal_imports_not_public(self):
        import stormpy.pars

        for name in ["Environment", "Formula", "Property", "RationalFunction", "SparseModel", "StormError", "Variable"]:
            assert name not in stormpy.pars.__all__

    def test_removed_names(self):
        import stormpy.pars

        for name in ["ModelInstantiationChecker", "DtmcParameterLiftingModelChecker", "MdpParameterLiftingModelChecker"]:
            assert not hasattr(stormpy.pars, name)
            assert not hasattr(stormpy.pars.developer, name)
        for name in ["_SparseParametricDtmcSimplifier", "_SparseParametricMdpSimplifier", "create_region_checker", "create_region_refinement_checker"]:
            assert not hasattr(stormpy.pars.developer, name)
        assert not hasattr(stormpy.pars.ParameterRegion, "create_from_string")
        for name in ["check_region", "get_bound", "get_split_suggestion"]:
            assert not hasattr(stormpy.pars.RegionModelChecker, name)
        assert not hasattr(stormpy.pars.RegionRefinementChecker, "compute_extremum")

    def test_developer_bindings(self):
        import stormpy.pars

        for name in [
            "SparseDtmcParameterLiftingModelChecker",
            "SparseMdpParameterLiftingModelChecker",
            "SparseParametricModelSimplifier",
            "initialize_region_model_checker",
            "initialize_region_refinement_checker",
            "parse_region",
            "GraphPreservationStatus",
            "RegionCheckEngine",
            "RegionSplitEstimateKind",
        ]:
            assert hasattr(stormpy.pars.developer, name)
        assert stormpy.pars.ParameterRegion is stormpy.pars.developer.ParameterRegion
        assert (
            stormpy.pars.ModelInstantiator[stormpy.models.ModelType.DTMC, float]
            is stormpy.pars.developer.ModelInstantiator[stormpy.models.ModelType.DTMC, float]
        )

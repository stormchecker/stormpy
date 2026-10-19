"""POMDP-specific tests for the public POMDP API (stormpy.pomdp).

Generic checks of all public APIs (names exist, documentation) are in tests/test_public_apis.py.
"""

import stormpy
from configurations import pomdp


@pomdp
class TestPublicPomdpApi:
    def test_internal_imports_not_public(self):
        import stormpy.pomdp

        for name in ["Environment", "ExpressionManager", "Formula", "Property", "SparseDtmc", "SparseMdp", "SparseModel", "SparsePomdp"]:
            assert name not in stormpy.pomdp.__all__

    def test_removed_names(self):
        import stormpy.pomdp

        for name in [
            "create_nondeterminstic_belief_tracker",
            "BeliefSupportTrackerDouble",
            "NondeterministicBeliefTrackerDoubleSparse",
            "NondeterministicBeliefTrackerDoubleSparseOptions",
            "ObservationTraceUnfolderDouble",
            "GenerateMonitorVerifierDouble",
            "GenerateMonitorVerifierDoubleOptions",
            "IterativeQualitativeSearchSolverDouble",
            "IterativeQualitativeSearchOptions",
            "BeliefSupportWinningRegion",
            "BeliefSupportWinningRegionQueryInterfaceDouble",
            "create_iterative_qualitative_search_solver_Double",
            "prepare_pomdp_for_qualitative_search_Double",
            "_make_canonic_Double",
            "_unfold_memory_Double",
            "_make_simple_Double",
            "_apply_unknown_fsc_Rf",
            "BeliefExplorationModelCheckerDouble",
            "BeliefExplorationModelCheckerOptionsDouble",
        ]:
            assert not hasattr(stormpy.pomdp, name)
            assert not hasattr(stormpy.pomdp.developer, name)

    def test_developer_bindings(self):
        import stormpy.pomdp

        for name in [
            "MakePOMDPCanonic",
            "PomdpMemoryUnfolder",
            "PomdpMemoryBuilder",
            "BinaryPomdpTransformer",
            "PomdpTransformationResult",
            "ApplyFiniteSchedulerToPomdp",
            "ObservationTraceUnfolderOptions",
            "NondeterministicBeliefTrackerOptions",
            "MemlessSearchOptions",
            "GenerateMonitorVerifier",
            "GenerateMonitorVerifierOptions",
            "create_iterative_policy_search",
            "prepare_pomdp_for_qualitative_search",
            "BeliefBasedModelCheckerOptions",
            "verify_with_belief_unfolding",
            "verify_with_belief_discretization",
        ]:
            assert hasattr(stormpy.pomdp.developer, name)
        assert stormpy.pomdp.PomdpMemory is stormpy.pomdp.developer.PomdpMemory
        assert stormpy.pomdp.BeliefSupportTracker[float] is stormpy.pomdp.developer.BeliefSupportTracker[float]
        assert stormpy.pomdp.BeliefBasedModelCheckerResult[float] is stormpy.pomdp.developer.BeliefBasedModelCheckerResult[float]
        assert set(stormpy.pomdp.developer.BeliefBasedModelCheckerOptions.instantiations) == {(float,), (stormpy.Rational,)}
        assert set(stormpy.pomdp.developer.MakePOMDPCanonic.instantiations) == {(float,), (stormpy.Rational,), (stormpy.RationalFunction,)}

"""Core-specific tests for the public API (stormpy) and the developer bindings (stormpy.developer).

Generic checks of all public APIs (names exist, documentation) are in tests/test_public_apis.py.
"""

import pytest
import stormpy
import stormpy.developer
from helpers.helper import get_example_path


class TestPublicApi:
    def test_templates_published(self):
        assert stormpy.ExplicitQuantitativeCheckResult.canonical_name == "stormpy.ExplicitQuantitativeCheckResult"
        assert stormpy.ExplicitQuantitativeCheckResult[float] is stormpy.developer.ExplicitQuantitativeCheckResult[float]

    @pytest.mark.parametrize(
        "name",
        [
            "_core",
            "CheckTask",
            "FlatSet",
            "build_sparse_model",
            "build_parametric_model",
            "build_sparse_model_with_options",
            "check_model_sparse",
            "check_model_dd",
            "check_model_hybrid",
            "check_interval_dtmc",
            "construct_submodel",
            "eliminate_ECs",
            "perform_symbolic_bisimulation",
            "preprocess_symbolic_input",
            "prob01min_states",
            "make_weighted_objective_mdp_model_checker",
            "eliminate_end_components",
            "pycarl",
            "EndComponentEliminatorReturnType",
            "parse_properties_for_prism_program",
            "SparseMatrixBuilder",
            "EventuallyFormula",
            # Moved to stormpy.logic
            "Property",
            "OptimizationDirection",
        ],
    )
    def test_removed_names(self, name):
        assert not hasattr(stormpy, name)


class TestDeveloperBindings:
    @pytest.mark.parametrize(
        "name",
        [
            # storm-parsers/api
            "parse_program",
            "parse_jani_model",
            "parse_jani_model_from_string",
            "parse_properties",
            "parse_properties_for_prism_program",
            "parse_properties_for_jani_model",
            "parse_properties_for_symbolic_model_description",
            "build_explicit_drn_model",
            "build_explicit_model",
            # storm/api
            "build_sparse_model",
            "build_symbolic_model",
            "make_explicit_model_builder",
            "perform_bisimulation_minimization",
            "export_sparse_model_as_drn",
            "transform_symbolic_to_sparse_model",
            "transform_continuous_to_discrete_time_sparse_model",
            "eliminate_non_markovian_chains",
            "verify_with_sparse_engine",
            "verify_with_dd_engine",
            "verify_with_hybrid_engine",
            "substitute_constants_in_properties",
            # storm/utility
            "perform_prob01",
            "perform_prob01_min",
            "perform_prob01_max",
            "get_reachable_states",
            "set_log_level",
            "set_timeout_alarm",
            "reset_timeout_alarm",
            # storm/transformer
            "build_subsystem",
            "EndComponentEliminator",
            "AddUncertainty",
            # storm/modelchecker
            "CheckTask",
            "PcaaWeightVectorChecker",
            "perform_multi_objective_model_checking",
            "compute_all_transient_probabilities",
            # storm-counterexamples
            "SMTMinimalLabelSetGenerator",
            "FlatSet",
        ],
    )
    def test_storm_names(self, name):
        assert hasattr(stormpy.developer, name)

    def test_public_classes_are_developer_classes(self):
        assert stormpy.logic.Property is stormpy.developer.Property
        assert stormpy.Environment is stormpy.developer.Environment
        assert issubclass(stormpy.BuilderOptions, stormpy.developer.BuilderOptions)

    @pytest.mark.parametrize(
        "name",
        [
            # Value types are selected via template function families
            "build_sparse_exact_model",
            "build_sparse_parametric_model",
            "build_sparse_interval_model",
            "build_sparse_exact_interval_model",
            "build_symbolic_exact_model",
            "build_symbolic_parametric_model",
            "make_explicit_exact_model_builder",
            "build_explicit_exact_drn_model",
            "build_explicit_parametric_drn_model",
            "as_explicit_quantitative_check_result",
        ],
    )
    def test_removed_names(self, name):
        assert not hasattr(stormpy.developer, name)
        assert not hasattr(stormpy.developer.CheckResult, name)

    def test_template_functions(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        formulas = [prop.get_raw_formula() for prop in stormpy.parse_properties('P=? [F "one"]', program)]
        assert "template function" in repr(stormpy.developer.build_sparse_model)
        model = stormpy.developer.build_sparse_model(program, formulas)
        assert type(model) is stormpy.models.SparseDtmc[float]
        exact_model = stormpy.developer.build_sparse_model[stormpy.Rational](program, formulas)
        assert type(exact_model) is stormpy.models.SparseDtmc[stormpy.Rational]
        assert (stormpy.Interval,) in stormpy.developer.build_sparse_model.instantiations
        with pytest.raises(TypeError):
            stormpy.developer.build_symbolic_model[stormpy.Interval](program, formulas)
        drn_model = stormpy.developer.build_explicit_drn_model[stormpy.Rational](get_example_path("ctmc", "dft.drn"))
        assert type(drn_model) is stormpy.models.SparseCtmc[stormpy.Rational]

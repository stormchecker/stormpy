import math
import pytest

import stormpy
from helpers.helper import get_example_path
from configurations import dft


@dft
class TestAnalysis:
    def test_analyze_and_mttf(self):
        dft = stormpy.dft.load_dft_json_file(get_example_path("dft", "and.json"))
        formula = stormpy.parse_property('T=? [ F "failed" ]')
        assert dft.nr_elements() == 3
        results = stormpy.dft.analyze_dft(dft, formula)
        assert math.isclose(results[0], 3)

    def test_analyze_hecs_mttf(self):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "hecs.dft"))
        formula_str = 'T=? [ F "failed" ]'
        formula = stormpy.parse_property(formula_str)
        results = stormpy.dft.analyze_dft(dft, formula)
        result = results[0]
        assert math.isclose(result, 363.8947965815, rel_tol=1e-6)

    def test_build_model(self):
        dft = stormpy.dft.load_dft_json_file(get_example_path("dft", "and.json"))
        model = stormpy.dft.build_model(dft)
        assert model.model_type == stormpy.models.ModelType.CTMC
        assert type(model) is stormpy.models.SparseCtmc[float]
        assert model.nr_states == 4
        assert model.nr_transitions == 5
        assert not model.supports_parameters

    def test_explicit_model_builder(self):
        dft = stormpy.dft.load_dft_json_file(get_example_path("dft", "and.json"))
        builder = stormpy.dft.developer.ExplicitDFTModelBuilder[float](stormpy.dft.DftEnvironment(), dft, stormpy.dft.developer.DftSymmetries())
        builder.build(0)
        model = builder.get_model()
        assert model.model_type == stormpy.models.ModelType.CTMC
        assert type(model) is stormpy.models.SparseCtmc[float]
        assert model.nr_states == 4
        assert model.nr_transitions == 5
        assert not model.supports_parameters

    def test_explicit_model_builder_symmetries(self):
        dft = stormpy.dft.load_dft_json_file(get_example_path("dft", "and.json"))
        symmetries = dft.symmetries()
        model = stormpy.dft.build_model(dft, symmetries=symmetries)
        assert model.nr_states == 3
        assert model.nr_transitions == 3
        assert model.model_type == stormpy.models.ModelType.CTMC

    def test_explicit_model_builder_unsupported_value_type(self):
        double_dft = stormpy.dft.load_dft_json_file(get_example_path("dft", "and.json"))
        with pytest.raises(TypeError, match="ExplicitDFTModelBuilder has no instantiation"):
            stormpy.dft.developer.ExplicitDFTModelBuilder[stormpy.Rational](double_dft)

    def test_explicit_model_builder_mismatched_dft_type(self):
        double_dft = stormpy.dft.load_dft_json_file(get_example_path("dft", "and.json"))
        with pytest.raises(TypeError, match="incompatible constructor arguments"):
            stormpy.dft.developer.ExplicitDFTModelBuilder[stormpy.RationalFunction](double_dft)

    def test_explicit_model_builder_approximation(self):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "rc.dft"))
        valid, output = stormpy.dft.developer.is_well_formed(dft)
        assert valid
        issue, output = stormpy.dft.developer.has_potential_modeling_issues(dft)
        assert not issue
        formula = stormpy.parse_property('T=? [ F "failed" ]')
        prop = formula
        builder = stormpy.dft.developer.ExplicitDFTModelBuilder(stormpy.dft.DftEnvironment(), dft, stormpy.dft.developer.DftSymmetries())

        # Iteration 0
        builder.build(0, 1.0)
        model_low = builder.get_partial_model(True, True)
        assert model_low.model_type == stormpy.models.ModelType.CTMC
        assert type(model_low) is stormpy.models.SparseCtmc[float]
        assert model_low.nr_states == 25
        assert model_low.nr_transitions == 46
        assert not model_low.supports_parameters
        initial_state = model_low.initial_states[0]
        assert initial_state == 1
        result_low = stormpy.model_checking(model_low, prop)
        assert math.isclose(result_low[initial_state], 0.5735024009)

        model_up = builder.get_partial_model(False, True)
        assert model_up.model_type == stormpy.models.ModelType.CTMC
        assert type(model_up) is stormpy.models.SparseCtmc[float]
        assert model_up.nr_states == 25
        assert model_up.nr_transitions == 46
        assert not model_up.supports_parameters
        result_up = stormpy.model_checking(model_up, prop)
        assert math.isclose(result_up[initial_state], 0.9225431553)

        # Iteration 1
        builder.build(1, 1.0)
        model_low = builder.get_partial_model(True, True)
        assert model_low.nr_states == 55
        assert model_low.nr_transitions == 143
        result_low = stormpy.model_checking(model_low, prop)
        assert math.isclose(result_low[initial_state], 0.6468192701)

        model_up = builder.get_partial_model(False, True)
        assert model_up.nr_states == 55
        assert model_up.nr_transitions == 143
        result_up = stormpy.model_checking(model_up, prop)
        assert math.isclose(result_up[initial_state], 0.8130197535)

        # Iteration 2
        builder.build(2, 1.0)
        model_low = builder.get_partial_model(True, True)
        assert model_low.nr_states == 91
        assert model_low.nr_transitions == 295
        result_low = stormpy.model_checking(model_low, prop)
        assert math.isclose(result_low[initial_state], 0.6471750688)

        model_up = builder.get_partial_model(False, True)
        assert model_up.nr_states == 91
        assert model_up.nr_transitions == 295
        result_up = stormpy.model_checking(model_up, prop)
        assert math.isclose(result_up[initial_state], 0.6484525286)

    def test_explicit_model_builder_approximation_complete(self):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "rc.dft"))
        formula = stormpy.parse_property('T=? [ F "failed" ]')
        prop = formula
        builder = stormpy.dft.developer.ExplicitDFTModelBuilder(stormpy.dft.DftEnvironment(), dft, stormpy.dft.developer.DftSymmetries())

        # Iteration 0
        builder.build(0, 1.0)
        model_low = builder.get_partial_model(True, True)
        assert model_low.model_type == stormpy.models.ModelType.CTMC
        assert type(model_low) is stormpy.models.SparseCtmc[float]
        assert model_low.nr_states == 25
        assert model_low.nr_transitions == 46
        assert not model_low.supports_parameters
        initial_state = model_low.initial_states[0]
        assert initial_state == 1
        result_low = stormpy.model_checking(model_low, prop)
        assert math.isclose(result_low[initial_state], 0.5735024009)

        # Final iteration
        builder.build(1)
        model = builder.get_model()
        assert model.model_type == stormpy.models.ModelType.CTMC
        assert type(model) is stormpy.models.SparseCtmc[float]
        assert model.nr_states == 145
        assert model.nr_transitions == 625
        assert not model.supports_parameters
        result = stormpy.model_checking(model, prop)
        assert math.isclose(result[initial_state], 0.6471760795)

    def _check_analyze_dft_with_approximation(self, heuristic):
        # Approximate analysis returns a (lower, upper) bound pair per property instead of a
        # single exact value.
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "rc.dft"))
        formula = stormpy.parse_property('T=? [ F "failed" ]')
        env = stormpy.dft.DftEnvironment()
        env.analysis_environment.approximation_error = 0.1
        env.analysis_environment.approximation_heuristic = heuristic
        results = stormpy.dft.analyze_dft(dft, formula, environment=env)
        assert len(results) == 1
        lower, upper = results[0]
        assert 0 <= lower <= upper

    def test_analyze_dft_with_approximation_depth(self):
        self._check_analyze_dft_with_approximation(stormpy.dft.ApproximationHeuristic.DEPTH)

    @pytest.mark.skip(reason="Currently bug in approximation")
    def test_analyze_dft_with_approximation_probability(self):
        self._check_analyze_dft_with_approximation(stormpy.dft.ApproximationHeuristic.PROBABILITY)

    @pytest.mark.skip(reason="Currently bug in approximation")
    def test_analyze_dft_with_approximation_bound_difference(self):
        self._check_analyze_dft_with_approximation(stormpy.dft.ApproximationHeuristic.BOUND_DIFFERENCE)

    def test_analyze_relevant_events(self):
        dft = stormpy.dft.load_dft_json_file(get_example_path("dft", "and.json"))
        prop = stormpy.parse_property('T=? [ F "failed" ]')
        relevant_events = stormpy.dft.compute_relevant_events(prop)
        results = stormpy.dft.analyze_dft(dft, prop, relevant_events=relevant_events)
        assert math.isclose(results[0], 3)

    def test_relevant_events_property(self):
        dft = stormpy.dft.load_dft_json_file(get_example_path("dft", "and.json"))
        prop = stormpy.parse_property('P=? [ F<=1 "A_failed" ]')
        relevant_events = stormpy.dft.compute_relevant_events(prop)
        assert relevant_events.is_relevant("A")
        assert not relevant_events.is_relevant("B")
        assert not relevant_events.is_relevant("C")
        results = stormpy.dft.analyze_dft(dft, prop, relevant_events=relevant_events)
        assert math.isclose(results[0], 0.1548181217)

    def test_relevant_events_additional(self):
        dft = stormpy.dft.load_dft_json_file(get_example_path("dft", "and.json"))
        prop = stormpy.parse_property('P=? [ F<=1 "failed" ]')
        relevant_events = stormpy.dft.compute_relevant_events(prop, additional_relevant_names=["B", "C"])
        assert relevant_events.is_relevant("B")
        assert relevant_events.is_relevant("C")
        assert not relevant_events.is_relevant("A")
        results = stormpy.dft.analyze_dft(dft, prop, relevant_events=relevant_events)
        assert math.isclose(results[0], 0.1548181217)

    def test_relevant_events_developer(self):
        formulas = [prop.get_raw_formula() for prop in stormpy.parse_properties('P=? [ F<=1 "A_failed" ]')]
        relevant_events = stormpy.dft.developer.compute_relevant_events(formulas, additional_relevant_names=["B"])
        assert relevant_events.is_relevant("A")
        assert relevant_events.is_relevant("B")
        assert not relevant_events.is_relevant("C")

    def test_transformation(self):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "rc2.dft"))
        valid, output = stormpy.dft.developer.is_well_formed(dft)
        assert not valid
        issue, output = stormpy.dft.developer.has_potential_modeling_issues(dft)
        assert issue
        dft = stormpy.dft.prepare_for_analysis(dft)
        valid, output = stormpy.dft.developer.is_well_formed(dft)
        assert valid
        issue, output = stormpy.dft.developer.has_potential_modeling_issues(dft)
        assert issue
        prop = stormpy.parse_property('Tmin=? [ F "failed" ]')
        results = stormpy.dft.analyze_dft(dft, prop)
        assert math.isclose(results[0], 6.380930905)

    def test_fdep_conflicts(self):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "rc2.dft"))
        dft = stormpy.dft.developer.transform_dft(dft, unique_constant_be=True, binary_fdeps=True, exponential_distributions=True)
        has_conflicts = stormpy.dft.developer.compute_dependency_conflicts(dft, use_smt=False, solver_timeout=0)
        assert not has_conflicts
        prop = stormpy.parse_property('T=? [ F "failed" ]')
        results = stormpy.dft.analyze_dft(dft, prop)
        assert math.isclose(results[0], 6.380930905)

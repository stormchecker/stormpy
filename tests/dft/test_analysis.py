import stormpy
from helpers.helper import get_example_path

import math
from configurations import dft


@dft
class TestAnalysis:

    def test_analyze_mttf(self):
        dft = stormpy.dft.load_dft_json_file(get_example_path("dft", "and.json"))
        formulas = stormpy.parse_properties('T=? [ F "failed" ]')
        assert dft.nr_elements() == 3
        results = stormpy.dft.analyze_dft(dft, [formulas[0].raw_formula])
        assert math.isclose(results[0], 3)

    def test_build_model(self):
        dft = stormpy.dft.load_dft_json_file(get_example_path("dft", "and.json"))
        model = stormpy.dft.build_model(dft)
        assert model.model_type == stormpy.ModelType.CTMC
        assert type(model) is stormpy.SparseCtmc
        assert model.nr_states == 4
        assert model.nr_transitions == 5
        assert not model.supports_parameters

    def test_explicit_model_builder(self):
        dft = stormpy.dft.load_dft_json_file(get_example_path("dft", "and.json"))
        builder = stormpy.dft.ExplicitDFTModelBuilder_double(dft)
        builder.build(0)
        model = builder.get_model()
        assert model.model_type == stormpy.ModelType.CTMC
        assert type(model) is stormpy.SparseCtmc
        assert model.nr_states == 4
        assert model.nr_transitions == 5
        assert not model.supports_parameters

    def test_explicit_model_builder_approximation(self):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "rc.dft"))
        valid, output = stormpy.dft.is_well_formed(dft)
        assert valid
        issue, output = stormpy.dft.has_potential_modeling_issues(dft)
        assert not issue
        properties = stormpy.parse_properties('T=? [ F "failed" ]')
        prop = properties[0]
        builder = stormpy.dft.ExplicitDFTModelBuilder_double(dft)

        # Iteration 0
        builder.build(0, 1.0)
        model_low = builder.get_partial_model(True, True)
        assert model_low.model_type == stormpy.ModelType.CTMC
        assert type(model_low) is stormpy.SparseCtmc
        assert model_low.nr_states == 25
        assert model_low.nr_transitions == 46
        assert not model_low.supports_parameters
        initial_state = model_low.initial_states[0]
        assert initial_state == 1
        result_low = stormpy.model_checking(model_low, prop)
        assert math.isclose(result_low.at(initial_state), 0.5735024009)

        model_up = builder.get_partial_model(False, True)
        assert model_up.model_type == stormpy.ModelType.CTMC
        assert type(model_up) is stormpy.SparseCtmc
        assert model_up.nr_states == 25
        assert model_up.nr_transitions == 46
        assert not model_up.supports_parameters
        result_up = stormpy.model_checking(model_up, prop)
        assert math.isclose(result_up.at(initial_state), 0.9225431553)

        # Iteration 1
        builder.build(1, 1.0)
        model_low = builder.get_partial_model(True, True)
        assert model_low.nr_states == 55
        assert model_low.nr_transitions == 143
        result_low = stormpy.model_checking(model_low, prop)
        assert math.isclose(result_low.at(initial_state), 0.6468192701)

        model_up = builder.get_partial_model(False, True)
        assert model_up.nr_states == 55
        assert model_up.nr_transitions == 143
        result_up = stormpy.model_checking(model_up, prop)
        assert math.isclose(result_up.at(initial_state), 0.8130197535)

        # Iteration 2
        builder.build(2, 1.0)
        model_low = builder.get_partial_model(True, True)
        assert model_low.nr_states == 91
        assert model_low.nr_transitions == 295
        result_low = stormpy.model_checking(model_low, prop)
        assert math.isclose(result_low.at(initial_state), 0.6471750688)

        model_up = builder.get_partial_model(False, True)
        assert model_up.nr_states == 91
        assert model_up.nr_transitions == 295
        result_up = stormpy.model_checking(model_up, prop)
        assert math.isclose(result_up.at(initial_state), 0.6484525286)

    def test_explicit_model_builder_approximation_complete(self):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "rc.dft"))
        properties = stormpy.parse_properties('T=? [ F "failed" ]')
        prop = properties[0]
        builder = stormpy.dft.ExplicitDFTModelBuilder_double(dft)

        # Iteration 0
        builder.build(0, 1.0)
        model_low = builder.get_partial_model(True, True)
        assert model_low.model_type == stormpy.ModelType.CTMC
        assert type(model_low) is stormpy.SparseCtmc
        assert model_low.nr_states == 25
        assert model_low.nr_transitions == 46
        assert not model_low.supports_parameters
        initial_state = model_low.initial_states[0]
        assert initial_state == 1
        result_low = stormpy.model_checking(model_low, prop)
        assert math.isclose(result_low.at(initial_state), 0.5735024009)

        # Final iteration
        builder.build(1)
        model = builder.get_model()
        assert model.model_type == stormpy.ModelType.CTMC
        assert type(model) is stormpy.SparseCtmc
        assert model.nr_states == 145
        assert model.nr_transitions == 625
        assert not model.supports_parameters
        result = stormpy.model_checking(model, prop)
        assert math.isclose(result.at(initial_state), 0.6471760795)

    def test_relevant_events_property(self):
        dft = stormpy.dft.load_dft_json_file(get_example_path("dft", "and.json"))
        properties = stormpy.parse_properties('P=? [ F<=1 "A_failed" ]')
        formulas = [p.raw_formula for p in properties]
        relevant_events = stormpy.dft.compute_relevant_events(formulas)
        assert relevant_events.is_relevant("A")
        assert not relevant_events.is_relevant("B")
        assert not relevant_events.is_relevant("C")
        results = stormpy.dft.analyze_dft(dft, formulas, relevant_events=relevant_events)
        assert math.isclose(results[0], 0.1548181217)

    def test_relevant_events_additional(self):
        dft = stormpy.dft.load_dft_json_file(get_example_path("dft", "and.json"))
        properties = stormpy.parse_properties('P=? [ F<=1 "failed" ]')
        formulas = [p.raw_formula for p in properties]
        relevant_events = stormpy.dft.compute_relevant_events(formulas, ["B", "C"])
        assert relevant_events.is_relevant("B")
        assert relevant_events.is_relevant("C")
        assert not relevant_events.is_relevant("A")
        results = stormpy.dft.analyze_dft(dft, formulas, relevant_events=relevant_events)
        assert math.isclose(results[0], 0.1548181217)

    def test_transformation(self):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "rc2.dft"))
        valid, output = stormpy.dft.is_well_formed(dft)
        assert not valid
        issue, output = stormpy.dft.has_potential_modeling_issues(dft)
        assert issue
        dft = stormpy.dft.transform_dft(dft, unique_constant_be=True, binary_fdeps=True, exponential_distributions=True)
        valid, output = stormpy.dft.is_well_formed(dft)
        assert valid
        issue, output = stormpy.dft.has_potential_modeling_issues(dft)
        assert issue
        formulas = stormpy.parse_properties('Tmin=? [ F "failed" ]')
        results = stormpy.dft.analyze_dft(dft, [formulas[0].raw_formula])
        assert math.isclose(results[0], 6.380930905)

    def test_fdep_conflicts(self):
        dft = stormpy.dft.load_dft_galileo_file(get_example_path("dft", "rc2.dft"))
        dft = stormpy.dft.transform_dft(dft, unique_constant_be=True, binary_fdeps=True, exponential_distributions=True)
        has_conflicts = stormpy.dft.compute_dependency_conflicts(dft, use_smt=False, solver_timeout=0)
        assert not has_conflicts
        formulas = stormpy.parse_properties('T=? [ F "failed" ]')
        results = stormpy.dft.analyze_dft(dft, [formulas[0].raw_formula])
        assert math.isclose(results[0], 6.380930905)

import pathlib
import pytest
import stormpy
from stormpy.exceptions import StormError

from helpers.helper import get_example_path


class TestParseProperties:
    def test_parse_formula(self):
        formula = 'P=? [F "one"]'
        properties = stormpy.parse_properties(formula)
        assert len(properties) == 1
        assert str(properties[0].get_raw_formula()) == formula

    def test_parse_properties(self):
        properties = stormpy.parse_properties('P=? [F "one"]; R{"coin_flips"}min=? [F "done"]')
        assert all(isinstance(prop, stormpy.logic.Property) for prop in properties)
        probability, reward = (prop.get_raw_formula() for prop in properties)
        assert isinstance(probability, stormpy.logic.ProbabilityOperatorFormula)
        assert probability.is_probability_operator_formula
        assert isinstance(reward, stormpy.logic.RewardOperatorFormula)
        assert reward.is_reward_operator_formula
        assert reward.has_reward_model_name()
        assert reward.optimality_type == stormpy.logic.OptimizationDirection.MINIMIZE

    def test_parse_properties_without_context(self):
        properties = stormpy.parse_properties('P=? [F "one"]; R=? [F "done"]')
        assert len(properties) == 2
        assert properties[0].get_raw_formula().is_probability_operator_formula

    def test_parse_properties_filters(self):
        properties = stormpy.parse_properties('"a": P=? [F "one"]; "b": P=? [F "two"]', property_filter=["b"])
        assert len(properties) == 1
        assert properties[0].get_name() == "b"

    def test_parse_properties_jani_context(self):
        jani_model, _ = stormpy.parse_jani_model(get_example_path("dtmc", "die.jani"))
        properties = stormpy.parse_properties("P=? [F s=7]", jani_model)
        assert len(properties) == 1

    def test_parse_properties_symbolic_description_context(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        properties = stormpy.parse_properties("P=? [F s=7]", stormpy.SymbolicModelDescription(program))
        assert len(properties) == 1
        jani_model, _ = stormpy.parse_jani_model(get_example_path("dtmc", "die.jani"))
        properties = stormpy.parse_properties("P=? [F s=7]", stormpy.SymbolicModelDescription(jani_model))
        assert len(properties) == 1

    def test_parse_properties_invalid_context(self):
        with pytest.raises(StormError):
            stormpy.parse_properties("P=? [F s=7]", 42)

    def test_parse_property(self):
        prop = stormpy.parse_property('P=? [F "one"]')
        assert isinstance(prop, stormpy.logic.Property)
        assert prop.get_raw_formula().is_probability_operator_formula
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        prop = stormpy.parse_property('"name": P=? [F s=7]', program)
        assert prop.get_name() == "name"

    def test_parse_property_not_single(self):
        with pytest.raises(StormError, match="exactly one property, but 2"):
            stormpy.parse_property('P=? [F "one"]; P=? [F "two"]')
        with pytest.raises(StormError, match="exactly one property, but 0"):
            stormpy.parse_property("")

    def test_single_property_for_building(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        prop = stormpy.parse_property("P=? [F s=7 & d=2]", program)
        model = stormpy.build_model(program, prop)
        model_from_list = stormpy.build_model(program, [prop])
        assert model.nr_states == model_from_list.nr_states
        assert model.labeling.get_labels() == model_from_list.labeling.get_labels()
        model_from_options = stormpy.build_model(program, options=stormpy.BuilderOptions(prop))
        assert model_from_options.nr_states == model.nr_states
        _, instantiated = stormpy.instantiate_constants(program, "", prop)
        assert len(instantiated) == 1

    def test_parse_jani_model_property_filter(self):
        _, properties = stormpy.parse_jani_model(get_example_path("dtmc", "die.jani"), property_filter=["Probability to throw a six"])
        assert len(properties) == 1


class TestParsePrismProgram:
    def test_parse_prism_program(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        assert program.nr_modules == 1
        assert program.model_type == stormpy.io.PrismModelType.DTMC
        assert not program.has_undefined_constants
        description = stormpy.SymbolicModelDescription(program)
        assert description.is_prism_program()
        assert not description.is_jani_model()

    def test_parse_parametric_prism_program(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        assert program.nr_modules == 5
        assert program.model_type == stormpy.io.PrismModelType.DTMC
        assert program.has_undefined_constants
        assert program.undefined_constants_are_graph_preserving

    def test_parse_from_path(self):
        program = stormpy.parse_prism_program(pathlib.Path(get_example_path("dtmc", "die.pm")))
        assert program.nr_modules == 1
        jani_model, properties = stormpy.parse_jani_model(pathlib.Path(get_example_path("dtmc", "die.jani")))
        assert len(properties) > 0
        with pytest.raises(TypeError):
            stormpy.parse_prism_program(42)


class TestParseJaniModel:
    def test_parse_jani_model(self):
        jani_model, properties = stormpy.parse_jani_model(get_example_path("dtmc", "die.jani"))
        assert jani_model.name == "die.jani"
        assert jani_model.model_type == stormpy.JaniModelType.DTMC
        assert not jani_model.has_undefined_constants
        description = stormpy.SymbolicModelDescription(jani_model)
        assert not description.is_prism_program()
        assert description.is_jani_model()

    def test_parse_jani_model_string(self):
        with open(get_example_path("dtmc", "die.jani"), "r") as file:
            json_string = file.read()
        jani_model, properties = stormpy.parse_jani_model_from_string(json_string)
        assert jani_model.name == "die.jani"
        assert jani_model.model_type == stormpy.JaniModelType.DTMC
        assert not jani_model.has_undefined_constants
        description = stormpy.SymbolicModelDescription(jani_model)
        assert not description.is_prism_program()
        assert description.is_jani_model()


class TestInstantiate:
    def test_instantiate_constants(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "brp.pm"))
        assert program.has_undefined_constants
        properties = stormpy.parse_properties("P=? [F s=5]", program)
        instantiated, instantiated_properties = stormpy.instantiate_constants(program, "N=16,MAX=2", properties)
        assert isinstance(instantiated, stormpy.io.PrismProgram)
        assert not instantiated.has_undefined_constants
        assert len(instantiated_properties) == 1
        model = stormpy.build_model(instantiated, instantiated_properties)
        assert model.nr_states > 0

    def test_instantiate_constants_mapping(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "brp.pm"))
        properties = stormpy.parse_properties("P=? [F s=5]", program)
        from_string, _ = stormpy.instantiate_constants(program, "N=16,MAX=2", properties)
        from_mapping, instantiated_properties = stormpy.instantiate_constants(program, {"N": 16, program.expression_manager.get_variable("MAX"): 2}, properties)
        assert not from_mapping.has_undefined_constants
        assert len(instantiated_properties) == 1
        assert stormpy.build_model(from_mapping).nr_states == stormpy.build_model(from_string).nr_states

    def test_instantiate_constants_mapping_values(self):
        program = stormpy.parse_prism_program(get_example_path("mdp", "firewire.nm"))
        from_string, _ = stormpy.instantiate_constants(program, "delay=10,fast=0.8")
        manager = program.expression_manager
        for fast in (0.8, stormpy.Rational("4/5"), manager.rational(stormpy.Rational("4/5"))):
            from_mapping, _ = stormpy.instantiate_constants(program, {"delay": 10, "fast": fast})
            assert not from_mapping.has_undefined_constants
            assert str(from_mapping) == str(from_string)

    def test_instantiate_constants_mapping_jani(self):
        jani_model, properties = stormpy.parse_jani_model(get_example_path("dtmc", "brp.jani"))
        instantiated, instantiated_properties = stormpy.instantiate_constants(jani_model, {"N": 16, "MAX": 2}, properties)
        assert isinstance(instantiated, stormpy.io.JaniModel)
        assert not instantiated.has_undefined_constants
        assert len(instantiated_properties) == len(properties)

    def test_instantiate_constants_mapping_errors(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "brp.pm"))
        with pytest.raises(StormError, match="Unknown constant"):
            stormpy.instantiate_constants(program, {"unknown": 1})
        with pytest.raises(StormError, match="Unsupported value"):
            stormpy.instantiate_constants(program, {"N": "16"})
        with pytest.raises(StormError, match="Unsupported constant definitions"):
            stormpy.instantiate_constants(program, [("N", 16)])

    def test_instantiate_constants_symbolic_description(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        instantiated, properties = stormpy.instantiate_constants(stormpy.SymbolicModelDescription(program), "")
        assert isinstance(instantiated, stormpy.SymbolicModelDescription)
        assert properties == []


class TestParseExplicit:
    def test_parse_explicit_dtmc(self):
        model = stormpy.build_model_from_explicit(get_example_path("dtmc", "die.tra"), get_example_path("dtmc", "die.lab"))
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        assert model.model_type == stormpy.models.ModelType.DTMC
        assert not model.supports_parameters
        assert type(model) is stormpy.models.SparseDtmc[float]

    def test_parse_explicit_mdp(self):
        model = stormpy.build_model_from_explicit(get_example_path("mdp", "two_dice.tra"), get_example_path("mdp", "two_dice.lab"))
        assert model.nr_states == 169
        assert model.nr_transitions == 436
        assert model.model_type == stormpy.models.ModelType.MDP
        assert not model.supports_parameters
        assert type(model) is stormpy.models.SparseMdp[float]

    def test_parse_drn_dtmc(self):
        model = stormpy.build_model_from_drn(get_example_path("ctmc", "dft.drn"))
        assert model.nr_states == 16
        assert model.nr_transitions == 33
        assert model.model_type == stormpy.models.ModelType.CTMC
        assert not model.supports_parameters
        assert type(model) is stormpy.models.SparseCtmc[float]

import stormpy
from helpers.helper import get_example_path


class TestStormpyParse:
    def test_parse_prism_program(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        assert program.nr_modules == 1
        assert program.model_type == stormpy.PrismModelType.DTMC
        assert not program.has_undefined_constants
        description = stormpy.SymbolicModelDescription(program)
        assert description.is_prism_program
        assert not description.is_jani_model

    def test_parse_parametric_prism_program(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        assert program.nr_modules == 5
        assert program.model_type == stormpy.PrismModelType.DTMC
        assert program.has_undefined_constants
        assert program.undefined_constants_are_graph_preserving

    def test_parse_jani_model(self):
        jani_model, properties = stormpy.parse_jani_model(get_example_path("dtmc", "die.jani"))
        assert jani_model.name == "die.jani"
        assert jani_model.model_type == stormpy.JaniModelType.DTMC
        assert not jani_model.has_undefined_constants
        description = stormpy.SymbolicModelDescription(jani_model)
        assert not description.is_prism_program
        assert description.is_jani_model

    def test_parse_jani_model_string(self):
        with open(get_example_path("dtmc", "die.jani"), "r") as file:
            json_string = file.read()
        jani_model, properties = stormpy.parse_jani_model_from_string(json_string)
        assert jani_model.name == "die.jani"
        assert jani_model.model_type == stormpy.JaniModelType.DTMC
        assert not jani_model.has_undefined_constants
        description = stormpy.SymbolicModelDescription(jani_model)
        assert not description.is_prism_program
        assert description.is_jani_model

    def test_parse_formula(self):
        formula = 'P=? [F "one"]'
        properties = stormpy.parse_properties(formula)
        assert len(properties) == 1
        assert str(properties[0].raw_formula) == formula

    def test_parse_explicit_dtmc(self):
        model = stormpy.build_sparse_model_from_explicit(get_example_path("dtmc", "die.tra"), get_example_path("dtmc", "die.lab"))
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        assert model.model_type == stormpy.ModelType.DTMC
        assert not model.supports_parameters
        assert type(model) is stormpy.SparseDtmc

    def test_parse_explicit_mdp(self):
        model = stormpy.build_sparse_model_from_explicit(get_example_path("mdp", "two_dice.tra"), get_example_path("mdp", "two_dice.lab"))
        assert model.nr_states == 169
        assert model.nr_transitions == 436
        assert model.model_type == stormpy.ModelType.MDP
        assert not model.supports_parameters
        assert type(model) is stormpy.SparseMdp

    def test_parse_drn_dtmc(self):
        model = stormpy.build_model_from_drn(get_example_path("ctmc", "dft.drn"))
        assert model.nr_states == 16
        assert model.nr_transitions == 33
        assert model.model_type == stormpy.ModelType.CTMC
        assert not model.supports_parameters
        assert type(model) is stormpy.SparseCtmc

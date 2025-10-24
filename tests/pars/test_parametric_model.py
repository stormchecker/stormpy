import stormpy
import stormpy.info
from helpers.helper import get_example_path

from configurations import pars


@pars
class TestSparseParametricModel:
    def test_build_parametric_dtmc(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        formulas = stormpy.parse_properties_for_prism_program("P=? [ F s=5 ]", program)
        model = stormpy.build_parametric_model(program, formulas)
        assert model.nr_states == 613
        assert model.nr_transitions == 803
        assert model.model_type == stormpy.ModelType.DTMC
        assert model.supports_parameters
        assert model.has_parameters
        assert type(model) is stormpy.SparseParametricDtmc

    def test_build_parametric_dtmc_preprocess(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "herman5.pm"))
        formulas = stormpy.parse_properties_for_prism_program('R=? [ F "stable" ]', program)
        trans_program, trans_formulas = stormpy.preprocess_symbolic_input(program, formulas, "")
        trans_prism = trans_program.as_prism_program()
        model = stormpy.build_parametric_model(trans_prism, trans_formulas)
        assert model.nr_states == 33
        assert model.nr_transitions == 266
        assert model.model_type == stormpy.ModelType.DTMC
        assert model.supports_parameters
        assert model.has_parameters
        assert type(model) is stormpy.SparseParametricDtmc

    def test_build_dtmc_supporting_parameters(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        formulas = stormpy.parse_properties_for_prism_program('P=? [ F "one" ]', program)
        model = stormpy.build_parametric_model(program, formulas)
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        assert model.model_type == stormpy.ModelType.DTMC
        assert model.supports_parameters
        assert not model.has_parameters
        assert type(model) is stormpy.SparseParametricDtmc

    def test_build_parametric_mdp(self):
        program = stormpy.parse_prism_program(get_example_path("pmdp", "two_dice.nm"))
        formulas = stormpy.parse_properties_for_prism_program('P=? [ F "two" ]', program)
        model = stormpy.build_parametric_model(program, formulas)
        assert model.nr_states == 169
        assert model.nr_transitions == 435
        assert model.model_type == stormpy.ModelType.MDP
        assert model.supports_parameters
        assert type(model) is stormpy.SparseParametricMdp


@pars
class TestSymbolicParametricModel:
    def test_build_parametric_dtmc(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        formulas = stormpy.parse_properties_for_prism_program("P=? [ F s=5 ]", program)
        model = stormpy.build_symbolic_parametric_model(program, formulas)
        assert model.nr_states == 613
        assert model.nr_transitions == 803
        assert model.model_type == stormpy.ModelType.DTMC
        assert model.supports_parameters
        assert model.has_parameters
        assert type(model) is stormpy.SymbolicSylvanParametricDtmc

    def test_build_parametric_dtmc_preprocess(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "herman5.pm"))
        formulas = stormpy.parse_properties_for_prism_program('R=? [ F "stable" ]', program)
        trans_program, trans_formulas = stormpy.preprocess_symbolic_input(program, formulas, "")
        trans_prism = trans_program.as_prism_program()
        model = stormpy.build_symbolic_parametric_model(trans_prism, trans_formulas)
        assert model.nr_states == 33
        assert model.nr_transitions == 266
        assert model.model_type == stormpy.ModelType.DTMC
        assert model.supports_parameters
        assert model.has_parameters
        assert type(model) is stormpy.SymbolicSylvanParametricDtmc

    def test_build_dtmc_supporting_parameters(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        formulas = stormpy.parse_properties_for_prism_program('P=? [ F "one" ]', program)
        model = stormpy.build_symbolic_parametric_model(program, formulas)
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        assert model.model_type == stormpy.ModelType.DTMC
        assert model.supports_parameters
        assert not model.has_parameters
        assert type(model) is stormpy.SymbolicSylvanParametricDtmc

    def test_build_parametric_mdp(self):
        program = stormpy.parse_prism_program(get_example_path("pmdp", "two_dice.nm"))
        formulas = stormpy.parse_properties_for_prism_program('P=? [ F "two" ]', program)
        model = stormpy.build_symbolic_parametric_model(program, formulas)
        assert model.nr_states == 169
        assert model.nr_transitions == 435
        assert model.model_type == stormpy.ModelType.MDP
        assert model.supports_parameters
        assert type(model) is stormpy.SymbolicSylvanParametricMdp

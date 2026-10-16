import stormpy
import stormpy.info
from helpers.helper import get_example_path

from configurations import pars


@pars
class TestSparseParametricModel:
    def test_build_parametric_dtmc(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        formula = stormpy.parse_property("P=? [ F s=5 ]", program)
        model = stormpy.build_model[stormpy.RationalFunction](program, formula)
        assert model.nr_states == 613
        assert model.nr_transitions == 803
        assert model.model_type == stormpy.models.ModelType.DTMC
        assert model.supports_parameters
        assert model.has_parameters
        assert type(model) is stormpy.models.SparseDtmc[stormpy.RationalFunction]
        assert {x.name for x in model.collect_all_parameters()} == {"pL", "pK"}

    def test_build_parametric_dtmc_preprocess(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "herman5.pm"))
        formulas = stormpy.parse_properties('R=? [ F "stable" ]', program)
        trans_prism, trans_formulas = stormpy.instantiate_constants(program, "", formulas)
        model = stormpy.build_model[stormpy.RationalFunction](trans_prism, trans_formulas)
        assert model.nr_states == 33
        assert model.nr_transitions == 266
        assert model.model_type == stormpy.models.ModelType.DTMC
        assert model.supports_parameters
        assert model.has_parameters
        assert type(model) is stormpy.models.SparseDtmc[stormpy.RationalFunction]
        assert {x.name for x in model.collect_all_parameters()} == {"p"}

    def test_build_dtmc_supporting_parameters(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        formula = stormpy.parse_property('P=? [ F "one" ]', program)
        model = stormpy.build_model[stormpy.RationalFunction](program, formula)
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        assert model.model_type == stormpy.models.ModelType.DTMC
        assert model.supports_parameters
        assert not model.has_parameters
        assert type(model) is stormpy.models.SparseDtmc[stormpy.RationalFunction]
        assert len(model.collect_all_parameters()) == 0

    def test_build_parametric_mdp(self):
        program = stormpy.parse_prism_program(get_example_path("pmdp", "two_dice.nm"))
        formula = stormpy.parse_property('P=? [ F "two" ]', program)
        model = stormpy.build_model[stormpy.RationalFunction](program, formula)
        assert model.nr_states == 169
        assert model.nr_transitions == 435
        assert model.model_type == stormpy.models.ModelType.MDP
        assert model.supports_parameters
        assert type(model) is stormpy.models.SparseMdp[stormpy.RationalFunction]
        assert {x.name for x in model.collect_all_parameters()} == {"p1", "p2"}


@pars
class TestSymbolicParametricModel:
    def test_build_parametric_dtmc(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        formula = stormpy.parse_property("P=? [ F s=5 ]", program)
        model = stormpy.build_symbolic_model[stormpy.RationalFunction](program, formula)
        assert model.nr_states == 613
        assert model.nr_transitions == 803
        assert model.model_type == stormpy.models.ModelType.DTMC
        assert model.supports_parameters
        assert model.has_parameters
        assert type(model) is stormpy.models.SymbolicDtmc[stormpy.models.DdType.Sylvan, stormpy.RationalFunction]

    def test_build_parametric_dtmc_preprocess(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "herman5.pm"))
        formulas = stormpy.parse_properties('R=? [ F "stable" ]', program)
        trans_prism, trans_formulas = stormpy.instantiate_constants(program, "", formulas)
        model = stormpy.build_symbolic_model[stormpy.RationalFunction](trans_prism, trans_formulas)
        assert model.nr_states == 33
        assert model.nr_transitions == 266
        assert model.model_type == stormpy.models.ModelType.DTMC
        assert model.supports_parameters
        assert model.has_parameters
        assert type(model) is stormpy.models.SymbolicDtmc[stormpy.models.DdType.Sylvan, stormpy.RationalFunction]

    def test_build_dtmc_supporting_parameters(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        formula = stormpy.parse_property('P=? [ F "one" ]', program)
        model = stormpy.build_symbolic_model[stormpy.RationalFunction](program, formula)
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        assert model.model_type == stormpy.models.ModelType.DTMC
        assert model.supports_parameters
        assert not model.has_parameters
        assert type(model) is stormpy.models.SymbolicDtmc[stormpy.models.DdType.Sylvan, stormpy.RationalFunction]

    def test_build_parametric_mdp(self):
        program = stormpy.parse_prism_program(get_example_path("pmdp", "two_dice.nm"))
        formula = stormpy.parse_property('P=? [ F "two" ]', program)
        model = stormpy.build_symbolic_model[stormpy.RationalFunction](program, formula)
        assert model.nr_states == 169
        assert model.nr_transitions == 435
        assert model.model_type == stormpy.models.ModelType.MDP
        assert model.supports_parameters
        assert type(model) is stormpy.models.SymbolicMdp[stormpy.models.DdType.Sylvan, stormpy.RationalFunction]

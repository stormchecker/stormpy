import stormpy
from helpers.helper import get_example_path
import pytest


class TestSparseModel:
    def test_build_dtmc_from_prism_program(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        model = stormpy.build_model(program)
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        assert model.model_type == stormpy.ModelType.DTMC
        assert not model.supports_parameters
        assert type(model) is stormpy.SparseDtmc

    def test_build_dtmc_from_prism_program_formulas(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        prop = 'P=? [F "one"]'
        properties = stormpy.parse_properties_for_prism_program(prop, program, None)
        model = stormpy.build_model(program, properties)
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        assert model.model_type == stormpy.ModelType.DTMC
        assert len(model.reward_models) == 0
        assert not model.supports_parameters
        assert type(model) is stormpy.SparseDtmc

    def test_build_dtmc_from_prism_program_reward_formulas(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        prop = 'R=? [F "done"]'
        properties = stormpy.parse_properties_for_prism_program(prop, program, None)
        model = stormpy.build_model(program, properties)
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        assert model.model_type == stormpy.ModelType.DTMC
        assert len(model.reward_models) == 1
        assert not model.reward_models["coin_flips"].has_state_rewards
        assert model.reward_models["coin_flips"].has_state_action_rewards
        for reward in model.reward_models["coin_flips"].state_action_rewards:
            assert reward == 1.0 or reward == 0.0
        assert not model.reward_models["coin_flips"].has_transition_rewards
        assert not model.supports_parameters
        assert type(model) is stormpy.SparseDtmc

    def test_reduce_to_state_based_rewards(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        prop = 'R=? [F "done"]'
        properties = stormpy.parse_properties_for_prism_program(prop, program, None)
        model = stormpy.build_model(program, properties)
        model.reduce_to_state_based_rewards()
        assert len(model.reward_models) == 1
        assert model.reward_models["coin_flips"].has_state_rewards
        assert not model.reward_models["coin_flips"].has_state_action_rewards
        for reward in model.reward_models["coin_flips"].state_rewards:
            assert reward == 1.0 or reward == 0.0
        assert not model.reward_models["coin_flips"].has_transition_rewards

    def test_build_dtmc_from_jani_model(self):
        jani_model, properties = stormpy.parse_jani_model(get_example_path("dtmc", "die.jani"))
        model = stormpy.build_model(jani_model)
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        assert model.model_type == stormpy.ModelType.DTMC
        assert not model.supports_parameters
        assert type(model) is stormpy.SparseDtmc

    def test_build_dtmc_with_undefined_constants(self):
        jani_model, properties = stormpy.parse_jani_model(get_example_path("dtmc", "brp.jani"))
        assert jani_model.has_undefined_constants
        assert not jani_model.undefined_constants_are_graph_preserving
        with pytest.raises(stormpy.exceptions.StormError):
            model = stormpy.build_model(jani_model)

    def test_build_instantiated_dtmc_prism(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "brp.pm"))
        assert program.has_undefined_constants
        assert not program.undefined_constants_are_graph_preserving
        description = stormpy.SymbolicModelDescription(program)
        constant_definitions = description.parse_constant_definitions("N=16, MAX=2")
        instantiated_program = description.instantiate_constants(constant_definitions).as_prism_program()
        model = stormpy.build_model(instantiated_program)
        assert model.nr_states == 677
        assert model.nr_transitions == 867
        assert model.model_type == stormpy.ModelType.DTMC
        assert not model.supports_parameters
        assert type(model) is stormpy.SparseDtmc

    def test_build_instantiated_dtmc_jani(self):
        jani_model, properties = stormpy.parse_jani_model(get_example_path("dtmc", "brp.jani"))
        assert jani_model.has_undefined_constants
        assert not jani_model.undefined_constants_are_graph_preserving
        description = stormpy.SymbolicModelDescription(jani_model)
        constant_definitions = description.parse_constant_definitions("N=16, MAX=2")
        instantiated_jani_model = description.instantiate_constants(constant_definitions).as_jani_model()
        model = stormpy.build_model(instantiated_jani_model)
        assert model.nr_states == 677
        assert model.nr_transitions == 867
        assert model.model_type == stormpy.ModelType.DTMC
        assert not model.supports_parameters
        assert type(model) is stormpy.SparseDtmc

    def test_build_mdp(self):
        program = stormpy.parse_prism_program(get_example_path("mdp", "two_dice.nm"))
        formulas = stormpy.parse_properties_for_prism_program('P=? [ F "two" ]', program)
        model = stormpy.build_model(program, formulas)
        assert model.nr_states == 169
        assert model.nr_transitions == 435
        assert model.model_type == stormpy.ModelType.MDP
        assert not model.supports_parameters
        assert type(model) is stormpy.SparseMdp

    def test_build_ctmc(self):
        program = stormpy.parse_prism_program(get_example_path("ctmc", "polling2.sm"), True)
        formulas = stormpy.parse_properties_for_prism_program('P=? [ F<=3 "target" ]', program)
        model = stormpy.build_model(program)
        assert model.nr_states == 12
        assert model.nr_transitions == 22
        assert model.model_type == stormpy.ModelType.CTMC
        assert not model.supports_parameters
        assert type(model) is stormpy.SparseCtmc
        model_for_formula = stormpy.build_model(program, formulas)
        assert model_for_formula.nr_states == 12
        assert model_for_formula.nr_transitions == 21
        assert model_for_formula.model_type == stormpy.ModelType.CTMC
        assert not model_for_formula.supports_parameters
        assert type(model_for_formula) is stormpy.SparseCtmc

    def test_build_pomdp(self):
        program = stormpy.parse_prism_program(get_example_path("pomdp", "maze_2.prism"))
        formulas = stormpy.parse_properties_for_prism_program('P=? [F "goal"]', program)
        model = stormpy.build_model(program, formulas)
        assert model.nr_states == 15
        assert model.nr_observations == 8

    def test_build_ma(self):
        program = stormpy.parse_prism_program(get_example_path("ma", "simple.ma"), False, True)
        formulas = stormpy.parse_properties_for_prism_program("Pmax=? [ F<=2 s=2 ]", program)
        model = stormpy.build_model(program, formulas)
        assert model.nr_states == 4
        assert model.nr_transitions == 7
        assert model.model_type == stormpy.ModelType.MA
        assert not model.supports_parameters
        assert type(model) is stormpy.SparseMA

    def test_build_smg(self):
        program = stormpy.parse_prism_program(get_example_path("smg", "example_smg.nm"))
        formulas = stormpy.parse_properties_for_prism_program("<<maxP>> Pmax=? [ F s=2 ]", program)
        model = stormpy.build_model(program, formulas)
        assert model.nr_states == 4
        assert model.nr_choices == 5
        assert model.nr_transitions == 7
        assert model.model_type == stormpy.ModelType.SMG
        assert type(model) is stormpy.SparseSmg
        assert model.get_state_player_indications() == [1, 0, 0, 0]

    def test_convert_ma_to_ctmc(self):
        program = stormpy.parse_prism_program(get_example_path("ma", "ctmc.ma"), True)
        formulas = stormpy.parse_properties_for_prism_program("P=? [ F<=3 s=2 ]", program)
        model = stormpy.build_model(program, formulas)
        assert model.nr_states == 4
        assert model.nr_transitions == 6
        assert model.model_type == stormpy.ModelType.MA
        assert type(model) is stormpy.SparseMA

        assert model.convertible_to_ctmc
        ctmc = model.convert_to_ctmc()
        assert ctmc.nr_states == 4
        assert ctmc.nr_transitions == 6
        assert ctmc.model_type == stormpy.ModelType.CTMC
        assert type(ctmc) is stormpy.SparseCtmc

    def test_initial_states(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        formulas = stormpy.parse_properties_for_prism_program('P=? [ F "one" ]', program)
        model = stormpy.build_model(program, formulas)
        initial_states = model.initial_states
        assert len(initial_states) == 1
        assert 0 in initial_states

    def test_choice_origins(self):
        program, _ = stormpy.parse_jani_model(get_example_path("dtmc", "die.jani"))
        a = stormpy.FlatSet()

        options = stormpy.BuilderOptions()
        options.set_build_with_choice_origins()
        model = stormpy.build_sparse_model_with_options(program, options)
        a = model.choice_origins.get_edge_index_set(3)


class TestSymbolicSylvanModel:
    def test_build_dtmc_from_prism_program(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        model = stormpy.build_symbolic_model(program)
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        assert model.model_type == stormpy.ModelType.DTMC
        assert not model.supports_parameters
        assert type(model) is stormpy.SymbolicSylvanDtmc

    def test_build_dtmc_from_prism_program_formulas(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        prop = 'P=? [F "one"]'
        properties = stormpy.parse_properties_for_prism_program(prop, program, None)
        model = stormpy.build_symbolic_model(program, properties)
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        assert model.model_type == stormpy.ModelType.DTMC
        assert len(model.reward_models) == 0
        assert not model.supports_parameters
        assert type(model) is stormpy.SymbolicSylvanDtmc

    def test_build_dtmc_from_prism_program_reward_formulas(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        prop = 'R=? [F "done"]'
        properties = stormpy.parse_properties_for_prism_program(prop, program, None)
        model = stormpy.build_symbolic_model(program, properties)
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        assert model.model_type == stormpy.ModelType.DTMC
        assert len(model.reward_models) == 1
        assert not model.reward_models["coin_flips"].has_state_rewards
        assert model.reward_models["coin_flips"].has_state_action_rewards
        assert not model.reward_models["coin_flips"].has_transition_rewards
        assert not model.supports_parameters
        assert type(model) is stormpy.SymbolicSylvanDtmc

    def test_reduce_to_state_based_rewards(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        prop = 'R=? [F "done"]'
        properties = stormpy.parse_properties_for_prism_program(prop, program, None)
        model = stormpy.build_symbolic_model(program, properties)
        model.reduce_to_state_based_rewards()
        assert len(model.reward_models) == 1
        assert model.reward_models["coin_flips"].has_state_rewards
        assert not model.reward_models["coin_flips"].has_state_action_rewards
        assert not model.reward_models["coin_flips"].has_transition_rewards

    def test_build_dtmc_from_jani_model(self):
        jani_model, properties = stormpy.parse_jani_model(get_example_path("dtmc", "brp.jani"))
        description = stormpy.SymbolicModelDescription(jani_model)
        constant_definitions = description.parse_constant_definitions("N=16, MAX=2")
        instantiated_jani_model = description.instantiate_constants(constant_definitions).as_jani_model()
        model = stormpy.build_symbolic_model(instantiated_jani_model)
        assert model.nr_states == 677
        assert model.nr_transitions == 867
        assert model.model_type == stormpy.ModelType.DTMC
        assert not model.supports_parameters
        assert type(model) is stormpy.SymbolicSylvanDtmc

    def test_build_mdp(self):
        program = stormpy.parse_prism_program(get_example_path("mdp", "two_dice.nm"))
        formulas = stormpy.parse_properties_for_prism_program('P=? [ F "two" ]', program)
        model = stormpy.build_symbolic_model(program, formulas)
        assert model.nr_states == 169
        assert model.nr_transitions == 435
        assert model.model_type == stormpy.ModelType.MDP
        assert not model.supports_parameters
        assert type(model) is stormpy.SymbolicSylvanMdp

    def test_build_ctmc(self):
        program = stormpy.parse_prism_program(get_example_path("ctmc", "polling2.sm"), True)
        formulas = stormpy.parse_properties_for_prism_program('P=? [ F<=3 "target" ]', program)
        model = stormpy.build_symbolic_model(program, formulas)
        assert model.nr_states == 12
        assert model.nr_transitions == 21
        assert model.model_type == stormpy.ModelType.CTMC
        assert not model.supports_parameters
        assert type(model) is stormpy.SymbolicSylvanCtmc

    def test_build_ma(self):
        program = stormpy.parse_prism_program(get_example_path("ma", "simple.ma"))
        formulas = stormpy.parse_properties_for_prism_program("P=? [ F<=2 s=2 ]", program)
        with pytest.raises(Exception):
            model = stormpy.build_symbolic_model(program, formulas)

    def test_build_ipomdp(self):
        model = stormpy.build_interval_model_from_drn(get_example_path("ipomdp", "tiny-01.drn"))
        assert model.nr_states == 4
        assert model.nr_choices == 5
        assert model.nr_transitions == 8
        assert model.nr_observations == 3

        for transition in model.transition_matrix.row_iter(0, 0):
            if transition.column == 1:
                assert transition.value().lower() == 0.2
                assert transition.value().upper() == 0.7
            elif transition.column == 2:
                assert transition.value().lower() == 0.3
                assert transition.value().upper() == 0.8

        assert model.model_type == stormpy.ModelType.POMDP
        assert type(model) is stormpy.SparseIntervalPomdp

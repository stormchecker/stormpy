import stormpy
from helpers.helper import get_example_path

import math
from configurations import spot


class TestScheduler:

    def test_scheduler_mdp(self):
        program = stormpy.parse_prism_program(get_example_path("mdp", "coin2-2.nm"))
        formulas = stormpy.parse_properties_for_prism_program('Pmin=? [ F "finished" & "all_coins_equal_1"]', program)
        options = stormpy.BuilderOptions(True, True)
        options.set_build_state_valuations()
        options.set_build_choice_labels()
        options.set_build_with_choice_origins()
        model = stormpy.build_sparse_model_with_options(program, options)
        assert model.nr_states == 272
        assert model.nr_transitions == 492
        assert len(model.initial_states) == 1
        initial_state = model.initial_states[0]
        assert initial_state == 0

        result = stormpy.model_checking(model, formulas[0], extract_scheduler=True)
        assert result.has_scheduler
        scheduler = result.scheduler
        assert scheduler.memoryless
        assert scheduler.memory_size == 1
        assert scheduler.deterministic

        for state in model.states:
            choice = scheduler.get_choice(state)
            assert choice.defined
            assert choice.deterministic
            action = choice.get_deterministic_choice()
            assert 0 <= action
            assert action < len(state.actions)
            action = state.actions[action]
            assert action.id < 268 or "done" in action.labels
            distribution = choice.get_choice()
            assert str(distribution).startswith("{[1:")

    def test_scheduler_ma_via_mdp(self):
        program = stormpy.parse_prism_program(get_example_path("ma", "simple.ma"), False, True)
        formulas = stormpy.parse_properties_for_prism_program("Tmin=? [ F s=4 ]", program)
        options = stormpy.BuilderOptions([f.raw_formula for f in formulas])
        options.set_build_state_valuations()
        options.set_build_choice_labels()
        options.set_build_with_choice_origins()
        ma = stormpy.build_sparse_model_with_options(program, options)
        assert ma.nr_states == 5
        assert ma.nr_transitions == 8
        assert ma.model_type == stormpy.ModelType.MA

        # Convert MA to MDP
        mdp, mdp_formulas = stormpy.transform_to_discrete_time_model(ma, formulas)
        assert mdp.nr_states == 5
        assert mdp.nr_transitions == 8
        assert mdp.model_type == stormpy.ModelType.MDP
        assert len(mdp.initial_states) == 1
        initial_state = mdp.initial_states[0]
        assert initial_state == 0

        result = stormpy.model_checking(mdp, mdp_formulas[0], extract_scheduler=True)
        assert math.isclose(result.at(initial_state), 0.08333333333)
        assert result.has_scheduler
        scheduler = result.scheduler
        assert scheduler.memoryless
        assert scheduler.memory_size == 1
        assert scheduler.deterministic
        for state in mdp.states:
            choice = scheduler.get_choice(state)
            assert choice.defined
            assert choice.deterministic
            action = choice.get_deterministic_choice()
            if state.id == 0:
                assert action == 1
            else:
                assert action == 0

    def test_apply_scheduler_mdp(self):
        program = stormpy.parse_prism_program(get_example_path("mdp", "coin2-2.nm"))
        formulas = stormpy.parse_properties_for_prism_program('Pmin=? [ F "finished" & "all_coins_equal_1"]', program)
        model = stormpy.build_model(program, formulas)
        assert model.nr_states == 272
        assert model.nr_transitions == 492
        assert len(model.initial_states) == 1
        initial_state = model.initial_states[0]
        assert initial_state == 0
        result = stormpy.model_checking(model, formulas[0], extract_scheduler=True)
        assert result.has_scheduler
        scheduler = result.scheduler
        assert scheduler.memoryless
        assert scheduler.memory_size == 1
        assert scheduler.deterministic
        assert not scheduler.partial
        intermediate = model.apply_scheduler(scheduler, True)
        assert intermediate.model_type == stormpy.ModelType.DTMC
        assert intermediate.nr_states == 126
        assert intermediate.nr_transitions == 156
        for state in intermediate.states:
            assert len(state.actions) == 1

    @spot
    def test_apply_scheduler_mdp_ltl(self):
        program = stormpy.parse_prism_program(get_example_path("mdp", "slipgrid.nm"))
        properties = stormpy.parse_properties_for_prism_program('Pmax=? [ GF "target" & GF "goal" ]', program)
        mdp = stormpy.build_model(program, properties)
        result = stormpy.model_checking(mdp, properties[0], extract_scheduler=True)
        assert result.has_scheduler
        scheduler = result.scheduler
        assert scheduler.memory_size == 8
        assert scheduler.deterministic
        induced = mdp.apply_scheduler(scheduler)
        assert induced.nr_states == induced.nr_choices

    def test_apply_scheduler_ma(self):
        program = stormpy.parse_prism_program(get_example_path("ma", "simple.ma"), False, True)
        formulas = stormpy.parse_properties_for_prism_program("Tmin=? [ F s=4 ]", program)
        ma = stormpy.build_model(program, formulas)
        assert ma.nr_states == 5
        assert ma.nr_transitions == 8
        assert ma.model_type == stormpy.ModelType.MA
        initial_state = ma.initial_states[0]
        assert initial_state == 0

        result = stormpy.model_checking(ma, formulas[0], extract_scheduler=True)
        assert math.isclose(result.at(initial_state), 0.08333333333)
        assert result.has_scheduler
        scheduler = result.scheduler
        assert scheduler.memoryless
        assert scheduler.memory_size == 1
        assert scheduler.deterministic
        intermediate = ma.apply_scheduler(scheduler)
        assert intermediate.model_type == stormpy.ModelType.MA
        assert intermediate.nr_states == 3
        assert intermediate.nr_transitions == 4
        for state in intermediate.states:
            assert len(state.actions) == 1

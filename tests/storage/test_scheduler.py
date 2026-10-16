import stormpy
from helpers.helper import get_example_path

import math
from configurations import spot


class TestScheduler:
    def test_scheduler_mdp(self):
        program = stormpy.parse_prism_program(get_example_path("mdp", "coin2-2.nm"))
        formula = stormpy.parse_property('Pmin=? [ F "finished" & "all_coins_equal_1"]', program)
        options = stormpy.BuilderOptions(build_full=True)
        model = stormpy.build_model(program, options=options)
        assert model.nr_states == 272
        assert model.nr_transitions == 492
        assert model.nr_choices == 400
        assert len(model.initial_states) == 1
        initial_state = model.initial_states[0]
        assert initial_state == 0

        result = stormpy.model_checking(model, formula, extract_scheduler=True)
        assert result.has_scheduler
        scheduler = result.get_scheduler()
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
            distribution = choice.get_choice_as_distribution()
            assert str(distribution).startswith("{[1:")

    def test_scheduler_ma_via_mdp(self):
        program = stormpy.parse_prism_program(get_example_path("ma", "simple.ma"))
        formula = stormpy.parse_property("Tmin=? [ F s=4 ]", program)
        options = stormpy.BuilderOptions(formula)
        options.set_build_state_valuations()
        options.set_build_choice_labels()
        options.set_build_choice_origins()
        ma = stormpy.build_model(program, options=options)
        assert ma.nr_states == 5
        assert ma.nr_transitions == 8
        assert ma.model_type == stormpy.models.ModelType.MA

        # Convert MA to MDP
        mdp, mdp_formulas = stormpy.transform_to_discrete_time_model(ma, formula)
        assert mdp.nr_states == 5
        assert mdp.nr_transitions == 8
        assert mdp.model_type == stormpy.models.ModelType.MDP
        assert len(mdp.initial_states) == 1
        initial_state = mdp.initial_states[0]
        assert initial_state == 0

        result = stormpy.model_checking(mdp, mdp_formulas[0], extract_scheduler=True)
        assert math.isclose(result[initial_state], 0.08333333333)
        assert result.has_scheduler
        scheduler = result.get_scheduler()
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
        formula = stormpy.parse_property('Pmin=? [ F "finished" & "all_coins_equal_1"]', program)
        model = stormpy.build_model(program, formula)
        assert model.nr_states == 272
        assert model.nr_transitions == 492
        assert len(model.initial_states) == 1
        initial_state = model.initial_states[0]
        assert initial_state == 0
        result = stormpy.model_checking(model, formula, extract_scheduler=True)
        assert result.has_scheduler
        scheduler = result.get_scheduler()
        assert scheduler.memoryless
        assert scheduler.memory_size == 1
        assert scheduler.deterministic
        assert not scheduler.partial
        intermediate = model.apply_scheduler(scheduler, True)
        assert intermediate.model_type == stormpy.models.ModelType.DTMC
        assert intermediate.nr_states == 126
        assert intermediate.nr_transitions == 156
        for state in intermediate.states:
            assert len(state.actions) == 1

    @spot
    def test_apply_scheduler_mdp_ltl(self):
        program = stormpy.parse_prism_program(get_example_path("mdp", "slipgrid.nm"))
        prop = stormpy.parse_property('Pmax=? [ GF "target" & GF "goal" ]', program)
        mdp = stormpy.build_model(program, prop)
        result = stormpy.model_checking(mdp, prop, extract_scheduler=True)
        assert result.has_scheduler
        scheduler = result.get_scheduler()
        assert scheduler.memory_size == 8
        assert scheduler.deterministic
        induced = mdp.apply_scheduler(scheduler)
        assert induced.nr_states == induced.nr_choices

    def test_scheduler_to_str(self):
        program = stormpy.parse_prism_program(get_example_path("mdp", "coin2-2.nm"))
        formula = stormpy.parse_property('Pmin=? [ F "finished" & "all_coins_equal_1"]', program)
        model = stormpy.build_model(program, formula)
        result = stormpy.model_checking(model, formula, extract_scheduler=True)
        scheduler = result.get_scheduler()
        s = scheduler.to_str(model)
        assert isinstance(s, str)
        assert len(s) > 0

    def test_scheduler_get_memoryless_for_memory_state(self):
        program = stormpy.parse_prism_program(get_example_path("mdp", "coin2-2.nm"))
        formula = stormpy.parse_property('Pmin=? [ F "finished" & "all_coins_equal_1"]', program)
        model = stormpy.build_model(program, formula)
        result = stormpy.model_checking(model, formula, extract_scheduler=True)
        scheduler = result.get_scheduler()
        assert scheduler.memoryless
        assert scheduler.memory_size == 1
        memoryless = scheduler.get_memoryless_scheduler_for_memory_state(0)
        assert memoryless.memoryless
        assert memoryless.memory_size == 1
        assert memoryless.deterministic

    def test_scheduler_cast_to_exact_interval_datatype(self):
        program = stormpy.parse_prism_program(get_example_path("mdp", "coin2-2.nm"))
        formula = stormpy.parse_property('Pmin=? [ F "finished" & "all_coins_equal_1"]', program)
        model = stormpy.build_model(program, formula)
        result = stormpy.model_checking(model, formula, extract_scheduler=True)
        scheduler = result.get_scheduler()
        assert scheduler.deterministic
        exact_interval_scheduler = scheduler.to_value_type(stormpy.RationalInterval)
        assert exact_interval_scheduler.deterministic
        assert exact_interval_scheduler.memoryless

    def test_apply_scheduler_ma(self):
        program = stormpy.parse_prism_program(get_example_path("ma", "simple.ma"))
        formula = stormpy.parse_property("Tmin=? [ F s=4 ]", program)
        ma = stormpy.build_model(program, formula)
        assert ma.nr_states == 5
        assert ma.nr_transitions == 8
        assert ma.model_type == stormpy.models.ModelType.MA
        initial_state = ma.initial_states[0]
        assert initial_state == 0

        result = stormpy.model_checking(ma, formula, extract_scheduler=True)
        assert math.isclose(result[initial_state], 0.08333333333)
        assert result.has_scheduler
        scheduler = result.get_scheduler()
        assert scheduler.memoryless
        assert scheduler.memory_size == 1
        assert scheduler.deterministic
        intermediate = ma.apply_scheduler(scheduler)
        assert intermediate.model_type == stormpy.models.ModelType.MA
        assert intermediate.nr_states == 3
        assert intermediate.nr_transitions == 4
        for state in intermediate.states:
            assert len(state.actions) == 1

import pytest

import stormpy

from configurations import pomdp

from helpers.helper import get_example_path

import math


@pomdp
@pytest.mark.skip(reason="Belief exploration bindings removed after revision in Storm (#1004); new bindings pending")
class TestPomdpQuantitative:
    def test_underapprox_mc_maze_pmax(self):
        program = stormpy.parse_prism_program(get_example_path("pomdp", "maze_2.prism"))
        formula = stormpy.parse_property('Pmax=? [ !"bad" U "goal" ]', program)
        model = stormpy.build_model(program, formula)
        model = stormpy.pomdp.make_canonic(model)
        options = stormpy.pomdp.BeliefExplorationModelCheckerOptionsDouble(False, True)
        options.use_state_elimination_cutoff = False
        options.size_threshold_init = 10
        options.use_clipping = False
        belmc = stormpy.pomdp.BeliefExplorationModelCheckerDouble(model, options)
        result = belmc.check(formula.get_raw_formula(), [])
        assert math.isclose(result.lower_bound, 0.35198, abs_tol=10**-4)
        assert math.isinf(result.upper_bound)
        assert result.induced_mc_from_scheduler.nr_states == 10
        assert result.induced_mc_from_scheduler.nr_transitions == 23

    def test_underapprox_mc_maze_rmin(self):
        program = stormpy.parse_prism_program(get_example_path("pomdp", "maze_2.prism"))
        formula = stormpy.parse_property('Rmin=? [ F "goal" ]', program)
        model = stormpy.build_model(program, formula)
        model = stormpy.pomdp.make_canonic(model)
        options = stormpy.pomdp.BeliefExplorationModelCheckerOptionsDouble(False, True)
        options.use_state_elimination_cutoff = False
        options.size_threshold_init = 10
        options.use_clipping = False
        belmc = stormpy.pomdp.BeliefExplorationModelCheckerDouble(model, options)
        result = belmc.check(formula.get_raw_formula(), [])
        assert math.isinf(result.lower_bound)
        assert math.isclose(result.upper_bound, 12.27043, abs_tol=10**-4)
        assert result.induced_mc_from_scheduler.nr_states == 9
        assert result.induced_mc_from_scheduler.nr_transitions == 17

    def test_underapprox_mc_cmaze_rmin(self):
        program = stormpy.parse_prism_program(get_example_path("pomdp", "maze-concise.prism"))
        formula = stormpy.parse_property('R{"steps"}min=? [F ((x = 2) & (y = 0))]', program)
        model = stormpy.build_model(program, formula)
        model = stormpy.pomdp.make_canonic(model)
        options = stormpy.pomdp.BeliefExplorationModelCheckerOptionsDouble(False, True)
        options.use_state_elimination_cutoff = False
        options.size_threshold_init = 10
        options.use_clipping = False
        belmc = stormpy.pomdp.BeliefExplorationModelCheckerDouble(model, options)
        result = belmc.check(formula.get_raw_formula(), [])
        assert math.isinf(result.lower_bound)
        assert math.isclose(result.upper_bound, 19.78127, abs_tol=10**-4)
        assert result.induced_mc_from_scheduler.nr_states == 9
        assert result.induced_mc_from_scheduler.nr_transitions == 15

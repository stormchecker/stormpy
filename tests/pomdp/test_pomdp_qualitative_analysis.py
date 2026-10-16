import stormpy

from configurations import pomdp

from helpers.helper import get_example_path


@pomdp
class TestPomdpQualitative:
    def test_winning_region(self):
        program = stormpy.parse_prism_program(get_example_path("pomdp", "maze_2.prism"))
        formulas = stormpy.parse_properties('Pmax=? [ !"bad" U "goal" ]', program)
        model = stormpy.pomdp.make_canonic(stormpy.build_model(program, formulas))
        formula = formulas[0].get_raw_formula()
        model = stormpy.pomdp.prepare_pomdp_for_qualitative_search_Double(model, formula)
        options = stormpy.pomdp.IterativeQualitativeSearchOptions()
        solver = stormpy.pomdp.create_iterative_qualitative_search_solver_Double(stormpy.environments.default(model), model, formula, options)
        assert isinstance(solver, stormpy.pomdp.IterativeQualitativeSearchSolverDouble)
        solver.compute_winning_region(10)
        assert isinstance(solver.last_winning_region, stormpy.pomdp.BeliefSupportWinningRegion)

import stormpy
from helpers.helper import get_example_path

from configurations import spot

import math


class TestModelChecking:
    def test_model_checking_prism_dtmc(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        formulas = stormpy.parse_properties_for_prism_program('P=? [ F "one" ]', program)
        model = stormpy.build_model(program, formulas)
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        assert len(model.initial_states) == 1
        initial_state = model.initial_states[0]
        assert initial_state == 0
        result = stormpy.model_checking(model, formulas[0])
        assert math.isclose(result.at(initial_state), 1 / 6)

    @spot
    def test_model_checking_prism_dtmc_ltl(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        formulas = stormpy.parse_properties_for_prism_program('P=? [ FG "one" ]', program)
        model = stormpy.build_model(program, formulas)
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        assert len(model.initial_states) == 1
        initial_state = model.initial_states[0]
        assert initial_state == 0
        result = stormpy.model_checking(model, formulas[0])
        assert math.isclose(result.at(initial_state), 1 / 6)

    def test_model_checking_prism_mdp(self):
        program = stormpy.parse_prism_program(get_example_path("mdp", "coin2-2.nm"))
        formulas = stormpy.parse_properties_for_prism_program('Pmin=? [ F "finished" & "all_coins_equal_1"]', program)
        model = stormpy.build_model(program, formulas)
        assert model.nr_states == 272
        assert model.nr_transitions == 492
        assert len(model.initial_states) == 1
        initial_state = model.initial_states[0]
        assert initial_state == 0
        result = stormpy.model_checking(model, formulas[0])
        assert math.isclose(result.at(initial_state), 49 / 128, rel_tol=1e-5)

    def test_model_checking_interval_mdp(self):
        model = stormpy.build_interval_model_from_drn(get_example_path("imdp", "tiny-01.drn"))
        formulas = stormpy.parse_properties('Pmax=? [ F "target"];Pmin=? [ F "target"]')
        initial_state = model.initial_states[0]
        assert initial_state == 0

        env = stormpy.Environment()
        env.solver_environment.minmax_solver_environment.method = stormpy.MinMaxMethod.value_iteration

        task = stormpy.CheckTask(formulas[0].raw_formula, only_initial_states=True)
        task.set_produce_schedulers()
        # Compute maximal robust
        task.set_robust_uncertainty(True)
        result = stormpy.check_interval_mdp(model, task, env)
        assert math.isclose(result.at(initial_state), 0.4, rel_tol=1e-4)
        # Compute maximal non-robust
        task.set_robust_uncertainty(False)
        result = stormpy.check_interval_mdp(model, task, env)
        assert math.isclose(result.at(initial_state), 0.5, rel_tol=1e-4)

        task = stormpy.CheckTask(formulas[1].raw_formula, only_initial_states=True)
        task.set_produce_schedulers()
        # Compute minimal robust
        task.set_robust_uncertainty(True)
        result = stormpy.check_interval_mdp(model, task, env)
        assert math.isclose(result.at(initial_state), 0.5, rel_tol=1e-4)
        # Compute minimal non-robust
        task.set_robust_uncertainty(False)
        result = stormpy.check_interval_mdp(model, task, env)
        assert math.isclose(result.at(initial_state), 0.4, rel_tol=1e-4)

    def test_model_checking_jani_dtmc(self):
        jani_model, formulas = stormpy.parse_jani_model(get_example_path("dtmc", "die.jani"))
        formulas = stormpy.eliminate_reward_accumulations(jani_model, formulas)
        assert len(formulas) == 2
        model = stormpy.build_model(jani_model, formulas)
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        assert len(model.initial_states) == 1
        initial_state = model.initial_states[0]
        assert initial_state == 0
        result = stormpy.model_checking(model, formulas[0])
        assert math.isclose(result.at(initial_state), 1 / 6)
        result = stormpy.model_checking(model, formulas[1])
        assert math.isclose(result.at(initial_state), 11 / 3)

    def test_model_checking_dtmc_all_labels(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        formulas = stormpy.parse_properties_for_prism_program('P=? [ F "one" ]', program)
        model = stormpy.build_model(program)
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        assert len(model.initial_states) == 1
        initial_state = model.initial_states[0]
        assert initial_state == 0
        result = stormpy.model_checking(model, formulas[0])
        assert math.isclose(result.at(initial_state), 1 / 6)
        formulas = stormpy.parse_properties_for_prism_program('P=? [ F "two" ]', program)
        result = stormpy.model_checking(model, formulas[0])
        assert math.isclose(result.at(initial_state), 1 / 6)

    def test_model_checking_all_dtmc(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        formulas = stormpy.parse_properties_for_prism_program('P=? [ F "one" ]', program)
        model = stormpy.build_model(program, formulas)
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        result = stormpy.model_checking(model, formulas[0])
        assert result.result_for_all_states
        reference = [1 / 6, 1 / 3, 0, 2 / 3, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        assert all(map(math.isclose, result.get_values(), reference))

    def test_model_checking_only_initial(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        formulas = stormpy.parse_properties_for_prism_program('Pmax=? [F{"coin_flips"}<=3 "one"]', program)
        model = stormpy.build_model(program, formulas)
        assert len(model.initial_states) == 1
        initial_state = model.initial_states[0]
        assert initial_state == 0
        result = stormpy.model_checking(model, formulas[0], only_initial_states=True)
        assert not result.result_for_all_states
        assert math.isclose(result.at(initial_state), 1 / 8)

    def test_model_checking_prob01(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        formulaPhi = stormpy.parse_properties("true")[0]
        formulaPsi = stormpy.parse_properties('"six"')[0]
        model = stormpy.build_model(program, [formulaPsi])
        phiResult = stormpy.model_checking(model, formulaPhi)
        phiStates = phiResult.get_truth_values()
        assert phiStates.number_of_set_bits() == model.nr_states
        psiResult = stormpy.model_checking(model, formulaPsi)
        psiStates = psiResult.get_truth_values()
        assert psiStates.number_of_set_bits() == 1
        (prob0, prob1) = stormpy.compute_prob01_states(model, phiStates, psiStates)
        assert prob0.number_of_set_bits() == 9
        assert prob1.number_of_set_bits() == 1
        labelprop = stormpy.Property("cora", formulaPsi.raw_formula)
        result = stormpy.model_checking(model, labelprop)
        assert result.get_truth_values().number_of_set_bits() == 1

        program = stormpy.parse_prism_program(get_example_path("mdp", "coin2-2.nm"))
        formulas = stormpy.parse_properties_for_prism_program('Pmin=? [ F "finished" & "all_coins_equal_1"]', program)
        model = stormpy.build_model(program, formulas)
        prob0, prob1 = stormpy.prob01min_states(model, formulas[0].raw_formula.subformula)
        assert prob0.number_of_set_bits() == 94
        assert prob1.number_of_set_bits() == 15
        prob0, prob1 = stormpy.prob01max_states(model, formulas[0].raw_formula.subformula)
        assert prob0.number_of_set_bits() == 83
        assert prob1.number_of_set_bits() == 18

    def test_model_checking_ctmc(self):
        model = stormpy.build_model_from_drn(get_example_path("ctmc", "dft.drn"))
        formulas = stormpy.parse_properties('T=? [ F "failed" ]')
        assert model.nr_states == 16
        assert model.nr_transitions == 33
        assert len(model.initial_states) == 1
        initial_state = model.initial_states[0]
        assert initial_state == 1
        result = stormpy.model_checking(model, formulas[0])
        assert math.isclose(result.at(initial_state), 4.166666667)

    def test_filter(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        formulas = stormpy.parse_properties_for_prism_program('P=? [ F "one" ]', program)
        model = stormpy.build_model(program, formulas)
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        assert len(model.initial_states) == 1
        initial_state = model.initial_states[0]
        assert initial_state == 0
        result = stormpy.model_checking(model, formulas[0])
        assert math.isclose(result.at(initial_state), 1 / 6)
        filter = stormpy.create_filter_initial_states_sparse(model)
        result.filter(filter)
        assert result.min == result.max
        assert math.isclose(result.min, 1 / 6)

    def test_model_checking_prism_dd_dtmc(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        formulas = stormpy.parse_properties_for_prism_program('P=? [ F "one" ]', program)
        model = stormpy.build_symbolic_model(program, formulas)
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        result = stormpy.check_model_dd(model, formulas[0])
        assert type(result) is stormpy.SymbolicQuantitativeCheckResult
        filter = stormpy.create_filter_initial_states_symbolic(model)
        result.filter(filter)
        assert result.min == result.max
        assert math.isclose(result.min, 1 / 6, rel_tol=1e-6)

    def test_model_checking_prism_hybrid_dtmc(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        formulas = stormpy.parse_properties_for_prism_program('P=? [ F "one" ]', program)
        model = stormpy.build_symbolic_model(program, formulas)
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        result = stormpy.check_model_hybrid(model, formulas[0])
        assert type(result) is stormpy.HybridQuantitativeCheckResult
        values = result.get_values()
        assert len(values) == 3
        assert math.isclose(values[0], 1 / 6)

    def test_compute_expected_number_of_visits(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        model = stormpy.build_model(program)
        environment = stormpy.Environment()
        result = stormpy.compute_expected_number_of_visits(environment, model)
        assert result.at(0) == 1
        assert math.isclose(result.at(1), 2.0 / 3)

    def test_compute_steady_state_distribution(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        model = stormpy.build_model(program)
        environment = stormpy.Environment()
        result = stormpy.compute_steady_state_distribution(environment, model)
        values = result.get_values()
        assert len(values) == 13
        sorted(values)
        for i in range(7):
            assert values[i] == 0
        for i in range(7, 13):
            assert math.isclose(values[i], 1.0 / 6)

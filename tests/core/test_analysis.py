import pytest
import stormpy
from stormpy.exceptions import StormError

from helpers.helper import get_example_path


class TestAnalysis:
    def test_topological_sort(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        model = stormpy.build_model(program)
        order = stormpy.topological_sort(model)
        assert sorted(order) == list(range(model.nr_states))
        backward = stormpy.topological_sort(model, forward=False, initial=[7])
        assert len(backward) > 0

    def test_create_weight_vector_checker_unsupported(self):
        program = stormpy.parse_prism_program(get_example_path("mdp", "multiobjective1.nm"))
        properties = stormpy.parse_properties('multi(Pmax=? [ F<=3 s=2 ],R{"rew"}max=? [ F s=2 ])', program)
        model = stormpy.build_model[stormpy.Interval](program, properties)
        with pytest.raises(StormError):
            stormpy.create_weight_vector_checker(model, properties[0])


class TestProb01:
    def test_prob01_dtmc(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        properties = stormpy.parse_properties('P=? [F "six"]', program)
        model = stormpy.build_model(program, properties)
        prob0, prob1 = stormpy.compute_prob01_states(model, properties[0])
        assert prob0.number_of_set_bits() == 9
        assert prob1.number_of_set_bits() == 1
        # Same as the developer function with all states as phi states
        psi_states = stormpy.model_checking(model, properties[0].get_raw_formula().subformula.subformula).get_truth_values_vector()
        assert (prob0, prob1) == tuple(stormpy.developer.perform_prob01(model, stormpy.BitVector(model.nr_states, True), psi_states))
        # Path formula without probability operator
        formula = properties[0].get_raw_formula().subformula
        assert stormpy.compute_prob01_states(model, formula) == (prob0, prob1)

    def test_prob01_until(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        properties = stormpy.parse_properties('P=? [s<7 U "six"]', program)
        model = stormpy.build_model(program, properties)
        phi_states = stormpy.model_checking(model, properties[0].get_raw_formula().subformula.left_subformula).get_truth_values_vector()
        psi_states = stormpy.model_checking(model, properties[0].get_raw_formula().subformula.right_subformula).get_truth_values_vector()
        expected = tuple(stormpy.developer.perform_prob01(model, phi_states, psi_states))
        assert stormpy.compute_prob01_states(model, properties[0]) == expected

    def test_prob01_mdp(self):
        program = stormpy.parse_prism_program(get_example_path("mdp", "coin2-2.nm"))
        properties = stormpy.parse_properties('Pmin=? [ F "finished" & "all_coins_equal_1"];Pmax=? [ F "finished" & "all_coins_equal_1"]', program)
        model = stormpy.build_model(program, properties)
        prob0_min, prob1_min = stormpy.compute_prob01_states(model, properties[0])
        assert prob0_min.number_of_set_bits() == 94
        assert prob1_min.number_of_set_bits() == 15
        prob0_max, prob1_max = stormpy.compute_prob01_states(model, properties[1])
        assert prob0_max.number_of_set_bits() == 83
        assert prob1_max.number_of_set_bits() == 18

    def test_prob01_errors(self):
        program = stormpy.parse_prism_program(get_example_path("mdp", "coin2-2.nm"))
        properties = stormpy.parse_properties('P=? [ F "finished"];Pmax=? [ F<=5 "finished"]', program)
        model = stormpy.build_model(program, properties)
        with pytest.raises(StormError, match="optimization direction"):
            stormpy.compute_prob01_states(model, properties[0])
        # Path formulas have no optimization direction
        with pytest.raises(StormError, match="optimization direction"):
            stormpy.compute_prob01_states(model, properties[0].get_raw_formula().subformula)
        with pytest.raises(StormError, match="unbounded"):
            stormpy.compute_prob01_states(model, properties[1])

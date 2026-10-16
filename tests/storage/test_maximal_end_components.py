import stormpy
from helpers.helper import get_example_path


class TestMaximalEndComponents:
    def test_create_decomposition_simple(self):
        program = stormpy.parse_prism_program(get_example_path("mdp", "two_dice.nm"))
        model = stormpy.build_model(program)

        decomposition = stormpy.datastructures.MaximalEndComponentDecomposition(model)
        assert decomposition.size == 36
        for mec in decomposition:
            assert mec.size == 1
            for state, choices in mec:
                assert 133 <= state <= 168
                assert len(choices) == 2

    def test_create_decomposition(self):
        program = stormpy.parse_prism_program(get_example_path("mdp", "maze_2.nm"))
        model = stormpy.build_model(program)

        decomposition = stormpy.datastructures.get_maximal_end_components(model)
        assert decomposition.size == 2
        matrix = model.transition_matrix
        for mec in decomposition:
            if mec.size == 1:
                for state_id, choices in mec:
                    assert state_id == 14
                    assert 53 in choices
                    state = model.states[state_id]
                    assert state.id == state_id
                    offset = matrix.get_row_group_start(state_id)
                    for choice_id in choices:
                        action = state.actions[choice_id - offset]
                        assert action.id == 0
                        assert len(action.transitions) == 1
                        for transition in action.transitions:
                            assert transition.value == 1
                            assert transition.column == 14

            else:
                assert mec.size == 13
                for state_id, choices in mec:
                    state = model.states[state_id]
                    assert state.id == state_id
                    offset = matrix.get_row_group_start(state_id)
                    assert len(choices) == 3 if state_id == 10 else len(choices) == 4
                    for choice_id in choices:
                        action = state.actions[choice_id - offset]
                        assert action.id in [0, 1, 2, 3]
                        for transition in action.transitions:
                            assert transition.value == 1
                            assert 1 <= transition.column <= 13

    def test_create_exact_interval_decomposition(self):
        model = stormpy.build_model_from_drn[stormpy.RationalInterval](get_example_path("imdp", "tiny-01.drn"))
        assert type(model) is stormpy.models.SparseMdp[stormpy.RationalInterval]
        assert model.nr_states == 3

        decomposition = stormpy.datastructures.get_maximal_end_components(model)
        assert decomposition.size == 2
        for mec in decomposition:
            assert mec.size == 1
            for state_id, choices in mec:
                assert state_id in [1, 2]


class TestECElimination:
    def test_elimination_interval(self):
        program = stormpy.parse_prism_program(get_example_path("mdp", "two_dice.nm"))
        formula = stormpy.parse_property('P=? [ F "two" ]', program)
        model = stormpy.build_model(program, formula)
        transformer = stormpy.developer.AddUncertainty[float](model)
        interval_model = transformer.transform(0.01)
        assert type(interval_model) is stormpy.models.SparseMdp[stormpy.Interval]
        subsystem = stormpy.datastructures.BitVector(interval_model.nr_states, True)
        possible_ec_rows = stormpy.datastructures.BitVector(interval_model.nr_choices, True)
        add_sink_rows = subsystem
        result = stormpy.developer.EndComponentEliminator[stormpy.Interval].transform(
            interval_model.transition_matrix, subsystem, possible_ec_rows, add_sink_rows, True
        )
        assert result.matrix.nr_rows == 218
        assert result.matrix.nr_columns == interval_model.nr_states
        assert result.sink_rows.get_number_of_set_bits() == 36

    def test_elimination_exact_interval(self):
        program = stormpy.parse_prism_program(get_example_path("mdp", "two_dice.nm"))
        formula = stormpy.parse_property('P=? [ F "two" ]', program)
        model = stormpy.build_model[stormpy.Rational](program, formula)
        transformer = stormpy.developer.AddUncertainty[stormpy.Rational](model)
        exact_interval_model = transformer.transform(stormpy.Rational("1/100"))
        assert type(exact_interval_model) is stormpy.models.SparseMdp[stormpy.RationalInterval]
        subsystem = stormpy.datastructures.BitVector(exact_interval_model.nr_states, True)
        possible_ec_rows = stormpy.datastructures.BitVector(exact_interval_model.nr_choices, True)
        add_sink_rows = subsystem
        result = stormpy.developer.EndComponentEliminator[stormpy.RationalInterval].transform(
            exact_interval_model.transition_matrix, subsystem, possible_ec_rows, add_sink_rows, True
        )
        assert result.matrix.nr_rows == 218
        assert result.matrix.nr_columns == exact_interval_model.nr_states
        assert result.sink_rows.get_number_of_set_bits() == 36

import stormpy
from helpers.helper import get_example_path


class TestMaximalEndComponents:
    def test_create_decomposition_simple(self):
        program = stormpy.parse_prism_program(get_example_path("mdp", "two_dice.nm"))
        model = stormpy.build_model(program)

        decomposition = stormpy.MaximalEndComponentDecomposition_double(model)
        assert decomposition.size == 36
        for mec in decomposition:
            assert mec.size == 1
            for state, choices in mec:
                assert 133 <= state <= 168
                assert len(choices) == 2

    def test_create_decomposition(self):
        program = stormpy.parse_prism_program(get_example_path("mdp", "maze_2.nm"))
        model = stormpy.build_model(program)

        decomposition = stormpy.get_maximal_end_components(model)
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
                            assert transition.value() == 1
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
                            assert transition.value() == 1
                            assert 1 <= transition.column <= 13

    def test_create_exact_interval_decomposition(self):
        model = stormpy.build_exact_interval_model_from_drn(get_example_path("imdp", "tiny-01.drn"))
        assert type(model) is stormpy.SparseRationalIntervalMdp
        assert model.nr_states == 3

        decomposition = stormpy.get_maximal_end_components(model)
        assert decomposition.size == 2
        for mec in decomposition:
            assert mec.size == 1
            for state_id, choices in mec:
                assert state_id in [1, 2]

import stormpy
from helpers.helper import get_example_path

import math
import gc

import pytest


class TestMatrix:
    @pytest.mark.parametrize("value_type", [float, stormpy.Rational, stormpy.RationalFunction, stormpy.Interval, stormpy.RationalInterval])
    def test_entry_value_property(self, value_type):
        if value_type is stormpy.RationalFunction:
            first, second = [stormpy.RationalFunction(stormpy.Polynomial(stormpy.RationalFunctionCoefficient(value))) for value in (1, 2)]
        elif value_type is stormpy.RationalInterval:
            first, second = [stormpy.RationalInterval(stormpy.Rational(value)) for value in (1, 2)]
        else:
            first, second = [value_type(value) for value in (1, 2)]
        builder = stormpy.datastructures.SparseMatrixBuilder[value_type](rows=1, columns=1)
        builder.add_next_value(0, 0, first)
        matrix = builder.build()
        entry = next(iter(matrix))
        saved_value = entry.value
        assert saved_value == entry.get_value() == first
        entry.value = second
        assert next(iter(matrix)).value == second
        assert saved_value == first
        entry.set_value(first)
        assert entry.value == first
        del entry, matrix
        gc.collect()
        assert saved_value == first

    def test_matrix(self):
        model = stormpy.build_model_from_explicit(get_example_path("dtmc", "die.tra"), get_example_path("dtmc", "die.lab"))
        matrix = model.transition_matrix
        assert type(matrix) is stormpy.datastructures.SparseMatrix[float]
        assert matrix.nr_rows == model.nr_states
        assert matrix.nr_columns == model.nr_states
        assert matrix.nr_entries == 20
        assert matrix.nr_entries == model.nr_transitions
        for e in matrix:
            assert e.value == 0.5 or e.value == 0 or (e.value == 1 and e.column > 6)

    def test_backward_matrix(self):
        model = stormpy.build_model_from_explicit(get_example_path("dtmc", "die.tra"), get_example_path("dtmc", "die.lab"))
        matrix = model.backward_transition_matrix
        assert type(matrix) is stormpy.datastructures.SparseMatrix[float]
        assert matrix.nr_rows == model.nr_states
        assert matrix.nr_columns == model.nr_states
        assert matrix.nr_entries == 20
        assert matrix.nr_entries == model.nr_transitions
        for e in matrix:
            assert e.value == 0.5 or e.value == 0 or (e.value == 1 and e.column > 6)

    def test_matrix_row_groups(self):
        model = stormpy.build_model_from_explicit(get_example_path("mdp", "two_dice.tra"), get_example_path("mdp", "two_dice.lab"))
        matrix = model.transition_matrix
        assert type(matrix) is stormpy.datastructures.SparseMatrix[float]
        assert matrix.nr_rows == 254
        assert matrix.nr_columns == model.nr_states
        assert matrix.nr_entries == 436
        assert matrix.nr_entries == model.nr_transitions
        i = 0
        for x in range(0, 8):
            for group in range(x * 12, x * 12 + 7):
                for row in matrix.get_rows_for_group(group):
                    assert row == i
                    i += 1
            for group in range(x * 12 + 7, x * 12 + 12):
                for row in matrix.get_rows_for_group(group):
                    assert row == i
                    i += 1
        for e in matrix:
            assert e.value == 0.5 or e.value == 0 or (e.value == 1 and e.column > 6)

    def test_change_matrix(self):
        model = stormpy.build_model_from_explicit(get_example_path("dtmc", "die.tra"), get_example_path("dtmc", "die.lab"))
        matrix = model.transition_matrix
        for e in matrix:
            assert e.value == 0.5 or e.value == 0 or e.value == 1
        i = 0
        for e in matrix:
            e.value = i
            i += 0.1
        i = 0
        for e in matrix:
            assert e.value == i
            i += 0.1

    def test_change_matrix_modelchecking(self):
        model = stormpy.build_model_from_explicit(get_example_path("dtmc", "die.tra"), get_example_path("dtmc", "die.lab"))
        matrix = model.transition_matrix
        # Check matrix
        for e in matrix:
            assert e.value == 0.5 or e.value == 0 or e.value == 1
        # First model checking
        formula = stormpy.parse_property('P=? [ F "one" ]')
        result = stormpy.model_checking(model, formula)
        resValue = result[model.initial_states[0]]
        assert math.isclose(resValue, 0.16666666666666663)

        # Change probabilities
        i = 0
        for e in matrix:
            if e.value == 0.5:
                if i % 2 == 0:
                    e.value = 0.3
                else:
                    e.value = 0.7
                i += 1
        for e in matrix:
            assert e.value == 0.3 or e.value == 0.7 or e.value == 1 or e.value == 0
        # Second model checking
        result = stormpy.model_checking(model, formula)
        resValue = result[model.initial_states[0]]
        assert math.isclose(resValue, 0.06923076923076932)

        # Change probabilities again
        for state in model.states:
            for action in state.actions:
                for transition in action.transitions:
                    if transition.value == 0.3:
                        transition.value = 0.8
                    elif transition.value == 0.7:
                        transition.value = 0.2
        # Third model checking
        result = stormpy.model_checking(model, formula)
        resValue = result[model.initial_states[0]]
        assert math.isclose(resValue, 0.3555555555555556)

    def test_change_parametric_matrix_modelchecking(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        formula = stormpy.parse_property("P=? [ F s=5 ]", program)
        model = stormpy.build_model[stormpy.RationalFunction](program, formula)
        initial_state = model.initial_states[0]
        assert initial_state == 0
        matrix = model.transition_matrix
        # Check matrix
        one_pol = stormpy.RationalFunctionCoefficient(1)
        one_pol = stormpy.Polynomial(one_pol)
        one = stormpy.RationalFunction(one_pol, one_pol)
        for e in matrix:
            assert e.value == one or len(e.value.gather_variables()) > 0
        # First model checking
        result = stormpy.model_checking(model, formula)
        ratFunc = result[initial_state]
        assert len(ratFunc.gather_variables()) > 0

        # Change probabilities
        two_pol = stormpy.RationalFunctionCoefficient(2)
        two_pol = stormpy.Polynomial(two_pol)
        new_val = stormpy.RationalFunction(one_pol, two_pol)
        for e in matrix:
            if len(e.value.gather_variables()) > 0:
                e.value = new_val
        for e in matrix:
            assert e.value == new_val or e.value == one
        # Second model checking
        result = stormpy.model_checking(model, formula)
        ratFunc = result[initial_state]
        assert len(ratFunc.gather_variables()) == 0

    def test_submatrix(self):
        model = stormpy.build_model_from_explicit(get_example_path("dtmc", "die.tra"), get_example_path("dtmc", "die.lab"))
        matrix = model.transition_matrix
        assert matrix.nr_rows == 13
        assert matrix.nr_columns == 13
        assert matrix.nr_entries == 20
        assert matrix.nr_entries == model.nr_transitions
        for e in matrix:
            assert e.value == 0.5 or e.value == 0 or (e.value == 1 and e.column > 6)

        row_constraint = stormpy.datastructures.BitVector(13, [0, 1, 3, 4, 7, 8, 9])
        submatrix = matrix.get_submatrix(True, row_constraint, row_constraint)
        assert submatrix.nr_rows == 7
        assert submatrix.nr_columns == 7
        assert submatrix.nr_entries == 10
        for e in submatrix:
            assert e.value == 0.5 or e.value == 0 or (e.value == 1 and e.column > 3)

    def test_submatrix_no_groups(self):
        model = stormpy.build_model_from_explicit(get_example_path("mdp", "two_dice.tra"), get_example_path("mdp", "two_dice.lab"))
        matrix = model.transition_matrix
        assert type(matrix) is stormpy.datastructures.SparseMatrix[float]
        assert matrix.nr_rows == 254
        assert matrix.nr_columns == model.nr_states
        assert matrix.nr_entries == 436
        assert matrix.nr_entries == model.nr_transitions

        assert matrix.nr_rows != matrix.nr_columns

        row_constraint = stormpy.datastructures.BitVector(254, [0, 1, 3, 4, 7, 8, 9])
        submatrix = matrix.get_submatrix(False, row_constraint, row_constraint)
        assert submatrix.nr_rows == 7
        assert submatrix.nr_columns == 7

import stormpy
from helpers.helper import get_example_path

import math


class TestTransformation:

    def test_transform_symbolic_dtmc_to_sparse(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "crowds5_5.pm"))
        symbolic_model = stormpy.build_symbolic_model(program)
        assert symbolic_model.nr_states == 8607
        assert symbolic_model.nr_transitions == 15113
        assert symbolic_model.model_type == stormpy.ModelType.DTMC
        assert not symbolic_model.supports_parameters
        assert type(symbolic_model) is stormpy.SymbolicSylvanDtmc
        sparse_model = stormpy.transform_to_sparse_model(symbolic_model)
        assert sparse_model.nr_states == 8607
        assert sparse_model.nr_transitions == 15113
        assert sparse_model.model_type == stormpy.ModelType.DTMC
        assert not sparse_model.supports_parameters
        assert type(sparse_model) is stormpy.SparseDtmc

    def test_transform_symbolic_parametric_dtmc_to_sparse(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "parametric_die.pm"))
        model = stormpy.build_symbolic_parametric_model(program)
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        assert model.model_type == stormpy.ModelType.DTMC
        assert model.supports_parameters
        assert type(model) is stormpy.SymbolicSylvanParametricDtmc
        symbolic_model = stormpy.transform_to_sparse_model(model)
        assert symbolic_model.nr_states == 13
        assert symbolic_model.nr_transitions == 20
        assert symbolic_model.model_type == stormpy.ModelType.DTMC
        assert symbolic_model.supports_parameters
        assert type(symbolic_model) is stormpy.SparseParametricDtmc

    def test_transform_continuous_to_discrete_time_model_ctmc(self):
        ctmc = stormpy.build_model_from_drn(get_example_path("ctmc", "dft.drn"))
        formulas = stormpy.parse_properties('T=? [ F "failed" ]')
        assert ctmc.nr_states == 16
        assert ctmc.nr_transitions == 33
        assert len(ctmc.initial_states) == 1
        initial_state = ctmc.initial_states[0]
        assert initial_state == 1
        result = stormpy.model_checking(ctmc, formulas[0])
        assert math.isclose(result.at(initial_state), 4.166666667)

        dtmc, dtmc_formulas = stormpy.transform_to_discrete_time_model(ctmc, formulas)
        assert dtmc.nr_states == 16
        assert dtmc.nr_transitions == 33
        assert len(dtmc.initial_states) == 1
        initial_state = dtmc.initial_states[0]
        assert initial_state == 1
        result = stormpy.model_checking(dtmc, dtmc_formulas[0])
        assert math.isclose(result.at(initial_state), 4.166666667)

    def test_transform_continuous_to_discrete_time_model_ma(self):
        program = stormpy.parse_prism_program(get_example_path("ma", "simple.ma"), False, True)
        formulas = stormpy.parse_properties_for_prism_program("Tmin=? [ F s=4 ]", program)
        ma = stormpy.build_model(program, formulas)
        assert ma.nr_states == 5
        assert ma.nr_transitions == 8
        assert ma.model_type == stormpy.ModelType.MA
        assert len(ma.initial_states) == 1
        initial_state = ma.initial_states[0]
        assert initial_state == 0
        result = stormpy.model_checking(ma, formulas[0])
        assert math.isclose(result.at(initial_state), 0.08333333333)

        mdp, mdp_formulas = stormpy.transform_to_discrete_time_model(ma, formulas)
        assert mdp.nr_states == 5
        assert mdp.nr_transitions == 8
        assert mdp.model_type == stormpy.ModelType.MDP
        assert len(mdp.initial_states) == 1
        initial_state = mdp.initial_states[0]
        assert initial_state == 0
        result = stormpy.model_checking(mdp, mdp_formulas[0])
        assert math.isclose(result.at(initial_state), 0.08333333333)

    def test_eliminate_non_markovian_chains(self):
        program = stormpy.parse_prism_program(get_example_path("ma", "stream2.ma"), False, True)
        formulas = stormpy.parse_properties_for_prism_program('Pmin=? [ F "done"];Tmin=? [ F "done" ]', program)
        ma = stormpy.build_model(program, formulas)
        assert ma.nr_states == 12
        assert ma.nr_transitions == 14
        assert ma.model_type == stormpy.ModelType.MA
        assert len(ma.initial_states) == 1
        initial_state = ma.initial_states[0]
        assert initial_state == 0
        assert len(formulas) == 2
        result = stormpy.model_checking(ma, formulas[0])
        assert math.isclose(result.at(initial_state), 1)

        # Keep labels
        ma_elim, ma_formulas_elim = stormpy.eliminate_non_markovian_chains(ma, formulas, stormpy.EliminationLabelBehavior.KEEP_LABELS)
        assert ma_elim.nr_states == 9
        assert ma_elim.nr_transitions == 11
        assert ma_elim.model_type == stormpy.ModelType.MA
        assert len(ma_elim.initial_states) == 1
        initial_state = ma_elim.initial_states[0]
        assert initial_state == 0
        assert len(ma_formulas_elim) == 1
        result = stormpy.model_checking(ma_elim, ma_formulas_elim[0])
        assert math.isclose(result.at(initial_state), 1)

        # Merge labels
        ma_elim, ma_formulas_elim = stormpy.eliminate_non_markovian_chains(ma, formulas, stormpy.EliminationLabelBehavior.MERGE_LABELS)
        assert ma_elim.nr_states == 8
        assert ma_elim.nr_transitions == 10
        assert ma_elim.model_type == stormpy.ModelType.MA
        assert len(ma_elim.initial_states) == 1
        initial_state = ma_elim.initial_states[0]
        assert initial_state == 0
        assert len(ma_formulas_elim) == 1
        result = stormpy.model_checking(ma_elim, ma_formulas_elim[0])
        assert math.isclose(result.at(initial_state), 1)

        # Delete labels
        ma_elim, ma_formulas_elim = stormpy.eliminate_non_markovian_chains(ma, formulas, stormpy.EliminationLabelBehavior.DELETE_LABELS)
        assert ma_elim.nr_states == 8
        assert ma_elim.nr_transitions == 10
        assert ma_elim.model_type == stormpy.ModelType.MA
        assert len(ma_elim.initial_states) == 1
        initial_state = ma_elim.initial_states[0]
        assert initial_state == 0
        assert len(ma_formulas_elim) == 1
        result = stormpy.model_checking(ma_elim, ma_formulas_elim[0])
        assert math.isclose(result.at(initial_state), 1)


class TestECElimination:
    def test_elimination_on_two_dice(self):
        program = stormpy.parse_prism_program(get_example_path("mdp", "two_dice.nm"))
        formulas = stormpy.parse_properties_for_prism_program('P=? [ F "two" ]', program)
        model = stormpy.build_model(program, formulas)
        subsystem = stormpy.BitVector(model.nr_states, True)
        possible_ec_rows = stormpy.BitVector(model.nr_choices, True)
        add_sink_rows = subsystem
        ec_elimination_result = stormpy.eliminate_ECs(model.transition_matrix, subsystem, possible_ec_rows, add_sink_rows, True)
        assert ec_elimination_result.matrix.nr_rows == 218
        assert ec_elimination_result.matrix.nr_columns == model.nr_states
        assert ec_elimination_result.old_to_new_state_mapping[23] == 23
        assert ec_elimination_result.new_to_old_row_mapping[200] == 245
        assert ec_elimination_result.sink_rows.number_of_set_bits() == 36


class TestSubsystemCreation:
    def test_for_ctmc(self):
        program = stormpy.parse_prism_program(get_example_path("ctmc", "polling2.sm"), True)
        formulas = stormpy.parse_properties_for_prism_program('P=? [ F<=3 "target" ]', program)
        model = stormpy.build_model(program, formulas)
        assert model.nr_states == 12
        selected_outgoing_transitions = stormpy.BitVector(model.nr_states, True)
        selected_outgoing_transitions.set(3, False)
        selected_outgoing_transitions.set(6, False)
        options = stormpy.SubsystemBuilderOptions()
        options.fix_deadlocks = True
        submodel_result = stormpy.construct_submodel(model, stormpy.BitVector(model.nr_states, True), selected_outgoing_transitions, False, options)
        submodel = submodel_result.model
        abort_label = submodel_result.deadlock_label
        assert submodel.nr_states == 8
        assert abort_label == "deadl"
        assert "deadl" in submodel.labeling.get_labels()

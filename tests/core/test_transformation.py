import pytest
import stormpy
from helpers.helper import build_sparse_model, get_example_path

import math
from stormpy.exceptions import StormError


@pytest.mark.parametrize("value_type", [float, stormpy.Rational, stormpy.RationalFunction, stormpy.Interval, stormpy.RationalInterval])
def test_subsystem_and_end_component_overloads(value_type, tmp_path):
    model = build_sparse_model(get_example_path("dtmc", "die.pm"), value_type)

    states = stormpy.datastructures.BitVector(model.nr_states, True)
    choices = stormpy.datastructures.BitVector(model.nr_choices, True)
    subsystem = stormpy.transformations.build_submodel(model, states, choices)
    assert type(subsystem) is stormpy.transformations.SubsystemBuilderReturnType[value_type]
    assert subsystem.model.nr_states == model.nr_states
    result = stormpy.developer.EndComponentEliminator[value_type].transform(model.transition_matrix, states, choices, states, True)
    assert type(result) is stormpy.developer.EndComponentEliminatorReturnType[value_type]
    assert result.matrix.nr_columns == model.nr_states

    output = tmp_path / "model.drn"
    stormpy.io.export_to_drn(model, output)
    assert f"@nr_states\n{model.nr_states}" in output.read_text()


class TestTransformation:
    def test_transform_symbolic_dtmc_to_sparse(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "crowds5_5.pm"))
        symbolic_model = stormpy.build_symbolic_model(program)
        assert symbolic_model.nr_states == 8607
        assert symbolic_model.nr_transitions == 15113
        assert symbolic_model.model_type == stormpy.models.ModelType.DTMC
        assert not symbolic_model.supports_parameters
        assert type(symbolic_model) is stormpy.models.SymbolicDtmc[stormpy.models.DdType.Sylvan, float]
        sparse_model = stormpy.transformations.transform_to_sparse_model(symbolic_model)
        assert sparse_model.nr_states == 8607
        assert sparse_model.nr_transitions == 15113
        assert sparse_model.model_type == stormpy.models.ModelType.DTMC
        assert not sparse_model.supports_parameters
        assert type(sparse_model) is stormpy.models.SparseDtmc[float]

    def test_transform_symbolic_parametric_dtmc_to_sparse(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "parametric_die.pm"))
        model = stormpy.build_symbolic_model[stormpy.RationalFunction](program)
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        assert model.model_type == stormpy.models.ModelType.DTMC
        assert model.supports_parameters
        assert type(model) is stormpy.models.SymbolicDtmc[stormpy.models.DdType.Sylvan, stormpy.RationalFunction]
        symbolic_model = stormpy.transformations.transform_to_sparse_model(model)
        assert symbolic_model.nr_states == 13
        assert symbolic_model.nr_transitions == 20
        assert symbolic_model.model_type == stormpy.models.ModelType.DTMC
        assert symbolic_model.supports_parameters
        assert type(symbolic_model) is stormpy.models.SparseDtmc[stormpy.RationalFunction]

    def test_transform_continuous_to_discrete_time_model_ctmc(self):
        ctmc = stormpy.build_model_from_drn(get_example_path("ctmc", "dft.drn"))
        formula = stormpy.parse_property('T=? [ F "failed" ]')
        assert ctmc.nr_states == 16
        assert ctmc.nr_transitions == 33
        assert len(ctmc.initial_states) == 1
        initial_state = ctmc.initial_states[0]
        assert initial_state == 1
        result = stormpy.model_checking(ctmc, formula)
        assert math.isclose(result[initial_state], 4.166666667)

        dtmc, dtmc_formulas = stormpy.transformations.transform_to_discrete_time_model(ctmc, formula)
        assert dtmc.nr_states == 16
        assert dtmc.nr_transitions == 33
        assert len(dtmc.initial_states) == 1
        initial_state = dtmc.initial_states[0]
        assert initial_state == 1
        result = stormpy.model_checking(dtmc, dtmc_formulas[0])
        assert math.isclose(result[initial_state], 4.166666667)

    def test_transform_continuous_to_discrete_time_model_ma(self):
        program = stormpy.parse_prism_program(get_example_path("ma", "simple.ma"))
        formula = stormpy.parse_property("Tmin=? [ F s=4 ]", program)
        ma = stormpy.build_model(program, formula)
        assert ma.nr_states == 5
        assert ma.nr_transitions == 8
        assert ma.model_type == stormpy.models.ModelType.MA
        assert len(ma.initial_states) == 1
        initial_state = ma.initial_states[0]
        assert initial_state == 0
        result = stormpy.model_checking(ma, formula)
        assert math.isclose(result[initial_state], 0.08333333333)

        mdp, mdp_formulas = stormpy.transformations.transform_to_discrete_time_model(ma, formula)
        assert mdp.nr_states == 5
        assert mdp.nr_transitions == 8
        assert mdp.model_type == stormpy.models.ModelType.MDP
        assert len(mdp.initial_states) == 1
        initial_state = mdp.initial_states[0]
        assert initial_state == 0
        result = stormpy.model_checking(mdp, mdp_formulas[0])
        assert math.isclose(result[initial_state], 0.08333333333)

    def test_transformations_return_formulas(self):
        program = stormpy.parse_prism_program(get_example_path("ma", "stream2.ma"))
        properties = stormpy.parse_properties('Pmin=? [ F "done"]; Tmin=? [ F "done" ]', program)
        ma = stormpy.build_model(program, properties)
        # Both formulas are preserved by the transformation to a discrete-time model
        _, mdp_formulas = stormpy.transformations.transform_to_discrete_time_model(ma, properties)
        assert len(mdp_formulas) == 2
        assert all(isinstance(formula, stormpy.logic.Formula) for formula in mdp_formulas)
        # Only the probability formula is preserved by the elimination of non-Markovian chains
        _, elim_formulas = stormpy.transformations.eliminate_non_markovian_chains(
            model=ma, properties=properties, label_behavior=stormpy.transformations.EliminationLabelBehavior.KEEP_LABELS
        )
        assert len(elim_formulas) == 1
        assert elim_formulas[0].is_probability_operator_formula

    def test_eliminate_non_markovian_chains(self):
        program = stormpy.parse_prism_program(get_example_path("ma", "stream2.ma"))
        formulas = stormpy.parse_properties('Pmin=? [ F "done"];Tmin=? [ F "done" ]', program)
        ma = stormpy.build_model(program, formulas)
        assert ma.nr_states == 12
        assert ma.nr_transitions == 14
        assert ma.model_type == stormpy.models.ModelType.MA
        assert len(ma.initial_states) == 1
        initial_state = ma.initial_states[0]
        assert initial_state == 0
        assert len(formulas) == 2
        result = stormpy.model_checking(ma, formulas[0])
        assert math.isclose(result[initial_state], 1)

        # Keep labels
        ma_elim, ma_formulas_elim = stormpy.transformations.eliminate_non_markovian_chains(
            ma, formulas, stormpy.transformations.EliminationLabelBehavior.KEEP_LABELS
        )
        assert ma_elim.nr_states == 9
        assert ma_elim.nr_transitions == 11
        assert ma_elim.model_type == stormpy.models.ModelType.MA
        assert len(ma_elim.initial_states) == 1
        initial_state = ma_elim.initial_states[0]
        assert initial_state == 0
        assert len(ma_formulas_elim) == 1
        result = stormpy.model_checking(ma_elim, ma_formulas_elim[0])
        assert math.isclose(result[initial_state], 1)

        # Merge labels
        ma_elim, ma_formulas_elim = stormpy.transformations.eliminate_non_markovian_chains(
            ma, formulas, stormpy.transformations.EliminationLabelBehavior.MERGE_LABELS
        )
        assert ma_elim.nr_states == 8
        assert ma_elim.nr_transitions == 10
        assert ma_elim.model_type == stormpy.models.ModelType.MA
        assert len(ma_elim.initial_states) == 1
        initial_state = ma_elim.initial_states[0]
        assert initial_state == 0
        assert len(ma_formulas_elim) == 1
        result = stormpy.model_checking(ma_elim, ma_formulas_elim[0])
        assert math.isclose(result[initial_state], 1)

        # Delete labels
        ma_elim, ma_formulas_elim = stormpy.transformations.eliminate_non_markovian_chains(
            ma, formulas, stormpy.transformations.EliminationLabelBehavior.DELETE_LABELS
        )
        assert ma_elim.nr_states == 8
        assert ma_elim.nr_transitions == 10
        assert ma_elim.model_type == stormpy.models.ModelType.MA
        assert len(ma_elim.initial_states) == 1
        initial_state = ma_elim.initial_states[0]
        assert initial_state == 0
        assert len(ma_formulas_elim) == 1
        result = stormpy.model_checking(ma_elim, ma_formulas_elim[0])
        assert math.isclose(result[initial_state], 1)

    def test_export_to_drn_options(self, tmp_path):
        model = stormpy.build_model(stormpy.parse_prism_program(get_example_path("dtmc", "crowds5_5.pm")))
        options = stormpy.io.DirectEncodingExporterOptions()
        options.output_precision = 1
        output = tmp_path / "model.drn"
        stormpy.io.export_to_drn(model, output, options=options)
        content = output.read_text()
        assert "0.8\n" in content
        assert "0.833" not in content
        assert stormpy.build_model_from_drn(output).nr_states == model.nr_states


class TestECElimination:
    def test_elimination_on_two_dice(self):
        program = stormpy.parse_prism_program(get_example_path("mdp", "two_dice.nm"))
        formula = stormpy.parse_property('P=? [ F "two" ]', program)
        model = stormpy.build_model(program, formula)
        subsystem = stormpy.datastructures.BitVector(model.nr_states, True)
        possible_ec_rows = stormpy.datastructures.BitVector(model.nr_choices, True)
        add_sink_rows = subsystem
        ec_elimination_result = stormpy.developer.EndComponentEliminator[float].transform(
            model.transition_matrix, subsystem, possible_ec_rows, add_sink_rows, True
        )
        assert ec_elimination_result.matrix.nr_rows == 218
        assert ec_elimination_result.matrix.nr_columns == model.nr_states
        assert ec_elimination_result.old_to_new_state_mapping[23] == 23
        assert ec_elimination_result.new_to_old_row_mapping[200] == 245
        assert ec_elimination_result.sink_rows.get_number_of_set_bits() == 36


class TestAddUncertainty:
    def test_add_uncertainty_dtmc(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        model = stormpy.build_model(program)
        assert type(model) is stormpy.models.SparseDtmc[float]
        assert model.nr_states == 13
        transformer = stormpy.developer.AddUncertainty[float](model)
        interval_model = transformer.transform(0.1)
        assert type(interval_model) is stormpy.models.SparseDtmc[stormpy.Interval]
        assert interval_model.nr_states == 13
        assert interval_model.nr_transitions == model.nr_transitions
        for row in range(interval_model.nr_states):
            for transition in interval_model.transition_matrix.row_iter(row, row):
                assert transition.value.lower() <= transition.value.upper()
                assert transition.value.lower() >= 0.0

    def test_add_uncertainty_exact_dtmc(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        model = stormpy.build_model[stormpy.Rational](program)
        assert type(model) is stormpy.models.SparseDtmc[stormpy.Rational]
        transformer = stormpy.developer.AddUncertainty[stormpy.Rational](model)
        interval_model = transformer.transform(stormpy.Rational("1/10"))
        assert type(interval_model) is stormpy.models.SparseDtmc[stormpy.RationalInterval]
        assert interval_model.nr_states == model.nr_states
        assert interval_model.nr_transitions == model.nr_transitions
        for row in range(interval_model.nr_states):
            for transition in interval_model.transition_matrix.row_iter(row, row):
                assert transition.value.lower() <= transition.value.upper()

    def test_add_uncertainty_api(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        model = stormpy.build_model(program)
        interval_model = stormpy.transformations.add_uncertainty(model, 0.1)
        assert type(interval_model) is stormpy.models.SparseDtmc[stormpy.Interval]
        exact_model = stormpy.build_model[stormpy.Rational](program)
        exact_interval_model = stormpy.transformations.add_uncertainty(exact_model, stormpy.Rational("1/10"))
        assert type(exact_interval_model) is stormpy.models.SparseDtmc[stormpy.RationalInterval]
        with pytest.raises(StormError):
            stormpy.transformations.add_uncertainty(interval_model, 0.1)


class TestSubsystemCreation:
    def test_for_interval_mdp(self):
        model = stormpy.build_model_from_drn[stormpy.Interval](get_example_path("imdp", "tiny-01.drn"))
        assert type(model) is stormpy.models.SparseMdp[stormpy.Interval]
        assert model.nr_states == 3
        states = stormpy.datastructures.BitVector(model.nr_states, True)
        states.set(2, False)
        options = stormpy.transformations.SubsystemBuilderOptions()
        options.fix_deadlocks = True
        result = stormpy.transformations.build_submodel(
            model, states, stormpy.datastructures.BitVector(model.nr_choices, True), keep_unreachable_states=True, options=options
        )
        assert type(result.model) is stormpy.models.SparseMdp[stormpy.Interval]
        assert result.model.nr_states == 2
        assert result.model.nr_transitions == 2

    def test_for_exact_interval_mdp(self):
        model = stormpy.build_model_from_drn[stormpy.RationalInterval](get_example_path("imdp", "tiny-01.drn"))
        assert type(model) is stormpy.models.SparseMdp[stormpy.RationalInterval]
        assert model.nr_states == 3
        states = stormpy.datastructures.BitVector(model.nr_states, True)
        states.set(2, False)
        options = stormpy.transformations.SubsystemBuilderOptions()
        options.fix_deadlocks = True
        result = stormpy.transformations.build_submodel(
            model, states, stormpy.datastructures.BitVector(model.nr_choices, True), keep_unreachable_states=True, options=options
        )
        assert type(result.model) is stormpy.models.SparseMdp[stormpy.RationalInterval]
        assert result.model.nr_states == 2
        assert result.model.nr_transitions == 2

    def test_for_ctmc(self):
        program = stormpy.parse_prism_program(get_example_path("ctmc", "polling2.sm"), prism_compatibility=True)
        formula = stormpy.parse_property('P=? [ F<=3 "target" ]', program)
        model = stormpy.build_model(program, formula)
        assert model.nr_states == 12
        selected_outgoing_transitions = stormpy.datastructures.BitVector(model.nr_states, True)
        selected_outgoing_transitions.set(3, False)
        selected_outgoing_transitions.set(6, False)
        options = stormpy.transformations.SubsystemBuilderOptions()
        options.fix_deadlocks = True
        submodel_result = stormpy.transformations.build_submodel(
            model, stormpy.datastructures.BitVector(model.nr_states, True), selected_outgoing_transitions, keep_unreachable_states=False, options=options
        )
        submodel = submodel_result.model
        abort_label = submodel_result.deadlock_label
        assert submodel.nr_states == 8
        assert abort_label == "deadl"
        assert "deadl" in submodel.labeling.get_labels()

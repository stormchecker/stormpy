import pytest
import stormpy
from helpers.helper import build_sparse_model, get_example_path

from configurations import spot

import math
from stormpy.exceptions import StormError


def test_symbolic_filter_template_and_shared_dd_type():
    program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
    model = stormpy.build_symbolic_model(program)
    result = stormpy.create_filter_initial_states(model)

    assert stormpy.DdType is stormpy.storage.DdType
    assert type(result) is stormpy.SymbolicQualitativeCheckResult[stormpy.DdType.Sylvan]
    assert stormpy.storage.Bdd.parameters_of(result.get_truth_values_vector()) == (stormpy.DdType.Sylvan,)


@pytest.mark.parametrize("value_type", [float, stormpy.Rational, stormpy.RationalFunction])
def test_initial_state_filter_overloads(value_type):
    model = build_sparse_model(get_example_path("dtmc", "die.pm"), value_type)
    result = stormpy.create_filter_initial_states(model)

    assert type(result) is stormpy.ExplicitQualitativeCheckResult[value_type]
    assert result.get_truth_values_vector() == model.initial_states_as_bitvector


@pytest.mark.parametrize("value_type", [float, stormpy.Rational])
def test_infinite_quantitative_values(value_type, tmp_path):
    # Goal is reached with probability 1/2 and the expected reward is infinite
    program = stormpy.parse_prism_program(get_example_path("dtmc", "infinite.pm"))
    properties = stormpy.parse_properties('R=? [ F "goal" ]', program)
    model = stormpy.build_model[value_type](program, properties)
    result = stormpy.model_checking(model, properties[0])
    assert result[0] == math.inf
    assert result[2] == math.inf
    assert result[1] == 0
    assert isinstance(result[1], value_type)
    assert result.get_max() == math.inf
    assert result.get_min() == 0
    assert result.get_value_vector() == [result[state] for state in range(model.nr_states)]
    assert math.inf in result.get_value_vector()
    if value_type is float:
        # Infinity can be represented by float
        assert result.get_finite_value_vector() == result.get_value_vector()
    else:
        with pytest.raises(RuntimeError, match="narrow inf"):
            result.get_finite_value_vector()


def test_result_index_error():
    program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
    properties = stormpy.parse_properties('P=? [ F "one" ]', program)
    model = stormpy.build_model(program, properties)
    # Quantitative result for all states
    result = stormpy.model_checking(model, properties[0])
    assert result.get_states() == stormpy.BitVector(model.nr_states, True)
    assert result.has_value_for_state(model.nr_states - 1)
    assert not result.has_value_for_state(model.nr_states)
    with pytest.raises(IndexError):
        result[model.nr_states]
    assert result.get_value_vector() == [result[state] for state in model.states]
    # Iteration stops at the end of the result
    assert list(result) == result.get_value_vector()
    # Qualitative result
    filter = stormpy.create_filter_initial_states(model)
    assert filter[0]
    assert not filter[1]
    with pytest.raises(IndexError):
        filter[model.nr_states]
    # Result only for the initial states
    stormpy.filter_initial_states(result, model)
    assert result.has_value_for_state(0)
    assert not result.has_value_for_state(1)
    assert math.isclose(result[0], 1 / 6)
    with pytest.raises(IndexError):
        result[1]
    assert result.get_value_vector() == [result[0]]


class TestModelChecking:
    def test_model_checking_prism_dtmc_label(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        formulas = stormpy.parse_properties('P=? [ F "one" ]', program)
        model = stormpy.build_model(program, formulas)
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        assert len(model.initial_states) == 1
        initial_state = model.initial_states[0]
        assert initial_state == 0
        result = stormpy.model_checking(model, formulas[0])
        assert math.isclose(result[initial_state], 1 / 6)

    def test_model_checking_prism_dtmc_p(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        formulas = stormpy.parse_properties("P=? [ F s=2 ]", program)
        model = stormpy.build_model(program, formulas)
        assert model.nr_states == 8
        assert model.nr_transitions == 12
        assert len(model.initial_states) == 1
        initial_state = model.initial_states[0]
        assert initial_state == 0
        result = stormpy.model_checking(model, formulas[0])
        assert math.isclose(result[initial_state], 1 / 2)

    def test_model_checking_prism_dtmc_reward(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        formulas = stormpy.parse_properties('R=? [F "done"]', program)
        model = stormpy.build_model(program, formulas)
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        assert len(model.initial_states) == 1
        initial_state = model.initial_states[0]
        assert initial_state == 0
        result = stormpy.model_checking(model, formulas[0])
        assert math.isclose(result[initial_state], 11 / 3)

    @spot
    def test_model_checking_prism_dtmc_ltl(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        formulas = stormpy.parse_properties('P=? [ FG "one" ]', program)
        model = stormpy.build_model(program, formulas)
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        assert len(model.initial_states) == 1
        initial_state = model.initial_states[0]
        assert initial_state == 0
        result = stormpy.model_checking(model, formulas[0])
        assert math.isclose(result[initial_state], 1 / 6)

    def test_model_checking_prism_mdp(self):
        program = stormpy.parse_prism_program(get_example_path("mdp", "coin2-2.nm"))
        formulas = stormpy.parse_properties('Pmin=? [ F "finished" & "all_coins_equal_1"]', program)
        model = stormpy.build_model(program, formulas)
        assert model.nr_states == 272
        assert model.nr_transitions == 492
        assert len(model.initial_states) == 1
        initial_state = model.initial_states[0]
        assert initial_state == 0
        result = stormpy.model_checking(model, formulas[0])
        assert math.isclose(result[initial_state], 49 / 128, rel_tol=1e-5)

    def test_model_checking_interval_dtmc(self):
        program = stormpy.parse_prism_program(get_example_path("idtmc", "die-intervals.pm"))
        formulas = stormpy.parse_properties('P=? [ F "one"]')
        model = stormpy.build_model[stormpy.Interval](program, formulas)
        initial_state = model.initial_states[0]
        assert initial_state == 0

        env = stormpy.Environment()
        env.solver().min_max().method = stormpy.MinMaxMethod.VALUE_ITERATION

        # Compute maximal
        result = stormpy.model_checking(
            model,
            formulas[0],
            only_initial_states=True,
            extract_scheduler=True,
            uncertainty_resolution_mode=stormpy.UncertaintyResolutionMode.MAXIMIZE,
            environment=env,
        )
        assert math.isclose(result[initial_state], 72.0 / 189.0, rel_tol=1e-4)
        # Compute minimal
        result = stormpy.model_checking(
            model,
            formulas[0],
            only_initial_states=True,
            extract_scheduler=True,
            uncertainty_resolution_mode=stormpy.UncertaintyResolutionMode.MINIMIZE,
            environment=env,
        )
        assert math.isclose(result[initial_state], 9.0 / 189.0, rel_tol=1e-4)

    def test_model_checking_interval_mdp(self):
        model = stormpy.build_model_from_drn[stormpy.Interval](get_example_path("imdp", "tiny-01.drn"))
        formulas = stormpy.parse_properties('Pmax=? [ F "target"];Pmin=? [ F "target"]')
        initial_state = model.initial_states[0]
        assert initial_state == 0

        env = stormpy.Environment()
        env.solver().min_max().method = stormpy.MinMaxMethod.VALUE_ITERATION

        # Compute maximal robust
        result = stormpy.model_checking(
            model,
            formulas[0],
            only_initial_states=True,
            extract_scheduler=True,
            uncertainty_resolution_mode=stormpy.UncertaintyResolutionMode.ROBUST,
            environment=env,
        )
        assert math.isclose(result[initial_state], 0.4, rel_tol=1e-4)
        # Compute maximal cooperative
        result = stormpy.model_checking(
            model,
            formulas[0],
            only_initial_states=True,
            extract_scheduler=True,
            uncertainty_resolution_mode=stormpy.UncertaintyResolutionMode.COOPERATIVE,
            environment=env,
        )
        assert math.isclose(result[initial_state], 0.5, rel_tol=1e-4)

        # Compute minimal robust
        result = stormpy.model_checking(
            model,
            formulas[1],
            only_initial_states=True,
            extract_scheduler=True,
            uncertainty_resolution_mode=stormpy.UncertaintyResolutionMode.ROBUST,
            environment=env,
        )
        assert math.isclose(result[initial_state], 0.5, rel_tol=1e-4)
        # Compute minimal cooperative
        result = stormpy.model_checking(
            model,
            formulas[1],
            only_initial_states=True,
            extract_scheduler=True,
            uncertainty_resolution_mode=stormpy.UncertaintyResolutionMode.COOPERATIVE,
            environment=env,
        )
        assert math.isclose(result[initial_state], 0.4, rel_tol=1e-4)

    def test_model_checking_exact_interval_dtmc(self):
        program = stormpy.parse_prism_program(get_example_path("idtmc", "die-intervals.pm"))
        formulas = stormpy.parse_properties('P=? [ F "one"]')
        model = stormpy.build_model[stormpy.RationalInterval](program, formulas)
        initial_state = model.initial_states[0]
        assert initial_state == 0

        env = stormpy.Environment()
        env.solver().min_max().method = stormpy.MinMaxMethod.VALUE_ITERATION

        # Compute maximal
        result = stormpy.model_checking(
            model,
            formulas[0],
            only_initial_states=True,
            extract_scheduler=True,
            uncertainty_resolution_mode=stormpy.UncertaintyResolutionMode.MAXIMIZE,
            environment=env,
        )
        assert math.isclose(result[initial_state], 72.0 / 189.0, rel_tol=1e-4)
        # Compute minimal
        result = stormpy.model_checking(
            model,
            formulas[0],
            only_initial_states=True,
            extract_scheduler=True,
            uncertainty_resolution_mode=stormpy.UncertaintyResolutionMode.MINIMIZE,
            environment=env,
        )
        assert math.isclose(result[initial_state], 9.0 / 189.0, rel_tol=1e-4)

    def test_model_checking_exact_interval_mdp(self):
        model = stormpy.build_model_from_drn[stormpy.RationalInterval](get_example_path("imdp", "tiny-01.drn"))
        formulas = stormpy.parse_properties('Pmax=? [ F "target"];Pmin=? [ F "target"]')
        initial_state = model.initial_states[0]
        assert initial_state == 0

        env = stormpy.Environment()
        env.solver().min_max().method = stormpy.MinMaxMethod.VALUE_ITERATION

        # Compute maximal robust
        result = stormpy.model_checking(
            model,
            formulas[0],
            only_initial_states=True,
            extract_scheduler=True,
            uncertainty_resolution_mode=stormpy.UncertaintyResolutionMode.ROBUST,
            environment=env,
        )
        assert math.isclose(result[initial_state], 0.4, rel_tol=1e-4)
        # Compute maximal cooperative
        result = stormpy.model_checking(
            model,
            formulas[0],
            only_initial_states=True,
            extract_scheduler=True,
            uncertainty_resolution_mode=stormpy.UncertaintyResolutionMode.COOPERATIVE,
            environment=env,
        )
        assert math.isclose(result[initial_state], 0.5, rel_tol=1e-4)

        # Compute minimal robust
        result = stormpy.model_checking(
            model,
            formulas[1],
            only_initial_states=True,
            extract_scheduler=True,
            uncertainty_resolution_mode=stormpy.UncertaintyResolutionMode.ROBUST,
            environment=env,
        )
        assert math.isclose(result[initial_state], 0.5, rel_tol=1e-4)
        # Compute minimal cooperative
        result = stormpy.model_checking(
            model,
            formulas[1],
            only_initial_states=True,
            extract_scheduler=True,
            uncertainty_resolution_mode=stormpy.UncertaintyResolutionMode.COOPERATIVE,
            environment=env,
        )
        assert math.isclose(result[initial_state], 0.4, rel_tol=1e-4)

    def test_model_checking_jani_dtmc(self):
        jani_model, formulas = stormpy.parse_jani_model(get_example_path("dtmc", "die.jani"))
        formulas = stormpy.storage.eliminate_reward_accumulations(jani_model, formulas)
        assert len(formulas) == 2
        model = stormpy.build_model(jani_model, formulas)
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        assert len(model.initial_states) == 1
        initial_state = model.initial_states[0]
        assert initial_state == 0
        result = stormpy.model_checking(model, formulas[0])
        assert math.isclose(result[initial_state], 1 / 6)
        result = stormpy.model_checking(model, formulas[1])
        assert math.isclose(result[initial_state], 11 / 3)

    def test_model_checking_dtmc_all_labels(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        formulas = stormpy.parse_properties('P=? [ F "one" ]', program)
        model = stormpy.build_model(program)
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        assert len(model.initial_states) == 1
        initial_state = model.initial_states[0]
        assert initial_state == 0
        result = stormpy.model_checking(model, formulas[0])
        assert math.isclose(result[initial_state], 1 / 6)
        formulas = stormpy.parse_properties('P=? [ F "two" ]', program)
        result = stormpy.model_checking(model, formulas[0])
        assert math.isclose(result[initial_state], 1 / 6)

    def test_model_checking_all_dtmc(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        formulas = stormpy.parse_properties('P=? [ F "one" ]', program)
        model = stormpy.build_model(program, formulas)
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        result = stormpy.model_checking(model, formulas[0])
        assert result.is_result_for_all_states()
        reference = [1 / 6, 1 / 3, 0, 2 / 3, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        assert all(map(math.isclose, result.get_finite_value_vector(), reference))

    def test_model_checking_only_initial(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        formulas = stormpy.parse_properties('Pmax=? [F{"coin_flips"}<=3 "one"]', program)
        model = stormpy.build_model(program, formulas)
        assert len(model.initial_states) == 1
        initial_state = model.initial_states[0]
        assert initial_state == 0
        result = stormpy.model_checking(model, formulas[0], only_initial_states=True)
        assert not result.is_result_for_all_states()
        assert math.isclose(result[initial_state], 1 / 8)

    def test_model_checking_prob01(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        formulaPhi = stormpy.parse_properties("true")[0]
        formulaPsi = stormpy.parse_properties('"six"')[0]
        model = stormpy.build_model(program, [formulaPsi])
        phiResult = stormpy.model_checking(model, formulaPhi)
        phiStates = phiResult.get_truth_values_vector()
        assert phiStates.number_of_set_bits() == model.nr_states
        psiResult = stormpy.model_checking(model, formulaPsi)
        psiStates = psiResult.get_truth_values_vector()
        assert psiStates.number_of_set_bits() == 1
        prob0, prob1 = stormpy.developer.perform_prob01(model, phiStates, psiStates)
        assert prob0.number_of_set_bits() == 9
        assert prob1.number_of_set_bits() == 1
        labelprop = stormpy.Property("cora", formulaPsi.get_raw_formula(), set())
        result = stormpy.model_checking(model, labelprop)
        assert result.get_truth_values_vector().number_of_set_bits() == 1

        program = stormpy.parse_prism_program(get_example_path("mdp", "coin2-2.nm"))
        formulas = stormpy.parse_properties('Pmin=? [ F "finished" & "all_coins_equal_1"]', program)
        model = stormpy.build_model(program, formulas)
        psi_states = stormpy.model_checking(model, formulas[0].get_raw_formula().subformula.subformula).get_truth_values_vector()
        prob0, prob1 = stormpy.developer.perform_prob01_min(model, stormpy.BitVector(model.nr_states, True), psi_states)
        assert prob0.number_of_set_bits() == 94
        assert prob1.number_of_set_bits() == 15
        psi_states = stormpy.model_checking(model, formulas[0].get_raw_formula().subformula.subformula).get_truth_values_vector()
        prob0, prob1 = stormpy.developer.perform_prob01_max(model, stormpy.BitVector(model.nr_states, True), psi_states)
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
        assert math.isclose(result[initial_state], 4.166666667)

    def test_filter(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        formulas = stormpy.parse_properties('P=? [ F "one" ]', program)
        model = stormpy.build_model(program, formulas)
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        assert len(model.initial_states) == 1
        initial_state = model.initial_states[0]
        assert initial_state == 0
        result = stormpy.model_checking(model, formulas[0])
        assert math.isclose(result[initial_state], 1 / 6)
        filter = stormpy.create_filter_initial_states(model)
        result.filter(filter)
        assert result.get_min() == result.get_max()
        assert math.isclose(result.get_min(), 1 / 6)

    @pytest.mark.parametrize("engine", [stormpy.Engine.SPARSE, stormpy.Engine.DD, stormpy.Engine.HYBRID])
    def test_filter_initial_states(self, engine):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        formulas = stormpy.parse_properties('P=? [ F "one" ]', program)
        if engine == stormpy.Engine.SPARSE:
            model = stormpy.build_model(program, formulas)
        else:
            model = stormpy.build_symbolic_model(program, formulas)
        result = stormpy.model_checking(model, formulas[0], engine=engine)
        assert stormpy.filter_initial_states(result, model) is result
        assert result.get_min() == result.get_max()
        assert math.isclose(result.get_min(), 1 / 6, rel_tol=1e-6)

    @pytest.mark.parametrize("value_type", [stormpy.Interval, stormpy.RationalInterval])
    def test_filter_initial_states_interval(self, value_type):
        program = stormpy.parse_prism_program(get_example_path("idtmc", "die-intervals.pm"))
        formulas = stormpy.parse_properties('P=? [ F "one"]')
        model = stormpy.build_model[value_type](program, formulas)
        env = stormpy.Environment()
        env.solver().min_max().method = stormpy.MinMaxMethod.VALUE_ITERATION
        result = stormpy.model_checking(model, formulas[0], uncertainty_resolution_mode=stormpy.UncertaintyResolutionMode.MAXIMIZE, environment=env)
        # Results of interval models contain values of the underlying number type
        result_type = float if value_type is stormpy.Interval else stormpy.Rational
        assert type(stormpy.create_filter_initial_states(model)) is stormpy.ExplicitQualitativeCheckResult[result_type]
        stormpy.filter_initial_states(result, model)
        assert result.get_min() == result.get_max()
        assert math.isclose(float(result.get_min()), 72.0 / 189.0, rel_tol=1e-4)

    def test_model_checking_prism_dd_dtmc(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        formulas = stormpy.parse_properties('P=? [ F "one" ]', program)
        model = stormpy.build_symbolic_model(program, formulas)
        assert isinstance(model, stormpy.SymbolicDtmc[stormpy.DdType.Sylvan, float])
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        result = stormpy.model_checking(model, formulas[0], engine=stormpy.Engine.DD)
        assert type(result) is stormpy.SymbolicQuantitativeCheckResult[stormpy.DdType.Sylvan, float]
        assert result.get_min() == 0.0
        assert result.get_max() == 1.0
        filter = stormpy.create_filter_initial_states(model)
        result.filter(filter)
        assert result.get_min() == result.get_max()
        assert math.isclose(result.get_min(), 1 / 6, rel_tol=1e-6)

    def test_model_checking_prism_hybrid_dtmc(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        formulas = stormpy.parse_properties('P=? [ F "one" ]', program)
        model = stormpy.build_symbolic_model(program, formulas)
        assert isinstance(model, stormpy.SymbolicDtmc[stormpy.DdType.Sylvan, float])
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        result = stormpy.model_checking(model, formulas[0], engine=stormpy.Engine.HYBRID)
        assert type(result) is stormpy.HybridQuantitativeCheckResult[stormpy.DdType.Sylvan, float]
        values = result.get_explicit_value_vector()
        assert len(values) == 3
        assert math.isclose(values[0], 1 / 6)
        filter = stormpy.create_filter_initial_states(model)
        result.filter(filter)
        assert result.get_min() == result.get_max()
        assert math.isclose(result.get_min(), 1 / 6, rel_tol=1e-6)

    def test_compute_expected_number_of_visits(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        model = stormpy.build_model(program)
        environment = stormpy.Environment()
        result = stormpy.compute_expected_number_of_visits(model, environment=environment)
        assert result[0] == 1
        assert math.isclose(result[1], 2.0 / 3)

    def test_compute_steady_state_distribution(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        model = stormpy.build_model(program)
        environment = stormpy.Environment()
        result = stormpy.compute_steady_state_distribution(model, environment=environment)
        values = result.get_finite_value_vector()
        assert len(values) == 13
        sorted(values)
        for i in range(7):
            assert values[i] == 0
        for i in range(7, 13):
            assert math.isclose(values[i], 1.0 / 6)

    def test_engines(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        properties = stormpy.parse_properties('P=? [F "one"]', program)
        sparse_model = stormpy.build_model(program, properties)
        symbolic_model = stormpy.build_symbolic_model(program, properties)
        result = stormpy.model_checking(sparse_model, properties[0], engine=stormpy.Engine.SPARSE)
        assert math.isclose(result[sparse_model.initial_states[0]], 1 / 6)
        for engine in [None, stormpy.Engine.DD, stormpy.Engine.HYBRID]:
            result = stormpy.model_checking(symbolic_model, properties[0], only_initial_states=True, engine=engine)
            result.filter(stormpy.create_filter_initial_states(symbolic_model))
            assert math.isclose(result.get_min(), 1 / 6, rel_tol=1e-6)

    def test_engine_mismatch(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        properties = stormpy.parse_properties('P=? [F "one"]', program)
        sparse_model = stormpy.build_model(program, properties)
        symbolic_model = stormpy.build_symbolic_model(program, properties)
        with pytest.raises(StormError):
            stormpy.model_checking(sparse_model, properties[0], engine=stormpy.Engine.DD)
        with pytest.raises(StormError):
            stormpy.model_checking(symbolic_model, properties[0], engine=stormpy.Engine.SPARSE)
        with pytest.raises(StormError):
            stormpy.model_checking(symbolic_model, properties[0], extract_scheduler=True)

    def test_uncertainty_resolution_mode_required(self):
        program = stormpy.parse_prism_program(get_example_path("idtmc", "die-intervals.pm"))
        properties = stormpy.parse_properties('P=? [ F "one"]')
        model = stormpy.build_model[stormpy.Interval](program, properties)
        with pytest.raises(StormError):
            stormpy.model_checking(model, properties[0])
        model = stormpy.build_model(stormpy.parse_prism_program(get_example_path("dtmc", "die.pm")), properties)
        with pytest.raises(StormError):
            stormpy.model_checking(model, properties[0], uncertainty_resolution_mode=stormpy.UncertaintyResolutionMode.ROBUST)

    def test_pomdp_requires_force_fully_observable(self):
        program = stormpy.parse_prism_program(get_example_path("pomdp", "maze_2.prism"))
        properties = stormpy.parse_properties('Pmax=? [ !"bad" U "goal" ]', program)
        model = stormpy.build_model(program, properties)
        with pytest.raises(StormError):
            stormpy.model_checking(model, properties[0])
        result = stormpy.model_checking(model, properties[0], force_fully_observable=True)
        assert math.isclose(result[model.initial_states[0]], 11 / 13)

    def test_scheduler_extraction(self):
        program = stormpy.parse_prism_program(get_example_path("mdp", "coin2-2.nm"))
        properties = stormpy.parse_properties('Pmin=? [ F "finished" & "all_coins_equal_1"]', program)
        model = stormpy.build_model(program, properties)
        result = stormpy.model_checking(model, properties[0], extract_scheduler=True)
        assert result.has_scheduler()
        assert result.get_scheduler().memoryless

    def test_multi_objective(self):
        program = stormpy.parse_prism_program(get_example_path("mdp", "multiobjective1.nm"))
        properties = stormpy.parse_properties('multi(Pmax=? [ F<=3 s=2 ],R{"rew"}max=? [ F s=2 ])', program)
        model = stormpy.build_model(program, properties)
        result = stormpy.model_checking(model, properties[0])
        assert type(result) is stormpy.ExplicitParetoCurveCheckResult[float]
        assert result.is_pareto_curve_check_result()

    def test_hint(self):
        program = stormpy.parse_prism_program(get_example_path("mdp", "coin2-2.nm"))
        properties = stormpy.parse_properties('Pmin=? [ F "finished" & "all_coins_equal_1"]', program)
        model = stormpy.build_model(program, properties)
        result = stormpy.model_checking(model, properties[0])
        hint = stormpy.ExplicitModelCheckerHint()
        hint.set_result_hint(result.get_finite_value_vector())
        result_hint = stormpy.model_checking(model, properties[0], hint=hint)
        assert math.isclose(result_hint[model.initial_states[0]], result[model.initial_states[0]], rel_tol=1e-4)

    def test_create_filter(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        properties = stormpy.parse_properties('P=? [F "one"]', program)
        symbolic_model = stormpy.build_symbolic_model(program, properties)
        parser = stormpy.storage.ExpressionParser(program.expression_manager)
        parser.set_identifier_mapping({variable.name: variable.get_expression() for variable in program.expression_manager.get_variables()})
        state_filter = stormpy.create_filter(symbolic_model, parser.parse("s=0"))
        assert type(state_filter) is stormpy.SymbolicQualitativeCheckResult[stormpy.DdType.Sylvan]
        result = stormpy.model_checking(symbolic_model, properties[0])
        result.filter(state_filter)
        # Only the initial state satisfies s=0
        assert math.isclose(result.get_min(), 1 / 6, rel_tol=1e-6)
        assert math.isclose(result.get_max(), 1 / 6, rel_tol=1e-6)
        sparse_model = stormpy.build_model(program, properties)
        with pytest.raises(StormError):
            stormpy.create_filter(sparse_model, parser.parse("s=0"))

    def test_qualitative_result_type(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        properties = stormpy.parse_properties('"one"', program)
        model = stormpy.build_model(program, properties)
        result = stormpy.model_checking(model, properties[0])
        assert isinstance(result, stormpy.QualitativeCheckResult)
        assert isinstance(result, stormpy.CheckResult)
        assert result.is_qualitative()

    def test_model_checker_hint_hierarchy(self):
        hint = stormpy.ExplicitModelCheckerHint[float]()
        assert isinstance(hint, stormpy.ModelCheckerHint)

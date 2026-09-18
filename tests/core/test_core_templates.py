import pytest

import stormpy
from helpers.helper import get_example_path


@pytest.mark.parametrize("value_type", [float, stormpy.Rational, stormpy.RationalFunction, stormpy.Interval, stormpy.RationalInterval])
def test_subsystem_and_end_component_overloads(value_type, tmp_path):
    program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
    if value_type in (stormpy.Rational, stormpy.RationalInterval):
        model = stormpy.build_sparse_exact_model(program)
    elif value_type is stormpy.RationalFunction:
        model = stormpy.build_parametric_model(program)
    else:
        model = stormpy.build_model(program)
    if value_type in (stormpy.Interval, stormpy.RationalInterval):
        uncertainty = 0.01 if value_type is stormpy.Interval else stormpy.Rational("1/100")
        model = stormpy.AddUncertainty(model).transform(uncertainty)

    states = stormpy.BitVector(model.nr_states, True)
    choices = stormpy.BitVector(model.nr_choices, True)
    subsystem = stormpy.construct_submodel(model, states, choices)
    assert type(subsystem) is stormpy.SubsystemBuilderReturnType[value_type]
    assert subsystem.model.nr_states == model.nr_states
    result = stormpy.eliminate_ECs(model.transition_matrix, states, choices, states, True)
    assert type(result) is stormpy.EndComponentEliminatorReturnType[value_type]
    assert result.matrix.nr_columns == model.nr_states

    output = tmp_path / "model.drn"
    stormpy.export_to_drn(model, str(output))
    assert f"@nr_states\n{model.nr_states}" in output.read_text()


def test_symbolic_filter_template_and_shared_dd_type():
    program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
    model = stormpy.build_symbolic_model(program)
    result = stormpy.create_filter_initial_states_symbolic(model)

    assert stormpy.DdType is stormpy.storage.DdType
    assert type(result) is stormpy.SymbolicQualitativeCheckResult[stormpy.DdType.Sylvan]
    assert stormpy.Bdd.parameters_of(result.get_truth_values()) == (stormpy.DdType.Sylvan,)


@pytest.mark.parametrize("exact", [False, True])
def test_initial_state_filter_overloads(exact):
    program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
    model = stormpy.build_sparse_exact_model(program) if exact else stormpy.build_model(program)
    result = stormpy.create_filter_initial_states_sparse(model)

    value_type = stormpy.Rational if exact else float
    assert type(result) is stormpy.ExplicitQualitativeCheckResult[value_type]
    assert result.get_truth_values() == model.initial_states_as_bitvector


def test_counterexample_options_default():
    options = stormpy.SMTCounterExampleGeneratorOptions()
    assert type(options) is stormpy.SMTCounterExampleGeneratorOptions[float]


def test_parameters_of_model():
    program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
    model = stormpy.build_sparse_exact_model(program)

    assert stormpy.storage.parameters_of_model(model) == (stormpy.Rational,)

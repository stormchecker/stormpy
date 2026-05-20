import stormpy
from helpers.helper import get_example_path
from configurations import pomdp


@pomdp
class TestPomdpTransformations:
    def test_make_canonic_exact(self):
        program = stormpy.parse_prism_program(get_example_path("pomdp", "maze_2.prism"))
        formulas = stormpy.parse_properties_for_prism_program('P=? [F "goal"]', program)
        model = stormpy.build_sparse_exact_model(program, formulas)
        assert type(model) is stormpy.SparseExactPomdp
        canonic = stormpy.pomdp.make_canonic(model)
        assert type(canonic) is stormpy.SparseExactPomdp
        assert canonic.nr_states == model.nr_states
        assert canonic.nr_observations == model.nr_observations

    def test_observation_trace_unfolder_options_defaults(self):
        options = stormpy.pomdp.ObservationTraceUnfolderOptions()
        assert options.restart_semantics is True

    def test_observation_trace_unfolder_options_set(self):
        options = stormpy.pomdp.ObservationTraceUnfolderOptions()
        options.restart_semantics = False
        assert options.restart_semantics is False

    def test_create_observation_trace_unfolder_with_options(self):
        program = stormpy.parse_prism_program(get_example_path("pomdp", "maze_2.prism"))
        model = stormpy.build_model(program)
        assert type(model) is stormpy.SparsePomdp
        risk = [0.0] * model.nr_observations
        expr_manager = stormpy.ExpressionManager()
        options = stormpy.pomdp.ObservationTraceUnfolderOptions()
        unfolder = stormpy.pomdp.create_observation_trace_unfolder(model, risk, expr_manager, options)
        unfolder.transform([6])
        assert unfolder.is_restart_semantics_set()

    def test_create_observation_trace_unfolder_no_restart(self):
        program = stormpy.parse_prism_program(get_example_path("pomdp", "maze_2.prism"))
        model = stormpy.build_model(program)
        risk = [0.0] * model.nr_observations
        expr_manager = stormpy.ExpressionManager()
        options = stormpy.pomdp.ObservationTraceUnfolderOptions()
        options.restart_semantics = False
        unfolder = stormpy.pomdp.create_observation_trace_unfolder(model, risk, expr_manager, options)
        unfolder.transform([6])
        assert not unfolder.is_restart_semantics_set()

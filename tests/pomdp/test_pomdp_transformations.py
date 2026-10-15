import stormpy
from helpers.helper import get_example_path
from configurations import pomdp


def _build_canonic_maze():
    program = stormpy.parse_prism_program(get_example_path("pomdp", "maze_2.prism"))
    formulas = stormpy.parse_properties('P=? [F "goal"]', program)
    return stormpy.pomdp.make_canonic(stormpy.build_model(program, formulas))


@pomdp
class TestPomdpTransformations:
    def test_make_canonic_exact(self):
        program = stormpy.parse_prism_program(get_example_path("pomdp", "maze_2.prism"))
        formula = stormpy.parse_property('P=? [F "goal"]', program)
        model = stormpy.build_model[stormpy.Rational](program, formula)
        assert type(model) is stormpy.models.SparsePomdp[stormpy.Rational]
        canonic = stormpy.pomdp.make_canonic(model)
        assert type(canonic) is stormpy.models.SparsePomdp[stormpy.Rational]
        assert canonic.nr_states == model.nr_states
        assert canonic.nr_observations == model.nr_observations

    def test_observation_trace_unfolder_options_defaults(self):
        options = stormpy.pomdp.developer.ObservationTraceUnfolderOptions()
        assert options.use_restart_semantics is True

    def test_observation_trace_unfolder_options_set(self):
        options = stormpy.pomdp.developer.ObservationTraceUnfolderOptions()
        options.use_restart_semantics = False
        assert options.use_restart_semantics is False

    def test_create_observation_trace_unfolder(self):
        program = stormpy.parse_prism_program(get_example_path("pomdp", "maze_2.prism"))
        model = stormpy.build_model(program)
        assert type(model) is stormpy.models.SparsePomdp[float]
        risk = [0.0] * model.nr_observations
        expr_manager = stormpy.expressions.ExpressionManager()
        unfolder = stormpy.pomdp.create_observation_trace_unfolder(model, risk, expr_manager)
        assert type(unfolder) is stormpy.pomdp.ObservationTraceUnfolder[float]
        unfolder.transform([6])
        assert unfolder.is_restart_semantics_set()

    def test_create_observation_trace_unfolder_no_restart(self):
        program = stormpy.parse_prism_program(get_example_path("pomdp", "maze_2.prism"))
        model = stormpy.build_model(program)
        risk = [0.0] * model.nr_observations
        expr_manager = stormpy.expressions.ExpressionManager()
        unfolder = stormpy.pomdp.create_observation_trace_unfolder(model, risk, expr_manager, use_restart_semantics=False)
        unfolder.transform([6])
        assert not unfolder.is_restart_semantics_set()

    def test_make_simple(self):
        model = _build_canonic_maze()
        simple = stormpy.pomdp.make_simple(model)
        assert type(simple) is stormpy.models.SparsePomdp[float]
        assert simple.nr_states == 41
        assert simple.nr_choices == 80

    def test_unfold_memory(self):
        model = _build_canonic_maze()
        memory = stormpy.pomdp.create_memory(stormpy.pomdp.PomdpMemoryPattern.SELECTIVE_COUNTER, 2)
        assert memory.nr_states == 2
        unfolded = stormpy.pomdp.unfold_memory(model, memory, add_memory_labels=True)
        assert type(unfolded) is stormpy.models.SparsePomdp[float]
        assert unfolded.nr_states == 29

    def test_apply_unknown_fsc(self):
        model = _build_canonic_maze()
        memory = stormpy.pomdp.create_memory(stormpy.pomdp.PomdpMemoryPattern.SELECTIVE_COUNTER, 2)
        model = stormpy.pomdp.unfold_memory(model, memory)
        pmc = stormpy.pomdp.apply_unknown_fsc(model, stormpy.pomdp.PomdpFscApplicationMode.SIMPLE_LINEAR)
        assert pmc.model_type == stormpy.models.ModelType.DTMC
        assert pmc.supports_parameters
        assert pmc.nr_states == 29

    def test_binary_pomdp_transformer(self):
        model = _build_canonic_maze()
        result = stormpy.pomdp.developer.BinaryPomdpTransformer[float]().transform(model, True)
        assert type(result) is stormpy.pomdp.developer.PomdpTransformationResult[float]
        assert result.transformed_pomdp.nr_states == 41
        assert len(result.transformed_state_to_original_state_map) == 41

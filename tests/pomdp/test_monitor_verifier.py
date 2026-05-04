import stormpy
import stormpy.storage
from configurations import pomdp


def _build_simple_mc():
    # s0 (init): 0.6->s1, 0.4->s2; s1 ("a","good"): self-loop; s2 ("b"): self-loop
    builder = stormpy.SparseMatrixBuilder(rows=0, columns=0, entries=0, force_dimensions=False, has_custom_row_grouping=False, row_groups=0)
    builder.add_next_value(0, 1, 0.6)
    builder.add_next_value(0, 2, 0.4)
    builder.add_next_value(1, 1, 1.0)
    builder.add_next_value(2, 2, 1.0)
    matrix = builder.build(3, 3)

    labeling = stormpy.storage.StateLabeling(3)
    for lbl in ["init", "a", "b", "good"]:
        labeling.add_label(lbl)
    labeling.add_label_to_state("init", 0)
    labeling.add_label_to_state("a", 1)
    labeling.add_label_to_state("good", 1)
    labeling.add_label_to_state("b", 2)

    components = stormpy.SparseModelComponents(transition_matrix=matrix, state_labeling=labeling)
    return stormpy.storage.SparseDtmc(components)


def _build_simple_monitor():
    # m0 (step0, init): [a]->m1, [b]->m1
    # m1 (step1, accepting): [a]->m2, [b]->m2
    # m2 (step2, horizon): [a]->m2 (self-loop)
    builder = stormpy.SparseMatrixBuilder(rows=0, columns=0, entries=0, force_dimensions=False, has_custom_row_grouping=True, row_groups=0)
    builder.new_row_group(0)
    builder.add_next_value(0, 1, 1.0)
    builder.add_next_value(1, 1, 1.0)
    builder.new_row_group(2)
    builder.add_next_value(2, 2, 1.0)
    builder.add_next_value(3, 2, 1.0)
    builder.new_row_group(4)
    builder.add_next_value(4, 2, 1.0)
    matrix = builder.build(5, 3)

    labeling = stormpy.storage.StateLabeling(3)
    for lbl in ["init", "step0", "step1", "accepting", "step2", "horizon"]:
        labeling.add_label(lbl)
    labeling.add_label_to_state("init", 0)
    labeling.add_label_to_state("step0", 0)
    labeling.add_label_to_state("step1", 1)
    labeling.add_label_to_state("accepting", 1)
    labeling.add_label_to_state("step2", 2)
    labeling.add_label_to_state("horizon", 2)

    choice_labeling = stormpy.storage.ChoiceLabeling(5)
    choice_labeling.add_label("a")
    choice_labeling.add_label("b")
    choice_labeling.add_label_to_choice("a", 0)
    choice_labeling.add_label_to_choice("a", 2)
    choice_labeling.add_label_to_choice("a", 4)
    choice_labeling.add_label_to_choice("b", 1)
    choice_labeling.add_label_to_choice("b", 3)

    components = stormpy.SparseModelComponents(transition_matrix=matrix, state_labeling=labeling)
    components.choice_labeling = choice_labeling
    return stormpy.storage.SparseMdp(components)


@pomdp
class TestMonitorVerifier:
    def test_product_has_expected_labels(self):
        mc = _build_simple_mc()
        monitor = _build_simple_monitor()
        expr_manager = stormpy.ExpressionManager()
        options = stormpy.pomdp.GenerateMonitorVerifierDoubleOptions()
        options.use_restart_semantics = False
        gen = stormpy.pomdp.GenerateMonitorVerifierDouble(mc, monitor, expr_manager, options)
        gen.set_risk([0.0, 1.0, 0.0])
        mv = gen.create_product()

        product = mv.get_product()
        labels = product.labeling.get_labels()
        assert "init" in labels
        assert "goal" in labels
        assert "stop" in labels
        assert "condition" in labels
        assert "sink" in labels
        assert product.labeling.get_states("goal").number_of_set_bits() == 1
        assert product.labeling.get_states("stop").number_of_set_bits() == 1
        assert product.labeling.get_states("condition").number_of_set_bits() == 2

    def test_observation_map_entries(self):
        mc = _build_simple_mc()
        monitor = _build_simple_monitor()
        expr_manager = stormpy.ExpressionManager()
        options = stormpy.pomdp.GenerateMonitorVerifierDoubleOptions()
        options.use_restart_semantics = False
        gen = stormpy.pomdp.GenerateMonitorVerifierDouble(mc, monitor, expr_manager, options)
        gen.set_risk([0.0, 1.0, 0.0])
        mv = gen.create_product()

        obs_map = mv.observation_map
        assert (0, False) in obs_map
        assert (1, True) in obs_map
        assert (2, False) in obs_map
        # All mapped observation values must be distinct
        assert len(set(obs_map.values())) == len(obs_map)

    def test_restart_semantics_has_no_sink(self):
        mc = _build_simple_mc()
        monitor = _build_simple_monitor()
        expr_manager = stormpy.ExpressionManager()
        options = stormpy.pomdp.GenerateMonitorVerifierDoubleOptions()
        options.use_restart_semantics = True
        gen = stormpy.pomdp.GenerateMonitorVerifierDouble(mc, monitor, expr_manager, options)
        gen.set_risk([0.0, 1.0, 0.0])
        mv = gen.create_product()

        labels = mv.get_product().labeling.get_labels()
        assert "sink" not in labels
        assert "goal" in labels
        assert "stop" in labels
        assert "init" in labels

    def test_default_action_map(self):
        mc = _build_simple_mc()
        monitor = _build_simple_monitor()
        expr_manager = stormpy.ExpressionManager()
        options = stormpy.pomdp.GenerateMonitorVerifierDoubleOptions()
        options.use_restart_semantics = False
        gen = stormpy.pomdp.GenerateMonitorVerifierDouble(mc, monitor, expr_manager, options)
        gen.set_risk([0.0, 1.0, 0.0])
        mv = gen.create_product()

        default_action_map = mv.default_action_map
        assert isinstance(default_action_map, dict)
        assert len(default_action_map) > 0
        for obs_id, action_label in default_action_map.items():
            assert isinstance(obs_id, int)
            assert isinstance(action_label, str)

    def test_reference_internal_stability(self):
        # Verify that get_product() and properties return stable references
        # (reference_internal policy keeps MonitorVerifier alive)
        mc = _build_simple_mc()
        monitor = _build_simple_monitor()
        expr_manager = stormpy.ExpressionManager()
        options = stormpy.pomdp.GenerateMonitorVerifierDoubleOptions()
        options.use_restart_semantics = False
        gen = stormpy.pomdp.GenerateMonitorVerifierDouble(mc, monitor, expr_manager, options)
        gen.set_risk([0.0, 1.0, 0.0])
        mv = gen.create_product()

        # Obtain references
        product = mv.get_product()
        obs_map = mv.observation_map
        default_map = mv.default_action_map

        # References remain valid and consistent after repeated access
        assert mv.get_product().nr_states == product.nr_states
        assert mv.observation_map == obs_map
        assert mv.default_action_map == default_map

import stormpy
from helpers.helper import get_example_path
from configurations import pomdp


def _build_canonic_maze(value_type=float):
    program = stormpy.parse_prism_program(get_example_path("pomdp", "maze_2.prism"))
    formulas = stormpy.parse_properties('P=? [F "goal"]', program)
    return stormpy.pomdp.make_canonic(stormpy.build_model[value_type](program, formulas))


@pomdp
class TestPomdpTracker:
    def test_belief_support_tracker(self):
        model = _build_canonic_maze()
        tracker = stormpy.pomdp.BeliefSupportTracker(model)
        assert type(tracker) is stormpy.pomdp.BeliefSupportTracker[float]
        initial = tracker.get_current_belief_support()
        assert initial.get_number_of_set_bits() == 1
        tracker.track(0, model.observations[1])
        tracker.reset()
        assert tracker.get_current_belief_support() == initial

    def test_nondeterministic_belief_tracker(self):
        model = _build_canonic_maze()
        tracker = stormpy.pomdp.create_nondeterministic_belief_tracker(model, reduction_timeout=100, track_timeout=100)
        assert type(tracker) is stormpy.pomdp.NondeterministicBeliefTracker[float]
        tracker.set_risk([0.0] * model.nr_states)
        assert tracker.reset(model.observations[model.initial_states[0]])
        assert tracker.track(model.observations[1])
        assert tracker.get_current_observation() == model.observations[1]
        assert tracker.get_number_of_beliefs() == 1
        assert tracker.get_current_risk() == 0.0
        for belief in tracker.get_current_beliefs():
            assert type(belief) is stormpy.pomdp.SparseBeliefState[float]
            assert belief.is_valid
            assert belief.risk == 0.0
        tracker.reduce()
        assert not tracker.has_timed_out()

    def test_nondeterministic_belief_tracker_exact(self):
        model = _build_canonic_maze(stormpy.Rational)
        tracker = stormpy.pomdp.create_nondeterministic_belief_tracker(model)
        assert type(tracker) is stormpy.pomdp.NondeterministicBeliefTracker[stormpy.Rational]

import math

import pytest

import stormpy

from configurations import pomdp

from helpers.helper import get_example_path


def _maze(property_string, value_type=float):
    program = stormpy.parse_prism_program(get_example_path("pomdp", "maze_2.prism"))
    prop = stormpy.parse_property(property_string, program)
    return stormpy.build_model[value_type](program, prop), prop


@pomdp
class TestPomdpQuantitative:
    def test_unfolding_pmax(self):
        import stormpy.pomdp

        model, prop = _maze('Pmax=? [ !"bad" U "goal" ]')
        result = stormpy.pomdp.verify_with_belief_unfolding(model, prop)
        assert type(result) is stormpy.pomdp.BeliefBasedModelCheckerResult[float]
        assert result.completed_exploration
        assert math.isclose(result.value, 11 / 13, rel_tol=1e-6)
        assert result.statistics.completed_exploration
        assert result.statistics.explored_beliefs > 0
        assert result.policy is None

    def test_unfolding_rmin(self):
        import stormpy.pomdp

        model, prop = _maze('Rmin=? [ F "goal" ]')
        result = stormpy.pomdp.verify_with_belief_unfolding(model, prop.get_raw_formula())
        assert result.completed_exploration
        assert math.isclose(result.value, 74 / 13, rel_tol=1e-6)

    def test_unfolding_exact(self):
        import stormpy.pomdp

        model, prop = _maze('Pmax=? [ !"bad" U "goal" ]', stormpy.Rational)
        result = stormpy.pomdp.verify_with_belief_unfolding(model, prop)
        assert type(result) is stormpy.pomdp.BeliefBasedModelCheckerResult[stormpy.Rational]
        assert result.completed_exploration
        assert result.value == stormpy.Rational(11) / stormpy.Rational(13)

    def test_unfolding_size_limit(self):
        import stormpy.pomdp

        # Incomplete exploration still yields a lower bound for maximization and an upper bound for minimization
        model, prop = _maze('Pmax=? [ !"bad" U "goal" ]')
        result = stormpy.pomdp.verify_with_belief_unfolding(model, prop, max_exploration_size=5)
        assert not result.completed_exploration
        assert 0 <= result.value < 11 / 13
        model, prop = _maze('Rmin=? [ F "goal" ]')
        result = stormpy.pomdp.verify_with_belief_unfolding(model, prop, max_exploration_size=5)
        assert not result.completed_exploration
        assert result.value > 74 / 13

    def test_unfolding_clipping(self):
        import stormpy.pomdp

        model, prop = _maze('Pmax=? [ !"bad" U "goal" ]')
        result = stormpy.pomdp.verify_with_belief_unfolding(
            model, prop, use_clipping=True, clipping_resolutions=[2] * model.nr_observations, max_exploration_size=5
        )
        assert 0 <= result.value <= 11 / 13 + 1e-6

    def test_unfolding_policy(self):
        import stormpy.pomdp

        model, prop = _maze('Pmax=? [ !"bad" U "goal" ]')
        result = stormpy.pomdp.verify_with_belief_unfolding(model, prop, generate_policy=True)
        policy = result.policy
        assert type(policy) is stormpy.pomdp.ObservationBasedFiniteStateController[float]
        node = policy.initial_node
        observations = [observation for observation in range(model.nr_observations) if policy.has_output(node, observation)]
        assert observations
        for observation in observations:
            distribution = policy.get_action_distribution(node, observation)
            assert math.isclose(sum(distribution.values()), 1, rel_tol=1e-6)
            if not policy.is_randomised(node, observation):
                assert distribution == {policy.get_action(node, observation): 1}
        assert "initial-node" in policy.to_json()
        assert policy.to_dot().startswith("digraph")
        assert str(policy)

    def test_discretization(self):
        import stormpy.pomdp

        # Discretization yields an upper bound for maximization and a lower bound for minimization
        model, prop = _maze('Pmax=? [ !"bad" U "goal" ]')
        result = stormpy.pomdp.verify_with_belief_discretization(model, prop)
        assert result.completed_exploration
        assert result.value >= 11 / 13 - 1e-6
        assert result.policy is None
        model, prop = _maze('Rmin=? [ F "goal" ]')
        result = stormpy.pomdp.verify_with_belief_discretization(model, prop, 3, use_dynamic=True)
        assert result.value <= 74 / 13 + 1e-6

    def test_bounds_infinite_belief_space(self):
        import stormpy.pomdp

        program = stormpy.parse_prism_program(get_example_path("pomdp", "maze-concise.prism"))
        prop = stormpy.parse_property('R{"steps"}min=? [F ((x = 2) & (y = 0))]', program)
        model = stormpy.build_model(program, prop)
        upper = stormpy.pomdp.verify_with_belief_unfolding(model, prop, max_exploration_size=100)
        lower = stormpy.pomdp.verify_with_belief_discretization(model, prop, 2)
        assert not upper.completed_exploration
        assert lower.completed_exploration
        assert 0 < lower.value <= upper.value < math.inf

    def test_unsupported_formula(self):
        import stormpy.pomdp

        model, prop = _maze('P>=0.5 [ F "goal" ]')
        with pytest.raises(RuntimeError, match="NotSupportedException"):
            stormpy.pomdp.verify_with_belief_unfolding(model, prop)

    def test_clipping_requires_resolutions(self):
        import stormpy.pomdp

        model, prop = _maze('Pmax=? [ !"bad" U "goal" ]')
        with pytest.raises(RuntimeError, match="IllegalArgumentException"):
            stormpy.pomdp.verify_with_belief_unfolding(model, prop, use_clipping=True)

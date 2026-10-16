import math

import stormpy
from helpers.helper import get_example_path

from configurations import plotting, numpy_avail


def assert_pareto_approximation(result, expected_vertices, precision):
    """
    Check that the under- and over-approximation of the Pareto curve enclose the expected Pareto curve up to the given precision.

    Storm guarantees the precision along the directions of the weight vectors and not per coordinate of a vertex.
    The directions are the normal vectors of the halfspaces of the over-approximation.
    Along each of them, the under-approximation is at most the precision away from the over-approximation.
    """
    under = result.get_under_approximation()
    over = result.get_over_approximation()
    expected = stormpy.developer.storage.Polytope[float].create_downward_closure(expected_vertices)
    assert over.contains(expected)
    assert expected.contains(under)
    for halfspace in over.halfspaces:
        point, exists = under.optimize(halfspace.normal_vector)
        assert exists
        assert halfspace.offset - sum(n * x for n, x in zip(halfspace.normal_vector, point)) <= precision


class TestMultiObjectiveModelChecking:
    def test_naive_api_double_no_plotting(self):
        program = stormpy.parse_prism_program(get_example_path("mdp", "multiobjective1.nm"))
        prop = stormpy.parse_property('multi(Pmax=? [ F<=3 s=2 ],R{"rew"}max=? [ F s=2 ])', program)
        model = stormpy.build_model(program, prop)
        result = stormpy.model_checking(model, prop)
        expected_vertices = [[124 / 125, 248 / 2125], [97 / 100, 5456 / 425], [91 / 100, 248 / 17]]
        assert_pareto_approximation(result, expected_vertices, 1e-4)

    @plotting
    @numpy_avail
    def test_naive_api_double_with_plotting(self):
        import matplotlib.pyplot as plt
        from stormpy.utility.multiobjective_plotting import prepare_multiobjective_result_for_plotting, plot_convex_pareto_curve_demo

        program = stormpy.parse_prism_program(get_example_path("mdp", "multiobjective1.nm"))
        prop = stormpy.parse_property('multi(Pmax=? [ F<=3 s=2 ],R{"rew"}max=? [ F s=2 ])', program)
        model = stormpy.build_model(program, prop)
        result = stormpy.model_checking(model, prop)
        lower_left = [0, 0]
        upper_right = [1, 20]
        formula = prop.get_raw_formula()
        underapprox_points, overapprox_points = prepare_multiobjective_result_for_plotting(result, lower_left, upper_right, formula)
        fig, ax = plt.subplots()
        plot_convex_pareto_curve_demo(ax, underapprox_points, overapprox_points, lower_left, upper_right)
        ax.set_xlabel(formula.subformulas[0])
        ax.set_ylabel(formula.subformulas[1])
        # plt.show()


class TestWeightedObjectiveModelChecking:
    def _check_maze_weighted_objective(self, model, prop):
        env = stormpy.environments.default(model)
        weighted_model_checker, inverter = stormpy.create_weight_vector_checker(model, prop, produce_scheduler=True, environment=env)
        precision = 0 if model.is_exact else 1e-4
        weighted_model_checker.set_weighted_precision(precision)
        weighted_model_checker.check(env, [1, 1])
        point = weighted_model_checker.get_achievable_point()
        assert len(point) == 2
        assert math.isclose(float(point[0]), 3.8, abs_tol=precision)
        assert math.isclose(float(point[1]), 0.4, abs_tol=precision)
        value = weighted_model_checker.get_optimal_weighted_sum()
        assert math.isclose(float(value), -3.4, abs_tol=precision)
        scheduler = inverter.create_memory_scheduler_from_product_scheduler(weighted_model_checker.compute_scheduler())
        assert scheduler.memory_size == 4

    def test_maze_double(self):
        path = stormpy.examples.files.prism_mdp_maze_multigoal
        prism_program = stormpy.parse_prism_program(path)
        formula_str = 'multi(Rmin=? [F "goalalt1"], Pmax=? [F "goalalt2"])'
        prop = stormpy.parse_property(formula_str, prism_program)
        options = stormpy.BuilderOptions(prop)
        options.set_build_state_valuations()
        model = stormpy.build_model(prism_program, options=options)
        self._check_maze_weighted_objective(model, prop)

    def test_maze_exact(self):
        path = stormpy.examples.files.prism_mdp_maze_multigoal
        prism_program = stormpy.parse_prism_program(path)
        formula_str = 'multi(Rmin=? [F "goalalt1"], Pmax=? [F "goalalt2"])'
        prop = stormpy.parse_property(formula_str, prism_program)
        model = stormpy.build_model[stormpy.Rational](prism_program, prop)
        assert model.is_exact
        self._check_maze_weighted_objective(model, prop)

import math

import stormpy
from helpers.helper import get_example_path


class TestEnvironment:
    def test_environment(self):
        env = stormpy.Environment()

    def test_environment_from_settings(self):
        default_method = stormpy.Environment().solver().min_max().method
        assert default_method != stormpy.MinMaxMethod.POLICY_ITERATION
        stormpy.developer.set_from_exploded_string(["--minmax:method", "pi"])
        env = stormpy.developer.EnvironmentBuilder.build_environment()
        assert isinstance(env, stormpy.Environment)
        assert env.solver().min_max().method == stormpy.MinMaxMethod.POLICY_ITERATION
        # Environments created directly do not depend on the settings
        assert stormpy.Environment().solver().min_max().method == default_method

    def test_exploration_environment(self):
        env = stormpy.Environment()
        exploration = env.exploration()
        exploration.precomputation_type = stormpy.PrecomputationType.LOCAL
        assert env.exploration().precomputation_type == stormpy.PrecomputationType.LOCAL
        exploration.next_state_heuristic = stormpy.NextStateHeuristic.UNIFORM
        assert env.exploration().next_state_heuristic == stormpy.NextStateHeuristic.UNIFORM
        exploration.steps_until_precomputation = 42
        assert env.exploration().steps_until_precomputation == 42
        exploration.precision = 1e-4
        assert env.exploration().precision == 1e-4
        exploration.sampled_paths_until_precomputation = 7
        assert env.exploration().sampled_paths_until_precomputation == 7
        exploration.sampled_paths_until_precomputation = None
        assert env.exploration().sampled_paths_until_precomputation is None

    def test_linear_equation_solver(self):
        env = stormpy.Environment()
        env.solver().set_linear_equation_solver_type(stormpy.EquationSolverType.NATIVE)
        env.solver().native().method = stormpy.NativeLinearEquationSolverMethod.POWER
        assert env.solver().get_linear_equation_solver_type() == stormpy.EquationSolverType.NATIVE
        assert env.solver().native().method == stormpy.NativeLinearEquationSolverMethod.POWER
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        prop = stormpy.parse_property('P=? [F "one"]', program)
        model = stormpy.build_model(program, prop)
        result = stormpy.model_checking(model, prop, environment=env)
        assert math.isclose(result[model.initial_states[0]], 1 / 6, rel_tol=1e-4)

    def test_multi_objective_method(self):
        env = stormpy.Environment()
        assert env.modelchecker().multi().method == stormpy.MultiObjectiveMethod.PCAA
        env.modelchecker().multi().method = stormpy.MultiObjectiveMethod.CONSTRAINT_BASED
        assert env.modelchecker().multi().method == stormpy.MultiObjectiveMethod.CONSTRAINT_BASED

    def test_steady_state_distribution_algorithm(self):
        model = stormpy.build_model_from_drn(get_example_path("ctmc", "dft.drn"))
        env = stormpy.Environment()
        assert env.modelchecker().steady_state_distribution_algorithm == stormpy.SteadyStateDistributionAlgorithm.AUTOMATIC
        env.modelchecker().steady_state_distribution_algorithm = stormpy.SteadyStateDistributionAlgorithm.CLASSIC
        assert env.modelchecker().steady_state_distribution_algorithm == stormpy.SteadyStateDistributionAlgorithm.CLASSIC
        default_result = stormpy.compute_steady_state_distribution(model).get_finite_value_vector()
        classic_result = stormpy.compute_steady_state_distribution(model, environment=env).get_finite_value_vector()
        assert all(math.isclose(a, b, abs_tol=1e-6) for a, b in zip(default_result, classic_result))

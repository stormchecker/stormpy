import math

import stormpy
from helpers.helper import get_example_path


class TestEnvironment:
    def test_environment(self):
        env = stormpy.Environment()

    def test_environment_from_settings(self):
        default_method = stormpy.Environment().solver().min_max().method
        assert default_method != stormpy.environments.MinMaxMethod.POLICY_ITERATION
        stormpy.developer.set_from_exploded_string(["--minmax:method", "pi"])
        env = stormpy.developer.EnvironmentBuilder.build_environment()
        assert isinstance(env, stormpy.Environment)
        assert env.solver().min_max().method == stormpy.environments.MinMaxMethod.POLICY_ITERATION
        # Environments created directly do not depend on the settings
        assert stormpy.Environment().solver().min_max().method == default_method

    def test_exploration_environment(self):
        env = stormpy.environments.sound()
        exploration = env.exploration()
        exploration.precomputation_type = stormpy.environments.PrecomputationType.LOCAL
        assert env.exploration().precomputation_type == stormpy.environments.PrecomputationType.LOCAL
        exploration.next_state_heuristic = stormpy.environments.NextStateHeuristic.UNIFORM
        assert env.exploration().next_state_heuristic == stormpy.environments.NextStateHeuristic.UNIFORM
        exploration.steps_until_precomputation = 42
        assert env.exploration().steps_until_precomputation == 42
        exploration.precision = 1e-4
        assert env.exploration().precision == 1e-4
        exploration.sampled_paths_until_precomputation = 7
        assert env.exploration().sampled_paths_until_precomputation == 7
        exploration.sampled_paths_until_precomputation = None
        assert env.exploration().sampled_paths_until_precomputation is None

    def test_linear_equation_solver(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        prop = stormpy.parse_property('P=? [F "one"]', program)
        model = stormpy.build_model(program, prop)
        env = stormpy.environments.default(model)
        env.solver().set_linear_equation_solver_type(stormpy.environments.EquationSolverType.NATIVE)
        env.solver().native().method = stormpy.environments.NativeLinearEquationSolverMethod.OPTIMISTIC_VALUE_ITERATION
        assert env.solver().get_linear_equation_solver_type() == stormpy.environments.EquationSolverType.NATIVE
        assert env.solver().native().method == stormpy.environments.NativeLinearEquationSolverMethod.OPTIMISTIC_VALUE_ITERATION
        result = stormpy.model_checking(model, prop, environment=env)
        assert math.isclose(result[model.initial_states[0]], 1 / 6, rel_tol=1e-4)

    def test_multi_objective_method(self):
        env = stormpy.environments.sound()
        assert env.modelchecker().multi().method == stormpy.environments.MultiObjectiveMethod.PCAA
        env.modelchecker().multi().method = stormpy.environments.MultiObjectiveMethod.CONSTRAINT_BASED
        assert env.modelchecker().multi().method == stormpy.environments.MultiObjectiveMethod.CONSTRAINT_BASED

    def test_steady_state_distribution_algorithm(self):
        model = stormpy.build_model_from_drn(get_example_path("ctmc", "dft.drn"))
        env = stormpy.environments.default(model)
        # The sound environment selects the algorithm based on expected visiting times
        assert env.modelchecker().steady_state_distribution_algorithm == stormpy.environments.SteadyStateDistributionAlgorithm.EXPECTED_VISITING_TIMES
        env.modelchecker().steady_state_distribution_algorithm = stormpy.environments.SteadyStateDistributionAlgorithm.CLASSIC
        assert env.modelchecker().steady_state_distribution_algorithm == stormpy.environments.SteadyStateDistributionAlgorithm.CLASSIC
        default_result = stormpy.analysis.compute_steady_state_distribution(model).get_finite_value_vector()
        classic_result = stormpy.analysis.compute_steady_state_distribution(model, environment=env).get_finite_value_vector()
        assert all(math.isclose(a, b, abs_tol=1e-6) for a, b in zip(default_result, classic_result))


class TestEnvironmentFactories:
    def test_sound(self):
        env = stormpy.environments.sound()
        assert isinstance(env, stormpy.Environment)
        assert env.solver().force_soundness
        assert not env.solver().force_exact
        assert not stormpy.Environment().solver().force_soundness

    def test_exact(self):
        env = stormpy.environments.exact()
        assert env.solver().force_exact
        assert not env.solver().force_soundness
        assert not stormpy.Environment().solver().force_exact

    def test_new_environment_per_call(self):
        env = stormpy.environments.sound()
        env.solver().force_soundness = False
        assert stormpy.environments.sound().solver().force_soundness

    def test_developer_factories(self):
        assert stormpy.developer.SoundEnvironmentFactory().create().solver().force_soundness
        assert stormpy.developer.ExactEnvironmentFactory().create().solver().force_exact
        assert isinstance(stormpy.developer.ExactEnvironmentFactory(), stormpy.developer.EnvironmentFactory)
        env = stormpy.developer.EnvironmentFactory().create()
        assert not env.solver().force_soundness and not env.solver().force_exact
        assert stormpy.developer.get_sound_environment().solver().force_soundness
        assert stormpy.developer.get_exact_environment().solver().force_exact

    def test_default(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        properties = stormpy.parse_properties('P=? [ F "one" ]', program)
        model = stormpy.build_model(program, properties)
        assert stormpy.environments.default(model).solver().force_soundness
        exact_model = stormpy.build_model[stormpy.Rational](program, properties)
        assert stormpy.environments.default(exact_model).solver().force_exact
        symbolic_model = stormpy.build_symbolic_model(program, properties)
        assert stormpy.environments.default(symbolic_model).solver().force_soundness

    def test_default_parametric(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "parametric_die.pm"))
        properties = stormpy.parse_properties("P=? [F s=7 & d=2]", program)
        model = stormpy.build_model[stormpy.RationalFunction](program, properties)
        assert stormpy.environments.default(model).solver().force_exact

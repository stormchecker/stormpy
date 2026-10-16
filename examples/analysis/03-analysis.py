import stormpy

import stormpy.examples
import stormpy.examples.files


def example_analysis_03():
    path = stormpy.examples.files.prism_dtmc_die
    prism_program = stormpy.parse_prism_program(path)

    formula_str = "P=? [F s=7 & d=2]"
    prop = stormpy.parse_property(formula_str, prism_program)
    model = stormpy.build_model(prism_program, prop)
    env = stormpy.environments.default(model)
    env.solver().set_linear_equation_solver_type(stormpy.environments.EquationSolverType.NATIVE)
    env.solver().native().method = stormpy.environments.NativeLinearEquationSolverMethod.OPTIMISTIC_VALUE_ITERATION
    env.solver().native().precision = stormpy.Rational("0.9")
    # env.solver().native().maximal_number_of_iterations = 2
    result = stormpy.model_checking(model, prop, environment=env)
    print(result[model.initial_states[0]])

    dd_model = stormpy.build_model(prism_program, prop, engine=stormpy.Engine.DD)
    result = stormpy.model_checking(dd_model, prop, engine=stormpy.Engine.DD, environment=env)
    stormpy.filter_initial_states(result, dd_model)
    assert result.get_min() == result.get_max()
    print(result.get_min())


if __name__ == "__main__":
    example_analysis_03()

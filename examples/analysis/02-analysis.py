import stormpy
from stormpy.storage import Expression

import stormpy.examples
import stormpy.examples.files


def example_analysis_02():
    path = stormpy.examples.files.prism_dtmc_die
    prism_program = stormpy.parse_prism_program(path)

    formula_str = "P=? [F s=7 & d=2]"
    properties = stormpy.parse_properties(formula_str, prism_program)
    model = stormpy.build_symbolic_model(prism_program, properties)
    result = stormpy.model_checking(model, properties[0])
    filter = stormpy.create_filter_initial_states_symbolic(model)
    result.filter(filter)
    assert result.min == result.max
    print(result.min)

    # Create an auxiliary mapping to build expressions that matches some state.
    variables = dict()
    for m in prism_program.modules:
        for v in m.integer_variables:
            variables[v.name] = v.expression_variable.get_expression()
    expr_manager = prism_program.expression_manager

    expr_for_state_1 = Expression.Conjunction(
        [Expression.Eq(variables["s"], expr_manager.create_integer(1)), Expression.Eq(variables["d"], expr_manager.create_integer(0))]
    )
    expr_for_state_2 = Expression.And(
        Expression.Eq(variables["s"], expr_manager.create_integer(4)), Expression.Eq(variables["d"], expr_manager.create_integer(0))
    )

    result = stormpy.model_checking(model, properties[0])
    cached_res = result.clone()
    cached_res.filter(stormpy.create_filter_symbolic(model, expr_for_state_1))
    print(cached_res.min)
    result.filter(stormpy.create_filter_symbolic(model, expr_for_state_2))
    assert result.min == result.max
    print(result.min)


if __name__ == "__main__":
    example_analysis_02()

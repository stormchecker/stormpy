import stormpy

import stormpy.examples
import stormpy.examples.files


def example_highlevel_models():
    """
    This method considers a grid with a constant V.
    We create an all-in-one MDP, i.e., we create an MDP that contains copies for different values of V.
    By model checking, we obtain values for different values of V.
    """
    path = stormpy.examples.files.prism_mdp_slipgrid_sketch
    prism_program = stormpy.parse_prism_program(path)
    prop_string = 'Rmin=? [F "target"]'
    prop = stormpy.parse_property(prop_string, prism_program)
    # Note: The following is necessary for the code to work correctly, as otherwise there will be a default initial value injected.
    prism_program = prism_program.replace_variable_initialization_by_init_expression()

    emgr = prism_program.expression_manager
    Vvar = prism_program.get_constant("V")
    Vvalues = {2, 4, 6, 8, 10}
    all_in_one_program = prism_program.replace_constant_by_variable(Vvar, emgr.integer(min(Vvalues)), emgr.integer(max(Vvalues)))
    options = [stormpy.expressions.Expression.Eq(Vvar.expression_variable.get_expression(), emgr.integer(val)) for val in Vvalues]
    all_in_one_program.update_initial_states_expression(
        stormpy.expressions.Expression.And(all_in_one_program.initial_states_expression, stormpy.expressions.Expression.Disjunction(options))
    )
    print(all_in_one_program)

    for v in all_in_one_program.constants:
        print(f"Variable {v.name} is {v.definition}")
    build_options = stormpy.BuilderOptions(prop)
    build_options.set_build_state_valuations()
    sparse_model = stormpy.build_model(all_in_one_program, options=build_options)
    print(sparse_model)
    result = stormpy.model_checking(sparse_model, prop, extract_scheduler=True, only_initial_states=True)
    stormpy.filter_initial_states(result, sparse_model)
    result_for_vvar = {int(sparse_model.state_valuations.get_value(x, Vvar.expression_variable)): result[x] for x in sparse_model.initial_states}
    print(result_for_vvar)

    dd_model = stormpy.build_symbolic_model(all_in_one_program)
    print(dd_model)
    result = stormpy.model_checking(dd_model, prop, only_initial_states=True, engine=stormpy.Engine.DD)
    stormpy.filter_initial_states(result, dd_model)

    resultvalues = result.get_value_vector()
    # Notice that the manager seems to be different than the manager for the prism program. So we solve it like this
    result_for_vvar = {int(valuation.get_value(valuation.expression_manager.get_variable("V"))): mc_result for valuation, mc_result in resultvalues}
    print(result_for_vvar)


if __name__ == "__main__":
    example_highlevel_models()

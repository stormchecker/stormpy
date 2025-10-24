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
    properties = stormpy.parse_properties(prop_string, prism_program)
    # Note: The following is necessary for the code to work correctly, as otherwise there will be a default initial value injected.
    prism_program = prism_program.replace_variable_initialization_by_init_expression()

    emgr = prism_program.expression_manager
    Vvar = prism_program.get_constant("V")
    Vvalues = {2, 4, 6, 8, 10, 12}
    all_in_one_program = prism_program.replace_constant_by_variable(Vvar, emgr.create_integer(min(Vvalues)), emgr.create_integer(max(Vvalues)))
    options = [stormpy.Expression.Eq(Vvar.expression_variable.get_expression(), emgr.create_integer(val)) for val in Vvalues]
    all_in_one_program.update_initial_states_expression(
        stormpy.Expression.And(all_in_one_program.initial_states_expression, stormpy.Expression.Disjunction(options))
    )
    print(all_in_one_program)

    for v in all_in_one_program.constants:
        print(f"Variable {v.name} is {v.definition}")
    build_options = stormpy.BuilderOptions([p.raw_formula for p in properties])
    build_options.set_build_state_valuations()
    sparse_model = stormpy.build_sparse_model_with_options(all_in_one_program, build_options)
    print(sparse_model)
    result = stormpy.check_model_sparse(sparse_model, properties[0], extract_scheduler=True, only_initial_states=True)
    filter_sparse = stormpy.create_filter_initial_states_sparse(sparse_model)
    result.filter(filter_sparse)
    result_for_vvar = {int(sparse_model.state_valuations.get_value(x, Vvar.expression_variable)): result.at(x) for x in sparse_model.initial_states}
    print(result_for_vvar)

    dd_model = stormpy.build_symbolic_model(all_in_one_program)
    print(dd_model)
    filter_dd = stormpy.create_filter_initial_states_symbolic(dd_model)
    result = stormpy.check_model_dd(dd_model, properties[0], only_initial_states=True)
    result.filter(filter_dd)

    resultvalues = result.get_values()
    # Notice that the manager seems to be different than the manager for the prism program. So we solve it like this
    result_for_vvar = {int(valuation.get_value(valuation.expression_manager.get_variable("V"))): mc_result for valuation, mc_result in resultvalues}
    print(result_for_vvar)


if __name__ == "__main__":
    example_highlevel_models()

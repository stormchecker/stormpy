import stormpy
import stormpy.examples
import stormpy.examples.files


class TestBuilding:
    def test_explicit_builder(self):
        path = stormpy.examples.files.prism_dtmc_die
        prism_program = stormpy.parse_prism_program(path)
        formula_str = "P=? [F s=7 & d=2]"
        properties = stormpy.parse_properties_for_prism_program(formula_str, prism_program)

        # Fix variables in the program.
        module = prism_program.modules[0]
        s_var = module.get_integer_variable("s").expression_variable
        d_var = module.get_integer_variable("d").expression_variable

        # Construct the model
        options = stormpy.BuilderOptions([p.raw_formula for p in properties])
        options.set_build_state_valuations()
        model_builder = stormpy.make_sparse_model_builder(prism_program, options)
        model = model_builder.build()
        # and export the model from building
        state_mapping = model_builder.export_lookup()

        # lookup 1
        state = {s_var: prism_program.expression_manager.create_integer(3), d_var: prism_program.expression_manager.create_integer(0)}
        id = state_mapping.lookup(state)
        assert model.state_valuations.get_value(id, s_var) == 3
        assert model.state_valuations.get_value(id, d_var) == 0

        # lookup 2
        state = {s_var: prism_program.expression_manager.create_integer(7), d_var: prism_program.expression_manager.create_integer(3)}
        id = state_mapping.lookup(state)
        assert model.state_valuations.get_value(id, s_var) == 7
        assert model.state_valuations.get_value(id, d_var) == 3

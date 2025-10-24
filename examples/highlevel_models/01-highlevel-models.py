import stormpy

import stormpy.examples
import stormpy.examples.files


def example_highlevel_models():
    path = stormpy.examples.files.prism_pdtmc_die
    prism_program = stormpy.parse_prism_program(path)
    for c in prism_program.constants:
        print("constant {} with type {} is {} defined".format(c.name, c.type, "" if c.defined else "not"))

    path = stormpy.examples.files.prism_dtmc_brp
    prism_program = stormpy.parse_prism_program(path)
    for module in prism_program.modules:
        for v in module.integer_variables:
            print(f"Variable {v.name} has bounds {v.lower_bound_expression} and {v.upper_bound_expression}")
        for v in module.boolean_variables:
            print(f"Variable {v.name} is Boolean")


if __name__ == "__main__":
    example_highlevel_models()

import stormpy

import stormpy.examples
import stormpy.examples.files


def example_analysis_01():
    path = stormpy.examples.files.prism_dtmc_die
    prism_program = stormpy.parse_prism_program(path)

    formula_str = "P=? [F s=7 & d=2]"
    properties = stormpy.parse_properties(formula_str, prism_program)
    model = stormpy.build_model(prism_program, properties)
    prob0E, prob1A = stormpy.prob01min_states(model, properties[0].raw_formula.subformula)
    print(prob0E)
    print(prob1A)


if __name__ == "__main__":
    example_analysis_01()

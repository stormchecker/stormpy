import stormpy
import stormpy.dft

import stormpy.examples
import stormpy.examples.files


def example_dfts_01():
    # Load from JSON
    path_json = stormpy.examples.files.dft_json_and
    dft_small = stormpy.dft.load_dft_json_file(path_json)
    print(dft_small)

    # Load from Galileo
    path = stormpy.examples.files.dft_galileo_hecs
    dft = stormpy.dft.load_dft_galileo_file(path)
    print("DFT with {} elements.".format(dft.nr_elements()))
    print("DFT has {} BEs and {} dynamic elements.".format(dft.nr_basic_elements(), dft.nr_dynamic_elements()))

    # Analyze
    formula_str = 'T=? [ F "failed" ]'
    formulas = stormpy.parse_properties(formula_str)
    env = stormpy.dft.DftEnvironment()
    results = stormpy.dft.analyze_dft(env, dft, formulas)
    result = results[0]
    print(result)


if __name__ == "__main__":
    example_dfts_01()

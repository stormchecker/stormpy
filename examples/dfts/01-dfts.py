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
    print("DFT has {} BEs and {} dynamic elements.".format(dft.nr_be(), dft.nr_dynamic()))

    # Analyze
    formula_str = 'T=? [ F "failed" ]'
    formulas = stormpy.parse_properties(formula_str)
    results = stormpy.dft.analyze_dft(dft, [formulas[0].raw_formula])
    result = results[0]
    print(result)


if __name__ == "__main__":
    example_dfts_01()

"""Demonstrate explicit and inferred stormpy template specializations."""

import stormpy
import stormpy.dft
import stormpy.examples.files


def demonstrate_generic_dft_types():
    # Readable aliases:
    assert stormpy.dft._dft._DFT_Double is stormpy.dft.DFT[float]
    assert stormpy.dft._dft._DFT_RationalFunction is stormpy.dft.DFT[stormpy.RationalFunction]

    path = stormpy.examples.files.dft_json_and
    double_dft = stormpy.dft.load_dft_json_file(path)
    assert type(double_dft) is stormpy.dft.DFT[float]

    rational_function_dft = stormpy.dft.load_parametric_dft_json_file(path)
    assert type(rational_function_dft) is stormpy.dft.DFT[stormpy.RationalFunction]

    # Construct a specialization explicitly:
    explicit_builder = stormpy.dft.ExplicitDFTModelBuilder[float](double_dft)
    assert type(explicit_builder) is stormpy.dft.ExplicitDFTModelBuilder[float]

    # Or deduce the specialization from the constructor argument:
    inferred_builder = stormpy.dft.ExplicitDFTModelBuilder(rational_function_dft)
    assert type(inferred_builder) is stormpy.dft.ExplicitDFTModelBuilder[stormpy.RationalFunction]

    # Overloaded functions call the specialization:
    concrete_model = stormpy.dft.build_model(double_dft)
    assert not concrete_model.supports_parameters

    parametric_model = stormpy.dft.build_model(rational_function_dft)
    assert parametric_model.supports_parameters


if __name__ == "__main__":
    demonstrate_generic_dft_types()

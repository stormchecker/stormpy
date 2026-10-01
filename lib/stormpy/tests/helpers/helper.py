import os
import stormpy
import stormpy.examples
import stormpy.examples.files

example_dir = stormpy.examples.files.testfile_dir


def get_example_path(*paths):
    return os.path.join(example_dir, *paths)


def build_sparse_model(path, value_type):
    program = stormpy.parse_prism_program(path)
    if value_type in (stormpy.Rational, stormpy.RationalInterval):
        model = stormpy.build_sparse_exact_model(program)
    elif value_type is stormpy.RationalFunction:
        model = stormpy.build_parametric_model(program)
    else:
        model = stormpy.build_model(program)
    # The following are hardcoded interval values for testing purposes
    if value_type is stormpy.Interval:
        model = stormpy.AddUncertainty(model).transform(0.01)
    elif value_type is stormpy.RationalInterval:
        model = stormpy.AddUncertainty(model).transform(stormpy.Rational("1/100"))
    return model

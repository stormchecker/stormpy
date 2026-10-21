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
        model = stormpy.build_model[stormpy.Rational](program)
    elif value_type is stormpy.RationalFunction:
        model = stormpy.build_model[stormpy.RationalFunction](program)
    else:
        model = stormpy.build_model(program)
    # The following are hardcoded interval values for testing purposes
    if value_type is stormpy.Interval:
        model = stormpy.transformations.add_uncertainty(model, 0.01)
    elif value_type is stormpy.RationalInterval:
        model = stormpy.transformations.add_uncertainty(model, stormpy.Rational("1/100"))
    return model

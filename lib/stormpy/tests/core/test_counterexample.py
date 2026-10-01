import stormpy


def test_counterexample_options_default():
    options = stormpy.SMTCounterExampleGeneratorOptions()
    assert type(options) is stormpy.SMTCounterExampleGeneratorOptions[float]

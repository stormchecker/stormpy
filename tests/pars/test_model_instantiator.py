import pytest
import stormpy
from helpers.helper import get_example_path

from configurations import pars
import math


@pars
class TestModelInstantiator:
    def test_instantiate_dtmc(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        formula = stormpy.parse_property("P=? [ F s=5 ]", program)
        model = stormpy.build_model[stormpy.RationalFunction](program, formula)
        parameters = model.collect_all_parameters()
        assert len(parameters) == 2
        instantiator = stormpy.pars.ModelInstantiator(model)
        assert type(instantiator) is stormpy.pars.ModelInstantiator[stormpy.models.ModelType.DTMC, float]
        assert tuple(parameter.kind for parameter in stormpy.pars.ModelInstantiator.metadata.parameters) == ("value", "type")

        point = {p: stormpy.RationalFunctionCoefficient("0.4") for p in parameters}
        instantiated_model = instantiator.instantiate(point)
        assert instantiated_model.nr_states == model.nr_states
        assert not instantiated_model.has_parameters
        assert "0.4" in str(instantiated_model.transition_matrix[1])

        point = {p: stormpy.RationalFunctionCoefficient("0.5") for p in parameters}
        instantiated_model2 = instantiator.instantiate(point)
        assert "0.5" in str(instantiated_model2.transition_matrix[1])

    def test_instantiate_dtmc_die(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "parametric_die.pm"))
        formula = stormpy.parse_property("P=? [F s=7 & d=2]", program)
        model = stormpy.build_model[stormpy.RationalFunction](program, formula)
        parameters = model.collect_all_parameters()
        assert len(parameters) == 2
        instantiator = stormpy.pars.ModelInstantiator[stormpy.models.ModelType.DTMC, float](model)
        point = dict()
        for x in parameters:
            assert x.name in {"p", "q"}
            point[x] = stormpy.RationalFunctionCoefficient(0.4)
        instantiated_model = instantiator.instantiate(point)
        assert instantiated_model.nr_states == model.nr_states
        assert not instantiated_model.has_parameters

        result = stormpy.model_checking(instantiated_model, formula)
        initial_state = instantiated_model.initial_states[0]
        assert initial_state == 0
        assert math.isclose(result[initial_state], 4 / 35, rel_tol=1e-6)

    def test_sample_pdtmc(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        formula = stormpy.parse_property('P=? [F "error"]', program)
        model = stormpy.build_model[stormpy.RationalFunction](program, formula)

        parameters = model.collect_all_parameters()
        instantiator = stormpy.pars.ModelInstantiator[stormpy.models.ModelType.DTMC, float](model)

        point = {p: stormpy.RationalFunctionCoefficient("0.4") for p in parameters}
        instantiated_model = instantiator.instantiate(point)
        assert instantiated_model.nr_states == model.nr_states
        assert not instantiated_model.has_parameters
        assert "0.4" in str(instantiated_model.transition_matrix[1])

        point = {p: stormpy.RationalFunctionCoefficient("0.5") for p in parameters}
        instantiated_model2 = instantiator.instantiate(point)
        assert "0.5" in str(instantiated_model2.transition_matrix[1])

    def test_pdtmc_instantiation_model_checking(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "herman5.pm"))
        formula = stormpy.parse_property('R=? [F "stable"]', program)
        model = stormpy.build_model[stormpy.RationalFunction](program, formula)

        parameters = model.collect_all_parameters()
        env = stormpy.environments.default(model)
        instantiator = stormpy.pars.ModelInstantiator(model)

        point = {p: stormpy.RationalFunctionCoefficient("1/2") for p in parameters}
        instantiated_model = instantiator.instantiate(point)
        result = stormpy.model_checking(instantiated_model, formula, only_initial_states=True, environment=env)
        assert isinstance(result, stormpy.ExplicitQuantitativeCheckResult[float])
        res = result[instantiated_model.initial_states[0]]
        assert isinstance(res, stormpy.BoundedValue)
        assert isinstance(res.value, float)
        assert math.isclose(res, 29 / 15)

    def test_pdtmc_exact_instantiation_model_checking(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "herman5.pm"))
        formula = stormpy.parse_property('R=? [F "stable"]', program)
        model = stormpy.build_model[stormpy.RationalFunction](program, formula)

        parameters = model.collect_all_parameters()
        env = stormpy.environments.default(model)
        instantiator = stormpy.pars.ModelInstantiator[stormpy.models.ModelType.DTMC, stormpy.Rational](model)

        point = {p: stormpy.RationalFunctionCoefficient("1/2") for p in parameters}
        instantiated_model = instantiator.instantiate(point)
        assert not instantiated_model.has_parameters
        result = stormpy.model_checking(instantiated_model, formula, only_initial_states=True, environment=env)
        assert isinstance(result, stormpy.ExplicitQuantitativeCheckResult[stormpy.Rational])
        res = result[instantiated_model.initial_states[0]]
        assert isinstance(res.value, stormpy.Rational)
        assert res == stormpy.Rational("29/15")
        assert res.lower == res.upper == res.value

    def test_pdtmc_exact_instantiation_model_checking_die(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "parametric_die.pm"))
        formula = stormpy.parse_property("P=? [F s=7 & d=2]", program)
        model = stormpy.build_model[stormpy.RationalFunction](program, formula)

        parameters = model.collect_all_parameters()
        env = stormpy.environments.default(model)
        instantiator = stormpy.pars.ModelInstantiator[stormpy.models.ModelType.DTMC, stormpy.Rational](model)

        point = {p: stormpy.RationalFunctionCoefficient("2/5") for p in parameters}
        instantiated_model = instantiator.instantiate(point)
        assert not instantiated_model.has_parameters
        result = stormpy.model_checking(instantiated_model, formula, only_initial_states=True, environment=env)
        assert isinstance(result, stormpy.ExplicitQuantitativeCheckResult[stormpy.Rational])
        res = result[instantiated_model.initial_states[0]]
        assert isinstance(res.value, stormpy.Rational)
        assert res == stormpy.Rational("4/35")
        assert res.lower == res.upper == res.value


@pars
class TestInstantiationCheckerDeveloper:
    @pytest.mark.parametrize("result_type", [float, stormpy.Rational], ids=["float", "rational"])
    @pytest.mark.parametrize(
        "model_file, property_text, valuations_and_results",
        [
            pytest.param(
                "herman5.pm",
                'R=? [F "stable"]',
                [("1/2", "29/15"), ("2/5", "38525/19456"), ("1/2", "29/15")],
                id="rewards",
            ),
            pytest.param(
                "parametric_die.pm",
                "P=? [F s=7 & d=2]",
                [("1/2", "1/6"), ("2/5", "4/35"), ("1/2", "1/6")],
                id="probabilities",
            ),
        ],
    )
    def test_repeated_valuations(self, result_type, model_file, property_text, valuations_and_results):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", model_file))
        prop = stormpy.parse_property(property_text, program)
        model = stormpy.build_model[stormpy.RationalFunction](program, prop)
        env = stormpy.environments.sound() if result_type is float else stormpy.environments.exact()
        family = stormpy.pars.developer.SparseInstantiationModelChecker
        checker_type = family[stormpy.models.ModelType.DTMC, result_type]
        checker = family(environment=env, model=model) if result_type is float else checker_type(env, model)
        assert type(checker) is checker_type
        checker.specify_formula(stormpy.developer.CheckTask[stormpy.RationalFunction](prop.get_raw_formula(), True))
        checker.set_instantiations_are_graph_preserving(True)

        for parameter_value, expected_value in valuations_and_results:
            valuation = {parameter: stormpy.RationalFunctionCoefficient(parameter_value) for parameter in model.collect_all_parameters()}
            result = checker.check(env, valuation)
            assert isinstance(result, stormpy.ExplicitQuantitativeCheckResult[result_type])
            value = result[model.initial_states[0]]
            assert isinstance(value, stormpy.BoundedValue)
            assert isinstance(value.value, result_type)
            if result_type is float:
                assert math.isclose(value.value, float(stormpy.Rational(expected_value)), rel_tol=1e-6)
            else:
                assert value.lower == value.upper == value.value == stormpy.Rational(expected_value)

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

    def test_pdtmc_instantiation_checker(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "herman5.pm"))
        formula = stormpy.parse_property('R=? [F "stable"]', program)
        model = stormpy.build_model[stormpy.RationalFunction](program, formula)

        parameters = model.collect_all_parameters()
        env = stormpy.environments.default(model)
        inst_checker = stormpy.pars.ModelInstantiationChecker(env, model)
        assert type(inst_checker) is stormpy.pars.ModelInstantiationChecker[stormpy.models.ModelType.DTMC, float]
        inst_checker.specify_formula(stormpy.developer.CheckTask[stormpy.RationalFunction](formula.get_raw_formula(), True))
        inst_checker.set_graph_preserving(True)

        point = {p: stormpy.RationalFunctionCoefficient(1 / 2) for p in parameters}
        result = inst_checker.check(env, point)
        assert isinstance(result, stormpy.ExplicitQuantitativeCheckResult[float])
        res = result[model.initial_states[0]]
        assert isinstance(res, stormpy.BoundedValue)
        assert isinstance(res.value, float)
        assert math.isclose(res, 29 / 15)

    def test_pdtmc_exact_instantiation_checker(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "herman5.pm"))
        formula = stormpy.parse_property('R=? [F "stable"]', program)
        model = stormpy.build_model[stormpy.RationalFunction](program, formula)

        parameters = model.collect_all_parameters()
        env = stormpy.environments.default(model)
        inst_checker = stormpy.pars.ModelInstantiationChecker[stormpy.models.ModelType.DTMC, stormpy.Rational](env, model)
        inst_checker.specify_formula(stormpy.developer.CheckTask[stormpy.RationalFunction](formula.get_raw_formula(), True))
        inst_checker.set_graph_preserving(True)

        point = {p: stormpy.RationalFunctionCoefficient("1/2") for p in parameters}
        result = inst_checker.check(env, point)
        assert isinstance(result, stormpy.ExplicitQuantitativeCheckResult[stormpy.Rational])
        res = result[model.initial_states[0]]
        assert isinstance(res.value, stormpy.Rational)
        assert res == stormpy.Rational("29/15")
        assert res.lower == res.upper == res.value

    def test_pdtmc_exact_instantiation_checker_die(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "parametric_die.pm"))
        formula = stormpy.parse_property("P=? [F s=7 & d=2]", program)
        model = stormpy.build_model[stormpy.RationalFunction](program, formula)

        parameters = model.collect_all_parameters()
        env = stormpy.environments.default(model)
        inst_checker = stormpy.pars.ModelInstantiationChecker[stormpy.models.ModelType.DTMC, stormpy.Rational](env, model)
        inst_checker.specify_formula(stormpy.developer.CheckTask[stormpy.RationalFunction](formula.get_raw_formula(), True))
        inst_checker.set_graph_preserving(True)

        point = {p: stormpy.RationalFunctionCoefficient("2/5") for p in parameters}
        result = inst_checker.check(env, point)
        assert isinstance(result, stormpy.ExplicitQuantitativeCheckResult[stormpy.Rational])
        res = result[model.initial_states[0]]
        assert isinstance(res.value, stormpy.Rational)
        assert res == stormpy.Rational("4/35")
        assert res.lower == res.upper == res.value

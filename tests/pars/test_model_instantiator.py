import stormpy
from helpers.helper import get_example_path

from configurations import pars
import math


@pars
class TestModelInstantiator:
    def test_instantiate_dtmc(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        formulas = stormpy.parse_properties_for_prism_program("P=? [ F s=5 ]", program)
        model = stormpy.build_parametric_model(program, formulas)
        parameters = model.collect_probability_parameters()
        assert len(parameters) == 2
        instantiator = stormpy.pars.ModelInstantiator(model)

        point = {p: stormpy.RationalRF("0.4") for p in parameters}
        instantiated_model = instantiator.instantiate(point)
        assert instantiated_model.nr_states == model.nr_states
        assert not instantiated_model.has_parameters
        assert "0.4" in str(instantiated_model.transition_matrix[1])

        point = {p: stormpy.RationalRF("0.5") for p in parameters}
        instantiated_model2 = instantiator.instantiate(point)
        assert "0.5" in str(instantiated_model2.transition_matrix[1])

    def test_sample_pdtmc(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        formulas = stormpy.parse_properties_for_prism_program('P=? [F "error"]', program)
        model = stormpy.build_parametric_model(program, formulas)

        parameters = model.collect_probability_parameters()
        instantiator = stormpy.pars.PDtmcInstantiator(model)

        point = {p: stormpy.RationalRF("0.4") for p in parameters}
        instantiated_model = instantiator.instantiate(point)
        assert instantiated_model.nr_states == model.nr_states
        assert not instantiated_model.has_parameters
        assert "0.4" in str(instantiated_model.transition_matrix[1])

        point = {p: stormpy.RationalRF("0.5") for p in parameters}
        instantiated_model2 = instantiator.instantiate(point)
        assert "0.5" in str(instantiated_model2.transition_matrix[1])

    def test_pdtmc_instantiation_checker(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "herman5.pm"))
        formulas = stormpy.parse_properties_for_prism_program('R=? [F "stable"]', program)
        model = stormpy.build_parametric_model(program, formulas)

        parameters = model.collect_probability_parameters()
        inst_checker = stormpy.pars.PDtmcInstantiationChecker(model)
        inst_checker.specify_formula(stormpy.ParametricCheckTask(formulas[0].raw_formula, True))
        inst_checker.set_graph_preserving(True)
        env = stormpy.Environment()

        point = {p: stormpy.RationalRF(1 / 2) for p in parameters}
        result = inst_checker.check(env, point)
        assert isinstance(result, stormpy.ExplicitQuantitativeCheckResult)
        res = result.at(model.initial_states[0])
        assert isinstance(res, float)
        assert math.isclose(res, 29 / 15)

    def test_pdtmc_exact_instantiation_checker(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "herman5.pm"))
        formulas = stormpy.parse_properties_for_prism_program('R=? [F "stable"]', program)
        model = stormpy.build_parametric_model(program, formulas)

        parameters = model.collect_probability_parameters()
        inst_checker = stormpy.pars.PDtmcExactInstantiationChecker(model)
        inst_checker.specify_formula(stormpy.ParametricCheckTask(formulas[0].raw_formula, True))
        inst_checker.set_graph_preserving(True)
        env = stormpy.Environment()

        point = {p: stormpy.RationalRF("1/2") for p in parameters}
        result = inst_checker.check(env, point)
        assert isinstance(result, stormpy.ExplicitExactQuantitativeCheckResult)
        res = result.at(model.initial_states[0])
        assert isinstance(res, stormpy.Rational)
        assert res == stormpy.Rational("29/15")

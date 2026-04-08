import stormpy
import math
from helpers.helper import get_example_path

from configurations import pars


@pars
class TestPLA:
    def test_to_string(self):
        assert str(stormpy.pars.RegionResultHypothesis.UNKNOWN) == "Unknown"
        assert str(stormpy.pars.RegionResultHypothesis.ALLSAT) == "AllSat?"
        assert str(stormpy.pars.RegionResult.EXISTSVIOLATED) == "ExistsViolated"
        assert str(stormpy.pars.RegionResult.ALLSAT) == "AllSat"

    def test_pla(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        prop = "P<=0.84 [F s=5 ]"
        formulas = stormpy.parse_properties_for_prism_program(prop, program)
        model = stormpy.build_parametric_model(program, formulas)
        assert model.nr_states == 613
        assert model.nr_transitions == 803
        assert model.model_type == stormpy.ModelType.DTMC
        assert model.has_parameters
        env = stormpy.Environment()
        checker = stormpy.pars.create_region_checker(env, model, formulas[0].raw_formula)
        parameters = model.collect_all_parameters()
        assert len(parameters) == 2
        region = stormpy.pars.ParameterRegion.create_from_string("0.7<=pL<=0.9,0.75<=pK<=0.95", parameters)
        result = checker.check_region(env, region)
        assert result == stormpy.pars.RegionResult.ALLSAT
        region = stormpy.pars.ParameterRegion.create_from_string("0.4<=pL<=0.65,0.75<=pK<=0.95", parameters)
        result = checker.check_region(env, region, stormpy.pars.RegionResultHypothesis.UNKNOWN, True)
        assert result == stormpy.pars.RegionResult.EXISTSBOTH
        region = stormpy.pars.ParameterRegion.create_from_string("0.1<=pL<=0.73,0.2<=pK<=0.715", parameters)
        result = checker.check_region(env, region)
        assert result == stormpy.pars.RegionResult.ALLVIOLATED

    def test_pla_region_valuation(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        prop = "P<=0.84 [F s=5 ]"
        formulas = stormpy.parse_properties_for_prism_program(prop, program)
        model = stormpy.build_parametric_model(program, formulas)
        assert model.nr_states == 613
        assert model.nr_transitions == 803
        assert model.model_type == stormpy.ModelType.DTMC
        assert model.has_parameters
        env = stormpy.Environment()
        checker = stormpy.pars.create_region_checker(env, model, formulas[0].raw_formula)
        parameters = model.collect_all_parameters()
        assert len(parameters) == 2
        for par in parameters:
            if par.name == "pL":
                pL = par
            elif par.name == "pK":
                pK = par
            else:
                assert False
        region_valuation = dict()
        region_valuation[pL] = (stormpy.RationalRF(0.7), stormpy.RationalRF(0.9))
        region_valuation[pK] = (stormpy.RationalRF(0.75), stormpy.RationalRF(0.95))
        region = stormpy.pars.ParameterRegion(region_valuation)
        result = checker.check_region(env, region)
        assert result == stormpy.pars.RegionResult.ALLSAT
        region_valuation[pL] = (stormpy.RationalRF(0.4), stormpy.RationalRF(0.65))
        region = stormpy.pars.ParameterRegion(region_valuation)
        result = checker.check_region(env, region, stormpy.pars.RegionResultHypothesis.UNKNOWN, True)
        assert result == stormpy.pars.RegionResult.EXISTSBOTH
        region_valuation[pK] = (stormpy.RationalRF(0.2), stormpy.RationalRF(0.715))
        region_valuation[pL] = (stormpy.RationalRF(0.1), stormpy.RationalRF(0.73))
        region = stormpy.pars.ParameterRegion(region_valuation)
        result = checker.check_region(env, region)
        assert result == stormpy.pars.RegionResult.ALLVIOLATED

    def test_pla_bounds(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        prop = "P=? [F s=5 ]"
        formulas = stormpy.parse_properties_for_prism_program(prop, program)
        model = stormpy.build_parametric_model(program, formulas)
        assert model.has_parameters
        env = stormpy.Environment()
        checker = stormpy.pars.create_region_checker(env, model, formulas[0].raw_formula)
        parameters = model.collect_all_parameters()
        assert len(parameters) == 2
        region = stormpy.pars.ParameterRegion.create_from_string("0.7<=pL<=0.9,0.75<=pK<=0.95", parameters)
        result = checker.get_bound(env, region, True)
        assert math.isclose(float(result), 0.8369631383670559, rel_tol=1e-6)
        result_vec = checker.get_bound_all_states(env, region, True)
        result = result_vec.at(model.initial_states[0])
        assert math.isclose(result, 0.8369631383670559, rel_tol=1e-6)

    def test_pla_manual(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        prop = "P=? [F s=5 ]"
        formulas = stormpy.parse_properties_for_prism_program(prop, program)
        model = stormpy.build_parametric_model(program, formulas)
        assert model.has_parameters
        env = stormpy.Environment()
        checker = stormpy.pars.DtmcParameterLiftingModelChecker()
        checker.specify(env, model, formulas[0].raw_formula)
        parameters = model.collect_all_parameters()
        assert len(parameters) == 2
        region = stormpy.pars.ParameterRegion.create_from_string("0.7<=pL<=0.9,0.75<=pK<=0.95", parameters)
        result = checker.get_bound(env, region, True)
        assert math.isclose(float(result), 0.8369631383670559, rel_tol=1e-6)

    def test_pla_manual_no_simplification(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        prop = "P=? [F s=5 ]"
        formulas = stormpy.parse_properties_for_prism_program(prop, program)
        model = stormpy.build_parametric_model(program, formulas)
        assert model.has_parameters
        env = stormpy.Environment()
        checker = stormpy.pars.DtmcParameterLiftingModelChecker()
        checker.specify(env, model, formulas[0].raw_formula, allow_model_simplification=False)
        parameters = model.collect_all_parameters()
        assert len(parameters) == 2
        region = stormpy.pars.ParameterRegion.create_from_string("0.7<=pL<=0.9,0.75<=pK<=0.95", parameters)
        result = checker.get_bound(env, region, True)
        assert math.isclose(float(result), 0.836963056082918, rel_tol=1e-6)

    def test_pla_state_bounds(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        prop = "P=? [F s=5 ]"
        formulas = stormpy.parse_properties_for_prism_program(prop, program)
        model = stormpy.build_parametric_model(program, formulas)
        assert model.has_parameters
        env = stormpy.Environment()
        checker = stormpy.pars.DtmcParameterLiftingModelChecker()
        checker.specify(env, model, formulas[0].raw_formula, allow_model_simplification=False)
        parameters = model.collect_all_parameters()
        assert len(parameters) == 2
        region = stormpy.pars.ParameterRegion.create_from_string("0.7<=pL<=0.9,0.75<=pK<=0.95", parameters)
        result_vec = checker.get_bound_all_states(env, region, True)
        assert len(result_vec.get_values()) == model.nr_states
        assert math.isclose(result_vec.at(model.initial_states[0]), 0.836963056082918, rel_tol=1e-6)

    def test_compute_extremum(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        prop = "P=? [F s=5 ]"
        formulas = stormpy.parse_properties_for_prism_program(prop, program)
        model = stormpy.build_parametric_model(program, formulas)
        assert model.has_parameters
        env = stormpy.Environment()
        parameters = model.collect_all_parameters()
        assert len(parameters) == 2
        region = stormpy.pars.ParameterRegion.create_from_string("0.7<=pL<=0.9,0.75<=pK<=0.95", parameters)

        refinement_checker = stormpy.pars.create_region_refinement_checker(env, model, formulas[0].raw_formula)
        precision = stormpy.RationalRF(1e-6)
        value, point = refinement_checker.compute_extremum(env, region, stormpy.OptimizationDirection.Maximize, precision, False)
        assert isinstance(value, stormpy.RationalRF)
        assert isinstance(point, dict)
        assert len(point) == 2
        assert 0.83 <= float(value) <= 0.84

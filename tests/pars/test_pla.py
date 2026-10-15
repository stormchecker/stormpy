import stormpy
import math
from helpers.helper import get_example_path

from configurations import pars


@pars
class TestPLA:
    def test_to_string(self):
        assert stormpy.pars.RegionResultHypothesis.UNKNOWN.friendly_name() == "Unknown"
        assert stormpy.pars.RegionResultHypothesis.ALL_SAT.friendly_name() == "AllSat?"
        assert stormpy.pars.RegionResult.EXISTS_VIOLATED.friendly_name() == "ExistsViolated"
        assert stormpy.pars.RegionResult.ALL_SAT.friendly_name() == "AllSat"

    def test_name(self):
        assert stormpy.pars.RegionResult.ALL_SAT.name == "ALL_SAT"
        assert stormpy.pars.RegionResultHypothesis.ALL_SAT.name == "ALL_SAT"

    def test_pla(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        prop = "P<=0.84 [F s=5 ]"
        formula = stormpy.parse_property(prop, program)
        model = stormpy.build_model[stormpy.RationalFunction](program, formula)
        assert model.nr_states == 613
        assert model.nr_transitions == 803
        assert model.model_type == stormpy.models.ModelType.DTMC
        assert model.has_parameters
        env = stormpy.environments.default(model)
        checker = stormpy.pars.create_region_checker(model, formula, environment=env)
        parameters = model.collect_all_parameters()
        assert len(parameters) == 2
        region = stormpy.pars.parse_region("0.7<=pL<=0.9,0.75<=pK<=0.95", parameters)
        result = checker.analyze_region(env, region)
        assert result == stormpy.pars.RegionResult.ALL_SAT
        region = stormpy.pars.parse_region("0.4<=pL<=0.65,0.75<=pK<=0.95", parameters)
        result = checker.analyze_region(env, region, stormpy.pars.RegionResultHypothesis.UNKNOWN, True)
        assert result == stormpy.pars.RegionResult.EXISTS_BOTH
        region = stormpy.pars.parse_region("0.1<=pL<=0.73,0.2<=pK<=0.715", parameters)
        result = checker.analyze_region(env, region)
        assert result == stormpy.pars.RegionResult.ALL_VIOLATED

    def test_pla_region_valuation(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        prop = "P<=0.84 [F s=5 ]"
        formula = stormpy.parse_property(prop, program)
        model = stormpy.build_model[stormpy.RationalFunction](program, formula)
        assert model.nr_states == 613
        assert model.nr_transitions == 803
        assert model.model_type == stormpy.models.ModelType.DTMC
        assert model.has_parameters
        env = stormpy.environments.default(model)
        checker = stormpy.pars.create_region_checker(model, formula, environment=env)
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
        region_valuation[pL] = (stormpy.RationalFunctionCoefficient(0.7), stormpy.RationalFunctionCoefficient(0.9))
        region_valuation[pK] = (stormpy.RationalFunctionCoefficient(0.75), stormpy.RationalFunctionCoefficient(0.95))
        region = stormpy.pars.create_region(region_valuation)
        result = checker.analyze_region(env, region)
        assert result == stormpy.pars.RegionResult.ALL_SAT
        region_valuation[pL] = (stormpy.RationalFunctionCoefficient(0.4), stormpy.RationalFunctionCoefficient(0.65))
        region = stormpy.pars.create_region(region_valuation)
        result = checker.analyze_region(env, region, stormpy.pars.RegionResultHypothesis.UNKNOWN, True)
        assert result == stormpy.pars.RegionResult.EXISTS_BOTH
        region_valuation[pK] = (stormpy.RationalFunctionCoefficient(0.2), stormpy.RationalFunctionCoefficient(0.715))
        region_valuation[pL] = (stormpy.RationalFunctionCoefficient(0.1), stormpy.RationalFunctionCoefficient(0.73))
        region = stormpy.pars.create_region(region_valuation)
        result = checker.analyze_region(env, region)
        assert result == stormpy.pars.RegionResult.ALL_VIOLATED

    def test_pla_bounds(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        prop = "P=? [F s=5 ]"
        formula = stormpy.parse_property(prop, program)
        model = stormpy.build_model[stormpy.RationalFunction](program, formula)
        assert model.has_parameters
        env = stormpy.environments.default(model)
        checker = stormpy.pars.create_region_checker(model, formula, environment=env)
        parameters = model.collect_all_parameters()
        assert len(parameters) == 2
        region = stormpy.pars.parse_region("0.7<=pL<=0.9,0.75<=pK<=0.95", parameters)
        result = checker.get_bound_at_init_state(env, region, stormpy.logic.OptimizationDirection.MAXIMIZE)
        assert math.isclose(float(result), 0.8369631383670559, rel_tol=1e-6)
        result_vec = checker.get_bound(env, region, stormpy.logic.OptimizationDirection.MAXIMIZE)
        result = result_vec[model.initial_states[0]]
        assert math.isclose(result, 0.8369631383670559, rel_tol=1e-6)

    def test_pla_manual(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        prop = "P=? [F s=5 ]"
        formula = stormpy.parse_property(prop, program)
        model = stormpy.build_model[stormpy.RationalFunction](program, formula)
        assert model.has_parameters
        env = stormpy.environments.default(model)
        checker = stormpy.pars.developer.SparseDtmcParameterLiftingModelChecker()
        checker.specify(env, model, stormpy.developer.CheckTask[stormpy.RationalFunction](formula.get_raw_formula(), True))
        parameters = model.collect_all_parameters()
        assert len(parameters) == 2
        region = stormpy.pars.parse_region("0.7<=pL<=0.9,0.75<=pK<=0.95", parameters)
        result = checker.get_bound_at_init_state(env, region, stormpy.logic.OptimizationDirection.MAXIMIZE)
        assert math.isclose(float(result), 0.8369631383670559, rel_tol=1e-6)

    def test_pla_manual_no_simplification(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        prop = "P=? [F s=5 ]"
        formula = stormpy.parse_property(prop, program)
        model = stormpy.build_model[stormpy.RationalFunction](program, formula)
        assert model.has_parameters
        env = stormpy.environments.default(model)
        checker = stormpy.pars.developer.SparseDtmcParameterLiftingModelChecker()
        checker.specify(env, model, stormpy.developer.CheckTask[stormpy.RationalFunction](formula.get_raw_formula(), True), allow_model_simplifications=False)
        parameters = model.collect_all_parameters()
        assert len(parameters) == 2
        region = stormpy.pars.parse_region("0.7<=pL<=0.9,0.75<=pK<=0.95", parameters)
        result = checker.get_bound_at_init_state(env, region, stormpy.logic.OptimizationDirection.MAXIMIZE)
        assert math.isclose(float(result), 0.836963056082918, rel_tol=1e-6)

    def test_pla_state_bounds(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        prop = "P=? [F s=5 ]"
        formula = stormpy.parse_property(prop, program)
        model = stormpy.build_model[stormpy.RationalFunction](program, formula)
        assert model.has_parameters
        env = stormpy.environments.default(model)
        checker = stormpy.pars.developer.SparseDtmcParameterLiftingModelChecker()
        checker.specify(env, model, stormpy.developer.CheckTask[stormpy.RationalFunction](formula.get_raw_formula(), True), allow_model_simplifications=False)
        parameters = model.collect_all_parameters()
        assert len(parameters) == 2
        region = stormpy.pars.parse_region("0.7<=pL<=0.9,0.75<=pK<=0.95", parameters)
        result_vec = checker.get_bound(env, region, stormpy.logic.OptimizationDirection.MAXIMIZE)
        assert len(result_vec.get_finite_value_vector()) == model.nr_states
        assert math.isclose(result_vec[model.initial_states[0]], 0.836963056082918, rel_tol=1e-6)

    def test_compute_extremum(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        prop = "P=? [F s=5 ]"
        formula = stormpy.parse_property(prop, program)
        model = stormpy.build_model[stormpy.RationalFunction](program, formula)
        assert model.has_parameters
        env = stormpy.environments.default(model)
        parameters = model.collect_all_parameters()
        assert len(parameters) == 2
        region = stormpy.pars.parse_region("0.7<=pL<=0.9,0.75<=pK<=0.95", parameters)

        refinement_checker = stormpy.pars.create_region_refinement_checker(model, formula, environment=env)
        precision = stormpy.RationalFunctionCoefficient(1e-6)
        value, point = refinement_checker.compute_extremal_value(env, region, stormpy.logic.OptimizationDirection.MAXIMIZE, precision, False)
        assert isinstance(value, stormpy.RationalFunctionCoefficient)
        assert isinstance(point, dict)
        assert len(point) == 2
        assert 0.83 <= float(value) <= 0.84

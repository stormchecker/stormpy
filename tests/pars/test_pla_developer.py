"""Lower-level parameter lifting features available only through the developer API."""

import math

import pytest
import stormpy
from helpers.helper import get_example_path

from configurations import pars


@pars
class TestPLADeveloper:
    def test_region_result_hypothesis(self):
        hypothesis = stormpy.pars.developer.RegionResultHypothesis
        assert hypothesis.UNKNOWN.friendly_name() == "Unknown"
        assert hypothesis.ALL_SAT.friendly_name() == "AllSat?"
        assert hypothesis.ALL_SAT.name == "ALL_SAT"

    def test_pla_bounds(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        prop = "P=? [F s=5 ]"
        formula = stormpy.parse_property(prop, program)
        model = stormpy.build_model[stormpy.RationalFunction](program, formula)
        assert model.has_parameters
        env = stormpy.environments.default(model)
        checker = stormpy.pars.developer.initialize_region_model_checker(
            env, model, stormpy.developer.CheckTask[stormpy.RationalFunction](formula.get_raw_formula(), True)
        )
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

        refinement_checker = stormpy.pars.developer.initialize_region_refinement_checker(
            env, model, stormpy.developer.CheckTask[stormpy.RationalFunction](formula.get_raw_formula(), True)
        )
        precision = stormpy.RationalFunction(stormpy.Polynomial(stormpy.RationalFunctionCoefficient("1/1000000")))
        value, point = refinement_checker.compute_extremal_value(env, region, stormpy.logic.OptimizationDirection.MAXIMIZE, precision, bound_invariant=None)
        assert isinstance(value, stormpy.RationalFunctionCoefficient)
        assert isinstance(point, dict)
        assert len(point) == 2
        assert 0.83 <= float(value) <= 0.84

    @pytest.mark.parametrize("respecify", [False, True])
    @pytest.mark.parametrize("discrete", [False, True])
    def test_discrete_variables(self, tmp_path, respecify, discrete):
        path = tmp_path / "discrete.pm"
        path.write_text("""dtmc
const double p;
module simple
 s : [0..3] init 0;
 [] s=0 -> (0.1+0.5*p) : (s'=1) + (0.9-0.5*p) : (s'=3);
 [] s=1 -> (0.9-0.5*p) : (s'=2) + (0.1+0.5*p) : (s'=3);
 [] s=2 -> (s'=2);
 [] s=3 -> (s'=3);
endmodule
label "target" = s=2;
""")
        program = stormpy.parse_prism_program(path)
        prop = stormpy.parse_property('P=? [F "target"]', program)
        model = stormpy.build_model[stormpy.RationalFunction](program, prop)
        env = stormpy.environments.default(model)
        task = stormpy.developer.CheckTask[stormpy.RationalFunction](prop.get_raw_formula(), True)
        parameters = model.collect_all_parameters()
        options = {"discrete_variables": parameters} if discrete else {}
        checker = stormpy.pars.developer.initialize_region_refinement_checker(env, model, task, **({} if respecify else options))
        if respecify:
            checker.specify(env, model, task, **options)
        region = stormpy.pars.parse_region("0<=p<=1", parameters)
        precision = stormpy.RationalFunction(stormpy.Polynomial(stormpy.RationalFunctionCoefficient("1/1000000")))
        value, point = checker.compute_extremal_value(env, region, stormpy.logic.OptimizationDirection.MAXIMIZE, precision, True)
        assert math.isclose(float(value), 0.24 if discrete else 0.25, abs_tol=1e-6)
        assert math.isclose(float(point[next(iter(parameters))]), 1.0 if discrete else 0.8, abs_tol=1e-3)

"""Parameter lifting through the public verification and feasibility API."""

import stormpy
from helpers.helper import get_example_path

from configurations import pars


@pars
class TestPLA:
    def test_to_string(self):
        assert stormpy.pars.RegionResult.EXISTS_VIOLATED.friendly_name() == "ExistsViolated"
        assert stormpy.pars.RegionResult.ALL_SAT.friendly_name() == "AllSat"

    def test_name(self):
        assert stormpy.pars.RegionResult.ALL_SAT.name == "ALL_SAT"

    def test_pla(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        prop = "P<=0.84 [F s=5 ]"
        formula = stormpy.parse_property(prop, program)
        complement = stormpy.parse_property("P>0.84 [F s=5]", program)
        model = stormpy.build_model[stormpy.RationalFunction](program, formula)
        assert model.nr_states == 613
        assert model.nr_transitions == 803
        assert model.model_type == stormpy.models.ModelType.DTMC
        assert model.has_parameters
        env = stormpy.environments.default(model)
        parameters = model.collect_all_parameters()
        assert len(parameters) == 2
        region = stormpy.pars.parse_region("0.7<=pL<=0.9,0.75<=pK<=0.95", parameters)
        assert stormpy.pars.verify(model, formula, region=region, environment=env)
        region = stormpy.pars.parse_region("0.4<=pL<=0.65,0.75<=pK<=0.95", parameters)
        assert not stormpy.pars.verify(model, formula, region=region, environment=env)
        for property in [formula, complement]:
            result = stormpy.pars.check_feasibility(model, property, region=region, method=stormpy.pars.FeasibilityMethod.PLA, environment=env)
            assert result.status == stormpy.pars.RegionResult.EXISTS_SAT
            assert result.witness is not None
        region = stormpy.pars.parse_region("0.1<=pL<=0.73,0.2<=pK<=0.715", parameters)
        assert not stormpy.pars.verify(model, formula, region=region, environment=env)
        result = stormpy.pars.check_feasibility(model, formula, region=region, method=stormpy.pars.FeasibilityMethod.PLA, environment=env)
        assert result.status == stormpy.pars.RegionResult.ALL_VIOLATED
        assert result.witness is None

    def test_pla_region_valuation(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        prop = "P<=0.84 [F s=5 ]"
        formula = stormpy.parse_property(prop, program)
        complement = stormpy.parse_property("P>0.84 [F s=5]", program)
        model = stormpy.build_model[stormpy.RationalFunction](program, formula)
        assert model.nr_states == 613
        assert model.nr_transitions == 803
        assert model.model_type == stormpy.models.ModelType.DTMC
        assert model.has_parameters
        env = stormpy.environments.default(model)
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
        assert stormpy.pars.verify(model, formula, region=region, environment=env)
        region_valuation[pL] = (stormpy.RationalFunctionCoefficient(0.4), stormpy.RationalFunctionCoefficient(0.65))
        region = stormpy.pars.create_region(region_valuation)
        assert not stormpy.pars.verify(model, formula, region=region, environment=env)
        for property in [formula, complement]:
            result = stormpy.pars.check_feasibility(model, property, region=region, method=stormpy.pars.FeasibilityMethod.PLA, environment=env)
            assert result.status == stormpy.pars.RegionResult.EXISTS_SAT
            assert result.witness is not None
        region_valuation[pK] = (stormpy.RationalFunctionCoefficient(0.2), stormpy.RationalFunctionCoefficient(0.715))
        region_valuation[pL] = (stormpy.RationalFunctionCoefficient(0.1), stormpy.RationalFunctionCoefficient(0.73))
        region = stormpy.pars.create_region(region_valuation)
        assert not stormpy.pars.verify(model, formula, region=region, environment=env)
        result = stormpy.pars.check_feasibility(model, formula, region=region, method=stormpy.pars.FeasibilityMethod.PLA, environment=env)
        assert result.status == stormpy.pars.RegionResult.ALL_VIOLATED
        assert result.witness is None

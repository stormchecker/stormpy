"""Integration tests of the public parameter synthesis API."""

import math

import pytest
import stormpy
from configurations import has_pars, pars

if not has_pars:
    pytest.skip("No support for parametric model checking", allow_module_level=True)


def _build_model(tmp_path, *, mdp=False, rewards=False):
    path = tmp_path / "synthesis.pm"
    source = """dtmc
const double p;
module simple
 s : [0..2] init 0;
 [] s=0 -> p : (s'=1) + (1-p) : (s'=2);
 [] s=1 -> (s'=1);
 [] s=2 -> (s'=2);
endmodule
label "target" = s=1;
"""
    if mdp:
        source = source.replace("dtmc", "mdp").replace(" [] s=1", " [] s=0 -> (s'=1);\n [] s=0 -> (s'=2);\n [] s=1")
    if rewards:
        source = source.replace("const double p;", "const double p; const double r;")
        source += 'rewards "cost"\n s=0 : r;\nendrewards\n'
    path.write_text(source)
    program = stormpy.parse_prism_program(path)
    return stormpy.build_model[stormpy.RationalFunction](program)


@pytest.fixture
def synthesis_model(tmp_path):
    """A DTMC whose probability of reaching target is p."""
    return _build_model(tmp_path)


def _property(text):
    return stormpy.parse_property(text)


@pars
class TestSynthesis:
    @pytest.mark.parametrize("direction", list(stormpy.logic.OptimizationDirection))
    @pytest.mark.parametrize("raw_formula", [False, True])
    @pytest.mark.parametrize("engine", [stormpy.pars.RegionCheckEngine.PARAMETER_LIFTING, stormpy.pars.RegionCheckEngine.EXACT_PARAMETER_LIFTING])
    def test_compute_extremal_value(self, synthesis_model, direction, raw_formula, engine):
        model = synthesis_model
        prop = _property('P=? [F "target"]')
        if raw_formula:
            prop = prop.get_raw_formula()
        region = stormpy.pars.parse_region("0.2<=p<=0.8", model.collect_all_parameters())
        options = {"environment": stormpy.environments.exact(), "absolute_precision": True} if raw_formula else {}
        precision = stormpy.numbers.RationalFunctionCoefficient("1/1000000")
        value, valuation = stormpy.pars.compute_extremal_value(model, prop, region=region, direction=direction, precision=precision, engine=engine, **options)
        expected = 0.8 if direction == stormpy.logic.OptimizationDirection.MAXIMIZE else 0.2
        assert math.isclose(float(value), expected, abs_tol=float(precision))
        assert set(valuation) == model.collect_all_parameters()
        instantiated = stormpy.pars.ModelInstantiator[stormpy.models.ModelType.DTMC, stormpy.Rational](model).instantiate(valuation)
        checked = stormpy.model_checking(instantiated, prop, only_initial_states=True)
        assert math.isclose(float(checked[instantiated.initial_states[0]].value), float(value), abs_tol=float(precision))

    @pytest.mark.parametrize("discrete", [False, True])
    @pytest.mark.parametrize("engine", [stormpy.pars.RegionCheckEngine.PARAMETER_LIFTING, stormpy.pars.RegionCheckEngine.EXACT_PARAMETER_LIFTING])
    def test_discrete_variables(self, tmp_path, discrete, engine):
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
        parameters = model.collect_all_parameters()
        region = stormpy.pars.parse_region("0<=p<=1", parameters)
        options = {"discrete_variables": iter(parameters)} if discrete else {}
        value, valuation = stormpy.pars.compute_extremal_value(
            model,
            prop,
            region=region,
            direction=stormpy.logic.OptimizationDirection.MAXIMIZE,
            precision=1e-6,
            absolute_precision=True,
            engine=engine,
            **options,
        )
        assert math.isclose(float(value), 0.24 if discrete else 0.25, abs_tol=1e-6)
        assert math.isclose(float(valuation[next(iter(parameters))]), 1.0 if discrete else 0.8, abs_tol=1e-3)

    @pytest.mark.parametrize("precision, coefficient", [(1e-6, "1/1000000"), (0.1, "1/10"), (1, "1")])
    def test_numeric_precision(self, synthesis_model, precision, coefficient):
        model = synthesis_model
        prop = _property('P=? [F "target"]')
        region = stormpy.pars.parse_region("0.2<=p<=0.8", model.collect_all_parameters())
        options = {"direction": stormpy.logic.OptimizationDirection.MAXIMIZE, "absolute_precision": True}
        result = stormpy.pars.compute_extremal_value(model, prop, region=region, precision=precision, **options)
        expected = stormpy.pars.compute_extremal_value(
            model, prop, region=region, precision=stormpy.numbers.RationalFunctionCoefficient(coefficient), **options
        )
        assert result == expected

    @pytest.mark.parametrize("precision", [math.nan, math.inf, -math.inf])
    def test_nonfinite_precision(self, synthesis_model, precision):
        model = synthesis_model
        prop = _property('P=? [F "target"]')
        region = stormpy.pars.parse_region("0.2<=p<=0.8", model.collect_all_parameters())
        with pytest.raises(ValueError, match="precision must be finite"):
            stormpy.pars.compute_extremal_value(model, prop, region=region, direction=stormpy.logic.OptimizationDirection.MAXIMIZE, precision=precision)

    def test_float_region_bound(self, synthesis_model):
        model = synthesis_model
        assert stormpy.pars.verify(model, _property('P>=0.1 [F "target"]'), region_bound=0.2)
        prop = _property('P<=0.3 [F "target"]')
        result = stormpy.pars.check_feasibility(model, prop, region_bound=0.2)
        expected = stormpy.pars.check_feasibility(model, prop, region_bound=stormpy.numbers.RationalFunctionCoefficient("1/5"))
        assert result.status == stormpy.pars.RegionResult.EXISTS_SAT
        assert result.witness.valuation == expected.witness.valuation
        assert result.witness.value == expected.witness.value

    def test_mdp_scheduler_quantification(self, tmp_path):
        model = _build_model(tmp_path, mdp=True)
        region = stormpy.pars.parse_region("0.2<=p<=0.8", model.collect_all_parameters())
        universal = _property('P>=0.6 [F "target"]')
        existential = _property('Pmax>=0.6 [F "target"]')
        assert not stormpy.pars.verify(model, universal, region=region)
        assert stormpy.pars.verify(model, existential, region=region)
        assert stormpy.pars.check_feasibility(model, universal, region=region).status == stormpy.pars.RegionResult.ALL_VIOLATED
        assert stormpy.pars.check_feasibility(model, existential, region=region).status == stormpy.pars.RegionResult.EXISTS_SAT
        with pytest.raises(RuntimeError, match="universal scheduler"):
            stormpy.pars.check_feasibility(model, existential, region=region, method=stormpy.pars.FeasibilityMethod.SCP)

    def test_reward_property(self, tmp_path):
        model = _build_model(tmp_path, rewards=True)
        region = stormpy.pars.parse_region("0.5<=p<=0.5,2<=r<=4", model.collect_all_parameters())
        assert stormpy.pars.verify(model, _property('R{"cost"}<=4 [F !"init"]'), region=region)
        result = stormpy.pars.check_feasibility(model, _property('R{"cost"}>=3 [F !"init"]'), region=region)
        assert result.status == stormpy.pars.RegionResult.EXISTS_SAT
        assert result.witness.value >= 3.0
        assert set(result.witness.valuation) == model.collect_all_parameters()

    @pytest.mark.parametrize("engine", list(stormpy.pars.RegionCheckEngine))
    @pytest.mark.parametrize("raw_formula", [False, True])
    def test_verify(self, synthesis_model, engine, raw_formula):
        model = synthesis_model
        prop = _property('P<=0.9 [F "target"]')
        if raw_formula:
            prop = prop.get_raw_formula()
        region = stormpy.pars.parse_region("0.2<=p<=0.8", model.collect_all_parameters())
        assert stormpy.pars.verify(model, prop, region=region, region_engine=engine)
        assert stormpy.pars.verify(model, prop, region_bound=stormpy.numbers.RationalFunctionCoefficient("1/5"), region_engine=engine)
        assert not stormpy.pars.verify(model, _property('P>=0.6 [F "target"]'), region=region, region_engine=engine, environment=stormpy.Environment())

    @pytest.mark.parametrize(
        "method, engine",
        [pytest.param(stormpy.pars.FeasibilityMethod.PLA, engine, id=f"PLA-{engine.name}") for engine in stormpy.pars.RegionCheckEngine]
        + [
            pytest.param(method, stormpy.pars.RegionCheckEngine.PARAMETER_LIFTING, id=method.name)
            for method in [stormpy.pars.FeasibilityMethod.GD, stormpy.pars.FeasibilityMethod.SCP]
        ],
    )
    def test_feasibility(self, synthesis_model, method, engine):
        model = synthesis_model
        parameters = model.collect_all_parameters()
        region = stormpy.pars.create_region(
            {p: (stormpy.numbers.RationalFunctionCoefficient("1/5"), stormpy.numbers.RationalFunctionCoefficient("4/5")) for p in parameters}
        )
        result = stormpy.pars.check_feasibility(model, _property('P>=0.6 [F "target"]'), region=region, method=method, region_engine=engine)
        assert isinstance(result, stormpy.pars.FeasibilitySynthesisResult)
        assert result.status == stormpy.pars.RegionResult.EXISTS_SAT
        assert isinstance(result.witness, stormpy.pars.FeasibilityResult)
        assert set(result.witness.valuation) == parameters
        assert 0.6 <= result.witness.value <= 0.8
        assert math.isclose(float(next(iter(result.witness.valuation.values()))), result.witness.value, rel_tol=1e-6)
        # The witness remains usable after its containing result is released.
        witness = result.witness
        del result
        assert witness.value >= 0.6
        result = stormpy.pars.check_feasibility(
            model,
            _property('P>=0.6 [F "target"]').get_raw_formula(),
            region_bound=0.2,
            method=method,
            region_engine=engine,
            environment=stormpy.Environment(),
        )
        assert result.status == stormpy.pars.RegionResult.EXISTS_SAT
        assert result.witness is not None
        assert 0.6 <= result.witness.value <= 0.8

        # GD keeps restarting on infeasible regions, so only PLA and SCP are checked here.
        if method != stormpy.pars.FeasibilityMethod.GD:
            result = stormpy.pars.check_feasibility(model, _property('P>=0.9 [F "target"]'), region_bound=0.2, method=method, region_engine=engine)
            expected_status = stormpy.pars.RegionResult.ALL_VIOLATED if method == stormpy.pars.FeasibilityMethod.PLA else stormpy.pars.RegionResult.UNKNOWN
            assert result.status == expected_status
            assert result.witness is None

    @pytest.mark.parametrize("method", [stormpy.pars.FeasibilityMethod.PLA, stormpy.pars.FeasibilityMethod.GD])
    @pytest.mark.parametrize("satisfiable", [False, True])
    def test_singleton(self, synthesis_model, method, satisfiable):
        prop = _property('P>=0.5 [F "target"]' if satisfiable else 'P>0.5 [F "target"]')
        result = stormpy.pars.check_feasibility(synthesis_model, prop, region_bound=stormpy.numbers.RationalFunctionCoefficient("1/2"), method=method)
        assert result.status == (stormpy.pars.RegionResult.EXISTS_SAT if satisfiable else stormpy.pars.RegionResult.ALL_VIOLATED)
        if satisfiable:
            assert result.witness.value == 0.5
        else:
            assert result.witness is None

    @pytest.mark.parametrize("function", [stormpy.pars.verify, stormpy.pars.check_feasibility])
    def test_region_arguments(self, synthesis_model, function):
        prop = _property('P<=1 [F "target"]')
        with pytest.raises(ValueError, match="exactly one"):
            function(synthesis_model, prop)
        region = stormpy.pars.parse_region("0.2<=p<=0.8", synthesis_model.collect_all_parameters())
        with pytest.raises(TypeError, match="positional"):
            function(synthesis_model, prop, region)
        with pytest.raises(ValueError, match="exactly one"):
            function(synthesis_model, prop, region=region, region_bound=stormpy.numbers.RationalFunctionCoefficient("1/5"))
        for invalid in ["-1", "1"]:
            with pytest.raises(RuntimeError, match="region bound"):
                function(synthesis_model, prop, region_bound=stormpy.numbers.RationalFunctionCoefficient(invalid))
        for invalid in [math.nan, math.inf, -math.inf]:
            with pytest.raises(ValueError, match="finite"):
                function(synthesis_model, prop, region_bound=invalid)
        with pytest.raises(RuntimeError, match="bounded"):
            function(synthesis_model, _property('P=? [F "target"]'), region=region)
        with pytest.raises(RuntimeError, match="cover"):
            function(synthesis_model, prop, region=stormpy.pars.create_region({}))

    @pytest.mark.parametrize("function", [stormpy.pars.verify, stormpy.pars.check_feasibility])
    @pytest.mark.parametrize("zero", [0, 0.0, stormpy.numbers.RationalFunctionCoefficient(0)])
    def test_graph_preservation(self, synthesis_model, function, zero):
        prop = _property('P<=1 [F "target"]')
        with pytest.raises(RuntimeError, match="graph-preserving"):
            function(synthesis_model, prop, region_bound=zero)
        result = function(synthesis_model, prop, region_bound=zero, region_engine=stormpy.pars.RegionCheckEngine.ROBUST_PARAMETER_LIFTING)
        if function is stormpy.pars.verify:
            assert result
        else:
            assert result.status == stormpy.pars.RegionResult.EXISTS_SAT

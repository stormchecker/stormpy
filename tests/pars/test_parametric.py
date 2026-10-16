import stormpy
import stormpy.info
from helpers.helper import get_example_path

from configurations import pars


@pars
class TestParametric:
    def test_parametric_model_checking_sparse(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        prop = "P=? [F s=5]"
        formula = stormpy.parse_property(prop, program)
        model = stormpy.build_model[stormpy.RationalFunction](program, formula)
        assert model.nr_states == 613
        assert model.nr_transitions == 803
        assert model.model_type == stormpy.models.ModelType.DTMC
        assert model.has_parameters
        initial_state = model.initial_states[0]
        assert initial_state == 0
        result = stormpy.model_checking(model, formula)
        func = result[initial_state]
        one = stormpy.Polynomial(stormpy.RationalFunctionCoefficient(1))
        assert func.denominator == one

    def test_parametric_model_checking_sparse_die(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "parametric_die.pm"))
        prop = "P=? [F s=7 & d=2]"
        formula = stormpy.parse_property(prop, program)
        model = stormpy.build_model[stormpy.RationalFunction](program, formula)
        assert model.nr_states == 13
        assert model.nr_transitions == 20
        assert model.model_type == stormpy.models.ModelType.DTMC
        assert model.has_parameters
        initial_state = model.initial_states[0]
        assert initial_state == 0
        result = stormpy.model_checking(model, formula)
        func = result[initial_state]

        # Create rational function for comparison
        if stormpy.info.storm_ratfunc_use_cln():
            from stormpy.numbers.developer import cln as pc
        else:
            from stormpy.numbers.developer import gmp as pc
        parameters = model.collect_all_parameters()
        for par in parameters:
            if par.name == "p":
                p = pc.create_factorized_polynomial(stormpy.RawPolynomial(par))
            else:
                assert par.name == "q"
                q = pc.create_factorized_polynomial(stormpy.RawPolynomial(par))

        one = stormpy.Polynomial(stormpy.RationalFunctionCoefficient(1))
        num = p * p * (q - one)
        denom = p * q - one
        assert func.numerator == num
        assert func.denominator == denom

    def test_parametric_model_checking_dd(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "parametric_die.pm"))
        prop = "P=? [F s=5]"
        formula = stormpy.parse_property(prop, program)
        model = stormpy.build_symbolic_model[stormpy.RationalFunction](program, formula)
        assert model.nr_states == 11
        assert model.nr_transitions == 17
        assert model.model_type == stormpy.models.ModelType.DTMC
        assert model.has_parameters
        result = stormpy.model_checking(model, formula, engine=stormpy.Engine.DD)
        assert type(result) is stormpy.SymbolicQuantitativeCheckResult[stormpy.models.DdType.Sylvan, stormpy.RationalFunction]

    def test_parametric_model_checking_hybrid(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "parametric_die.pm"))
        prop = "P=? [F s=5]"
        formula = stormpy.parse_property(prop, program)
        model = stormpy.build_symbolic_model[stormpy.RationalFunction](program, formula)
        assert model.nr_states == 11
        assert model.nr_transitions == 17
        assert model.model_type == stormpy.models.ModelType.DTMC
        assert model.has_parameters
        result = stormpy.model_checking(model, formula, engine=stormpy.Engine.HYBRID)
        assert type(result) is stormpy.HybridQuantitativeCheckResult[stormpy.models.DdType.Sylvan, stormpy.RationalFunction]
        values = result.get_explicit_value_vector()
        assert len(values) == 3

    def test_parameters_dtmc(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        formula = stormpy.parse_property("P=? [F s=5]", program)
        model = stormpy.build_model[stormpy.RationalFunction](program, formula)
        model_parameters = model.collect_probability_parameters()
        reward_parameters = model.collect_reward_parameters()
        rate_parameters = model.collect_rate_parameters()
        all_parameters = model.collect_all_parameters()
        assert len(model_parameters) == 2
        assert len(reward_parameters) == 0
        assert len(rate_parameters) == 0
        assert len(all_parameters) == 2

        model = stormpy.build_symbolic_model[stormpy.RationalFunction](program, formula)
        assert len(model.get_parameters()) == 4

        program_reward = stormpy.parse_prism_program(get_example_path("pdtmc", "brp_rewards16_2.pm"))
        formula_reward = stormpy.parse_property('Rmin=? [ F "target" ]', program_reward)
        model = stormpy.build_model[stormpy.RationalFunction](program_reward, formula_reward)
        model_parameters = model.collect_probability_parameters()
        reward_parameters = model.collect_reward_parameters()
        rate_parameters = model.collect_rate_parameters()
        all_parameters = model.collect_all_parameters()
        assert len(model_parameters) == 2
        assert len(reward_parameters) == 2
        assert len(rate_parameters) == 0
        assert len(all_parameters) == 4

        model = stormpy.build_symbolic_model[stormpy.RationalFunction](program_reward, formula_reward)
        assert len(model.get_parameters()) == 4

    def test_parameters_ctmc(self):
        program = stormpy.parse_prism_program(get_example_path("pctmc", "polling3.sm"), prism_compatibility=True)
        model = stormpy.build_model[stormpy.RationalFunction](program)
        model_parameters = model.collect_probability_parameters()
        reward_parameters = model.collect_reward_parameters()
        rate_parameters = model.collect_rate_parameters()
        all_parameters = model.collect_all_parameters()
        assert len(model_parameters) == 2
        assert len(reward_parameters) == 0
        assert len(rate_parameters) == 2
        assert len(all_parameters) == 2

        model = stormpy.build_symbolic_model[stormpy.RationalFunction](program)
        assert len(model.get_parameters()) == 2

    def test_constraints_collector(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        prop = "P=? [F s=5]"
        formula = stormpy.parse_property(prop, program)
        model = stormpy.build_model[stormpy.RationalFunction](program, formula)
        collector = stormpy.ConstraintCollector(model)
        constraints_well_formed = collector.get_wellformed_constraints()
        assert len(constraints_well_formed) == 4
        for constraint in constraints_well_formed:
            assert constraint.operator == stormpy.expressions.OperatorType.LESS_OR_EQUAL
        constraints_graph_preserving = collector.get_graph_preserving_constraints()
        assert len(constraints_graph_preserving) == 4
        for constraint in constraints_graph_preserving:
            assert constraint.operator == stormpy.expressions.OperatorType.NOT_EQUAL

    def test_derivatives(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        prop = "P<=0.84 [F s=5 ]"
        formula = stormpy.parse_property(prop, program)
        model = stormpy.build_model[stormpy.RationalFunction](program, formula)
        assert model.nr_states == 613
        assert model.nr_transitions == 803
        assert model.model_type == stormpy.models.ModelType.DTMC
        assert model.has_parameters
        parameters = model.collect_all_parameters()
        assert len(parameters) == 2
        derivatives = stormpy.pars.gather_derivatives(model, list(parameters)[0])
        assert len(derivatives) == 0

    def test_dtmc_simplification(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        prop = "P<=0.84 [F s=5 ]"
        parsed_property = stormpy.parse_property(prop, program)
        formula = parsed_property.get_raw_formula()
        model = stormpy.build_model[stormpy.RationalFunction](program, parsed_property)
        assert model.nr_states == 613
        assert model.nr_transitions == 803
        model, formula = stormpy.pars.simplify_model(model, formula)
        assert model.nr_states == 193
        assert model.nr_transitions == 383

    def test_mdp_simplification(self):
        program = stormpy.parse_prism_program(get_example_path("pmdp", "two_dice.nm"))
        prop = stormpy.parse_property('Pmin=? [ F "two" ]', program)
        formula = prop.get_raw_formula()
        model = stormpy.build_model[stormpy.RationalFunction](program, prop)
        assert model.nr_states == 169
        assert model.nr_transitions == 435
        model, formula = stormpy.pars.simplify_model(model, formula)
        assert model.nr_states == 17
        assert model.nr_transitions == 50

    def test_simplification_with_property(self):
        program = stormpy.parse_prism_program(get_example_path("pmdp", "two_dice.nm"))
        prop = stormpy.parse_property('Pmin=? [ F "two" ]', program)
        model = stormpy.build_model[stormpy.RationalFunction](program, prop)
        simplified, formula = stormpy.pars.simplify_model(model, prop)
        assert simplified.nr_states == 17
        assert formula.is_probability_operator_formula

    def test_region(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        prop = "P<=0.84 [F s=5 ]"
        formula = stormpy.parse_property(prop, program)
        model = stormpy.build_model[stormpy.RationalFunction](program, formula)
        parameters = model.collect_all_parameters()
        assert len(parameters) == 2
        region = stormpy.pars.ParameterRegion.create_from_string("0.7<=pL<=0.9,0.75<=pK<=0.95", parameters)
        assert region.area == stormpy.RationalFunctionCoefficient(1) / stormpy.RationalFunctionCoefficient(25)
        for par in parameters:
            if par.name == "pL":
                pL = par
            elif par.name == "pK":
                pK = par
            else:
                assert False
        dec = stormpy.RationalFunctionCoefficient(100)
        region_valuation = {
            pL: (stormpy.RationalFunctionCoefficient(70) / dec, stormpy.RationalFunctionCoefficient(90) / dec),
            pK: (stormpy.RationalFunctionCoefficient(75) / dec, stormpy.RationalFunctionCoefficient(95) / dec),
        }
        region = stormpy.pars.ParameterRegion(region_valuation)
        assert region.area == stormpy.RationalFunctionCoefficient(1) / stormpy.RationalFunctionCoefficient(25)

import stormpy
import stormpy.info
from helpers.helper import get_example_path

from configurations import pars


@pars
class TestParametric:
    def test_parametric_model_checking_sparse(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        prop = "P=? [F s=5]"
        formulas = stormpy.parse_properties_for_prism_program(prop, program)
        model = stormpy.build_parametric_model(program, formulas)
        assert model.nr_states == 613
        assert model.nr_transitions == 803
        assert model.model_type == stormpy.ModelType.DTMC
        assert model.has_parameters
        initial_state = model.initial_states[0]
        assert initial_state == 0
        result = stormpy.model_checking(model, formulas[0])
        func = result.at(initial_state)
        one = stormpy.FactorizedPolynomial(stormpy.RationalRF(1))
        assert func.denominator == one

    def test_parametric_model_checking_dd(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "parametric_die.pm"))
        prop = "P=? [F s=5]"
        formulas = stormpy.parse_properties_for_prism_program(prop, program)
        model = stormpy.build_symbolic_parametric_model(program, formulas)
        assert model.nr_states == 11
        assert model.nr_transitions == 17
        assert model.model_type == stormpy.ModelType.DTMC
        assert model.has_parameters
        result = stormpy.check_model_dd(model, formulas[0])
        assert type(result) is stormpy.SymbolicParametricQuantitativeCheckResult

    def test_parametric_model_checking_hybrid(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "parametric_die.pm"))
        prop = "P=? [F s=5]"
        formulas = stormpy.parse_properties_for_prism_program(prop, program)
        model = stormpy.build_symbolic_parametric_model(program, formulas)
        assert model.nr_states == 11
        assert model.nr_transitions == 17
        assert model.model_type == stormpy.ModelType.DTMC
        assert model.has_parameters
        result = stormpy.check_model_hybrid(model, formulas[0])
        assert type(result) is stormpy.HybridParametricQuantitativeCheckResult
        values = result.get_values()
        assert len(values) == 3

    def test_parameters(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        formulas = stormpy.parse_properties_for_prism_program("P=? [F s=5]", program)
        model = stormpy.build_parametric_model(program, formulas)
        model_parameters = model.collect_probability_parameters()
        reward_parameters = model.collect_reward_parameters()
        all_parameters = model.collect_all_parameters()
        assert len(model_parameters) == 2
        assert len(reward_parameters) == 0
        assert len(all_parameters) == 2

        program_reward = stormpy.parse_prism_program(get_example_path("pdtmc", "brp_rewards16_2.pm"))
        formulas_reward = stormpy.parse_properties_for_prism_program('Rmin=? [ F "target" ]', program_reward)
        model = stormpy.build_parametric_model(program_reward, formulas_reward)
        model_parameters = model.collect_probability_parameters()
        reward_parameters = model.collect_reward_parameters()
        all_parameters = model.collect_all_parameters()
        assert len(model_parameters) == 2
        assert len(reward_parameters) == 2
        assert len(all_parameters) == 4

        model = stormpy.build_symbolic_parametric_model(program, formulas)
        assert len(model.get_parameters()) == 4

        model = stormpy.build_symbolic_parametric_model(program_reward, formulas_reward)
        assert len(model.get_parameters()) == 4

    def test_constraints_collector(self):
        from stormpy.pycarl.formula import FormulaType, Relation

        if stormpy.info.storm_ratfunc_use_cln():
            from stormpy.pycarl.cln import formula
        else:
            from stormpy.pycarl.gmp import formula
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        prop = "P=? [F s=5]"
        formulas = stormpy.parse_properties_for_prism_program(prop, program)
        model = stormpy.build_parametric_model(program, formulas)
        collector = stormpy.ConstraintCollector(model)
        constraints_well_formed = collector.wellformed_constraints
        for formula in constraints_well_formed:
            assert formula.type == FormulaType.CONSTRAINT
            constraint = formula.get_constraint()
            assert constraint.relation == Relation.LEQ
        constraints_graph_preserving = collector.graph_preserving_constraints
        for formula in constraints_graph_preserving:
            assert formula.type == FormulaType.CONSTRAINT
            constraint = formula.get_constraint()
            assert constraint.relation == Relation.NEQ

    def test_derivatives(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        prop = "P<=0.84 [F s=5 ]"
        formulas = stormpy.parse_properties_for_prism_program(prop, program)
        model = stormpy.build_parametric_model(program, formulas)
        assert model.nr_states == 613
        assert model.nr_transitions == 803
        assert model.model_type == stormpy.ModelType.DTMC
        assert model.has_parameters
        parameters = model.collect_probability_parameters()
        assert len(parameters) == 2
        derivatives = stormpy.pars.gather_derivatives(model, list(parameters)[0])
        assert len(derivatives) == 0

    def test_dtmc_simplification(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        prop = "P<=0.84 [F s=5 ]"
        formulas = stormpy.parse_properties_for_prism_program(prop, program)
        formula = formulas[0].raw_formula
        model = stormpy.build_parametric_model(program, formulas)
        assert model.nr_states == 613
        assert model.nr_transitions == 803
        model, formula = stormpy.pars.simplify_model(model, formula)
        assert model.nr_states == 193
        assert model.nr_transitions == 383

    def test_mdp_simplification(self):
        program = stormpy.parse_prism_program(get_example_path("pmdp", "two_dice.nm"))
        formulas = stormpy.parse_properties_for_prism_program('Pmin=? [ F "two" ]', program)
        formula = formulas[0].raw_formula
        model = stormpy.build_parametric_model(program, formulas)
        assert model.nr_states == 169
        assert model.nr_transitions == 435
        model, formula = stormpy.pars.simplify_model(model, formula)
        assert model.nr_states == 17
        assert model.nr_transitions == 50

    def test_region(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "brp16_2.pm"))
        prop = "P<=0.84 [F s=5 ]"
        formulas = stormpy.parse_properties_for_prism_program(prop, program)
        model = stormpy.build_parametric_model(program, formulas)
        parameters = model.collect_probability_parameters()
        assert len(parameters) == 2
        region = stormpy.pars.ParameterRegion.create_from_string("0.7<=pL<=0.9,0.75<=pK<=0.95", parameters)
        assert region.area == stormpy.RationalRF(1) / stormpy.RationalRF(25)
        for par in parameters:
            if par.name == "pL":
                pL = par
            elif par.name == "pK":
                pK = par
            else:
                assert False
        dec = stormpy.RationalRF(100)
        region_valuation = {pL: (stormpy.RationalRF(70) / dec, stormpy.RationalRF(90) / dec), pK: (stormpy.RationalRF(75) / dec, stormpy.RationalRF(95) / dec)}
        region = stormpy.pars.ParameterRegion(region_valuation)
        assert region.area == stormpy.RationalRF(1) / stormpy.RationalRF(25)

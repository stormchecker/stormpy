import math
import pathlib
import pytest
import stormpy
import stormpy.examples
import stormpy.examples.files
from stormpy.exceptions import StormError

from helpers.helper import get_example_path
from configurations import pars


class TestBuilding:
    def test_explicit_builder(self):
        path = stormpy.examples.files.prism_dtmc_die
        prism_program = stormpy.parse_prism_program(path)
        formula_str = "P=? [F s=7 & d=2]"
        prop = stormpy.parse_property(formula_str, prism_program)

        # Fix variables in the program.
        module = prism_program.modules[0]
        s_var = module.get_integer_variable("s").expression_variable
        d_var = module.get_integer_variable("d").expression_variable

        # Construct the model
        options = stormpy.BuilderOptions(prop)
        options.set_build_state_valuations()
        model_builder = stormpy.developer.make_explicit_model_builder(prism_program, options)
        model = model_builder.build()
        # and export the model from building
        state_mapping = model_builder.export_explicit_state_lookup()

        # lookup 1
        state = {s_var: prism_program.expression_manager.integer(3), d_var: prism_program.expression_manager.integer(0)}
        id = state_mapping.lookup(state)
        assert model.state_valuations.get_value(id, s_var) == 3
        assert model.state_valuations.get_value(id, d_var) == 0

        # lookup 2
        state = {s_var: prism_program.expression_manager.integer(7), d_var: prism_program.expression_manager.integer(3)}
        id = state_mapping.lookup(state)
        assert model.state_valuations.get_value(id, s_var) == 7
        assert model.state_valuations.get_value(id, d_var) == 3

    @pytest.mark.parametrize(
        "value_type", [float, stormpy.Rational, pytest.param(stormpy.RationalFunction, marks=pars), stormpy.Interval, stormpy.RationalInterval]
    )
    def test_build_model_value_types(self, value_type):
        program = stormpy.parse_prism_program(
            get_example_path("idtmc", "die-intervals.pm") if value_type in (stormpy.Interval, stormpy.RationalInterval) else get_example_path("dtmc", "die.pm")
        )
        model = stormpy.build_model[value_type](program)
        assert type(model) is stormpy.models.SparseDtmc[value_type]
        assert model.nr_states == 13

    def test_build_model_unsupported_value_type(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        with pytest.raises(TypeError, match="Supported are: float, "):
            stormpy.build_model[int](program)

    def test_build_model_all_labels(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        model = stormpy.build_model(program)
        assert "one" in model.labeling.get_labels()
        assert "coin_flips" in model.reward_models
        prop = stormpy.parse_property('P=? [F "one"]', program)
        model = stormpy.build_model(program, prop)
        assert "one" in model.labeling.get_labels()
        assert "two" not in model.labeling.get_labels()
        assert len(model.reward_models) == 0

    def test_build_model_with_options(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        options = stormpy.BuilderOptions(build_full=True)
        model = stormpy.build_model(program, options=options)
        assert model.has_state_valuations()
        assert model.has_choice_labeling()
        assert model.has_choice_origins()
        # Without options, no additional information is built
        model = stormpy.build_model(program)
        assert not model.has_state_valuations()
        prop = stormpy.parse_property('P=? [F "one"]', program)
        with pytest.raises(StormError):
            stormpy.build_model(program, prop, options=options)

    @pytest.mark.parametrize("engine", [stormpy.Engine.SPARSE, stormpy.Engine.DD, stormpy.Engine.HYBRID])
    def test_build_model_engine(self, engine):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        prop = stormpy.parse_property('P=? [F "one"]', program)
        model = stormpy.build_model(program, prop, engine=engine)
        if engine == stormpy.Engine.SPARSE:
            assert type(model) is stormpy.models.SparseDtmc[float]
        else:
            assert type(model) is stormpy.models.SymbolicDtmc[stormpy.models.DdType.Sylvan, float]
        assert model.nr_states == 13
        result = stormpy.model_checking(model, prop, engine=engine)
        stormpy.filter_initial_states(result, model)
        assert math.isclose(result.get_min(), 1 / 6, rel_tol=1e-6)

    def test_build_model_engine_value_types(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        model = stormpy.build_model[stormpy.Rational](program, engine=stormpy.Engine.DD)
        assert type(model) is stormpy.models.SymbolicDtmc[stormpy.models.DdType.Sylvan, stormpy.Rational]
        # Interval value types are not supported by symbolic models
        with pytest.raises(TypeError, match="Supported are"):
            stormpy.build_model[stormpy.Interval](program, engine=stormpy.Engine.DD)

    def test_build_model_engine_errors(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        with pytest.raises(StormError, match="Builder options"):
            stormpy.build_model(program, options=stormpy.BuilderOptions(), engine=stormpy.Engine.DD)
        with pytest.raises(StormError, match="environment"):
            stormpy.build_model(program, environment=stormpy.environments.sound())

    def test_builder_options_defaults(self):
        options = stormpy.BuilderOptions()
        assert not options.is_build_all_labels_set()
        assert not options.is_build_all_reward_models_set()

    def test_builder_options_from_properties(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        properties = stormpy.parse_properties('P=? [F "one"]', program)
        options = stormpy.BuilderOptions(properties)
        raw_options = stormpy.developer.BuilderOptions([p.get_raw_formula() for p in properties])
        assert isinstance(options, stormpy.developer.BuilderOptions)
        assert options.get_label_names() == raw_options.get_label_names() == {"one"}
        assert stormpy.BuilderOptions(properties=properties).get_label_names() == {"one"}
        options_full = stormpy.BuilderOptions(properties, build_full=True)
        assert options_full.is_build_all_labels_set() and options_full.is_build_all_reward_models_set()
        assert options_full.is_build_state_valuations_set() and options_full.is_build_choice_labels_set() and options_full.is_build_choice_origins_set()
        assert options_full.get_label_names() == {"one"}
        assert stormpy.BuilderOptions(properties, stormpy.io.SymbolicModelDescription(program)).get_label_names() == {"one"}
        # Options are accepted by the developer bindings
        model = stormpy.developer.build_sparse_model(program, options)
        assert model.labeling.get_labels() == {"init", "deadlock", "one"}

    def test_builder_options_without_properties(self):
        options = stormpy.BuilderOptions(build_full=True)
        assert options.is_build_all_labels_set() and options.is_build_all_reward_models_set()
        assert options.is_build_state_valuations_set() and options.is_build_choice_labels_set() and options.is_build_choice_origins_set()
        options = stormpy.BuilderOptions()
        assert not options.is_build_all_reward_models_set() and not options.is_build_all_labels_set()
        assert not options.is_build_state_valuations_set() and not options.is_build_choice_labels_set() and not options.is_build_choice_origins_set()
        # Flags are keyword-only
        with pytest.raises(TypeError, match="keyword-only"):
            stormpy.BuilderOptions(True)
        # The separate flags are only available in the developer bindings
        with pytest.raises(TypeError):
            stormpy.BuilderOptions(build_all_labels=True)

    def test_build_model_undefined_constants(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "brp.pm"))
        with pytest.raises(StormError):
            stormpy.build_model(program)

    @pars
    def test_build_parametric_model_from_drn(self):
        model = stormpy.build_model_from_drn[stormpy.RationalFunction](get_example_path("pdtmc", "die.drn"))
        assert type(model) is stormpy.models.SparseDtmc[stormpy.RationalFunction]
        assert model.has_parameters

    def test_build_model_from_explicit_with_rewards(self):
        model = stormpy.build_model_from_explicit(get_example_path("dtmc", "die.tra"), get_example_path("dtmc", "die.lab"))
        assert type(model) is stormpy.models.SparseDtmc[float]
        assert model.nr_states == 13

    @pytest.mark.parametrize("value_type", [float, stormpy.Rational, pytest.param(stormpy.RationalFunction, marks=pars)])
    def test_build_symbolic_model_value_types(self, value_type):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        model = stormpy.build_symbolic_model[value_type](program)
        assert type(model) is stormpy.models.SymbolicDtmc[stormpy.models.DdType.Sylvan, value_type]
        assert model.nr_states == 13

    def test_build_symbolic_model_interval(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        with pytest.raises(TypeError, match="Supported are: float, Rational, RationalFunction"):
            stormpy.build_symbolic_model[stormpy.Interval](program)

    def test_direct_encoding_parser_options(self):
        assert not stormpy.build_model_from_drn(stormpy.examples.files.drn_pomdp_maze).has_choice_labeling()
        options = stormpy.io.DirectEncodingParserOptions()
        assert not options.build_choice_labeling
        options.build_choice_labeling = True
        assert stormpy.build_model_from_drn(stormpy.examples.files.drn_pomdp_maze, options=options).has_choice_labeling()

    def test_explicit_model_parser_options(self):
        options = stormpy.io.ExplicitModelParserOptions()
        assert options.fix_deadlocks and not options.build_choice_labels
        options.fix_deadlocks = False
        options.build_choice_labels = True
        assert not options.fix_deadlocks and options.build_choice_labels
        model = stormpy.build_model_from_explicit(get_example_path("dtmc", "die.tra"), get_example_path("dtmc", "die.lab"), options=options)
        assert model.nr_states == 13

    def test_build_symbolic_ma(self):
        program = stormpy.parse_prism_program(get_example_path("ma", "simple.ma"))
        jani_model, _ = program.to_jani([])
        model = stormpy.build_symbolic_model(jani_model)
        assert type(model) is stormpy.models.SymbolicMA[stormpy.models.DdType.Sylvan, float]
        assert model.model_type == stormpy.models.ModelType.MA

    def test_build_from_path(self):
        model = stormpy.build_model_from_drn(pathlib.Path(get_example_path("ctmc", "dft.drn")))
        assert model.nr_states == 16
        model = stormpy.build_model_from_explicit(pathlib.Path(get_example_path("dtmc", "die.tra")), pathlib.Path(get_example_path("dtmc", "die.lab")))
        assert model.nr_states == 13

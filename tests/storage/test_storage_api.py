"""Public storage packages and their shared native developer bindings."""

import importlib
import inspect

import numpy as np
import pytest
import stormpy
from helpers.helper import get_example_path
from stormpy._template import _TemplateClass, _TemplateFunction

PACKAGES = ("models", "datastructures", "expressions", "io")


@pytest.mark.parametrize("package", PACKAGES)
def test_public_exports_are_explicit(package):
    module = importlib.import_module(f"stormpy.{package}")
    exported = {name for name in vars(module) if not name.startswith("_")}
    assert exported == set(module.__all__)


@pytest.mark.parametrize("package", PACKAGES)
def test_public_classes_share_native_types(package):
    module = importlib.import_module(f"stormpy.{package}")
    for name in module.__all__:
        public = getattr(module, name)
        if isinstance(public, _TemplateFunction):
            continue
        if isinstance(public, _TemplateClass):
            internal = getattr(stormpy.developer.storage, name)
            assert public.canonical_name == f"stormpy.{package}.{name}"
            assert internal.canonical_name == f"stormpy.developer.storage.{name}"
            assert public.instantiations == internal.instantiations
        elif inspect.isclass(public):
            assert public is getattr(stormpy.developer.storage, name, None) or public is getattr(stormpy.developer, name)


def test_native_module_location():
    native = stormpy.developer.storage._storage
    assert native.__name__ == "stormpy.developer.storage._storage"
    assert stormpy.datastructures.BitVector.__module__ == native.__name__


def test_storm_method_names_and_keyword_arguments():
    raw = stormpy.developer.storage
    manager = raw.ExpressionManager()
    variable = manager.declare_integer_variable(name="counter")
    assert variable.has_integer_type()
    assert manager.integer(integer=2).is_literal()
    assert raw.BitVector(4, [1, 3]).get_number_of_set_bits() == 2
    builder = raw.SparseMatrixBuilder(rows=1, columns=1)
    builder.add_next_value(row=0, column=0, value=1.0)
    matrix = builder.build(overridden_row_group_count=1)
    selected = raw.BitVector(1, True)
    assert matrix.get_submatrix(use_groups=True, row_constraint=selected, column_constraint=selected).nr_rows == 1


@pytest.mark.parametrize("value_type", [float, stormpy.Rational, stormpy.RationalFunction, stormpy.Interval, stormpy.RationalInterval])
def test_build_matrix_selects_value_type(value_type):
    if value_type is stormpy.RationalFunction:
        values = [stormpy.RationalFunction(stormpy.numbers.Polynomial(stormpy.numbers.RationalFunctionCoefficient(value))) for value in (1, 2)]
    elif value_type is stormpy.RationalInterval:
        values = [stormpy.RationalInterval(stormpy.Rational(value)) for value in (1, 2)]
    else:
        values = [value_type(value) for value in (1, 2)]
    array = np.array([values], dtype=object)
    matrix = stormpy.datastructures.build_sparse_matrix[value_type](array)
    assert type(matrix) is stormpy.datastructures.SparseMatrix[value_type]
    assert matrix.nr_rows == 1
    assert matrix.nr_columns == 2
    assert matrix.nr_entries == 2


def test_public_valuations_convert_boolean_bitvector_to_list():
    manager = stormpy.expressions.ExpressionManager()
    flag = manager.declare_boolean_variable("flag")
    builder = stormpy.models.ValuationDescriptionBuilder(manager)
    builder.add_boolean_variable(flag)
    values = stormpy.models.Valuations(builder.build_class_description(), manager, 3)
    values.write_value(1, flag, True)
    assert list(values.get_boolean_values(flag)) == [1]
    assert values.get_values_states(flag) == [False, True, False]
    assert values.get_value(1, flag) is True


def test_public_and_raw_jani_export_argument_order(tmp_path):
    program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
    model, properties = program.to_jani([])
    public_path = tmp_path / "public.jani"
    raw_path = tmp_path / "raw.jani"
    stormpy.io.export_jani_to_file(public_path, model, properties)
    stormpy.developer.storage.JsonExporter.to_file(model=model, properties=properties, filepath=str(raw_path))
    assert public_path.read_text() == raw_path.read_text()


def test_public_umb_accepts_pathlike_and_allocates_default_options(tmp_path):
    program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
    model = stormpy.build_model(program)
    umb = stormpy.io.sparse_model_to_umb(model)
    path = tmp_path / "model.umb"
    stormpy.io.umb_to_archive(umb, path)
    restored = stormpy.io.import_umb(path)
    assert restored.validate()[0]
    assert stormpy.build_model_from_umb(path).nr_states == model.nr_states


def test_scheduler_conversion_uses_one_template_family():
    program = stormpy.parse_prism_program(get_example_path("mdp", "coin2-2.nm"))
    prop = stormpy.parse_property('Pmin=? [ F "finished" & "all_coins_equal_1"]', program)
    model = stormpy.build_model(program, prop)
    scheduler = stormpy.model_checking(model, prop, extract_scheduler=True).get_scheduler()
    raw = stormpy.developer.storage
    exact = raw.to_value_type[stormpy.Rational](scheduler=scheduler)
    assert type(exact) is stormpy.models.Scheduler[stormpy.Rational]
    assert exact.deterministic
    floating = raw.to_value_type[float](exact)
    assert type(floating) is stormpy.models.Scheduler[float]
    assert type(scheduler.to_value_type(stormpy.RationalInterval)) is stormpy.models.Scheduler[stormpy.RationalInterval]
    with pytest.raises(TypeError):
        raw.to_value_type[float](scheduler.to_value_type(stormpy.Interval))


def test_public_static_expression_constructors():
    manager = stormpy.expressions.ExpressionManager()
    first, second = manager.integer(2), manager.integer(3)
    assert (first == first) is True
    assert (first == second) is False
    assert (first != second) is True
    assert stormpy.expressions.Expression.Eq(first, second).evaluate_as_bool() is False
    assert stormpy.expressions.Expression.Plus(first, second).evaluate_as_int() == 5
    assert stormpy.expressions.Expression.Modulo(second, first).evaluate_as_int() == 1
    true, false = manager.boolean(True), manager.boolean(False)
    assert stormpy.expressions.Expression.Implies(true, false).evaluate_as_bool() is False
    assert stormpy.expressions.Expression.Iff(true, false).evaluate_as_bool() is False
    assert stormpy.expressions.Expression.Conjunction([true, false]).evaluate_as_bool() is False
    assert stormpy.expressions.Expression.Disjunction([true, false]).evaluate_as_bool() is True


def test_raw_prism_to_jani_overloads_and_valuation_defaults():
    raw = stormpy.developer.storage
    program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
    assert isinstance(program.to_jani(), raw.JaniModel)
    assert isinstance(program.to_jani(properties=[], suffix="_properties")[0], raw.JaniModel)
    manager = raw.ExpressionManager()
    builder = raw.ValuationDescriptionBuilder(manager)
    values = raw.Valuations(class_description=builder.build_class_description())
    assert values.get_number_of_entities() == 0

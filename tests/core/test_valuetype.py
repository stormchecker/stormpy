import stormpy
import stormpy.info
from stormpy import pycarl
from helpers.helper import get_example_path

from configurations import pars, pycarl_cln


def exact_package():
    """Pycarl package (gmp/cln) which is the base for storm::RationalNumber and storm::RationalInterval."""
    return pycarl.cln if stormpy.info.storm_exact_use_cln() else pycarl.gmp


def ratfunc_package():
    """Pycarl package (gmp/cln) which is the base for storm::RationalFunction."""
    return pycarl.cln if stormpy.info.storm_ratfunc_use_cln() else pycarl.gmp


def first_matrix_value(model):
    for entry in model.transition_matrix:
        return entry.value()
    raise AssertionError("Model has no transition matrix entries")


class TestValueType:
    """Check that Storm's C++ ValueTypes match stormpy's Python types."""

    def test_double(self):
        value = stormpy._core._valuetype_double()
        assert type(value) is float

    def test_rationalnumber(self):
        value = stormpy._core._valuetype_rationalnumber()
        assert type(value) is stormpy.Rational
        assert type(value) is exact_package().Rational

    def test_gmprationalnumber(self):
        value = stormpy._core._valuetype_gmprationalnumber()
        assert type(value) is pycarl.gmp.Rational

    @pycarl_cln
    def test_clnrationalnumber(self):
        value = stormpy._core._valuetype_clnrationalnumber()
        assert type(value) is pycarl.cln.Rational

    def test_polynomial(self):
        value = stormpy._core._valuetype_polynomial()
        assert type(value) is stormpy.Polynomial
        assert type(value) is ratfunc_package().FactorizedPolynomial
        assert type(value) is not ratfunc_package().Polynomial

    def test_rationalfunction(self):
        value = stormpy._core._valuetype_rationalfunction()
        assert type(value) is stormpy.RationalFunction
        assert type(value) is ratfunc_package().FactorizedRationalFunction
        # Also test RationalFunctionCoefficient
        value_rf = stormpy._core._valuetype_rationalfunctioncoefficient()
        assert type(value_rf) is stormpy.RationalFunctionCoefficient
        assert type(value_rf) is ratfunc_package().Rational

    def test_interval(self):
        value = stormpy._core._valuetype_interval()
        assert type(value) is stormpy.Interval
        assert type(value) is pycarl.Interval
        assert type(value) is not exact_package().Interval

    def test_rationalinterval(self):
        value = stormpy._core._valuetype_rationalinterval()
        assert type(value) is stormpy.RationalInterval
        assert type(value) is exact_package().Interval
        assert type(value) is not pycarl.Interval


class TestValueTypeMatrix:
    """Check the ValueType against values read out of a model's transition matrix."""

    def test_double(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        model = stormpy.build_model(program)
        assert type(first_matrix_value(model)) is float

    def test_rationalnumber(self):
        program = stormpy.parse_prism_program(get_example_path("dtmc", "die.pm"))
        model = stormpy.build_sparse_exact_model(program)
        assert type(first_matrix_value(model)) is stormpy.Rational
        assert type(first_matrix_value(model)) is exact_package().Rational

    @pars
    def test_rationalfunction(self):
        program = stormpy.parse_prism_program(get_example_path("pdtmc", "parametric_die.pm"))
        model = stormpy.build_parametric_model(program)
        assert type(first_matrix_value(model)) is stormpy.RationalFunction
        assert type(first_matrix_value(model).constant_part()) is ratfunc_package().Rational

    def test_interval(self):
        program = stormpy.parse_prism_program(get_example_path("idtmc", "die-intervals.pm"))
        model = stormpy.build_sparse_interval_model(program)
        assert type(first_matrix_value(model)) is pycarl.Interval

    def test_rationalinterval(self):
        program = stormpy.parse_prism_program(get_example_path("idtmc", "die-intervals.pm"))
        model = stormpy.build_sparse_exact_interval_model(program)
        assert type(first_matrix_value(model)) is exact_package().Interval

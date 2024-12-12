#include "common.h"
#include "helpers.h"

#include "formula/formula_type.h"
#include "formula/relation.h"

PYBIND11_MODULE(formula, m) {
    m.attr("__name__") = "stormpy.pycarl.formula";
	m.doc() = "pycarl formula untyped functions";


	// Constraint relies on Rational
	m.import("stormpy.pycarl");

	define_relation(m);
	define_formula_type(m);

}

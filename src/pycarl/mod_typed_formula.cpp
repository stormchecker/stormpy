#include "common.h"
#include "helpers.h"

#include "typed_formula/constraint.h"
#include "typed_formula/formula.h"

PYBIND11_MODULE(formula, m) {
    m.attr("__name__") = "stormpy.pycarl.formula";
	m.doc() = "pycarl formula typed functions";


	// Constraint relies on Rational
	m.import("stormpy.pycarl");
    m.import("stormpy.pycarl.formula");

	define_constraint(m);
	define_simple_constraint(m);
	define_formula(m);

}

#include "src/common.h"
#include "src/helpers.h"
#include "src/pycarl/typed_formula/constraint.h"
#include "src/pycarl/typed_formula/formula.h"

PYBIND11_MODULE(_formula, m) {
    m.attr("__name__") = "stormpy.pycarl.formula";
    m.doc() = "pycarl formula typed functions";

    // Constraint relies on Rational
    m.import("stormpy.pycarl");
    m.import("stormpy.pycarl.formula");

    define_constraint(m);
    define_simple_constraint(m);
    define_formula(m);
}

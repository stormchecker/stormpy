#include "src/common.h"
#include "src/helpers.h"
#include "src/pycarl/formula/formula_type.h"
#include "src/pycarl/formula/relation.h"

PYBIND11_MODULE(_formula, m) {
    m.attr("__name__") = "stormpy.pycarl.formula";
    m.doc() = "pycarl formula untyped functions";

    // Constraint relies on Rational
    m.import("stormpy.pycarl");

    define_relation(m);
    define_formula_type(m);
}

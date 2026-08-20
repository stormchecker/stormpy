#include "src/common.h"
#include "src/helpers.h"
#include "src/pycarl/formula/formula_type.h"
#include "src/pycarl/formula/relation.h"

namespace {

void bindFormula(py::module& m) {
    define_relation(m);
    define_formula_type(m);
}

}  // namespace

PYBIND11_MODULE(_formula, m) {
    m.attr("__name__") = "stormpy.pycarl.formula";
    m.doc() = "pycarl formula untyped functions";

    // Constraint relies on Rational
    m.import("stormpy.pycarl");

    py::bindModule(m, bindFormula);
}

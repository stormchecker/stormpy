#include "src/common.h"
#include "src/helpers.h"
#include "src/pycarl/typed_formula/constraint.h"
#include "src/pycarl/typed_formula/formula.h"

namespace {

void bindTypedFormula(py::module& m) {
    define_constraint(m);
    define_simple_constraint(m);
    define_formula(m);
}

}  // namespace

PYBIND11_MODULE(_formula, m) {
#ifdef PYCARL_USE_CLN
    m.attr("__name__") = "stormpy.pycarl.cln.formula";
#else
    m.attr("__name__") = "stormpy.pycarl.gmp.formula";
#endif
    m.doc() = "pycarl formula typed functions";

    // Constraint relies on Rational
    m.import("stormpy.pycarl");
    m.import("stormpy.pycarl.formula");

    py::bindModule(m, bindTypedFormula);
}

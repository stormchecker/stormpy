#include "src/common.h"
#include "src/pycarl/core/bound_type.h"
#include "src/pycarl/core/monomial.h"
#include "src/pycarl/core/variable.h"
#include "src/pycarl/typed_core/interval.h"

PYBIND11_MODULE(_pycarl_core, m) {
    m.doc() = "pycarl core untyped functions";

    define_variabletype(m);
    define_variable(m);
    define_monomial(m);
    define_boundtype(m);
    define_interval<double>(m);

    py::register_exception<NoPickling>(m, "NoPicklingSupport");
}

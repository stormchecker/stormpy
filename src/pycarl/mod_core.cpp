#include "common.h"

#include "pycarl_core/variable.h"
#include "pycarl_core/monomial.h"
#include "pycarl_core/bound_type.h"
#include "typed_core/interval.h"

PYBIND11_MODULE(pycarl_core, m) {
    m.doc() = "pycarl core untyped functions";

    define_variabletype(m);
    define_variable(m);
    define_monomial(m);
    define_boundtype(m);

    define_interval<double>(m);

    py::register_exception<NoPickling>(m, "NoPicklingSupport");
}

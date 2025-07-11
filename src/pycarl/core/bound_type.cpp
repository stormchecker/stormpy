#include "bound_type.h"

#include "src/pycarl/types.h"
#include "src/pycarl/helpers.h"


void define_boundtype(py::module& m) {
    py::enum_<carl::BoundType>(m, "BoundType")
        .value("STRICT", carl::BoundType::STRICT)
        .value("WEAK", carl::BoundType::WEAK)
        .value("INFTY", carl::BoundType::INFTY)
    ;
}

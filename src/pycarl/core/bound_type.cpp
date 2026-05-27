#include "bound_type.h"

#include "src/helpers.h"
#include "src/pycarl/types.h"

void define_boundtype(py::module& m) {
    py::native_enum<carl::BoundType>(m, "BoundType", "enum.Enum")
        .value("STRICT", carl::BoundType::STRICT)
        .value("WEAK", carl::BoundType::WEAK)
        .value("INFTY", carl::BoundType::INFTY)
        .finalize();
}

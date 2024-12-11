#include "relation.h"
#include "src/pycarl/helpers.h"

#include <carl/core/Relation.h>

void define_relation(py::module& m) {
    py::enum_<carl::Relation>(m, "Relation")
        .value("EQ", carl::Relation::EQ)
        .value("NEQ", carl::Relation::NEQ)
        .value("LESS", carl::Relation::LESS)
        .value("LEQ", carl::Relation::LEQ)
        .value("GREATER", carl::Relation::GREATER)
        .value("GEQ", carl::Relation::GEQ)
        .def("__str__", &streamToString<carl::Relation>, py::prepend() /* use custom method instead of default enum overload */)
    ;
}

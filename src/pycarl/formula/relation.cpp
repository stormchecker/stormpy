#include "relation.h"

#include <carl/core/Relation.h>

#include "src/helpers.h"

void define_relation(py::module& m) {
    py::native_enum<carl::Relation>(m, "Relation", "enum.Enum")
        .value("EQ", carl::Relation::EQ)
        .value("NEQ", carl::Relation::NEQ)
        .value("LESS", carl::Relation::LESS)
        .value("LEQ", carl::Relation::LEQ)
        .value("GREATER", carl::Relation::GREATER)
        .value("GEQ", carl::Relation::GEQ)
        .finalize()
        .def("friendly_name", &streamToString<carl::Relation>);
}

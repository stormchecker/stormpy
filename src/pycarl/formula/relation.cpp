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
        .finalize();
    m.attr("Relation").attr("friendly_name") = py::cpp_function(
        streamToString<carl::Relation>, py::name("friendly_name"), py::is_method(m.attr("Relation")));
}

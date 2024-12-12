
#include "common.h"
#include "types.h"

#include "typed_parse/parser.h"

#include <carl-parser/Parser.h>

/**
 * The actual module definition
 */
PYBIND11_MODULE(parse, m) {
    m.attr("__name__") = "stormpy.pycarl.parse";
    m.doc() = "pycarl parse typed functions";

    py::class_<ParserResultWrapper<Polynomial>>(m, "_ParserResultWrapper")
        .def("get_type", &ParserResultWrapper<Polynomial>::getType)
        .def("as_rational", &ParserResultWrapper<Polynomial>::asRational)
        .def("as_variable", &ParserResultWrapper<Polynomial>::asVariable)
        .def("as_monomial", &ParserResultWrapper<Polynomial>::asMonomial)
        .def("as_term", &ParserResultWrapper<Polynomial>::asTerm)
        .def("as_polynomial", &ParserResultWrapper<Polynomial>::asPolynomial)
        .def("as_rational_function", &ParserResultWrapper<Polynomial>::asRationalFunction)
        .def("as_constraint", &ParserResultWrapper<Polynomial>::asConstraint)
        .def("as_formula", &ParserResultWrapper<Polynomial>::asFormula)
    ;

    m.def("_deserialize", &from_string);
    m.def("_check_parsed_type", &carlparser::check_type<Polynomial>);

}

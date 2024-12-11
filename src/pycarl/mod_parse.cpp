
#include "common.h"


#include <carl-parser/Parser.h>
#include <carl/formula/Formula.h>

/**
 * The actual module definition
 */
PYBIND11_MODULE(parse, m) {
    m.attr("__name__") = "stormpy.pycarl.parse";
    m.doc() = "pycarl parsing functions";

    // Constraint relies on Rational
    m.import("stormpy.pycarl");


    py::enum_<carlparser::ParserReturnType>(m, "_ParserReturnType")
        .value("Rational", carlparser::ParserReturnType::Rational)
        .value("Variable", carlparser::ParserReturnType::Variable)
        .value("Monomial", carlparser::ParserReturnType::Monomial)
        .value("Term", carlparser::ParserReturnType::Term)
        .value("Polynomial", carlparser::ParserReturnType::Polynomial)
        .value("RationalFunction", carlparser::ParserReturnType::RationalFunction)
        .value("Constraint", carlparser::ParserReturnType::Constraint)
        .value("Formula", carlparser::ParserReturnType::Formula)
    ;

}

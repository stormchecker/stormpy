#include "formula_type.h"
#include <carl/formula/Formula.h>

void define_formula_type(py::module& m) {
    // Mostly just the operators are useful for Python, but as other values may be returned,
    // all of them are included
    py::enum_<carl::FormulaType>(m, "FormulaType")
        .value("ITE", carl::FormulaType::ITE)
        .value("EXISTS", carl::FormulaType::EXISTS)
        .value("FORALL", carl::FormulaType::FORALL)
        .value("TRUE", carl::FormulaType::TRUE)
        .value("FALSE", carl::FormulaType::FALSE)
        .value("BOOL", carl::FormulaType::BOOL)
        .value("NOT", carl::FormulaType::NOT)
        .value("IMPLIES", carl::FormulaType::IMPLIES)
        .value("AND", carl::FormulaType::AND)
        .value("OR", carl::FormulaType::OR)
        .value("XOR", carl::FormulaType::XOR)
        .value("IFF", carl::FormulaType::IFF)
        .value("CONSTRAINT", carl::FormulaType::CONSTRAINT)
        .value("BITVECTOR", carl::FormulaType::BITVECTOR)
        .value("UEQ", carl::FormulaType::UEQ)
    ;
}
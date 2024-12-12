/*
 * constraint.cpp
 *
 *  Created on: 16 Apr 2016
 *      Author: harold
 */

#include "constraint.h"

#include "common.h"


//
void define_constraint(py::module& m) {
    py::class_<Constraint>(m, "Constraint")
        .def(py::init<bool>())
        .def(py::init<carl::Variable, carl::Relation, Rational>(), py::arg("var"), py::arg("rel"), py::arg("bound"))
        .def(py::init<Polynomial, carl::Relation>())
        .def("__str__", &streamToString<Constraint>)
        .def("to_smt2", [](Constraint const& c) {
                return c.toString(2, false, true);
            })

        .def("__invert__", [](const Constraint& lhs){
                return Formula(carl::FormulaType::NOT, Formula(lhs));
            })
        .def("__and__", [](const Constraint& lhs, const Constraint& rhs){
                return Formula(carl::FormulaType::AND, {Formula(lhs), Formula(rhs)});
            })
        .def("__and__", [](const Constraint& lhs, const Formula& rhs){
                return Formula(carl::FormulaType::AND, {Formula(lhs), rhs});
            })
        .def("__or__", [](const Constraint& lhs, const Constraint& rhs){
                return Formula(carl::FormulaType::OR, {Formula(lhs), Formula(lhs)});
            })
        .def("__or__", [](const Constraint& lhs, const Formula& rhs){
                return Formula(carl::FormulaType::OR, {Formula(lhs), rhs});
            })
        .def("__xor__", [](const Constraint& lhs, const Constraint& rhs){
                return Formula(carl::FormulaType::XOR, {Formula(lhs), Formula(rhs)});
            })
        .def("__xor__", [](const Constraint& lhs, const Formula& rhs){
                return Formula(carl::FormulaType::XOR, {Formula(lhs), rhs});
            })

        //.def("satisfied_by", [](const Constraint& constraint, const carl::EvaluationMap<Rational>& evaluation) { return Formula(constraint).satisfiedBy(evaluation); })

        .def_property_readonly("relation", &Constraint::relation)
        .def_property_readonly("lhs", &Constraint::lhs)
        .def(py::pickle(
                [](const Constraint& val) -> std::tuple<std::string> {
                    throw NoPickling();
                },
                [](const std::tuple<std::string>& data) -> Constraint {
                    throw NoPickling();
                }
            ))
    ;
}
//
void define_simple_constraint(py::module& m) {
    py::class_<SimpleConstraint>(m, "SimpleConstraint")
        .def(py::init<bool>())
        .def(py::init<Polynomial, carl::Relation>())
        .def("__str__", &streamToString<SimpleConstraint>)

        .def("lhs", &SimpleConstraint::lhs, "Get the left hand side of the constraint")
        .def("rel", &SimpleConstraint::rel, "Get the relation of the constraint")
        .def(py::pickle(
                [](const SimpleConstraint& val) -> std::tuple<std::string> {
                    throw NoPickling();
                },
                [](const std::tuple<std::string>& data) -> SimpleConstraint {
                    throw NoPickling();
                }
            ))
    ;
    
    py::class_<SimpleConstraintRatFunc>(m, "SimpleConstraintRatFunc")
        .def(py::init<bool>())
        .def(py::init<FactorizedRationalFunction, carl::Relation>())
        .def("__str__", &streamToString<SimpleConstraintRatFunc>)

        .def("lhs", &SimpleConstraintRatFunc::lhs, "Get the left hand side of the constraint")
        .def("rel", &SimpleConstraintRatFunc::rel, "Get the relation of the constraint")

        .def(py::pickle(
                [](const SimpleConstraintRatFunc& val) -> std::tuple<std::string> {
                    throw NoPickling();
                },
                [](const std::tuple<std::string>& data) -> SimpleConstraintRatFunc {
                    throw NoPickling();
                }
            ))
    ;
}

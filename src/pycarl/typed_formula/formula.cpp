/*
 * formula.cpp
 *
 *  Created on: 16 Apr 2016
 *      Author: harold
 */

#include "formula.h"

#include "common.h"


void define_formula(py::module& m) {
    py::class_<Formula>(m, "Formula")
        .def(py::init<carl::Variable>(), "Create Formula given Boolean variable")
        .def(py::init<Constraint>())
        .def(py::init<carl::FormulaType, Formula>())
        .def(py::init<carl::FormulaType, carl::Formulas<Polynomial>>())
        .def(py::init([](bool b) {
                return b ? Formula(carl::FormulaType::TRUE) : Formula(carl::FormulaType::FALSE);
            }))
        .def("__str__", &streamToString<carl::Formula<Polynomial>>)
        .def("to_smt2", [](Formula const& f) {
                return f.toString(false, 2);
            })

        .def("__invert__", [](const Formula& lhs){
                return lhs.negated();
            })
        .def("__and__", [](const Formula& lhs, const Constraint& rhs){
                return Formula(carl::FormulaType::AND, {lhs, Formula(rhs)});
            })
        .def("__and__", [](const Formula& lhs, const Formula& rhs){
                return Formula(carl::FormulaType::AND, {lhs, rhs});
            })
        .def("__or__", [](const Formula& lhs, const Constraint& rhs){
                return Formula(carl::FormulaType::OR, {lhs, Formula(rhs)});
            })
        .def("__or__", [](const Formula& lhs, const Formula& rhs){
                return Formula(carl::FormulaType::OR, {lhs, rhs});
            })
        .def("__xor__", [](const Formula& lhs, const Constraint& rhs){
                return Formula(carl::FormulaType::XOR, {lhs, Formula(rhs)});
            })
        .def("__xor__", [](const Formula& lhs, const Formula& rhs){
                return Formula(carl::FormulaType::XOR, {lhs, rhs});
            })

        //.def("satisfied_by", &Formula::satisfiedBy)

        .def("__len__", &Formula::size)
        .def("__iter__", [](const Formula& f) {
                return py::make_iterator(f.begin(), f.end());
            }, py::keep_alive<0, 1>() /* Essential: keep object alive while iterator exists */)

        .def_property_readonly("type", &Formula::getType)

        .def("get_negation_subformula", &Formula::subformula, "Get subformula of negation formula")
        .def("get_implication_premise", &Formula::premise, "Get premise of implication formula")
        .def("get_implication_conclusion", &Formula::conclusion, "Get conclusion of implication formula")
        .def("get_ite_condition", &Formula::condition, "Get condition of ITE formula")
        .def("get_ite_first_case", &Formula::firstCase, "Get then case of ITE formula")
        .def("get_ite_second_case", &Formula::secondCase, "Get else case of ITE formula")
        .def("get_subformulas", &Formula::subformulas, "Get list of subformulas for n-ary formula")
        .def("get_constraint", &Formula::constraint, "Get constraint of constraint formula")

        .def(py::pickle(
                [](const Formula& val) -> std::tuple<std::string> {
                    throw NoPickling();
                },
                [](const std::tuple<std::string>& data) -> Formula {
                    throw NoPickling();
                }
            ))
    ;
}

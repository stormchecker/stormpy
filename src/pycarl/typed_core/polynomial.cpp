/*
 * polynomial.cpp
 *
 *  Created on: 16 Apr 2016
 *      Author: harold
 */

#include "polynomial.h"

#include "src/pycarl/types.h"
#include "src/pycarl/helpers.h"


void define_polynomial(py::module& m) {


    py::class_<Polynomial>(m, "Polynomial","Represent a multivariate polynomial")
        .def(py::init<const Term&>())
        .def(py::init<const Monomial::Arg&>())
        .def(py::init<carl::Variable::Arg>())
        .def(py::init<Rational>())
        .def(py::init<std::vector<Term>&>())

        .def("is_constant", &Polynomial::isConstant)

        .def("__add__", [](const Polynomial& lhs, const Integer& rhs) -> Polynomial { return lhs + Rational(rhs); })
        .def(py::self + Rational())
        .def(py::self + carl::Variable())
        .def("__add__", [](const Polynomial& lhs, Monomial::Arg rhs) -> Polynomial { return lhs + rhs; })
        .def("__radd__", [](const Polynomial& lhs, Monomial::Arg rhs) -> Polynomial { return lhs + rhs; })
        .def(py::self + Term())
        .def(py::self + py::self)
        .def("__add__", [](const Polynomial& lhs, const RationalFunction& rhs) -> RationalFunction { return rhs + lhs; })

        .def("__sub__", [](const Polynomial& lhs, const Integer& rhs) -> Polynomial { return lhs - Rational(rhs); })
        .def(py::self - Rational())
        .def(py::self - carl::Variable())
        .def("__sub__", [](const Polynomial& lhs, Monomial::Arg rhs) -> Polynomial { return lhs - rhs; })
        .def("__rsub__", [](const Polynomial& lhs, Monomial::Arg rhs) -> Polynomial { return rhs - lhs; })
        .def("__rsub__", [](const Polynomial& lhs, carl::Variable::Arg rhs) -> Polynomial { return rhs - lhs; })
        .def(py::self - Term())
        .def(py::self - py::self)

        .def("__mul__", [](const Polynomial& lhs, const Integer& rhs) -> Polynomial { return lhs * Rational(rhs); })
        .def(py::self * Rational())
        .def("__mul__", [](const Polynomial& lhs, carl::Variable::Arg rhs) -> Polynomial { return lhs * rhs; })
        .def("__rmul__", [](const Polynomial& rhs, carl::Variable::Arg lhs) -> Polynomial { return rhs * lhs; })
        .def("__mul__", [](const Polynomial& lhs, Monomial::Arg rhs) -> Polynomial { return lhs * rhs; })
        .def("__rmul__", [](const Polynomial& rhs, Monomial::Arg lhs) -> Polynomial { return rhs * lhs; })
        .def(py::self * Term())
        .def(py::self * py::self)

        .def(PY_DIV, [](const Polynomial& lhs, const RationalFunction& rhs) { return RationalFunction(lhs) / rhs; })
        .def(PY_DIV, [](const Polynomial& lhs, const Polynomial& rhs) { return RationalFunction(lhs, rhs); })
        .def(PY_DIV, [](const Polynomial& lhs, const Term& rhs) { return RationalFunction(lhs) / rhs; })
        .def(PY_DIV, [](const Polynomial& lhs, const Monomial::Arg& rhs) { return RationalFunction(lhs) / rhs; })
        .def(PY_DIV, [](const Polynomial& lhs, carl::Variable::Arg rhs) { return RationalFunction(lhs) / rhs; })
        .def(py::self / Rational())
        .def(PY_DIV, [](const Polynomial& lhs, const Integer& rhs) -> Polynomial { return lhs / Rational(rhs); })

        .def("__pow__", [](const Polynomial& var, carl::uint exp) {return var.pow(exp);})

        .def("__pos__", [](const Polynomial& var) {return Polynomial(var);})
        .def("__neg__", [](const Polynomial& var) {return var * Polynomial(-1);})

        .def("constant_part", [](const Polynomial& pol) -> Rational { return pol.constantPart(); })
        .def("evaluate", &Polynomial::evaluate<Rational>)
        .def("substitute", [](const Polynomial& orig, std::map<carl::Variable, Polynomial>& substitutions) {return orig.substitute(substitutions);})
        .def("gather_variables", static_cast<std::set<carl::Variable> (Polynomial::*)() const>(&Polynomial::gatherVariables))
        .def_property_readonly("total_degree", &Polynomial::totalDegree)//, py::doc("The maximum degree of the terms in the polynomial"))
        .def("degree", &Polynomial::degree)//, py::doc("Computes the degree with respect to the given variable"))
        .def_property_readonly("nr_terms", &Polynomial::nrTerms)
        .def("derive", [](Polynomial const& pol, carl::Variable const& var) {
                return pol.derivative(var, 1);
            }, "Compute the derivative", py::arg("variable"))
        .def("__str__", [](const Polynomial& pol) { return pol.toString(); })
        .def("__repr__", [](const Polynomial& pol) { return pol.toString(); })
        .def("to_smt2", [](Polynomial const& pol) {
                return pol.toString(false, true);
            })

        .def(py::self != py::self)
        .def(py::self == py::self)
        .def(py::self != Rational())
        .def(py::self == Rational())
        .def("__eq__", [](const Polynomial& lhs, const Integer& rhs) -> bool {return lhs == Rational(rhs);})
        .def("__ne__", [](const Polynomial& lhs, const Integer& rhs) -> bool {return lhs != Rational(rhs);})

        .def("__len__", &Polynomial::size)
        .def("__getitem__", [](const Polynomial& p, std::size_t index) { return *(p.begin()+index); })
        .def("__iter__", [](const Polynomial& p) {
                return py::make_iterator(p.begin(), p.end());
            }, py::keep_alive<0, 1>() /* Essential: keep object alive while iterator exists */)
        .def(py::pickle(
                [](const Polynomial& val) -> std::tuple<std::string> {
                    throw NoPickling();
                },
                [](const std::tuple<std::string>& data) -> Polynomial {
                    throw NoPickling();
                }
            ))
        .def("__hash__", [](const Polynomial& v) { std::hash<Polynomial> h; return h(v);})
    ;
}

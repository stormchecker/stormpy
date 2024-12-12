#include "term.h"

#include "src/pycarl/helpers.h"
#include "src/pycarl/types.h"


void define_term(py::module& m) {
    py::class_<Term>(m, "Term")
        .def(py::init<Rational, const Monomial::Arg&>())
        .def(py::init<carl::Variable&>())
        .def(py::init<Rational const&>())

        .def("__add__",  static_cast<Polynomial (*)(const Term&, const Polynomial&)>(&carl::operator+))
        .def("__add__",  static_cast<Polynomial (*)(const Term&, const Term&)>(&carl::operator+))
        .def("__add__",  static_cast<Polynomial (*)(const Term&, const Monomial::Arg&)>(&carl::operator+))
        .def("__add__",  static_cast<Polynomial (*)(const Term&, carl::Variable::Arg)>(&carl::operator+))
        .def("__add__",  static_cast<Polynomial (*)(const Term&, const Rational&)>(&carl::operator+))

        .def("__sub__",  static_cast<Polynomial (*)(const Term&, const Polynomial&)>(&carl::operator-))
        .def("__sub__",  static_cast<Polynomial (*)(const Term&, const Term&)>(&carl::operator-))
        .def("__sub__",  static_cast<Polynomial (*)(const Term&, const Monomial::Arg&)>(&carl::operator-))
        .def("__sub__",  static_cast<Polynomial (*)(const Term&, carl::Variable::Arg)>(&carl::operator-))
        .def("__sub__",  static_cast<Polynomial (*)(const Term&, const Rational&)>(&carl::operator-))

        .def("__mul__",  static_cast<Polynomial (*)(const Term&, const Polynomial&)>(&carl::operator*))
        .def("__mul__",  static_cast<Term (*)(Term, const Term&)>(&carl::operator*))
        .def("__mul__",  static_cast<Term (*)(Term, const Monomial::Arg&)>(&carl::operator*))
        .def("__mul__",  static_cast<Term (*)(Term, carl::Variable)>(&carl::operator*))
        .def("__mul__",  static_cast<Term (*)(Term, const Rational&)>(&carl::operator*))

        .def(PY_DIV, [](const Term& lhs, const RationalFunction& rhs) { return RationalFunction(Polynomial(lhs)) / rhs; })
        .def(PY_DIV, [](const Term& lhs, const Polynomial& rhs) { return RationalFunction(Polynomial(lhs)) / rhs; })
        .def(PY_DIV, [](const Term& lhs, const Term& rhs) { return RationalFunction(Polynomial(lhs)) / rhs; })
        .def(PY_DIV, [](const Term& lhs, const Monomial::Arg& rhs) { return RationalFunction(Polynomial(lhs)) / rhs; })
        .def(PY_DIV, [](const Term& lhs, carl::Variable::Arg rhs) { return RationalFunction(Polynomial(lhs)) / rhs; })
        .def(py::self / Rational())

        .def("__pow__", [](const Term& var, carl::uint exp) {return var.pow(exp);})

        .def("__pos__", [](const Term& var) {return Term(var);})
        .def("__neg__", [](const Term& var) {return var * Term(-1);})

        .def(py::self != py::self)
        .def(py::self == py::self)
        .def("is_constant", [](const Term& arg) {return arg.isConstant();})
        .def("is_one", [](const Term& arg) {return arg.isOne();})
        .def_property_readonly("tdeg", [](const Term& arg) { return arg.tdeg();} )

        .def_property_readonly("coeff", [] (const Term& arg) { return arg.coeff(); })
        .def_property_readonly("monomial", [](const Term& arg) { return arg.monomial(); })

        .def("__str__", &streamToString<Term>)

        .def(py::pickle(
                [](const Term& val) -> std::tuple<std::string> {
                    throw NoPickling();
                },
                [](const std::tuple<std::string>& data) -> Term {
                    throw NoPickling();
                }
            ))
        .def("__hash__", [](const Term& v) { std::hash<Term> h; return h(v);})
    ;
}

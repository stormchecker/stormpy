#include "rationalfunction.h"


#include "src/pycarl/types.h"
#include "src/pycarl/helpers.h"



void define_rationalfunction(py::module& m) {
    py::class_<RationalFunction>(m, "RationalFunction", "Represent a rational function, that is the fraction of two multivariate polynomials ")
        .def(py::init<carl::Variable>())
        .def(py::init<Polynomial>())
        .def(py::init<Polynomial, Polynomial>())

        .def("__add__",  static_cast<RationalFunction (*)(const RationalFunction&, const Polynomial&)>(&carl::operator+))
        .def("__add__",  static_cast<RationalFunction (*)(const RationalFunction&, const Term&)>(&carl::operator+))
        .def("__add__",  static_cast<RationalFunction (*)(const RationalFunction&, const Monomial::Arg&)>(&carl::operator+))
        .def("__add__",  static_cast<RationalFunction (*)(const RationalFunction&, carl::Variable)>(&carl::operator+))
        .def("__add__",  static_cast<RationalFunction (*)(const RationalFunction&, const Rational&)>(&carl::operator+))
        .def(py::self + py::self)
        .def("__radd__", [](const RationalFunction& rhs, const Polynomial& lhs) -> RationalFunction {return rhs + lhs;})
        .def("__radd__", [](const RationalFunction& rhs, const Term& lhs) -> RationalFunction {return rhs + lhs;})
        .def("__radd__", [](const RationalFunction& rhs, const Monomial::Arg& lhs) -> RationalFunction {return rhs + lhs;})
        .def("__radd__", [](const RationalFunction& rhs, carl::Variable::Arg lhs) -> RationalFunction {return rhs + lhs;})
        .def("__radd__", [](const RationalFunction& rhs, const Rational& lhs) -> RationalFunction {return rhs + lhs;})

        .def("__sub__",  static_cast<RationalFunction (*)(const RationalFunction&, const Polynomial&)>(&carl::operator-))
        .def("__sub__",  static_cast<RationalFunction (*)(const RationalFunction&, const Term&)>(&carl::operator-))
        .def("__sub__",  static_cast<RationalFunction (*)(const RationalFunction&, const Monomial::Arg&)>(&carl::operator-))
        .def("__sub__",  static_cast<RationalFunction (*)(const RationalFunction&, carl::Variable)>(&carl::operator-))
        .def("__sub__",  static_cast<RationalFunction (*)(const RationalFunction&, const Rational&)>(&carl::operator-))
        .def(py::self - py::self)

        .def("__mul__",  static_cast<RationalFunction (*)(const RationalFunction&, const Polynomial&)>(&carl::operator*))
        .def("__rmul__", [](const RationalFunction& rhs, const Polynomial& lhs) -> RationalFunction { return rhs * lhs; })
        .def("__mul__",  static_cast<RationalFunction (*)(const RationalFunction&, const Term&)>(&carl::operator*))
        .def("__mul__",  static_cast<RationalFunction (*)(const RationalFunction&, const Monomial::Arg&)>(&carl::operator*))
        .def("__mul__",  static_cast<RationalFunction (*)(const RationalFunction&, carl::Variable)>(&carl::operator*))
        .def("__mul__",  static_cast<RationalFunction (*)(const RationalFunction&, const Rational&)>(&carl::operator*))
        .def(py::self * py::self)

        .def(PY_DIV, static_cast<RationalFunction (*)(const RationalFunction&, const Rational&)>(&carl::operator/))
        .def(PY_DIV, static_cast<RationalFunction (*)(const RationalFunction&, const Polynomial&)>(&carl::operator/))
        .def(PY_DIV, static_cast<RationalFunction (*)(const RationalFunction&, const Term&)>(&carl::operator/))
        .def(PY_DIV, static_cast<RationalFunction (*)(const RationalFunction&, carl::Variable)>(&carl::operator/))
        .def(PY_DIV, static_cast<RationalFunction (*)(const RationalFunction&, const Rational&)>(&carl::operator/))
        .def(py::self / py::self)

        .def("__pow__", [](const RationalFunction& var, carl::uint exp) {return carl::pow(var, exp);})

        .def("__pos__", [](const RationalFunction& var) {return RationalFunction(var);})
        .def("__neg__", [](const RationalFunction& var) {return var * RationalFunction(-1);})

        .def("evaluate", &RationalFunction::evaluate)
        .def("gather_variables", static_cast<std::set<carl::Variable> (RationalFunction::*)() const>(&RationalFunction::gatherVariables))
        .def_property_readonly("nominator", &RationalFunction::nominator)
        .def_property_readonly("numerator", &RationalFunction::nominator)
        .def_property_readonly("denominator", &RationalFunction::denominator)
        .def("derive", [](RationalFunction const& ratFunc, carl::Variable const& var) {
                return ratFunc.derivative(var, 1);
            }, "Compute the derivative", py::arg("variable"))
        .def("is_constant", &RationalFunction::isConstant)
        .def("constant_part", &RationalFunction::constantPart)

        .def("__str__", &streamToString<RationalFunction>)
        .def("to_smt2", [](RationalFunction const& rf) {
                return rf.toString(false, true);
            })

        .def(py::self == py::self)
        .def(py::self != py::self)
        .def("__eq__", [](const RationalFunction& lhs, const Polynomial& rhs) -> bool {return lhs == RationalFunction(rhs);})
        .def("__ne__", [](const RationalFunction& lhs, const Polynomial& rhs) -> bool {return lhs != RationalFunction(rhs);})

        .def(py::pickle(
                [](const RationalFunction& val) -> std::tuple<std::string> {
                    throw NoPickling();
                },
                [](const std::tuple<std::string>& data) -> RationalFunction {
                    throw NoPickling();
                }
            ))
        .def("__hash__", [](const RationalFunction& v) { std::hash<RationalFunction> h; return h(v);})
    ;
}

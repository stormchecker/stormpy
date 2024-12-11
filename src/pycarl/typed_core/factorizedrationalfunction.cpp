#include "factorizedrationalfunction.h"


#include "src/pycarl/types.h"
#include "src/pycarl/helpers.h"


void define_factorizedrationalfunction(py::module& m) {
    py::class_<FactorizedRationalFunction>(m, "FactorizedRationalFunction", "Represent a rational function, that is the fraction of two factorized polynomials ")
        .def(py::init<FactorizedPolynomial>())
        .def(py::init<FactorizedPolynomial, FactorizedPolynomial>())
        .def("evaluate", &FactorizedRationalFunction::evaluate)
        .def("gather_variables", static_cast<std::set<carl::Variable> (FactorizedRationalFunction::*)() const>(&FactorizedRationalFunction::gatherVariables))
        .def_property_readonly("numerator", &FactorizedRationalFunction::nominator)
        .def_property_readonly("denominator", &FactorizedRationalFunction::denominator)
        .def("is_constant", &FactorizedRationalFunction::isConstant)
        .def("constant_part", &FactorizedRationalFunction::constantPart)
        .def("rational_function", [](FactorizedRationalFunction const& rf) -> RationalFunction {
            if(rf.isConstant()) {
                return RationalFunction(rf.constantPart());
            } else {
                return RationalFunction(rf.nominator().polynomialWithCoefficient(), rf.denominator().polynomialWithCoefficient());
            };
        })
        .def("derive", [](FactorizedRationalFunction const& ratFunc, carl::Variable const& var) {
                return ratFunc.derivative(var, 1);
            }, "Compute the derivative", py::arg("variable"))
        .def("__str__", &streamToString<FactorizedRationalFunction>)
        .def("to_smt2", [](FactorizedRationalFunction const& rf) {
            return rf.toString(false, true);
        })

        .def(py::self - py::self)
        .def(py::self + py::self)
        .def(py::self * py::self)
        .def(py::self / py::self)
        .def(py::self == py::self)
        .def(py::self != py::self)
        .def(py::self + Rational())
        .def(py::pickle(
                [](const FactorizedRationalFunction& val) -> std::tuple<std::string> {
                    throw NoPickling();
                },
                [](const std::tuple<std::string>& data) -> FactorizedRationalFunction {
                    throw NoPickling();
                }
            ))
        .def("__hash__", [](const FactorizedRationalFunction& v) { std::hash<FactorizedRationalFunction> h; return h(v);})
    ;
}

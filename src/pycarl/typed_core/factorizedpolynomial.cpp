#include "factorizedpolynomial.h"

#include "src/pycarl/types.h"
#include "src/pycarl/helpers.h"

void define_factorizedpolynomial(py::module& m) {
    py::class_<FactorizedPolynomial>(m, "FactorizedPolynomial", "Represent a polynomial with its factorization")
        .def(py::init<const Rational&>(), py::arg("number"), "Constructor")
        .def(py::init<const Polynomial&, const std::shared_ptr<carl::Cache<FactorizationPair>>&>(), py::arg("polynomial"), py::arg("cache"), "Constructor")

        .def("is_constant", &FactorizedPolynomial::isConstant)
        .def("is_one", &FactorizedPolynomial::isOne)
        .def("constant_part", &FactorizedPolynomial::constantPart)
        .def_property("coefficient", &FactorizedPolynomial::coefficient, &FactorizedPolynomial::setCoefficient)

        .def("factorization", [](const FactorizedPolynomial& pol) {
                if (pol.isConstant())
                    return Factorization();
                else
                    return pol.factorization();
            }, "Get factorization")
        .def("polynomial",  [](const FactorizedPolynomial& pol) {
                if (pol.isConstant())
                    throw std::invalid_argument("Function not applicable for constants");
                else
                    return pol.polynomialWithCoefficient();
            },"Get underlying polynomial")
        .def("cache", &FactorizedPolynomial::pCache)

        .def("evaluate", &FactorizedPolynomial::evaluate<Rational>)
        .def("gather_variables", static_cast<std::set<carl::Variable> (FactorizedPolynomial::*)() const>(&FactorizedPolynomial::gatherVariables))
        .def("derive", [](FactorizedPolynomial const& pol, carl::Variable const& var) {
                return pol.derivative(var, 1);
            }, "Compute the derivative", py::arg("variable"))
        .def("__str__", &streamToString<FactorizedPolynomial>)
        .def("to_smt2", [](FactorizedPolynomial const& pol) {
                return pol.toString(false, true);
            })
        .def(py::self - py::self)
        .def(py::self + py::self)
        .def(py::self * py::self)

        .def("__pow__", [](const FactorizedPolynomial& pol, carl::uint exp) {
                return pol.pow(exp);
            }, py::arg("exponent"), "Raise polynomial to the power")

        .def(py::self == py::self)
        .def(py::self != py::self)
        .def(py::self == Rational())
        .def(py::self != Rational())
        .def(py::pickle(
                [](const FactorizedPolynomial& val) -> std::tuple<std::string> {
                    throw NoPickling();
                },
                [](const std::tuple<std::string>& data) -> FactorizedPolynomial {
                    throw NoPickling();
                }
            ))
        .def("__hash__", [](const FactorizedPolynomial& v) { std::hash<FactorizedPolynomial> h; return h(v);})
    ;
}

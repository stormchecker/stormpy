#include "rational.h"

#include <stdexcept>

#include "src/pycarl/helpers.h"
#include "src/pycarl/types.h"

#include "carl/numbers/numbers.h"
#include "carl/numbers/conversion/cln_gmp.h"

void define_cln_rational(py::module& m) {
#ifdef PYCARL_USE_CLN
    py::class_<cln::cl_RA>(m, "Rational", "Class wrapping cln-rational numbers")
        .def(py::init([](double val) { return carl::rationalize<cln::cl_RA>(val); }))
        .def(py::init([](carl::sint val) { return carl::rationalize<cln::cl_RA>(val); }))
        .def(py::init([](const cln::cl_I& numerator, const cln::cl_I& denominator) { return cln::cl_RA(numerator)/cln::cl_RA(denominator); }))
        .def(py::init([](const std::string& val) {
                cln::cl_RA tmp;
                bool suc = carl::try_parse<cln::cl_RA>(val, tmp);
                if(!suc) {
                   throw std::invalid_argument("Cannot translate " + val + " into a rational.");
                }
                return tmp;
            }))
        .def(py::init(&carl::convert<mpq_class, cln::cl_RA>))

        .def("__add__", [](const cln::cl_RA& lhs, const cln::cl_RA& rhs) -> cln::cl_RA { return lhs + rhs; })
        .def("__add__", [](const cln::cl_RA& lhs, carl::sint rhs) -> cln::cl_RA { return lhs + carl::rationalize<cln::cl_RA>(rhs); })
        .def("__add__", [](const cln::cl_RA& lhs, const Polynomial& rhs) -> Polynomial { return lhs + rhs; })
        .def("__add__", [](const cln::cl_RA& lhs, const FactorizedRationalFunction& rhs) -> FactorizedRationalFunction { return rhs + lhs; })
        .def("__radd__", [](const cln::cl_RA& rhs, carl::sint lhs) -> cln::cl_RA { return carl::rationalize<cln::cl_RA>(lhs) + rhs; })
        .def("__radd__", [](const cln::cl_RA& rhs, carl::Variable::Arg lhs) -> Polynomial { return lhs + rhs; })


        .def("__sub__", [](const cln::cl_RA& lhs, const cln::cl_RA& rhs) -> cln::cl_RA { return lhs - rhs; })
        .def("__sub__", [](const cln::cl_RA& lhs, carl::sint rhs) -> cln::cl_RA { return lhs - carl::rationalize<cln::cl_RA>(rhs); })
        .def("__sub__", [](const cln::cl_RA& lhs, carl::Variable::Arg rhs) -> Polynomial { return lhs - rhs; })
        .def("__rsub__", [](const cln::cl_RA& rhs, carl::sint lhs) -> cln::cl_RA { return carl::rationalize<cln::cl_RA>(lhs) - rhs; })
        .def("__rsub__", [](const cln::cl_RA& rhs, carl::Variable::Arg lhs) -> Polynomial { return lhs - rhs; })


        .def("__mul__", [](const cln::cl_RA& lhs, const cln::cl_RA& rhs) -> cln::cl_RA { return lhs * rhs; })
        .def("__mul__", [](const cln::cl_RA& lhs, carl::sint rhs) -> cln::cl_RA { return lhs * carl::rationalize<cln::cl_RA>(rhs); })
        .def("__mul__", [](const cln::cl_RA& lhs, carl::Variable::Arg rhs) -> Term { return lhs * rhs; })
        .def("__rmul__", [](const cln::cl_RA& rhs, carl::sint lhs) -> cln::cl_RA { return carl::rationalize<cln::cl_RA>(lhs) * rhs; })
        .def("__rmul__", [](const cln::cl_RA& rhs, carl::Variable::Arg lhs) -> Term { return rhs * lhs; })

        .def(PY_DIV, [](const cln::cl_RA& lhs, const cln::cl_RA& rhs) -> cln::cl_RA {
                if (carl::isZero(rhs))
                    throw std::runtime_error("Div by zero");
                return lhs / rhs;
            })
        .def(PY_DIV, [](const cln::cl_RA& lhs, carl::sint rhs) -> cln::cl_RA {
                if (rhs == 0.0)
                    throw std::runtime_error("Div by zero");
                return lhs / carl::rationalize<cln::cl_RA>(rhs);
            })
        .def(PY_RDIV, [](const cln::cl_RA& rhs, carl::sint lhs) -> cln::cl_RA {
                if (carl::isZero(rhs))
                    throw std::runtime_error("Div by zero");
                return carl::rationalize<cln::cl_RA>(lhs) / rhs;
            })

        .def(PY_DIV, [](const Rational& lhs, const RationalFunction& rhs) { return RationalFunction(lhs) / rhs; })
        .def(PY_DIV, [](const Rational& lhs, const Polynomial& rhs) { return RationalFunction(lhs) / rhs; })
        .def(PY_DIV, [](const Rational& lhs, const Term& rhs) { return RationalFunction(lhs) / rhs; })
        .def(PY_DIV, [](const Rational& lhs, const Monomial::Arg& rhs) { return RationalFunction(lhs) / rhs; })
        .def(PY_DIV, [](const Rational& lhs, carl::Variable::Arg rhs) { return RationalFunction(lhs) / rhs; })
        .def(PY_RDIV, [](const Rational& rhs, carl::Variable::Arg lhs) { return RationalFunction(lhs) / rhs; })


        .def("__pow__", static_cast<cln::cl_RA (*)(const cln::cl_RA&, std::size_t)>(&carl::pow))
        .def("__pos__", [](const cln::cl_RA& var) {return cln::cl_RA(var);})
        .def("__neg__", [](const cln::cl_RA& var) -> cln::cl_RA {return -var;})
        .def("__abs__", [](const cln::cl_RA& var) {return carl::abs(var);})

        .def(py::self > py::self)
        .def(py::self < py::self)
        .def(py::self == py::self)
        .def(py::self != py::self)
        .def(py::self >= py::self)
        .def(py::self <= py::self)

        .def(py::self == cln::cl_I())
        .def(py::self < cln::cl_I())
        .def(py::self > cln::cl_I())
        .def(py::self <= cln::cl_I())
        .def(py::self >= cln::cl_I())
        .def(py::self != cln::cl_I())

        .def(py::self == Polynomial())
        .def(py::self != Polynomial())

        .def(py::self > int())
        .def(py::self < int())
        .def(py::self == int())
        .def(py::self != int())
        .def(py::self >= int())
        .def(py::self <= int())


        .def("is_one", [](const cln::cl_RA& r) { return carl::isOne(r); })
        .def("is_minus_one", [](const cln::cl_RA& r) {return carl::isOne(-r); })
        .def("__float__", static_cast<double (*)(cln::cl_RA const&)>(&carl::toDouble))
        .def("__str__", &streamToString<cln::cl_RA>)
		.def("__repr__", [](const cln::cl_RA& r) { return "<Rational  (cln)" + streamToString<cln::cl_RA>(r) + ">"; })

        .def_property_readonly("nominator", [](const cln::cl_RA& val) -> cln::cl_I {
            return carl::getNum(val);
        })
        .def_property_readonly("numerator", [](const cln::cl_RA& val) ->  cln::cl_I {
                return carl::getNum(val);
            })
        .def_property_readonly("denominator", [](const cln::cl_RA& val) ->  cln::cl_I {
                return carl::getDenom(val);
            })

        .def(py::pickle(
                [](const cln::cl_RA& val) {
                    return std::pair<std::string, std::string>(carl::toString(carl::getNum(val)), carl::toString(carl::getDenom(val)));
                },
                [](std::pair<std::string, std::string> data) {
                    return carl::parse<cln::cl_RA>(data.first) / carl::parse<cln::cl_RA>(data.second);
                }
            ))
        .def("__hash__", [](const cln::cl_RA& v) { std::hash<cln::cl_RA> h; return h(v);})
    ;

	py::implicitly_convertible<carl::uint, cln::cl_RA>();
#endif
}



void define_gmp_rational(py::module& m) {
#ifndef PYCARL_USE_CLN
    py::class_<mpq_class>(m, "Rational", "Class wrapping gmp-rational numbers")
        .def(py::init([](double val) { return carl::rationalize<mpq_class>(val); }))
        .def(py::init([](carl::sint val) { return carl::rationalize<mpq_class>(val); }))
        .def(py::init<const mpz_class&, const mpz_class&>())
        .def(py::init([](const std::string& val) {
                mpq_class tmp;
                bool suc = carl::try_parse<mpq_class>(val, tmp);
                if(!suc) {
                    throw std::invalid_argument("Cannot translate " + val + " into a rational.");
                }
                return tmp;
            }))
#ifdef PYCARL_HAS_CLN
        .def(py::init(&carl::convert<cln::cl_RA, mpq_class>))
#endif

        .def("__add__", [](const mpq_class& lhs, const mpq_class& rhs) -> mpq_class { return lhs + rhs; })
        .def("__add__", [](const mpq_class& lhs, carl::sint rhs) -> mpq_class { return lhs + carl::rationalize<mpq_class>(rhs); })
        .def("__radd__", [](const mpq_class& rhs, carl::sint lhs) -> mpq_class { return carl::rationalize<mpq_class>(lhs) + rhs; })
        .def("__radd__", [](const mpq_class& rhs, carl::Variable::Arg lhs) -> Polynomial { return lhs + rhs; })


        .def("__sub__", [](const mpq_class& lhs, const mpq_class& rhs) -> mpq_class { return lhs - rhs; })
        .def("__sub__", [](const mpq_class& lhs, carl::sint rhs) -> mpq_class { return lhs - carl::rationalize<mpq_class>(rhs); })
        .def("__sub__", [](const mpq_class& lhs, carl::Variable::Arg rhs) -> Polynomial { return lhs - rhs; })
        .def("__rsub__", [](const mpq_class& rhs, carl::sint lhs) -> mpq_class { return carl::rationalize<mpq_class>(lhs) - rhs; })
        .def("__rsub__", [](const mpq_class& rhs, carl::Variable::Arg lhs) -> Polynomial { return lhs - rhs; })

        .def("__mul__", [](const mpq_class& lhs, const mpq_class& rhs) -> mpq_class { return lhs * rhs; })
        .def("__mul__", [](const mpq_class& lhs, carl::sint rhs) -> mpq_class { return lhs * carl::rationalize<mpq_class>(rhs); })
        .def("__mul__", [](const mpq_class& lhs, carl::Variable::Arg rhs) -> Term { return lhs * rhs; })
        .def("__rmul__", [](const mpq_class& rhs, carl::sint lhs) -> mpq_class { return carl::rationalize<mpq_class>(lhs) * rhs; })
        .def("__rmul__", [](const mpq_class& rhs, carl::Variable::Arg lhs) -> Term { return rhs * lhs; })

        .def(PY_DIV, [](const mpq_class& lhs, const mpq_class& rhs) -> mpq_class {
                if (carl::isZero(rhs))
                    throw std::runtime_error("Div by zero");
                return lhs / rhs;
            })
        .def(PY_DIV, [](const mpq_class& lhs, carl::sint rhs) -> mpq_class {
                if (rhs == 0.0)
                    throw std::runtime_error("Div by zero");
                return lhs / carl::rationalize<mpq_class>(rhs);
            })
        .def(PY_RDIV, [](const mpq_class& rhs, carl::sint lhs) -> mpq_class {
                if (carl::isZero(rhs))
                    throw std::runtime_error("Div by zero");
                return carl::rationalize<mpq_class>(lhs) / rhs;
            })

        .def(PY_DIV, [](const Rational& lhs, const RationalFunction& rhs) { return RationalFunction(lhs) / rhs; })
        .def(PY_DIV, [](const Rational& lhs, const Polynomial& rhs) { return RationalFunction(lhs) / rhs; })
        .def(PY_DIV, [](const Rational& lhs, const Term& rhs) { return RationalFunction(lhs) / rhs; })
        .def(PY_DIV, [](const Rational& lhs, const Monomial::Arg& rhs) { return RationalFunction(lhs) / rhs; })
        .def(PY_DIV, [](const Rational& lhs, carl::Variable::Arg rhs) { return RationalFunction(lhs) / rhs; })
        .def(PY_RDIV, [](const Rational& rhs, carl::Variable::Arg lhs) { return RationalFunction(lhs) / rhs; })

        .def("__pow__", static_cast<mpq_class (*)(const mpq_class&, std::size_t)>(&carl::pow))
        .def("__pos__", [](const mpq_class& var) {return mpq_class(var);})
        .def("__neg__", [](const mpq_class& var) -> mpq_class {return -var;})
        .def("__abs__", [](const mpq_class& var) {return carl::abs(var);})

        .def(py::self > py::self)
        .def(py::self < py::self)
        .def(py::self == py::self)
        .def(py::self != py::self)
        .def(py::self >= py::self)
        .def(py::self <= py::self)

        .def(py::self == mpz_class())
        .def(py::self < mpz_class())
        .def(py::self > mpz_class())
        .def(py::self <= mpz_class())
        .def(py::self >= mpz_class())
        .def(py::self != mpz_class())

        .def(py::self == Polynomial())
        .def(py::self != Polynomial())

        .def(py::self > int())
        .def(py::self < int())
        .def(py::self == int())
        .def(py::self != int())
        .def(py::self >= int())
        .def(py::self <= int())


        .def("__float__", static_cast<double (*)(mpq_class const&)>(&carl::toDouble))
        .def("__str__", &streamToString<mpq_class>)
        .def("__repr__", [](const mpq_class& r) { return "<Rational  (gmp)" + streamToString<mpq_class>(r) + ">"; })


        .def_property_readonly("nominator", [](const mpq_class& val) -> mpz_class {
                return carl::getNum(val);
            })
        .def_property_readonly("numerator", [](const mpq_class& val) -> mpz_class {
                return carl::getNum(val);
            })
        .def_property_readonly("denominator", [](const mpq_class& val) -> mpz_class {
                return carl::getDenom(val);
            })

        .def(py::pickle(
                [](const mpq_class& val) {
                    return std::pair<std::string, std::string>(carl::toString(carl::getNum(val)), carl::toString(carl::getDenom(val)));
                },
                [](std::pair<std::string, std::string> data) {
                    return carl::parse<mpq_class>(data.first) / carl::parse<mpq_class>(data.second);
                }
            ))
        .def("__hash__", [](const mpq_class& v) { std::hash<mpq_class> h; return h(v);})
    ;

    py::implicitly_convertible<carl::uint, mpq_class>();
#endif
}

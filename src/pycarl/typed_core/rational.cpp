#include "rational.h"

#include <stdexcept>

#include "src/helpers.h"
#include "src/pycarl/types.h"

// Must be included last
#include <carl/numbers/conversion/cln_gmp.h>
#include <carl/numbers/numbers.h>

struct PyFraction {
    py::object obj;
};

namespace pybind11 {
namespace detail {
template<>
struct type_caster<PyFraction> {
    PYBIND11_TYPE_CASTER(PyFraction, const_name("fractions.Fraction"));
    bool load(handle src, bool) {
        auto fractions = py::module_::import("fractions");
        if (!py::isinstance(src, fractions.attr("Fraction")))
            return false;
        value.obj = py::reinterpret_borrow<py::object>(src);
        return true;
    }
    static handle cast(PyFraction, return_value_policy, handle) {
        return py::none().release();
    }
};
}  // namespace detail
}  // namespace pybind11

#ifdef PYCARL_USE_CLN
static cln::cl_I pyint_to_cl_I(py::int_ val) {
    bool negative = val.attr("__lt__")(py::int_(0)).cast<bool>();
    py::int_ absval = negative ? val.attr("__neg__")().cast<py::int_>() : val;
    int bit_len = absval.attr("bit_length")().cast<int>();
    if (bit_len == 0)
        return cln::cl_I(0);
    std::size_t byte_len = (static_cast<std::size_t>(bit_len) + 7) / 8;
    std::string raw = absval.attr("to_bytes")(py::int_(byte_len), py::str("big")).cast<std::string>();

    const auto* data = reinterpret_cast<const unsigned char*>(raw.data());
    cln::cl_I result(0);
    std::size_t i = 0;
    for (; i + 4 <= byte_len; i += 4) {
        uint32_t chunk = ((uint32_t)data[i] << 24) | ((uint32_t)data[i + 1] << 16) | ((uint32_t)data[i + 2] << 8) | (uint32_t)data[i + 3];
        result = cln::ash(result, 32) + cln::cl_I((unsigned int)chunk);
    }
    for (; i < byte_len; i++) result = cln::ash(result, 8) + cln::cl_I((unsigned int)data[i]);

    return negative ? -result : result;
}
#endif

[[maybe_unused]] static mpz_class pyint_to_mpz(py::int_ val) {
    bool negative = val.attr("__lt__")(py::int_(0)).cast<bool>();
    py::int_ absval = negative ? val.attr("__neg__")().cast<py::int_>() : val;
    int bit_len = absval.attr("bit_length")().cast<int>();
    if (bit_len == 0)
        return mpz_class(0);
    std::size_t byte_len = (static_cast<std::size_t>(bit_len) + 7) / 8;
    std::string raw = absval.attr("to_bytes")(py::int_(byte_len), py::str("big")).cast<std::string>();
    mpz_class result;
    mpz_import(result.get_mpz_t(), raw.size(), 1, 1, 0, 0, raw.data());
    if (negative)
        return -result;
    return result;
}

void define_cln_rational(py::module& m) {
#ifdef PYCARL_USE_CLN
    py::class_<cln::cl_RA>(m, "Rational", "Class wrapping cln-rational numbers")
        .def(py::init([](double val) { return carl::rationalize<cln::cl_RA>(val); }))
        .def(py::init([](carl::sint val) { return carl::rationalize<cln::cl_RA>(val); }))
        .def(py::init([](const cln::cl_I& numerator, const cln::cl_I& denominator) { return cln::cl_RA(numerator) / cln::cl_RA(denominator); }))
        .def(py::init([](const std::string& val) {
            cln::cl_RA tmp;
            bool suc = carl::try_parse<cln::cl_RA>(val, tmp);
            if (!suc) {
                throw std::invalid_argument("Cannot translate " + val + " into a rational.");
            }
            return tmp;
        }))
        .def(py::init(&carl::convert<mpq_class, cln::cl_RA>))
        .def(py::init([](PyFraction frac) {
            cln::cl_I num = pyint_to_cl_I(frac.obj.attr("numerator").cast<py::int_>());
            cln::cl_I den = pyint_to_cl_I(frac.obj.attr("denominator").cast<py::int_>());
            return cln::cl_RA(num) / cln::cl_RA(den);
        }))

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

        .def("__truediv__",
             [](const cln::cl_RA& lhs, const cln::cl_RA& rhs) -> cln::cl_RA {
                 if (carl::isZero(rhs))
                     throw std::runtime_error("Div by zero");
                 return lhs / rhs;
             })
        .def("__truediv__",
             [](const cln::cl_RA& lhs, carl::sint rhs) -> cln::cl_RA {
                 if (rhs == 0.0)
                     throw std::runtime_error("Div by zero");
                 return lhs / carl::rationalize<cln::cl_RA>(rhs);
             })
        .def("__rtruediv__",
             [](const cln::cl_RA& rhs, carl::sint lhs) -> cln::cl_RA {
                 if (carl::isZero(rhs))
                     throw std::runtime_error("Div by zero");
                 return carl::rationalize<cln::cl_RA>(lhs) / rhs;
             })

        .def("__truediv__", [](const Rational& lhs, const RationalFunction& rhs) { return RationalFunction(lhs) / rhs; })
        .def("__truediv__", [](const Rational& lhs, const Polynomial& rhs) { return RationalFunction(lhs) / rhs; })
        .def("__truediv__", [](const Rational& lhs, const Term& rhs) { return RationalFunction(lhs) / rhs; })
        .def("__truediv__", [](const Rational& lhs, const Monomial::Arg& rhs) { return RationalFunction(lhs) / rhs; })
        .def("__truediv__", [](const Rational& lhs, carl::Variable::Arg rhs) { return RationalFunction(lhs) / rhs; })
        .def("__rtruediv__", [](const Rational& rhs, carl::Variable::Arg lhs) { return RationalFunction(lhs) / rhs; })

        .def("__pow__", static_cast<cln::cl_RA (*)(const cln::cl_RA&, std::size_t)>(&carl::pow))
        .def("__pos__", [](const cln::cl_RA& var) { return cln::cl_RA(var); })
        .def("__neg__", [](const cln::cl_RA& var) -> cln::cl_RA { return -var; })
        .def("__abs__", [](const cln::cl_RA& var) { return carl::abs(var); })

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
        .def("is_minus_one", [](const cln::cl_RA& r) { return carl::isOne(-r); })
        .def("__float__", static_cast<double (*)(cln::cl_RA const&)>(&carl::toDouble))
        .def("__str__", &streamToString<cln::cl_RA>)
        .def("__repr__", [](const cln::cl_RA& r) { return "<Rational  (cln)" + streamToString<cln::cl_RA>(r) + ">"; })

        .def_property_readonly("nominator", [](const cln::cl_RA& val) -> cln::cl_I { return carl::getNum(val); })
        .def_property_readonly("numerator", [](const cln::cl_RA& val) -> cln::cl_I { return carl::getNum(val); })
        .def_property_readonly("denominator", [](const cln::cl_RA& val) -> cln::cl_I { return carl::getDenom(val); })

        .def(py::pickle(
            [](const cln::cl_RA& val) { return std::pair<std::string, std::string>(carl::toString(carl::getNum(val)), carl::toString(carl::getDenom(val))); },
            [](std::pair<std::string, std::string> data) { return carl::parse<cln::cl_RA>(data.first) / carl::parse<cln::cl_RA>(data.second); }))
        .def("__hash__", [](const cln::cl_RA& v) {
            std::hash<cln::cl_RA> h;
            return h(v);
        });

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
            if (!suc) {
                throw std::invalid_argument("Cannot translate " + val + " into a rational.");
            }
            return tmp;
        }))
#ifdef PYCARL_HAS_CLN
        .def(py::init(&carl::convert<cln::cl_RA, mpq_class>))
#endif
        .def(py::init([](PyFraction frac) {
            mpz_class num = pyint_to_mpz(frac.obj.attr("numerator").cast<py::int_>());
            mpz_class den = pyint_to_mpz(frac.obj.attr("denominator").cast<py::int_>());
            return mpq_class(num, den);
        }))

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

        .def("__truediv__",
             [](const mpq_class& lhs, const mpq_class& rhs) -> mpq_class {
                 if (carl::isZero(rhs))
                     throw std::runtime_error("Div by zero");
                 return lhs / rhs;
             })
        .def("__truediv__",
             [](const mpq_class& lhs, carl::sint rhs) -> mpq_class {
                 if (rhs == 0.0)
                     throw std::runtime_error("Div by zero");
                 return lhs / carl::rationalize<mpq_class>(rhs);
             })
        .def("__rtruediv__",
             [](const mpq_class& rhs, carl::sint lhs) -> mpq_class {
                 if (carl::isZero(rhs))
                     throw std::runtime_error("Div by zero");
                 return carl::rationalize<mpq_class>(lhs) / rhs;
             })

        .def("__truediv__", [](const Rational& lhs, const RationalFunction& rhs) { return RationalFunction(lhs) / rhs; })
        .def("__truediv__", [](const Rational& lhs, const Polynomial& rhs) { return RationalFunction(lhs) / rhs; })
        .def("__truediv__", [](const Rational& lhs, const Term& rhs) { return RationalFunction(lhs) / rhs; })
        .def("__truediv__", [](const Rational& lhs, const Monomial::Arg& rhs) { return RationalFunction(lhs) / rhs; })
        .def("__truediv__", [](const Rational& lhs, carl::Variable::Arg rhs) { return RationalFunction(lhs) / rhs; })
        .def("__rtruediv__", [](const Rational& rhs, carl::Variable::Arg lhs) { return RationalFunction(lhs) / rhs; })

        .def("__pow__", static_cast<mpq_class (*)(const mpq_class&, std::size_t)>(&carl::pow))
        .def("__pos__", [](const mpq_class& var) { return mpq_class(var); })
        .def("__neg__", [](const mpq_class& var) -> mpq_class { return -var; })
        .def("__abs__", [](const mpq_class& var) { return carl::abs(var); })

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

        .def_property_readonly("nominator", [](const mpq_class& val) -> mpz_class { return carl::getNum(val); })
        .def_property_readonly("numerator", [](const mpq_class& val) -> mpz_class { return carl::getNum(val); })
        .def_property_readonly("denominator", [](const mpq_class& val) -> mpz_class { return carl::getDenom(val); })

        .def(py::pickle(
            [](const mpq_class& val) { return std::pair<std::string, std::string>(carl::toString(carl::getNum(val)), carl::toString(carl::getDenom(val))); },
            [](std::pair<std::string, std::string> data) { return carl::parse<mpq_class>(data.first) / carl::parse<mpq_class>(data.second); }))
        .def("__hash__", [](const mpq_class& v) {
            std::hash<mpq_class> h;
            return h(v);
        });

    py::implicitly_convertible<carl::uint, mpq_class>();
#endif
}
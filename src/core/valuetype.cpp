#include "valuetype.h"

#include <storm/adapters/IntervalAdapter.h>
#include <storm/adapters/RationalFunctionAdapter.h>
#include <storm/adapters/RationalNumberAdapter.h>
#include <storm/utility/constants.h>

// Bindings that return a representative value of each Storm C++ ValueType back to Python.
// These are used to check that Storm's C++ ValueTypes match stormpy's Python types.
void define_value_types(py::module& m) {
    m.def("_valuetype_double", []() { return storm::utility::one<double>(); }, "Representative value of C++ type 'double'");
    m.def(
        "_valuetype_rationalnumber", []() { return storm::utility::one<storm::RationalNumber>(); }, "Representative value of C++ type 'storm::RationalNumber'");
    m.def(
        "_valuetype_rationalfunction", []() { return storm::utility::one<storm::RationalFunction>(); },
        "Representative value of C++ type 'storm::RationalFunction'");
    m.def(
        "_valuetype_rationalfunctioncoefficient", []() { return storm::utility::one<storm::RationalFunctionCoefficient>(); },
        "Representative value of C++ type 'storm::RationalFunctionCoefficient'");
    m.def("_valuetype_interval", []() { return storm::utility::one<storm::Interval>(); }, "Representative value of C++ type 'storm::Interval'");
    m.def(
        "_valuetype_rationalinterval", []() { return storm::utility::one<storm::RationalInterval>(); },
        "Representative value of C++ type 'storm::RationalInterval'");
    m.def("_valuetype_polynomial", []() { return storm::utility::one<storm::Polynomial>(); }, "Representative value of C++ type 'storm::Polynomial'");
    m.def(
        "_valuetype_gmprationalnumber", []() { return storm::utility::one<storm::GmpRationalNumber>(); },
        "Representative value of C++ type 'storm::GmpRationalNumber'");
#ifdef STORM_HAVE_CLN
    m.def(
        "_valuetype_clnrationalnumber", []() { return storm::utility::one<storm::ClnRationalNumber>(); },
        "Representative value of C++ type 'storm::ClnRationalNumber'");
#endif
}

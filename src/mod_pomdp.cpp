
#include "common.h"

#include "pomdp/memory.h"
#include "pomdp/qualitative_analysis.h"
#include "pomdp/quantitative_analysis.h"
#include "pomdp/tracker.h"
#include "pomdp/transformations.h"
#include <storm/adapters/RationalFunctionAdapter.h>
#include <storm/adapters/RationalNumberAdapter.h>

template <typename T> std::string streamToString(const T &value) {
  std::stringstream sstream;
  sstream << value;
  return sstream.str();
}

PYBIND11_MODULE(pomdp, m) {
  m.doc() = "Functionality for POMDP analysis";

#ifdef STORMPY_DISABLE_SIGNATURE_DOC
  py::options options;
  options.disable_function_signatures();
#endif
  define_tracker<double>(m, "Double");
  define_tracker<storm::RationalNumber>(m, "Exact");
  define_qualitative_policy_search<double>(m, "Double");
  define_qualitative_policy_search_nt(m);
  define_memory(m);
  define_transformations_nt(m);
  define_transformations<double>(m, "Double");
  define_transformations<storm::RationalNumber>(m, "Exact");
  define_transformations<storm::RationalFunction>(m, "Rf");
  define_transformations_int<double>(m, "Double");
  define_transformations_int<storm::RationalNumber>(m, "Exact");
  define_transformations_int<storm::RationalFunction>(m, "Rf");
  define_belief_exploration<double>(m, "Double");

  //   using Interval = storm::Interval;

  //   py::class_<Interval>(m, "Interval")
  //       .def(py::init<const double &>())
  //       .def(py::init<const double &, const double &>())
  //       .def(py::init<const double &, carl::BoundType, const double &,
  //                     carl::BoundType>())

  //       .def_static("unboundedInterval", &Interval::unboundedInterval)
  //       .def_static("emptyInterval", &Interval::emptyInterval)
  //       .def_static("zeroInterval", &Interval::zeroInterval)

  //       // TODO: does not work :-(
  //       //.def_property("lower", &Interval::lower, &Interval::setLower)
  //       .def("lower", &Interval::lower,
  //            py::return_value_policy::reference_internal)
  //       .def("setLower", &Interval::setLower)
  //       .def("upper", &Interval::upper,
  //            py::return_value_policy::reference_internal)
  //       .def("setUpper", &Interval::setUpper)

  //       .def("isInfinite", &Interval::isInfinite)
  //       .def("isUnbounded", &Interval::isUnbounded)
  //       .def("isHalfBounded", &Interval::isHalfBounded)
  //       .def("isEmpty", &Interval::isEmpty)
  //       .def("isPointInterval", &Interval::isPointInterval)
  //       .def("isOpenInterval", &Interval::isOpenInterval)
  //       .def("isClosedInterval", &Interval::isClosedInterval)
  //       .def("isZero", &Interval::isZero)
  //       .def("isOne", &Interval::isOne)
  //       .def("isPositive", &Interval::isPositive)
  //       .def("isNegative", &Interval::isNegative)
  //       .def("isSemiPositive", &Interval::isSemiPositive)
  //       .def("isSemiNegative", &Interval::isSemiNegative)

  //       .def("integralPart", &Interval::integralPart)
  //       .def("diameter", &Interval::diameter)
  //       .def("center", [](const Interval &i) { return i.center(); })
  //       .def("sample", &Interval::sample)
  //       .def("contains",
  //            [](const Interval &i, const double &r) { return i.contains(r);
  //            })
  //       .def("contains",
  //            [](const Interval &i, const Interval &i2) { return
  //            i.contains(i2); })
  //       .def("meets", &Interval::meets)
  //       .def("isSubset", &Interval::isSubset)
  //       .def("isProperSubset", &Interval::isProperSubset)

  //       .def("div", &Interval::div)

  //       .def("inverse", &Interval::inverse)
  //       .def("abs", &Interval::abs)
  //       .def("__pow__",
  //            [](const Interval &i, carl::uint exp) { return i.pow(exp); })
  //       .def("intersectsWith", &Interval::intersectsWith)
  //       .def("intersect", &Interval::intersect)
  //       .def("unite", &Interval::unite)
  //       .def("difference", &Interval::difference)
  //       .def("complement", &Interval::complement)
  //       .def("symmetricDifference", &Interval::symmetricDifference)

  //       .def(py::self + py::self)
  //       .def(double() + py::self)
  //       .def(py::self + double())
  //       .def(py::self += py::self)
  //       .def(py::self += double())

  //       .def(-py::self)

  //       .def(py::self - py::self)
  //       .def(double() - py::self)
  //       .def(py::self - double())
  //       .def(py::self -= py::self)
  //       .def(py::self -= double())

  //       .def(py::self * py::self)
  //       .def(double() * py::self)
  //       .def(py::self * double())
  //       .def(py::self *= py::self)
  //       .def(py::self *= double())

  //       .def(py::self / double())
  //       .def(py::self /= double())

  //       .def(py::self == py::self)
  //       .def(py::self != py::self)
  //       .def(py::self <= py::self)
  //       .def(py::self <= double())
  //       .def(double() <= py::self)
  //       .def(py::self >= py::self)
  //       .def(py::self >= double())
  //       .def(double() >= py::self)
  //       .def(py::self < py::self)
  //       .def(py::self < double())
  //       .def(double() < py::self)
  //       .def(py::self > py::self)
  //       .def(py::self > double())
  //       .def(double() > py::self)

  //       .def("__str__", &streamToString<Interval>);

  define_transformations_int<storm::Interval>(m, "Interval");
}

#pragma once

#include "src/pycarl/common.h"
#include "src/pycarl/types.h"
#include "src/pycarl/helpers.h"

template<typename Number>
void define_interval(py::module& m) {
    using Interval = carl::Interval<Number>;

	py::class_<Interval>(m, "Interval")
		.def(py::init<const Number&>())
		.def(py::init<const Number&, const Number&>())
		.def(py::init<const Number&, carl::BoundType, const Number&, carl::BoundType>())

		.def_static("unboundedInterval", &Interval::unboundedInterval)
		.def_static("emptyInterval", &Interval::emptyInterval)
		.def_static("zeroInterval", &Interval::zeroInterval)

		// TODO: does not work :-(
		//.def_property("lower", &Interval::lower, &Interval::setLower)
		.def("lower", &Interval::lower, py::return_value_policy::reference_internal)
		.def("setLower", &Interval::setLower)
		.def("upper", &Interval::upper, py::return_value_policy::reference_internal)
		.def("setUpper", &Interval::setUpper)
		
		.def("isInfinite", &Interval::isInfinite)
		.def("isUnbounded", &Interval::isUnbounded)
		.def("isHalfBounded", &Interval::isHalfBounded)
		.def("isEmpty", &Interval::isEmpty)
		.def("isPointInterval", &Interval::isPointInterval)
		.def("isOpenInterval", &Interval::isOpenInterval)
		.def("isClosedInterval", &Interval::isClosedInterval)
		.def("isZero", &Interval::isZero)
		.def("isOne", &Interval::isOne)
		.def("isPositive", &Interval::isPositive)
		.def("isNegative", &Interval::isNegative)
		.def("isSemiPositive", &Interval::isSemiPositive)
		.def("isSemiNegative", &Interval::isSemiNegative)
		
		.def("integralPart", &Interval::integralPart)
		.def("diameter", &Interval::diameter)
		.def("center", [](const Interval& i){ return i.center(); })
		.def("sample", &Interval::sample)
		.def("contains", [](const Interval& i, const Number& r){ return i.contains(r); })
		.def("contains", [](const Interval& i, const Interval& i2){ return i.contains(i2); })
		.def("meets", &Interval::meets)
		.def("isSubset", &Interval::isSubset)
		.def("isProperSubset", &Interval::isProperSubset)
		
		.def("div", &Interval::div)
		
		.def("inverse", &Interval::inverse)
		.def("abs", &Interval::abs)
		.def("__pow__", [](const Interval& i, carl::uint exp) { return i.pow(exp); })
		.def("intersectsWith", &Interval::intersectsWith)
		.def("intersect", &Interval::intersect)
		.def("unite", &Interval::unite)
		.def("difference", &Interval::difference)
		.def("complement", &Interval::complement)
		.def("symmetricDifference", &Interval::symmetricDifference)
		
		.def(py::self + py::self)
		.def(Number() + py::self)
		.def(py::self + Number())
		.def(py::self += py::self)
		.def(py::self += Number())
		
		.def(-py::self)
		
		.def(py::self - py::self)
		.def(Number() - py::self)
		.def(py::self - Number())
		.def(py::self -= py::self)
		.def(py::self -= Number())
		
		.def(py::self * py::self)
		.def(Number() * py::self)
		.def(py::self * Number())
		.def(py::self *= py::self)
		.def(py::self *= Number())
		
		.def(py::self / Number())
		.def(py::self /= Number())
		
		.def(py::self == py::self)
		.def(py::self != py::self)
		.def(py::self <= py::self)
		.def(py::self <= Number())
		.def(Number() <= py::self)
		.def(py::self >= py::self)
		.def(py::self >= Number())
		.def(Number() >= py::self)
		.def(py::self < py::self)
		.def(py::self < Number())
		.def(Number() < py::self)
		.def(py::self > py::self)
		.def(py::self > Number())
		.def(Number() > py::self)
		
		.def("__str__", &streamToString<Interval>)
		.def("__repr__", [](const Interval& i) { return "<Interval " + streamToString<Interval>(i) + ">"; })
        .def(py::pickle(
                [](const Interval& val) -> std::tuple<std::string> {
                    throw NoPickling();
                },
                [](const std::tuple<std::string>& data) -> Interval {
                    throw NoPickling();
                }
            ))
	;
	
	m.def("isInteger", [](const Interval& i){ return carl::isInteger(i); });
	m.def("div", [](const Interval& l, const Interval& r){ return carl::div(l, r); });
	m.def("quotient", [](const Interval& l, const Interval& r){ return carl::quotient(l, r); });
	m.def("abs", [](const Interval& i){ return carl::abs(i); });
	m.def("pow", [](const Interval& i, carl::uint exp){ return carl::pow(i, exp); });
	m.def("floor", [](const Interval& i){ return carl::floor(i); });
	m.def("ceil", [](const Interval& i){ return carl::ceil(i); });
}

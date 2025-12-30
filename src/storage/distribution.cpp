#include "distribution.h"
#include "src/helpers.h"

#include "storm/adapters/IntervalAdapter.h"
#include "storm/adapters/RationalNumberAdapter.h"
#include "storm/storage/Distribution.h"

template<typename ValueType>
void define_distribution(py::module& m, std::string vt_suffix) {
    using Distrib = storm::storage::Distribution<ValueType, uint_fast64_t>;

    std::string distributionClassName = std::string("Distribution") + vt_suffix;
    py::class_<Distrib> distribution(m, distributionClassName.c_str(), "Finite Support Distribution");
    distribution
            .def("__str__", &streamToString<Distrib>);
}


template void define_distribution<double>(py::module&, std::string vt_suffix);
template void define_distribution<storm::RationalNumber>(py::module&, std::string vt_suffix);
template void define_distribution<storm::Interval>(py::module&, std::string vt_suffix);

#include "kwekMehlhorn.h"

#include <storm/adapters/RationalNumberAdapter.h>
#include <storm/utility/KwekMehlhorn.h>

#include "src/common.h"

template<typename RationalValueType>
void define_kwek_mehlhorn(py::module &m) {
    m.def("sharpen", py::overload_cast<uint64_t, double const &>(&storm::utility::kwek_mehlhorn::sharpen<RationalValueType, double>),
          "Convert a float to the nearest rational within precision using Kwek "
          "Mehlhorn",
          py::arg("precision"), py::arg("value"));
}

template void define_kwek_mehlhorn<storm::RationalNumber>(py::module &m);
#include "kwekMehlhorn.h"
#include "src/common.h"
#include <pybind11/pybind11.h>
#include <storm/adapters/RationalNumberAdapter.h>
#include <storm/utility/KwekMehlhorn.h>

template <typename RationalValueType>
void define_kwek_mehlhorn(py::module &m, std::string const &vtSuffix) {
  m.def(
      "sharpen",
      [](uint64_t precision, double value) {
        return storm::utility::kwek_mehlhorn::sharpen<RationalValueType,
                                                      double>(precision, value);
      },
      "Convert a float to the nearest rational within precision using Kwek "
      "Mehlhorn",
      py::arg("precision"), py::arg("value"));
}

template void
define_kwek_mehlhorn<storm::RationalNumber>(py::module &m,
                                            std::string const &vtSuffix);
#include "chrono.h"

#include <chrono>

#include "src/helpers.h"

void define_chrono(py::module& m) {
    py::classh<std::chrono::milliseconds>(m, "milliseconds")
        .def("count", &std::chrono::milliseconds::count)
        .def("__str__", [](std::chrono::milliseconds const& t) { return std::to_string(t.count()); });
}
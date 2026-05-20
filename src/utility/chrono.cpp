#include "chrono.h"
#include "src/helpers.h"

#include <chrono>

void define_chrono(py::module& m) {
    py::class_<std::chrono::milliseconds>(m, "milliseconds")
        .def("count", &std::chrono::milliseconds::count)
        .def("__str__", [](std::chrono::milliseconds const& t) {
            std::stringstream strstr;
            strstr << t.count();
            return strstr.str();
        });
}
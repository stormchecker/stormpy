#include "factorization.h"

#include "src/pycarl/types.h"
#include "src/pycarl/helpers.h"


void define_factorizationcache(py::module& m) {
    py::class_<carl::Cache<FactorizationPair>, std::shared_ptr<carl::Cache<FactorizationPair>>>(m, "_FactorizationCache", "Cache storing all factorized polynomials")
        .def(py::init(), "Constructor")
        .def(py::pickle(
                [](const carl::Cache<FactorizationPair>& val) -> std::tuple<std::string> {
                    throw NoPickling();
                },
                [](const std::tuple<std::string>& data) -> std::shared_ptr<carl::Cache<FactorizationPair>> {
                    throw NoPickling();
                }
            ))
    ;
}

void define_factorization(py::module& m) {
    py::class_<Factorization, std::shared_ptr<Factorization>>(m, "Factorization", "Factorization")
        .def("__str__", &streamToString<Factorization>)
        .def(py::self == py::self)

        .def("__len__", [](const Factorization& f) {
                return f.size();
            })
        .def("__iter__", [](const Factorization& f) {
                return py::make_iterator(f.begin(), f.end());
            }, py::keep_alive<0, 1>() /* Essential: keep object alive while iterator exists */)

        .def(py::pickle(
                [](const Factorization& val) -> std::tuple<std::string> {
                    throw NoPickling();
                },
                [](const std::tuple<std::string>& data) -> Factorization {
                    throw NoPickling();
                }
            ))
    ;
}

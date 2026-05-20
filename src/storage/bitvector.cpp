#include "bitvector.h"
#include "src/helpers.h"
#include "storm/storage/BitVector.h"

void define_bitvector(py::module& m) {
    using BitVector = storm::storage::BitVector;

    py::class_<BitVector>(m, "BitVector")
        .def(py::init<>())
        .def(py::init<BitVector>(), "other"_a)
        .def(py::init<uint_fast64_t>(), "length"_a)
        .def(py::init<uint_fast64_t, bool>(), "length"_a, "init"_a)
        .def(py::init<uint_fast64_t, std::vector<uint_fast64_t>>(), "length"_a, "set_entries"_a)

        .def("size", &BitVector::size)
        .def("number_of_set_bits", &BitVector::getNumberOfSetBits)
        //.def("get", &BitVector::get, "index"_a) // no idea why this does not work
        .def(
            "get", [](BitVector const& b, uint_fast64_t i) { return b.get(i); }, "index"_a)
        .def(
            "set", [](BitVector& b, uint_fast64_t i, bool v) { b.set(i, v); }, py::arg("index"), py::arg("value") = true, "Set")
        .def("as_int", &BitVector::getAsInt, py::arg("index"), py::arg("no_bits"), "Get as unsigned int")

        .def("__len__", [](BitVector const& b) { return b.size(); })
        .def("__getitem__",
             [](BitVector const& b, uint_fast64_t i) {
                 if (i >= b.size())
                     throw py::index_error();
                 return b.get(i);
             })
        .def("__setitem__", [](BitVector& b, uint_fast64_t i, bool v) { b.set(i, v); })

        .def(
            "__iter__", [](const BitVector& b) { return py::make_iterator(b.begin(), b.end()); },
            py::keep_alive<0, 1>() /* Essential: keep object alive while iterator exists */)

        .def("store_as_string",
             [](const BitVector& bv) {
                 std::stringstream strs;
                 bv.store(strs);
                 return strs.str();
             })
        .def_static("load_from_string", &BitVector::load, py::arg("description"))
        .def(py::self == py::self)
        .def(py::self != py::self)

        .def(py::self < py::self)
        .def(py::self & py::self)
        .def(py::self | py::self)
        .def(py::self ^ py::self)
        .def(py::self % py::self)
        .def(~py::self)

        .def(py::self &= py::self)
        .def(py::self |= py::self)

        .def("__str__", &streamToString<BitVector>)
        .def("__hash__", [](const BitVector& b) { return storm::storage::Murmur3BitVectorHash<uint64_t>()(b); });
}

#include "bitvector.h"

#include <storm/storage/BitVector.h>

#include "src/helpers.h"

void define_bitvector(py::module& m) {
    using BitVector = storm::storage::BitVector;

    py::class_<BitVector>(m, "BitVector")
        .def(py::init<>())
        .def(py::init<BitVector>(), "other"_a)
        .def(py::init<uint_fast64_t>(), "length"_a)
        .def(py::init<uint_fast64_t, bool>(), "length"_a, "init"_a)
        .def(py::init<uint_fast64_t, std::vector<uint_fast64_t>>(), "length"_a, "set_entries"_a)

        .def("size", &BitVector::size)
        .def("number_of_set_bits", &BitVector::getNumberOfSetBits, "Get the number of bits that are set to true in this bit vector")
        .def(
            "get", [](BitVector const& b, uint_fast64_t i) { return b.get(i); }, "index"_a)
        .def(
            "set", [](BitVector& b, uint_fast64_t i, bool v) { b.set(i, v); }, py::arg("index"), py::arg("value") = true, "Set")
        .def("as_int", &BitVector::getAsInt, py::arg("index"), py::arg("no_bits"), "Get as unsigned int")
        .def("resize", &BitVector::resize, py::arg("new_size"), py::arg("init") = false, "Resize the bitvector to the given new_size")
        .def("complement", &BitVector::complement, "Complement the bitvector")
        .def("increment", &BitVector::increment, "Increment the bitvector as if it was a binary number")
        .def("is_subset_of", &BitVector::isSubsetOf, py::arg("other"), "Check if this bitvector is a subset of another")
        .def("is_disjoint_from", &BitVector::isDisjointFrom, py::arg("other"), "Check if this bitvector is disjoint from another")
        .def("empty", &BitVector::empty, "Check if the bitvector is empty (no bits set)")
        .def("full", &BitVector::full, "Check if the bitvector is full (all bits set)")
        .def("clear", &BitVector::clear, "Clear all bits in the bitvector")
        .def("fill", &BitVector::fill, "Fill all bits in the bitvector")
        .def("number_of_set_bits_before_index", &BitVector::getNumberOfSetBitsBeforeIndex, py::arg("index"),
             "Get the number of bits that are set to true before the given index")
        .def("has_unique_set_bit", &BitVector::hasUniqueSetBit, "Check if the bitvector has a unique set bit")
        .def("get_next_set_index", &BitVector::getNextSetIndex, py::arg("starting_index"), "Get the index of the next set bit after the given starting index")
        .def("get_next_unset_index", &BitVector::getNextUnsetIndex, py::arg("starting_index"),
             "Get the index of the next unset bit after the given starting index")

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

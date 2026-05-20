#include "memory.h"
#include <storm-pomdp/storage/PomdpMemory.h>
#include "src/helpers.h"

void define_memory(py::module& m) {
    py::class_<storm::storage::PomdpMemory> memory(m, "PomdpMemory", "Memory for POMDP policies");
    memory.def_property_readonly("nr_states", &storm::storage::PomdpMemory::getNumberOfStates, "How many states does the memory structure have");

    // Trivial, FixedCounter, SelectiveCounter, FixedRing, SelectiveRing, SettableBits, Full
    py::enum_<storm::storage::PomdpMemoryPattern>(m, "PomdpMemoryPattern", "Memory pattern for POMDP memory")
        .value("trivial", storm::storage::PomdpMemoryPattern::Trivial)
        .value("fixed_counter", storm::storage::PomdpMemoryPattern::FixedCounter)
        .value("selective_counter", storm::storage::PomdpMemoryPattern::SelectiveCounter)
        .value("fixed_ring", storm::storage::PomdpMemoryPattern::FixedRing)
        .value("selective_ring", storm::storage::PomdpMemoryPattern::SelectiveRing)
        .value("settable_bits", storm::storage::PomdpMemoryPattern::SettableBits)
        .value("full", storm::storage::PomdpMemoryPattern::Full);

    py::class_<storm::storage::PomdpMemoryBuilder> memorybuilder(m, "PomdpMemoryBuilder", "MemoryBuilder for POMDP policies");
    memorybuilder.def(py::init<>());
    memorybuilder.def("build", &storm::storage::PomdpMemoryBuilder::build, py::arg("pattern"), py::arg("nr_states"));
}
#include "memory.h"

#include <storm-pomdp/storage/PomdpMemory.h>

#include "src/helpers.h"

void define_memory(py::module& m) {
    py::classh<storm::storage::PomdpMemory> memory(m, "PomdpMemory", "Memory for POMDP policies");
    memory.def_property_readonly("nr_states", &storm::storage::PomdpMemory::getNumberOfStates, "How many states does the memory structure have");

    py::native_enum<storm::storage::PomdpMemoryPattern>(m, "PomdpMemoryPattern", "enum.Enum", "Memory pattern for POMDP memory")
        .value("TRIVIAL", storm::storage::PomdpMemoryPattern::Trivial)
        .value("FIXED_COUNTER", storm::storage::PomdpMemoryPattern::FixedCounter)
        .value("SELECTIVE_COUNTER", storm::storage::PomdpMemoryPattern::SelectiveCounter)
        .value("FIXED_RING", storm::storage::PomdpMemoryPattern::FixedRing)
        .value("SELECTIVE_RING", storm::storage::PomdpMemoryPattern::SelectiveRing)
        .value("SETTABLE_BITS", storm::storage::PomdpMemoryPattern::SettableBits)
        .value("FULL", storm::storage::PomdpMemoryPattern::Full)
        .finalize();

    py::classh<storm::storage::PomdpMemoryBuilder> memorybuilder(m, "PomdpMemoryBuilder", "MemoryBuilder for POMDP policies");
    memorybuilder.def(py::init<>());
    memorybuilder.def("build", &storm::storage::PomdpMemoryBuilder::build, py::arg("pattern"), py::arg("nr_states"));
}

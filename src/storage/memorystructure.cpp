#include "memorystructure.h"

#include <storm/adapters/IntervalAdapter.h>
#include <storm/adapters/RationalFunctionAdapter.h>
#include <storm/storage/memorystructure/MemoryStructure.h>
#include <storm/storage/memorystructure/MemoryStructureBuilder.h>
#include <storm/storage/memorystructure/SparseModelMemoryProduct.h>
#include <storm/storage/memorystructure/SparseModelMemoryProductReverseData.h>

#include "src/binding_type_index.h"

template<typename ValueType>
void define_memorystructure_product_each(py::classh<storm::storage::MemoryStructure>& memoryStructure,
                                         py::classh<storm::storage::SparseModelMemoryProductReverseData>& reverseData) {
    memoryStructure.def(
        "product_model",
        [](storm::storage::MemoryStructure& ms, storm::models::sparse::Model<ValueType> const& sparseModel) { return ms.product(sparseModel); },
        py::arg("model"), py::keep_alive<0, 1>(), py::keep_alive<0, 2>() /* Product keeps references to memory structure and model */);
    reverseData.def("create_memory_scheduler_from_product_scheduler",
                    &storm::storage::SparseModelMemoryProductReverseData::createMemorySchedulerFromProductScheduler<ValueType>, py::arg("product_scheduler"));
}

void define_memorystructure_untyped(py::module& m) {
    typedef storm::storage::MemoryStructure MemoryStructure;
    py::classh<MemoryStructure> memoryStructure(m, "MemoryStructure", "Finite memory states, labels and transitions used by a scheduler");
    memoryStructure.def("product", [](MemoryStructure& ms, MemoryStructure const& memModel) { return ms.product(memModel); });
    memoryStructure.def_property_readonly("nr_states", &MemoryStructure::getNumberOfStates);
    memoryStructure.def_property_readonly("state_labeling", &MemoryStructure::getStateLabeling);

    py::classh<storm::storage::SparseModelMemoryProductReverseData> memoryProductReverseData(m, "SparseModelMemoryProductReverseData",
                                                                                             "Maps schedulers on a memory product back to the original model");
    define_memorystructure_product_each<double>(memoryStructure, memoryProductReverseData);
    define_memorystructure_product_each<storm::RationalNumber>(memoryStructure, memoryProductReverseData);
    define_memorystructure_product_each<storm::RationalFunction>(memoryStructure, memoryProductReverseData);
}

template<typename ValueType>
void define_memorystructure_typed(py::module& m) {
    typedef storm::storage::MemoryStructureBuilder<ValueType> MemoryStructureBuilder;
    auto const index = stormpy::bindings::typeIndex<ValueType>();
    auto msb = stormpy::bindings::bindTemplateClass<MemoryStructureBuilder>(m, "MemoryStructureBuilder", index, "Memory structure builder");
    msb.def(py::init<uint_fast64_t, storm::models::sparse::Model<ValueType> const&, bool>(), py::arg("nr_memory_states"), py::arg("model"),
            py::arg("only_initial_states_relevant") = true, py::keep_alive<1, 3>());
    msb.def("build", &MemoryStructureBuilder::build);
    msb.def("set_label", &MemoryStructureBuilder::setLabel, py::arg("state"), py::arg("label"));
    msb.def("set_transition", &MemoryStructureBuilder::setTransition, py::arg("start_state"), py::arg("goal_state"), py::arg("model_states"),
            py::arg("model_choices") = boost::none);
    msb.def("set_initial_memory_state", &MemoryStructureBuilder::setInitialMemoryState, py::arg("state"), py::arg("value"));

    typedef storm::storage::SparseModelMemoryProduct<ValueType> MemoryStructureProduct;
    auto msp = stormpy::bindings::bindTemplateClass<MemoryStructureProduct>(m, "MemoryStructureProduct", index, "Memory structure product");
    msp.def("build", &MemoryStructureProduct::build, py::arg("preserve_model_type") = false);
    msp.def("set_build_full_product", &MemoryStructureProduct::setBuildFullProduct,
            "Enforces that every state is considered reachable and thus constructed. This causes the product to have the size of the product of the original "
            "model and the memory structure.");
}

template void define_memorystructure_typed<double>(py::module& m);
template void define_memorystructure_typed<storm::RationalNumber>(py::module& m);
template void define_memorystructure_typed<storm::Interval>(py::module& m);
template void define_memorystructure_typed<storm::RationalInterval>(py::module& m);
template void define_memorystructure_typed<storm::RationalFunction>(py::module& m);

#include "memorystructure.h"
#include <storm/adapters/RationalFunctionAdapter.h>
#include <storm/adapters/IntervalAdapter.h>
#include <storm/storage/memorystructure/MemoryStructure.h>
#include <storm/storage/memorystructure/MemoryStructureBuilder.h>
#include <storm/storage/memorystructure/SparseModelMemoryProduct.h>


void define_memorystructure_untyped(py::module& m) {
    typedef storm::storage::MemoryStructure MemoryStructure;
    py::class_<MemoryStructure, std::shared_ptr<MemoryStructure>> memoryStructure(m, "MemoryStructure");
    memoryStructure.def("product",  [](MemoryStructure& ms, MemoryStructure const& memModel) {return ms.product(memModel);});
    memoryStructure.def("_product_model_double", [](MemoryStructure& ms, storm::models::sparse::Model<double> const& sparseModel) {return ms.product(sparseModel);});
    memoryStructure.def("_product_model_exact", [](MemoryStructure& ms, storm::models::sparse::Model<storm::RationalNumber> const& sparseModel) {return ms.product(sparseModel);});
    memoryStructure.def("_product_model_parametric", [](MemoryStructure& ms, storm::models::sparse::Model<storm::RationalFunction> const& sparseModel) {return ms.product(sparseModel);});
    memoryStructure.def_property_readonly("nr_states", &MemoryStructure::getNumberOfStates);
    memoryStructure.def_property_readonly("state_labeling", &MemoryStructure::getStateLabeling);
}

template<typename VT>
void define_memorystructure_typed(py::module& m, std::string const& vtSuffix) {
    typedef storm::storage::MemoryStructureBuilder<VT> MemoryStructureBuilder;
    py::class_<MemoryStructureBuilder, std::shared_ptr<MemoryStructureBuilder>> msb(m, ("MemoryStructureBuilder" + vtSuffix).c_str());
    msb.def(py::init<uint_fast64_t, storm::models::sparse::Model<VT> const&, bool>(),  py::arg("nr_memory_states"), py::arg("model"), py::arg("only_initial_states_relevant")=true);
    msb.def("build", &MemoryStructureBuilder::build);
    msb.def("set_label", &MemoryStructureBuilder::setLabel, py::arg("state"), py::arg("label"));
    msb.def("set_transition", &MemoryStructureBuilder::setTransition, py::arg("start_state"), py::arg("goal_state"), py::arg("model_states"), py::arg("model_choices")=boost::none);
    msb.def("set_initial_memory_state", &MemoryStructureBuilder::setInitialMemoryState, py::arg("state"), py::arg("value"));

    typedef storm::storage::SparseModelMemoryProduct<VT> MemoryStructureProduct;
    py::class_<MemoryStructureProduct, std::shared_ptr<MemoryStructureProduct>> msp(m, ("MemoryStructureProduct" + vtSuffix).c_str());
    msp.def("build", &MemoryStructureProduct::build, py::arg("preserve_model_type") = false);
    msp.def("set_build_full_product", &MemoryStructureProduct::setBuildFullProduct, "Enforces that every state is considered reachable and thus constructed. This causes the product to have the size of the product of the original model and the memory structure.");
}

template void define_memorystructure_typed<double>(py::module& m, std::string const& vt_suffix);
template void define_memorystructure_typed<storm::RationalNumber>(py::module& m, std::string const& vt_suffix);
template void define_memorystructure_typed<storm::Interval>(py::module& m, std::string const& vt_suffix);
template void define_memorystructure_typed<storm::RationalFunction>(py::module& m, std::string const& vt_suffix);

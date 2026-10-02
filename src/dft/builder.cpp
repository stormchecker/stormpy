#include "builder.h"

#include <storm-dft/builder/ExplicitDFTModelBuilder.h>
#include <storm-dft/environment/DftEnvironment.h>
#include <storm-dft/environment/ModelBuilderEnvironment.h>
#include <storm-dft/storage/DftSymmetries.h>
#include <storm-dft/utility/RelevantEvents.h>
#include <storm/adapters/RationalFunctionAdapter.h>

#include "src/binding_type_index.h"

template<typename ValueType>
using ExplicitDFTModelBuilder = storm::dft::builder::ExplicitDFTModelBuilder<ValueType>;

// Thin wrapper for building state space from DFT
template<typename ValueType>
std::shared_ptr<storm::models::sparse::Model<ValueType>> buildModel(storm::dft::DftEnvironment const& env, storm::dft::storage::DFT<ValueType> const& dft,
                                                                    storm::dft::storage::DftSymmetries const& symmetries,
                                                                    storm::dft::utility::RelevantEvents const& relevantEvents) {
    dft.setRelevantEvents(relevantEvents, env.modelBuilder().isAllowDCForRelevantEvents());
    storm::dft::builder::ExplicitDFTModelBuilder<ValueType> builder(env, dft, symmetries);
    builder.buildModel(0, 0.0);
    return builder.getModel();
}

void define_builder(py::module& m) {
    py::native_enum<storm::dft::builder::ApproximationHeuristic>(m, "ApproximationHeuristic", "enum.Enum", "Heuristic for selecting states to explore next")
        .value("DEPTH", storm::dft::builder::ApproximationHeuristic::DEPTH)
        .value("PROBABILITY", storm::dft::builder::ApproximationHeuristic::PROBABILITY)
        .value("BOUND_DIFFERENCE", storm::dft::builder::ApproximationHeuristic::BOUNDDIFFERENCE)
        .finalize();
}

template<typename ValueType>
void define_builder_typed(py::module& m) {
    auto builder = stormpy::bindings::bindTemplateClass<ExplicitDFTModelBuilder<ValueType>>(
        m, "ExplicitDFTModelBuilder", stormpy::bindings::typeIndex<ValueType>(), "Builder to generate explicit model from DFT");
    builder
        .def(py::init<storm::dft::DftEnvironment const&, storm::dft::storage::DFT<ValueType> const&, storm::dft::storage::DftSymmetries const&>(),
             py::keep_alive<1, 2>(), py::keep_alive<1, 3>(), "Constructor", py::arg("env"), py::arg("dft"), py::arg("symmetries"))
        .def("build", &ExplicitDFTModelBuilder<ValueType>::buildModel, "Build state space of model", py::arg("iteration"),
             py::arg("approximation_threshold") = 0.0, py::arg("approximation_heuristic") = storm::dft::builder::ApproximationHeuristic::DEPTH)
        .def("get_model", &ExplicitDFTModelBuilder<ValueType>::getModel, "Get complete model")
        .def("get_partial_model", &ExplicitDFTModelBuilder<ValueType>::getModelApproximation, "Get partial model", py::arg("lower_bound"),
             py::arg("expected_time"));

    m.def("build_model", &buildModel<ValueType>, "Build state-space model (CTMC or MA) for DFT", py::arg("env"), py::arg("dft"), py::arg("symmetries"),
          py::arg("relevant_events"));
}

template void define_builder_typed<double>(py::module& m);
template void define_builder_typed<storm::RationalFunction>(py::module& m);

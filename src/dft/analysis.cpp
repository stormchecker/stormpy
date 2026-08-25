#include "analysis.h"

#include <storm-dft/builder/ExplicitDFTModelBuilder.h>
#include <storm-dft/parser/DFTJsonParser.h>
#include <storm-dft/storage/DftSymmetries.h>
#include <storm/adapters/RationalFunctionAdapter.h>

#include "src/binding_type_index.h"

template<typename ValueType>
using ExplicitDFTModelBuilder = storm::dft::builder::ExplicitDFTModelBuilder<ValueType>;

// Thin wrapper for DFT analysis
template<typename ValueType>
std::vector<ValueType> analyzeDFT(storm::dft::storage::DFT<ValueType> const& dft, std::vector<std::shared_ptr<storm::logic::Formula const>> const& properties,
                                  bool symred, bool allowModularisation, storm::dft::utility::RelevantEvents const& relevantEvents, bool allowDCForRelevant) {
    typename storm::dft::modelchecker::DFTModelChecker<ValueType>::dft_results dftResults = storm::dft::api::analyzeDFT(
        dft, properties, symred, allowModularisation, relevantEvents, allowDCForRelevant, 0.0, storm::dft::builder::ApproximationHeuristic::DEPTH, false);

    std::vector<ValueType> results;
    for (auto result : dftResults) {
        results.push_back(boost::get<ValueType>(result));
    }
    return results;
}

// Thin wrapper for building state space from DFT
template<typename ValueType>
std::shared_ptr<storm::models::sparse::Model<ValueType>> buildModel(storm::dft::storage::DFT<ValueType> const& dft,
                                                                    storm::dft::storage::DftSymmetries const& symmetries,
                                                                    storm::dft::utility::RelevantEvents const& relevantEvents, bool allowDCForRelevant) {
    dft.setRelevantEvents(relevantEvents, allowDCForRelevant);
    storm::dft::builder::ExplicitDFTModelBuilder<ValueType> builder(dft, symmetries);
    builder.buildModel(0, 0.0);
    return builder.getModel();
}

// Define python bindings
void define_analysis(py::module& m) {
    py::native_enum<storm::dft::builder::ApproximationHeuristic>(m, "ApproximationHeuristic", "enum.Enum", "Heuristic for selecting states to explore next")
        .value("DEPTH", storm::dft::builder::ApproximationHeuristic::DEPTH)
        .value("PROBABILITY", storm::dft::builder::ApproximationHeuristic::PROBABILITY)
        .value("BOUNDDIFFERENCE", storm::dft::builder::ApproximationHeuristic::BOUNDDIFFERENCE)
        .finalize();

    // RelevantEvents
    py::class_<storm::dft::utility::RelevantEvents, std::shared_ptr<storm::dft::utility::RelevantEvents>>(m, "RelevantEvents",
                                                                                                          "Relevant events which should be observed")
        .def(py::init<>(), "Create empty list of relevant events")
        .def("is_relevant", &storm::dft::utility::RelevantEvents::isRelevant, "Check whether the given name is a relevant event", py::arg("name"));

    m.def("compute_relevant_events", &storm::dft::api::computeRelevantEvents, "Compute relevant event ids from properties and additional relevant names",
          py::arg("properties"), py::arg("additional_relevant_names") = std::vector<std::string>());
}

template<typename ValueType>
void define_analysis_typed(py::module& m) {
    auto builder = stormpy::bindings::bindTemplateClass<ExplicitDFTModelBuilder<ValueType>, std::shared_ptr<ExplicitDFTModelBuilder<ValueType>>>(
        m, "ExplicitDFTModelBuilder", stormpy::bindings::typeIndex<ValueType>(), "Builder to generate explicit model from DFT");
    builder
        .def(py::init<storm::dft::storage::DFT<ValueType> const&, storm::dft::storage::DftSymmetries const&>(), "Constructor", py::arg("dft"),
             py::arg("symmetries") = storm::dft::storage::DftSymmetries())
        .def("build", &ExplicitDFTModelBuilder<ValueType>::buildModel, "Build state space of model", py::arg("iteration"),
             py::arg("approximation_threshold") = 0.0, py::arg("approximation_heuristic") = storm::dft::builder::ApproximationHeuristic::DEPTH)
        .def("get_model", &ExplicitDFTModelBuilder<ValueType>::getModel, "Get complete model")
        .def("get_partial_model", &ExplicitDFTModelBuilder<ValueType>::getModelApproximation, "Get partial model", py::arg("lower_bound"),
             py::arg("expected_time"));

    m.def("analyze_dft", &analyzeDFT<ValueType>, "Analyze the DFT", py::arg("dft"), py::arg("properties"), py::arg("symred") = true,
          py::arg("allow_modularisation") = false, py::arg("relevant_events") = storm::dft::utility::RelevantEvents(),
          py::arg("allow_dc_for_relevant") = false);

    m.def("build_model", &buildModel<ValueType>, "Build state-space model (CTMC or MA) for DFT", py::arg("dft"),
          py::arg("symmetries") = storm::dft::storage::DftSymmetries(), py::arg("relevant_events") = storm::dft::utility::RelevantEvents(),
          py::arg("allow_dc_for_relevant") = false);

    m.def("transform_dft", &storm::dft::api::applyTransformations<ValueType>, "Apply transformations on DFT", py::arg("dft"), py::arg("unique_constant_be"),
          py::arg("binary_fdeps"), py::arg("exponential_distributions"));

    m.def("compute_dependency_conflicts", &storm::dft::api::computeDependencyConflicts<ValueType>, "Set conflicts between FDEPs. Is used in analysis.",
          py::arg("dft"), py::arg("use_smt") = false, py::arg("solver_timeout") = 0);

    m.def("is_well_formed", &storm::dft::api::isWellFormed<ValueType>, "Check whether DFT is well-formed.", py::arg("dft"),
          py::arg("check_valid_for_analysis") = true);
    m.def("has_potential_modeling_issues", &storm::dft::api::hasPotentialModelingIssues<ValueType>, "Check whether DFT has potential modeling issues.",
          py::arg("dft"));
}

template void define_analysis_typed<double>(py::module& m);
template void define_analysis_typed<storm::RationalFunction>(py::module& m);

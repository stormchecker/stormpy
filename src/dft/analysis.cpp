#include "analysis.h"

#include "storm-dft/parser/DFTJsonParser.h"
#include "storm-dft/builder/ExplicitDFTModelBuilder.h"
#include "storm-dft/storage/DftSymmetries.h"

template<typename ValueType> using ExplicitDFTModelBuilder = storm::dft::builder::ExplicitDFTModelBuilder<ValueType>;

// Thin wrapper for DFT analysis
template<typename ValueType>
std::vector<ValueType> analyzeDFT(storm::dft::storage::DFT<ValueType> const& dft, std::vector<std::shared_ptr<storm::logic::Formula const>> const& properties, bool symred, bool allowModularisation, storm::dft::utility::RelevantEvents const& relevantEvents, bool allowDCForRelevant) {
    typename storm::dft::modelchecker::DFTModelChecker<ValueType>::dft_results dftResults = storm::dft::api::analyzeDFT(dft, properties, symred, allowModularisation, relevantEvents, allowDCForRelevant, 0.0, storm::dft::builder::ApproximationHeuristic::DEPTH, false);

    std::vector<ValueType> results;
    for (auto result : dftResults) {
        results.push_back(boost::get<ValueType>(result));
    }
    return results;
}

// Thin wrapper for building state space from DFT
template<typename ValueType>
std::shared_ptr<storm::models::sparse::Model<ValueType>> buildModel(storm::dft::storage::DFT<ValueType> const& dft, storm::dft::storage::DftSymmetries const& symmetries, storm::dft::utility::RelevantEvents const& relevantEvents, bool allowDCForRelevant) {
    dft.setRelevantEvents(relevantEvents, allowDCForRelevant);
    storm::dft::builder::ExplicitDFTModelBuilder<ValueType> builder(dft, symmetries);
    builder.buildModel(0, 0.0);
    return builder.getModel();
}

// Define python bindings
void define_analysis(py::module& m) {

    py::enum_<storm::dft::builder::ApproximationHeuristic>(m, "ApproximationHeuristic", "Heuristic for selecting states to explore next")
        .value("DEPTH", storm::dft::builder::ApproximationHeuristic::DEPTH)
        .value("PROBABILITY", storm::dft::builder::ApproximationHeuristic::PROBABILITY)
        .value("BOUNDDIFFERENCE", storm::dft::builder::ApproximationHeuristic::BOUNDDIFFERENCE)
    ;

    // RelevantEvents
    py::class_<storm::dft::utility::RelevantEvents, std::shared_ptr<storm::dft::utility::RelevantEvents>>(m, "RelevantEvents", "Relevant events which should be observed")
        .def(py::init<>(), "Create empty list of relevant events")
        .def("is_relevant", &storm::dft::utility::RelevantEvents::isRelevant, "Check whether the given name is a relevant event", py::arg("name"))
    ;

    m.def("compute_relevant_events", &storm::dft::api::computeRelevantEvents, "Compute relevant event ids from properties and additional relevant names", py::arg("properties"), py::arg("additional_relevant_names") = std::vector<std::string>());
}

template<typename ValueType>
void define_analysis_typed(py::module& m, std::string const& vt_suffix) {

    py::class_<ExplicitDFTModelBuilder<ValueType>, std::shared_ptr<ExplicitDFTModelBuilder<ValueType>>>(m, ("ExplicitDFTModelBuilder"+vt_suffix).c_str(), "Builder to generate explicit model from DFT")
        .def(py::init<storm::dft::storage::DFT<ValueType> const&, storm::dft::storage::DftSymmetries const&>(), "Constructor", py::arg("dft"), py::arg("symmetries")=storm::dft::storage::DftSymmetries())
        .def("build", &ExplicitDFTModelBuilder<ValueType>::buildModel, "Build state space of model", py::arg("iteration"), py::arg("approximation_threshold")=0.0, py::arg("approximation_heuristic")=storm::dft::builder::ApproximationHeuristic::DEPTH)
        .def("get_model", &ExplicitDFTModelBuilder<ValueType>::getModel, "Get complete model")
        .def("get_partial_model", &ExplicitDFTModelBuilder<ValueType>::getModelApproximation, "Get partial model", py::arg("lower_bound"), py::arg("expected_time"))
    ;

    m.def(("_analyze_dft"+vt_suffix).c_str(), &analyzeDFT<ValueType>, "Analyze the DFT", py::arg("dft"), py::arg("properties"), py::arg("symred")=true, py::arg("allow_modularisation")=false, py::arg("relevant_events")=storm::dft::utility::RelevantEvents(), py::arg("allow_dc_for_relevant")=false);

    m.def(("_build_model"+vt_suffix).c_str(), &buildModel<ValueType>, "Build state-space model (CTMC or MA) for DFT", py::arg("dft"), py::arg("symmetries"), py::arg("relevant_events")=storm::dft::utility::RelevantEvents(), py::arg("allow_dc_for_relevant")=false);

    m.def(("_transform_dft"+vt_suffix).c_str(), &storm::dft::api::applyTransformations<ValueType>, "Apply transformations on DFT", py::arg("dft"), py::arg("unique_constant_be"), py::arg("binary_fdeps"), py::arg("exponential_distributions"));

    m.def(("_compute_dependency_conflicts"+vt_suffix).c_str(), &storm::dft::api::computeDependencyConflicts<ValueType>, "Set conflicts between FDEPs. Is used in analysis.", py::arg("dft"), py::arg("use_smt") = false, py::arg("solver_timeout") = 0);

    m.def(("_is_well_formed"+vt_suffix).c_str(), &storm::dft::api::isWellFormed<ValueType>, "Check whether DFT is well-formed.", py::arg("dft"), py::arg("check_valid_for_analysis") = true);
    m.def(("_has_potential_modeling_issues"+vt_suffix).c_str(), &storm::dft::api::hasPotentialModelingIssues<ValueType>, "Check whether DFT has potential modeling issues.", py::arg("dft"));
}


template void define_analysis_typed<double>(py::module& m, std::string const& vt_suffix);
template void define_analysis_typed<storm::RationalFunction>(py::module& m, std::string const& vt_suffix);

#include "api.h"

#include <storm-dft/api/analysis.h>
#include <storm-dft/api/io.h>
#include <storm-dft/api/transformation.h>
#include <storm-dft/environment/DftEnvironment.h>
#include <storm/adapters/RationalFunctionAdapter.h>
#include <storm/utility/ExtendedNumber.h>

// Thin wrapper for DFT analysis
template<typename ValueType>
std::vector<py::object> analyzeDFT(storm::dft::DftEnvironment const& env, storm::dft::storage::DFT<ValueType> const& dft,
                                   std::vector<std::shared_ptr<storm::logic::Formula const>> const& properties,
                                   storm::dft::utility::RelevantEvents const& relevantEvents) {
    using Checker = storm::dft::modelchecker::DFTModelChecker<ValueType>;
    typename Checker::dft_results dftResults = storm::dft::api::analyzeDFT(env, dft, properties, relevantEvents);

    std::vector<py::object> results;

    class AnalysisResultVisitor : public boost::static_visitor<py::object> {
       public:
        py::object operator()(typename Checker::ExtendedValueType const& exact) const {
            return py::cast(storm::utility::narrow<ValueType>(exact));
        }

        py::object operator()(typename Checker::approximation_result const& approx) const {
            return py::cast(std::make_pair(storm::utility::narrow<ValueType>(approx.first), storm::utility::narrow<ValueType>(approx.second)));
        }
    } visitor;
    for (auto const& result : dftResults) {
        results.push_back(boost::apply_visitor(visitor, result));
    }
    return results;
}

void define_api_io_input(py::module& m) {
    // Load DFT input
    m.def("load_dft_galileo_file", &storm::dft::api::loadDFTGalileoFile<double>, "Load DFT from Galileo file", py::arg("path"));
    m.def("load_parametric_dft_galileo_file", &storm::dft::api::loadDFTGalileoFile<storm::RationalFunction>, "Load parametric DFT from Galileo file",
          py::arg("path"));
    // Parse Jani model
    m.def("load_dft_json_file", &storm::dft::api::loadDFTJsonFile<double>, "Load DFT from JSON file", py::arg("path"));
    m.def("load_dft_json_string", &storm::dft::api::loadDFTJsonString<double>, "Load DFT from JSON string", py::arg("json_string"));
    m.def("load_parametric_dft_json_file", &storm::dft::api::loadDFTJsonFile<storm::RationalFunction>, "Load parametric DFT from JSON file", py::arg("path"));
    m.def("load_parametric_dft_json_string", &storm::dft::api::loadDFTJsonString<storm::RationalFunction>, "Load parametric DFT from JSON string",
          py::arg("json_string"));
}

void define_api_io_output(py::module& m) {
    // Export DFT
    m.def("export_dft_json_file", &storm::dft::api::exportDFTToJsonFile<double>, "Export DFT to JSON file", py::arg("dft"), py::arg("path"));
    m.def("export_dft_json_string", &storm::dft::api::exportDFTToJsonString<double>, "Export DFT to JSON string", py::arg("dft"));
    m.def("export_dft_json_file", &storm::dft::api::exportDFTToJsonFile<storm::RationalFunction>, "Export DFT to JSON file", py::arg("dft"), py::arg("path"));
    m.def("export_dft_json_string", &storm::dft::api::exportDFTToJsonString<storm::RationalFunction>, "Export DFT to JSON string", py::arg("dft"));
}

void define_api_analysis(py::module& m) {
    m.def("compute_relevant_events", &storm::dft::api::computeRelevantEvents, "Compute relevant event ids from properties and additional relevant names",
          py::arg("properties"), py::arg("additional_relevant_names") = std::vector<std::string>(), py::arg("add_labels_claiming") = false);
}

template<typename ValueType>
void define_api_analysis_typed(py::module& m) {
    m.def("analyze_dft", &analyzeDFT<ValueType>, "Analyze the DFT", py::arg("env"), py::arg("dft"), py::arg("properties"), py::arg("relevant_events"));
}

template<typename ValueType>
void define_api_transformation_typed(py::module& m) {
    m.def("transform_dft", &storm::dft::api::applyTransformations<ValueType>, "Apply transformations on DFT", py::arg("dft"), py::arg("unique_constant_be"),
          py::arg("binary_fdeps"), py::arg("exponential_distributions"));

    m.def("compute_dependency_conflicts", &storm::dft::api::computeDependencyConflicts<ValueType>, "Set conflicts between FDEPs. Is used in analysis.",
          py::arg("dft"), py::arg("use_smt") = false, py::arg("solver_timeout") = 0);

    m.def("is_well_formed", &storm::dft::api::isWellFormed<ValueType>, "Check whether DFT is well-formed.", py::arg("dft"),
          py::arg("check_valid_for_analysis") = true);
    m.def("has_potential_modeling_issues", &storm::dft::api::hasPotentialModelingIssues<ValueType>, "Check whether DFT has potential modeling issues.",
          py::arg("dft"));
}

template void define_api_analysis_typed<double>(py::module& m);
template void define_api_analysis_typed<storm::RationalFunction>(py::module& m);
template void define_api_transformation_typed<double>(py::module& m);
template void define_api_transformation_typed<storm::RationalFunction>(py::module& m);

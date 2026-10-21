#include "api.h"

#include <storm/adapters/IntervalAdapter.h>
#include <storm/adapters/RationalFunctionAdapter.h>
#include <storm/api/bisimulation.h>
#include <storm/api/builder.h>
#include <storm/api/export.h>
#include <storm/api/properties.h>
#include <storm/api/transformation.h>
#include <storm/api/verification.h>
#include <storm/environment/Environment.h>
#include <storm/generator/NextStateGenerator.h>
#include <storm/io/DirectEncodingExporter.h>
#include <storm/languages/jani/Property.h>
#include <storm/modelchecker/prctl/SparseDtmcPrctlModelChecker.h>
#include <storm/modelchecker/prctl/SparseMdpPrctlModelChecker.h>
#include <storm/models/symbolic/StandardRewardModel.h>

#include "src/binding_type_index.h"
#include "src/numbers.h"

namespace stormpy {

using Formulas = std::vector<std::shared_ptr<storm::logic::Formula const>>;

template<typename ValueType>
using CheckTask = storm::modelchecker::CheckTask<storm::logic::Formula, ValueType>;

void define_api_properties(py::module& m) {
    m.def("substitute_constants_in_properties", &storm::api::substituteConstantsInProperties, "Substitute constants in properties", py::arg("properties"),
          py::arg("substitution"));
}

template<typename ValueType>
void define_api_builder_typed(py::module& m) {
    using ExplorationOptions = typename storm::builder::ExplicitModelBuilder<ValueType>::Options;
    auto const index = stormpy::bindings::typeIndex<ValueType>();

    // Value type cannot be deduced from the arguments -> bind as template function families
    stormpy::bindings::bindTemplateFunction(
        m, "build_sparse_model", index,
        py::overload_cast<storm::languages::SymbolicModelDescription const&, storm::builder::BuilderOptions const&, ExplorationOptions const&>(
            &storm::api::buildSparseModel<ValueType>),
        "Build model in sparse representation", py::arg("model"), py::arg("options"), py::arg("exploration_options") = ExplorationOptions(),
        py::call_guard<py::gil_scoped_release>());
    // Additional overload of the registered instantiation
    stormpy::bindings::bindInternalFunction(
        m, stormpy::bindings::templateClassName("build_sparse_model", index),
        py::overload_cast<storm::languages::SymbolicModelDescription const&, Formulas const&>(&storm::api::buildSparseModel<ValueType>),
        "Build model in sparse representation preserving the given formulas", py::arg("model"), py::arg("formulas"), py::call_guard<py::gil_scoped_release>());
    stormpy::bindings::bindTemplateFunction(m, "make_explicit_model_builder", index, &storm::api::makeExplicitModelBuilder<ValueType>,
                                            "Construct an explicit model builder", py::arg("model"), py::arg("options"), py::arg("action_mask") = nullptr,
                                            py::arg("exploration_options") = ExplorationOptions());

    if constexpr (!storm::IsIntervalType<ValueType>) {
        stormpy::bindings::bindTemplateFunction(m, "build_symbolic_model", index, &storm::api::buildSymbolicModel<storm::dd::DdType::Sylvan, ValueType>,
                                                "Build model in symbolic representation", py::arg("env"), py::arg("model"), py::arg("formulas"),
                                                py::arg("build_full_model") = false, py::arg("apply_maximum_progress") = true, py::arg("fix_deadlocks") = true,
                                                py::call_guard<py::gil_scoped_release>());
    }
}

template<typename ValueType>
void define_api_bisimulation_typed(py::module& m) {
    m.def("perform_bisimulation_minimization", &storm::api::performBisimulationMinimization<ValueType>, "Perform bisimulation minimization on sparse model",
          py::arg("model"), py::arg("formulas") = Formulas(), py::arg("options") = storm::bisimulation::Options());
    m.def("perform_bisimulation_minimization", &storm::api::performBisimulationMinimization<storm::dd::DdType::Sylvan, ValueType, ValueType>,
          "Perform bisimulation minimization on symbolic model", py::arg("model"), py::arg("formulas"),
          py::arg("bisimulation_type") = storm::bisimulation::BisimulationType::Strong, py::arg("mode") = storm::dd::bisimulation::SignatureMode::Eager,
          py::arg("quotient_format") = storm::dd::bisimulation::QuotientFormat::Dd,
          py::arg("bisimulation_options") = storm::dd::bisimulation::BisimulationOptions());
}

template<typename ValueType>
void define_api_export_typed(py::module& m) {
    using Model = std::shared_ptr<storm::models::sparse::Model<ValueType>>;
    m.def("export_sparse_model_as_drn",
          py::overload_cast<Model const&, std::string const&, storm::io::DirectEncodingExporterOptions, std::vector<std::string> const&>(
              &storm::api::exportSparseModelAsDrn<ValueType>),
          "Export sparse model in DRN format", py::arg("model"), py::arg("filename"), py::arg("options"),
          py::arg("parameter_names") = std::vector<std::string>());
}

template<typename ValueType>
void define_api_transformation_typed(py::module& m) {
    m.def("transform_symbolic_to_sparse_model", &storm::api::transformSymbolicToSparseModel<storm::dd::DdType::Sylvan, ValueType>,
          "Transform symbolic model into sparse model", py::arg("symbolic_model"), py::arg("formulas") = Formulas());
    m.def("transform_continuous_to_discrete_time_sparse_model",
          py::overload_cast<std::shared_ptr<storm::models::sparse::Model<ValueType>> const&, Formulas const&>(
              &storm::api::transformContinuousToDiscreteTimeSparseModel<ValueType>),
          "Transform continuous-time model into discrete-time model", py::arg("model"), py::arg("formulas"));
    m.def("eliminate_non_markovian_chains", &storm::api::eliminateNonMarkovianChains<ValueType>, "Eliminate chains of non-Markovian states in MA",
          py::arg("ma"), py::arg("formulas"), py::arg("label_behavior"));
}

namespace {

// Thin wrapper for checking interval models with a (non-interval) check task
template<typename ModelType, typename ValueType>
std::unique_ptr<storm::modelchecker::CheckResult> verifyIntervalModelWithSparseEngine(storm::Environment const& env, std::shared_ptr<ModelType> const& model,
                                                                                      CheckTask<ValueType> const& task) {
    if constexpr (std::is_same_v<ModelType, storm::models::sparse::Dtmc<typename ModelType::ValueType>>) {
        return storm::modelchecker::SparseDtmcPrctlModelChecker<ModelType>(*model).check(env, task);
    } else {
        return storm::modelchecker::SparseMdpPrctlModelChecker<ModelType>(*model).check(env, task);
    }
}

}  // namespace

template<typename ValueType>
void define_api_verification_typed(py::module& m) {
    if constexpr (storm::IsIntervalType<ValueType>) {
        // Interval models are checked with check tasks over the corresponding non-interval value type
        using TaskType = storm::IntervalBaseType<ValueType>;
        m.def("verify_with_sparse_engine", &verifyIntervalModelWithSparseEngine<storm::models::sparse::Dtmc<ValueType>, TaskType>,
              "Verify interval DTMC with sparse engine", py::arg("env"), py::arg("model"), py::arg("task"), py::call_guard<py::gil_scoped_release>());
        m.def("verify_with_sparse_engine", &verifyIntervalModelWithSparseEngine<storm::models::sparse::Mdp<ValueType>, TaskType>,
              "Verify interval MDP with sparse engine", py::arg("env"), py::arg("model"), py::arg("task"), py::call_guard<py::gil_scoped_release>());
    } else {
        // The MDP overload comes first such that POMDPs are checked as fully observable MDPs
        m.def("verify_with_sparse_engine",
              py::overload_cast<storm::Environment const&, std::shared_ptr<storm::models::sparse::Mdp<ValueType>> const&, CheckTask<ValueType> const&>(
                  &storm::api::verifyWithSparseEngine<ValueType>),
              "Verify MDP with sparse engine", py::arg("env"), py::arg("mdp"), py::arg("task"), py::call_guard<py::gil_scoped_release>());
        m.def("verify_with_sparse_engine",
              py::overload_cast<storm::Environment const&, std::shared_ptr<storm::models::sparse::Model<ValueType>> const&, CheckTask<ValueType> const&, bool>(
                  &storm::api::verifyWithSparseEngine<ValueType>),
              "Verify model with sparse engine", py::arg("env"), py::arg("model"), py::arg("task"), py::arg("prefer_elimination_checker") = false,
              py::call_guard<py::gil_scoped_release>());
        m.def("verify_with_hybrid_engine",
              py::overload_cast<storm::Environment const&, std::shared_ptr<storm::models::symbolic::Model<storm::dd::DdType::Sylvan, ValueType>> const&,
                                CheckTask<ValueType> const&>(&storm::api::verifyWithHybridEngine<storm::dd::DdType::Sylvan, ValueType>),
              "Verify model with hybrid engine", py::arg("env"), py::arg("model"), py::arg("task"), py::call_guard<py::gil_scoped_release>());
        m.def("verify_with_dd_engine",
              py::overload_cast<storm::Environment const&, std::shared_ptr<storm::models::symbolic::Model<storm::dd::DdType::Sylvan, ValueType>> const&,
                                CheckTask<ValueType> const&>(&storm::api::verifyWithDdEngine<storm::dd::DdType::Sylvan, ValueType>),
              "Verify model with dd engine", py::arg("env"), py::arg("model"), py::arg("task"), py::call_guard<py::gil_scoped_release>());
    }

    if constexpr (std::is_same_v<ValueType, double> || std::is_same_v<ValueType, storm::RationalNumber>) {
        m.def("compute_steady_state_distribution_with_sparse_engine",
              py::overload_cast<storm::Environment const&, std::shared_ptr<storm::models::sparse::Model<ValueType>> const&>(
                  &storm::api::computeSteadyStateDistributionWithSparseEngine<ValueType>),
              "Compute steady-state distribution of deterministic model", py::arg("env"), py::arg("model"));
        m.def("compute_expected_visiting_times_with_sparse_engine",
              py::overload_cast<storm::Environment const&, std::shared_ptr<storm::models::sparse::Model<ValueType>> const&>(
                  &storm::api::computeExpectedVisitingTimesWithSparseEngine<ValueType>),
              "Compute expected visiting times of deterministic model", py::arg("env"), py::arg("model"));
    }
}

template void define_api_builder_typed<double>(py::module&);
template void define_api_builder_typed<storm::RationalNumber>(py::module&);
template void define_api_builder_typed<storm::RationalFunction>(py::module&);
template void define_api_builder_typed<storm::Interval>(py::module&);
template void define_api_builder_typed<storm::RationalInterval>(py::module&);

template void define_api_bisimulation_typed<double>(py::module&);
template void define_api_bisimulation_typed<storm::RationalFunction>(py::module&);

template void define_api_export_typed<double>(py::module&);
template void define_api_export_typed<storm::RationalNumber>(py::module&);
template void define_api_export_typed<storm::RationalFunction>(py::module&);
template void define_api_export_typed<storm::Interval>(py::module&);
template void define_api_export_typed<storm::RationalInterval>(py::module&);

template void define_api_transformation_typed<double>(py::module&);
template void define_api_transformation_typed<storm::RationalNumber>(py::module&);
template void define_api_transformation_typed<storm::RationalFunction>(py::module&);

template void define_api_verification_typed<double>(py::module&);
template void define_api_verification_typed<storm::RationalNumber>(py::module&);
template void define_api_verification_typed<storm::RationalFunction>(py::module&);
template void define_api_verification_typed<storm::Interval>(py::module&);
template void define_api_verification_typed<storm::RationalInterval>(py::module&);

}  // namespace stormpy

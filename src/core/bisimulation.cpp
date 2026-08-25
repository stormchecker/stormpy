#include "bisimulation.h"

#include <storm/adapters/RationalFunctionAdapter.h>
#include <storm/models/symbolic/StandardRewardModel.h>

template<storm::dd::DdType DdType, typename ValueType>
std::shared_ptr<storm::models::Model<ValueType>> performBisimulationMinimization(
    std::shared_ptr<storm::models::symbolic::Model<DdType, ValueType>> const& model, std::vector<std::shared_ptr<storm::logic::Formula const>> const& formulas,
    storm::storage::BisimulationType const& bisimulationType, storm::dd::bisimulation::QuotientFormat const& quotientFormat,
    storm::dd::bisimulation::BisimulationOptions const& bisimulationOptions) {
    return storm::api::performBisimulationMinimization<DdType, ValueType, ValueType>(
        model, formulas, bisimulationType, storm::dd::bisimulation::SignatureMode::Eager, quotientFormat, bisimulationOptions);
}

// Define python bindings
void define_bisimulation(py::module& m) {
    // Bisimulation
    m.def("_perform_bisimulation", &storm::api::performBisimulationMinimization<double>, "Perform bisimulation", py::arg("model"), py::arg("formulas"),
          py::arg("bisimulation_type"), py::arg("graph_preserving"), py::arg("tolerance"));
    m.def("_perform_parametric_bisimulation", &storm::api::performBisimulationMinimization<storm::RationalFunction>, "Perform bisimulation on parametric model",
          py::arg("model"), py::arg("formulas"), py::arg("bisimulation_type"), py::arg("graph_preserving"), py::arg("tolerance"));
    m.def("_perform_symbolic_bisimulation", &performBisimulationMinimization<storm::dd::DdType::Sylvan, double>, "Perform bisimulation", py::arg("model"),
          py::arg("formulas"), py::arg("bisimulation_type"), py::arg("quotient_format"), py::arg("bisimulation_options"));
    m.def("_perform_symbolic_parametric_bisimulation", &performBisimulationMinimization<storm::dd::DdType::Sylvan, storm::RationalFunction>,
          "Perform bisimulation on parametric model", py::arg("model"), py::arg("formulas"), py::arg("bisimulation_type"), py::arg("quotient_format"),
          py::arg("bisimulation_options"));

    // BisimulationType
    py::native_enum<storm::storage::BisimulationType>(m, "BisimulationType", "enum.Enum", "Types of bisimulation")
        .value("STRONG", storm::storage::BisimulationType::Strong)
        .value("WEAK", storm::storage::BisimulationType::Weak)
        .finalize();

    // QuotientFormat
    py::native_enum<storm::dd::bisimulation::QuotientFormat>(m, "QuotientFormat", "enum.Enum", "Return format of bisimulation quotient")
        .value("SPARSE", storm::dd::bisimulation::QuotientFormat::Sparse)
        .value("DD", storm::dd::bisimulation::QuotientFormat::Dd)
        .finalize();

    py::classh<storm::dd::bisimulation::BisimulationOptions>(m, "BisimulationOptionsDd", "Options for Dd bisimulation")
        .def(py::init<>(), "Create")
        .def_readwrite("reuse_mode", &storm::dd::bisimulation::BisimulationOptions::reuseMode, "Reuse mode")
        .def_readwrite("refinement_mode", &storm::dd::bisimulation::BisimulationOptions::refinementMode, "Refinement mode")
        .def_readwrite("initial_partition_mode", &storm::dd::bisimulation::BisimulationOptions::initialPartitionMode, "Initial partition mode")
        .def_readwrite("use_representative", &storm::dd::bisimulation::BisimulationOptions::useRepresentatives, "Whether to use a representative")
        .def_readwrite("use_original_variables", &storm::dd::bisimulation::BisimulationOptions::useOriginalVariables, "Whether to use the original variables");
}

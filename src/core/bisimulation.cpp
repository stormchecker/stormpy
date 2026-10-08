#include "bisimulation.h"

#include <storm/adapters/RationalFunctionAdapter.h>
#include <storm/models/symbolic/StandardRewardModel.h>

template<storm::dd::DdType DdType, typename ValueType>
std::shared_ptr<storm::models::Model<ValueType>> performBisimulationMinimization(
    std::shared_ptr<storm::models::symbolic::Model<DdType, ValueType>> const& model, std::vector<std::shared_ptr<storm::logic::Formula const>> const& formulas,
    storm::bisimulation::BisimulationType const& bisimulationType, storm::dd::bisimulation::QuotientFormat const& quotientFormat,
    storm::dd::bisimulation::BisimulationOptions const& bisimulationOptions) {
    return storm::api::performBisimulationMinimization<DdType, ValueType, ValueType>(
        model, formulas, bisimulationType, storm::dd::bisimulation::SignatureMode::Eager, quotientFormat, bisimulationOptions);
}

// Define python bindings
void define_bisimulation(py::module& m) {
    // Bisimulation
    m.def("_perform_bisimulation", &storm::api::performBisimulationMinimization<double>, "Perform bisimulation", py::arg("model"), py::arg("formulas"),
          py::arg("options"));
    m.def("_perform_parametric_bisimulation", &storm::api::performBisimulationMinimization<storm::RationalFunction>, "Perform bisimulation on parametric model",
          py::arg("model"), py::arg("formulas"), py::arg("options"));
    m.def("_perform_symbolic_bisimulation", &performBisimulationMinimization<storm::dd::DdType::Sylvan, double>, "Perform bisimulation", py::arg("model"),
          py::arg("formulas"), py::arg("bisimulation_type"), py::arg("quotient_format"), py::arg("bisimulation_options"));
    m.def("_perform_symbolic_parametric_bisimulation", &performBisimulationMinimization<storm::dd::DdType::Sylvan, storm::RationalFunction>,
          "Perform bisimulation on parametric model", py::arg("model"), py::arg("formulas"), py::arg("bisimulation_type"), py::arg("quotient_format"),
          py::arg("bisimulation_options"));

    // BisimulationType
    py::native_enum<storm::bisimulation::BisimulationType>(m, "BisimulationType", "enum.Enum", "Types of bisimulation")
        .value("STRONG", storm::bisimulation::BisimulationType::Strong)
        .value("WEAK", storm::bisimulation::BisimulationType::Weak)
        .finalize();

    // StateLabelPreservation
    py::native_enum<storm::bisimulation::StateLabelPreservation>(m, "StateLabelPreservation", "enum.Enum", "Which state labels to preserve during bisimulation")
        .value("DEFAULT", storm::bisimulation::StateLabelPreservation::Default)
        .value("ALL", storm::bisimulation::StateLabelPreservation::All)
        .value("NONE", storm::bisimulation::StateLabelPreservation::None)
        .value("FORMULA_PROPOSITIONAL", storm::bisimulation::StateLabelPreservation::FormulaPropositional)
        .value("FORMULA_INDIVIDUAL", storm::bisimulation::StateLabelPreservation::FormulaIndividual)
        .finalize();

    // BisimulationOptions
    py::classh<storm::bisimulation::Options>(m, "BisimulationOptions", "Options for bisimulation")
        .def(py::init<>(), "Create")
        .def_readwrite("bisimulation_type", &storm::bisimulation::Options::bisimulationType, "Type of bisimulation")
        .def_readwrite("state_label_preservation", &storm::bisimulation::Options::stateLabelPreservation, "Which state labels to preserve")
        .def_readwrite("preserve_all_rewards", &storm::bisimulation::Options::preserveAllRewards,
                       "Whether to preserve all reward models. If None, then all rewards are preserved iff no formula is given")
        .def_readwrite("preserve_choice_labels", &storm::bisimulation::Options::preserveChoiceLabels, "Whether to preserve choice labels")
        .def_readwrite("preserve_choice_origins", &storm::bisimulation::Options::preserveChoiceOrigins, "Whether to preserve choice origins")
        .def_readwrite("action_sensitive", &storm::bisimulation::Options::actionSensitive, "Whether matching choices must occur at identical positions")
        .def_readwrite("tolerance", &storm::bisimulation::Options::tolerance,
                       "Maximum permitted numerical deviation in values (probabilities, rates, rewards) between the original and quotient model")
        .def_readwrite("create_quotient_choice_mapping", &storm::bisimulation::Options::createQuotientChoiceMapping,
                       "Whether to create a mapping from quotient to original choices")
        .def_readwrite("prefer_signature_refinement", &storm::bisimulation::Options::preferSignatureRefinement,
                       "Whether to prefer signature-based over splitter-based refinement");

    // QuotientFormat
    py::native_enum<storm::dd::bisimulation::QuotientFormat>(m, "QuotientFormat", "enum.Enum", "Return format of bisimulation quotient")
        .value("SPARSE", storm::dd::bisimulation::QuotientFormat::Sparse)
        .value("DD", storm::dd::bisimulation::QuotientFormat::Dd)
        .finalize();

    // ReuseMode
    py::native_enum<storm::dd::bisimulation::ReuseMode>(m, "ReuseMode", "enum.Enum", "Reuse mode for Dd bisimulation")
        .value("NONE", storm::dd::bisimulation::ReuseMode::None)
        .value("BLOCK_NUMBERS", storm::dd::bisimulation::ReuseMode::BlockNumbers)
        .finalize();

    // RefinementMode
    py::native_enum<storm::dd::bisimulation::RefinementMode>(m, "RefinementMode", "enum.Enum", "Refinement mode for Dd bisimulation")
        .value("FULL", storm::dd::bisimulation::RefinementMode::Full)
        .value("CHANGED_STATES", storm::dd::bisimulation::RefinementMode::ChangedStates)
        .finalize();

    // InitialPartitionMode
    py::native_enum<storm::dd::bisimulation::InitialPartitionMode>(m, "InitialPartitionMode", "enum.Enum", "Initial partition mode for Dd bisimulation")
        .value("REGULAR", storm::dd::bisimulation::InitialPartitionMode::Regular)
        .value("FINER", storm::dd::bisimulation::InitialPartitionMode::Finer)
        .finalize();

    py::classh<storm::dd::bisimulation::BisimulationOptions>(m, "BisimulationOptionsDd", "Options for Dd bisimulation")
        .def(py::init<>(), "Create")
        .def_readwrite("reuse_mode", &storm::dd::bisimulation::BisimulationOptions::reuseMode, "Reuse mode")
        .def_readwrite("refinement_mode", &storm::dd::bisimulation::BisimulationOptions::refinementMode, "Refinement mode")
        .def_readwrite("initial_partition_mode", &storm::dd::bisimulation::BisimulationOptions::initialPartitionMode, "Initial partition mode")
        .def_readwrite("use_representative", &storm::dd::bisimulation::BisimulationOptions::useRepresentatives, "Whether to use a representative")
        .def_readwrite("use_original_variables", &storm::dd::bisimulation::BisimulationOptions::useOriginalVariables, "Whether to use the original variables");
}

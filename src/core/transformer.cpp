#include "transformer.h"

#include <storm/adapters/IntervalAdapter.h>
#include <storm/adapters/RationalFunctionAdapter.h>
#include <storm/transformer/AddUncertainty.h>
#include <storm/transformer/EndComponentEliminator.h>
#include <storm/transformer/NonMarkovianChainTransformer.h>
#include <storm/transformer/SubsystemBuilder.h>
#include <storm/transformer/bisimulation/BisimulationType.h>
#include <storm/transformer/bisimulation/dd/BisimulationOptions.h>
#include <storm/transformer/bisimulation/dd/InitialPartitionMode.h>
#include <storm/transformer/bisimulation/dd/QuotientFormat.h>
#include <storm/transformer/bisimulation/dd/RefinementMode.h>
#include <storm/transformer/bisimulation/dd/ReuseMode.h>
#include <storm/transformer/bisimulation/dd/SignatureMode.h>
#include <storm/transformer/bisimulation/sparse/Options.h>

#include "src/binding_type_index.h"

namespace stormpy {

void define_transformer(py::module& m) {
    using SubsystemBuilderOptions = storm::transformer::SubsystemBuilderOptions;
    py::classh<SubsystemBuilderOptions>(m, "SubsystemBuilderOptions", "Options for constructing a subsystem")
        .def(py::init<>(), "Create default options")
        .def_readwrite("check_transitions_outside", &SubsystemBuilderOptions::checkTransitionsOutside, "Check for transitions leaving the subsystem")
        .def_readwrite("build_state_mapping", &SubsystemBuilderOptions::buildStateMapping, "Build mapping from new to old states")
        .def_readwrite("build_action_mapping", &SubsystemBuilderOptions::buildActionMapping, "Build mapping from new to old actions")
        .def_readwrite("build_kept_actions", &SubsystemBuilderOptions::buildKeptActions, "Build the set of kept actions")
        .def_readwrite("fix_deadlocks", &SubsystemBuilderOptions::fixDeadlocks, "Fix deadlocks by adding self-loops")
        .def_readwrite("make_row_grouping_trivial", &SubsystemBuilderOptions::makeRowGroupingTrivial, "Make the row grouping trivial if possible");

    py::native_enum<storm::transformer::EliminationLabelBehavior>(m, "EliminationLabelBehavior", "enum.Enum",
                                                                  "Behavior of labels while eliminating non-Markovian chains")
        .value("KEEP_LABELS", storm::transformer::EliminationLabelBehavior::KeepLabels)
        .value("MERGE_LABELS", storm::transformer::EliminationLabelBehavior::MergeLabels)
        .value("DELETE_LABELS", storm::transformer::EliminationLabelBehavior::DeleteLabels)
        .value("EXTEND_LABELS", storm::transformer::EliminationLabelBehavior::ExtendLabels)
        .finalize();

    py::native_enum<storm::bisimulation::BisimulationType>(m, "BisimulationType", "enum.Enum", "Type of bisimulation")
        .value("STRONG", storm::bisimulation::BisimulationType::Strong)
        .value("WEAK", storm::bisimulation::BisimulationType::Weak)
        .finalize();

    py::native_enum<storm::bisimulation::StateLabelPreservation>(m, "StateLabelPreservation", "enum.Enum", "Which state labels to preserve during bisimulation")
        .value("DEFAULT", storm::bisimulation::StateLabelPreservation::Default)
        .value("ALL", storm::bisimulation::StateLabelPreservation::All)
        .value("NONE", storm::bisimulation::StateLabelPreservation::None)
        .value("FORMULA_PROPOSITIONAL", storm::bisimulation::StateLabelPreservation::FormulaPropositional)
        .value("FORMULA_INDIVIDUAL", storm::bisimulation::StateLabelPreservation::FormulaIndividual)
        .finalize();

    using Options = storm::bisimulation::Options;
    // Named 'BisimulationOptions' as 'Options' is ambiguous
    py::classh<Options>(m, "BisimulationOptions", "Options for bisimulation on sparse models")
        .def(py::init<>(), "Create default options")
        .def_readwrite("bisimulation_type", &Options::bisimulationType, "Type of bisimulation")
        .def_readwrite("state_label_preservation", &Options::stateLabelPreservation, "Which state labels to preserve")
        .def_readwrite("preserve_all_rewards", &Options::preserveAllRewards,
                       "Whether to preserve all reward models. If None, then all rewards are preserved iff no formula is given")
        .def_readwrite("preserve_choice_labels", &Options::preserveChoiceLabels, "Whether to preserve choice labels")
        .def_readwrite("preserve_choice_origins", &Options::preserveChoiceOrigins, "Whether to preserve choice origins")
        .def_readwrite("action_sensitive", &Options::actionSensitive, "Whether matching choices must occur at identical positions")
        .def_readwrite("tolerance", &Options::tolerance,
                       "Maximum permitted numerical deviation in values (probabilities, rates, rewards) between the original and quotient model")
        .def_readwrite("create_quotient_choice_mapping", &Options::createQuotientChoiceMapping, "Whether to create a mapping from quotient to original choices")
        .def_readwrite("prefer_signature_refinement", &Options::preferSignatureRefinement, "Whether to prefer signature-based over splitter-based refinement");

    py::native_enum<storm::dd::bisimulation::SignatureMode>(m, "SignatureMode", "enum.Enum", "Signature mode for symbolic bisimulation")
        .value("EAGER", storm::dd::bisimulation::SignatureMode::Eager)
        .value("LAZY", storm::dd::bisimulation::SignatureMode::Lazy)
        .value("QUALITATIVE", storm::dd::bisimulation::SignatureMode::Qualitative)
        .finalize();

    py::native_enum<storm::dd::bisimulation::QuotientFormat>(m, "QuotientFormat", "enum.Enum", "Format of the quotient of symbolic bisimulation")
        .value("SPARSE", storm::dd::bisimulation::QuotientFormat::Sparse)
        .value("DD", storm::dd::bisimulation::QuotientFormat::Dd)
        .finalize();

    py::native_enum<storm::dd::bisimulation::ReuseMode>(m, "ReuseMode", "enum.Enum", "Reuse mode for symbolic bisimulation")
        .value("NONE", storm::dd::bisimulation::ReuseMode::None)
        .value("BLOCK_NUMBERS", storm::dd::bisimulation::ReuseMode::BlockNumbers)
        .finalize();

    py::native_enum<storm::dd::bisimulation::RefinementMode>(m, "RefinementMode", "enum.Enum", "Refinement mode for symbolic bisimulation")
        .value("FULL", storm::dd::bisimulation::RefinementMode::Full)
        .value("CHANGED_STATES", storm::dd::bisimulation::RefinementMode::ChangedStates)
        .finalize();

    py::native_enum<storm::dd::bisimulation::InitialPartitionMode>(m, "InitialPartitionMode", "enum.Enum", "Initial partition mode for symbolic bisimulation")
        .value("REGULAR", storm::dd::bisimulation::InitialPartitionMode::Regular)
        .value("FINER", storm::dd::bisimulation::InitialPartitionMode::Finer)
        .finalize();

    using DdOptions = storm::dd::bisimulation::BisimulationOptions;
    // Named DdBisimulationOptions
    py::classh<DdOptions>(m, "DdBisimulationOptions", "Options for bisimulation on symbolic models")
        .def(py::init<>(), "Create default options")
        .def_readwrite("reuse_mode", &DdOptions::reuseMode, "Reuse mode")
        .def_readwrite("refinement_mode", &DdOptions::refinementMode, "Refinement mode")
        .def_readwrite("initial_partition_mode", &DdOptions::initialPartitionMode, "Initial partition mode")
        .def_readwrite("use_representatives", &DdOptions::useRepresentatives, "Whether to use representatives")
        .def_readwrite("use_original_variables", &DdOptions::useOriginalVariables, "Whether to use the original variables")
        .def_readwrite("verbose", &DdOptions::verbose, "Whether to print verbose output")
        .def_readwrite("show_progress_delay", &DdOptions::showProgressDelay, "Delay between progress outputs");
}

template<typename ValueType>
void define_transformer_typed(py::module& m) {
    auto const index = stormpy::bindings::typeIndex<ValueType>();

    using SubsystemReturnType = storm::transformer::SubsystemBuilderReturnType<ValueType>;
    stormpy::bindings::bindTemplateClass<SubsystemReturnType>(m, "SubsystemBuilderReturnType", index, "Result of the construction of a subsystem")
        .def_readonly("model", &SubsystemReturnType::model, "The submodel")
        .def_readonly("new_to_old_state_index_mapping", &SubsystemReturnType::newToOldStateIndexMapping,
                      "For each state in the result, the state index in the original model")
        .def_readonly("new_to_old_action_index_mapping", &SubsystemReturnType::newToOldActionIndexMapping,
                      "For each action in the result, the action index in the original model")
        .def_readonly("kept_actions", &SubsystemReturnType::keptActions, "Actions of the subsystem available in the original system")
        .def_readonly("deadlock_label", &SubsystemReturnType::deadlockLabel, "If set, deadlock states have been introduced and have been assigned this label");
    m.def("build_subsystem", &storm::transformer::buildSubsystem<ValueType>, "Build a subsystem of a sparse model", py::arg("original_model"),
          py::arg("subsystem_states"), py::arg("subsystem_actions"), py::arg("keep_unreachable_states") = true,
          py::arg("options") = storm::transformer::SubsystemBuilderOptions());

    using Eliminator = storm::transformer::EndComponentEliminator<ValueType>;
    using EliminatorReturnType = typename Eliminator::EndComponentEliminatorReturnType;
    stormpy::bindings::bindTemplateClass<EliminatorReturnType>(m, "EndComponentEliminatorReturnType", index, "Result of end component elimination")
        .def_readonly("matrix", &EliminatorReturnType::matrix, "The resulting matrix")
        .def_readonly("new_to_old_row_mapping", &EliminatorReturnType::newToOldRowMapping,
                      "Index mapping that gives for each row of the new matrix the corresponding row in the original matrix")
        .def_readonly("old_to_new_state_mapping", &EliminatorReturnType::oldToNewStateMapping,
                      "For each state of the original matrix (and subsystem) the corresponding state in the result. Removed states are mapped to the EC.")
        .def_readonly("sink_rows", &EliminatorReturnType::sinkRows, "Rows that indicate staying in the EC forever");
    stormpy::bindings::bindTemplateClass<Eliminator>(m, "EndComponentEliminator", index, "Elimination of end components")
        .def_static("transform",
                    py::overload_cast<storm::storage::SparseMatrix<ValueType> const&, storm::storage::BitVector const&, storm::storage::BitVector const&,
                                      storm::storage::BitVector const&, bool>(&Eliminator::transform),
                    "Eliminate end components in the subsystem", py::arg("original_matrix"), py::arg("subsystem_states"), py::arg("possible_ec_rows"),
                    py::arg("add_sink_row_states"), py::arg("add_self_loop_at_sink_states") = false);
}

template<typename ValueType>
void define_transformer_add_uncertainty_typed(py::module& m) {
    using AddUncertainty = storm::transformer::AddUncertainty<ValueType>;
    stormpy::bindings::bindTemplateClass<AddUncertainty>(m, "AddUncertainty", stormpy::bindings::typeIndex<ValueType>(),
                                                         "Transform model into interval model with specified uncertainty")
        .def(py::init<std::shared_ptr<storm::models::sparse::Model<ValueType>> const&>(), "Create transformer", py::arg("original_model"))
        .def("transform", &AddUncertainty::transform, "Transform the model", py::arg("additive_uncertainty"),
             py::arg("minimal_value") = storm::utility::convertNumber<ValueType>(0.0001), py::arg("max_successors") = std::optional<uint64_t>{});
}

template void define_transformer_typed<double>(py::module& m);
template void define_transformer_typed<storm::RationalNumber>(py::module& m);
template void define_transformer_typed<storm::RationalFunction>(py::module& m);
template void define_transformer_typed<storm::Interval>(py::module& m);
template void define_transformer_typed<storm::RationalInterval>(py::module& m);

template void define_transformer_add_uncertainty_typed<double>(py::module& m);
template void define_transformer_add_uncertainty_typed<storm::RationalNumber>(py::module& m);

}  // namespace stormpy

#include "transformation.h"

#include <storm/adapters/RationalFunctionAdapter.h>
#include <storm/api/transformation.h>
#include <storm/models/symbolic/StandardRewardModel.h>
#include <storm/transformer/AddUncertainty.h>
#include <storm/transformer/EndComponentEliminator.h>
#include <storm/transformer/SubsystemBuilder.h>

// Thin wrappers.
template<typename VT>
storm::transformer::SubsystemBuilderReturnType<VT> constructSubsystem(storm::models::sparse::Model<VT> const& originalModel,
                                                                      storm::storage::BitVector const& subsystemStates,
                                                                      storm::storage::BitVector const& subsystemActions, bool keepUnreachableStates,
                                                                      storm::transformer::SubsystemBuilderOptions options) {
    return storm::transformer::buildSubsystem(originalModel, subsystemStates, subsystemActions, keepUnreachableStates, options);
}

template<typename ValueType>
std::pair<std::shared_ptr<storm::models::sparse::Model<ValueType>>, std::vector<std::shared_ptr<storm::logic::Formula const>>>
transformContinuousToDiscreteTimeSparseModel(std::shared_ptr<storm::models::sparse::Model<ValueType>> const& model,
                                             std::vector<std::shared_ptr<storm::logic::Formula const>> const& formulas) {
    return storm::api::transformContinuousToDiscreteTimeSparseModel(model, formulas);
}

template<typename ValueType>
typename storm::transformer::EndComponentEliminator<ValueType>::EndComponentEliminatorReturnType eliminateECs(
    storm::storage::SparseMatrix<ValueType> const& matrix, storm::storage::BitVector const& subsystemStates, storm::storage::BitVector const& possibleECRows,
    storm::storage::BitVector const& addSinkRowStates, bool addSelfLoopAtSinkStates) {
    return storm::transformer::EndComponentEliminator<ValueType>::transform(matrix, subsystemStates, possibleECRows, addSinkRowStates, addSelfLoopAtSinkStates);
}

template<typename ValueType>
void define_transformation_mdef(py::module& m) {
    std::string type, desc;
    if constexpr (std::is_same_v<ValueType, double>) {
        type = "";
        desc = "";
    } else if constexpr (std::is_same_v<ValueType, storm::RationalFunction>) {
        type = "_parametric";
        desc = "parametric ";
    }

    m.def(("_transform_to_sparse" + type + "_model").c_str(), &storm::api::transformSymbolicToSparseModel<storm::dd::DdType::Sylvan, ValueType>,
          ("Transform symbolic " + desc + "model into sparse " + desc + "model").c_str(), py::arg("model"),
          py::arg("formulae") = std::vector<std::shared_ptr<storm::logic::Formula const>>());
    m.def(("_transform_to_discrete_time" + type + "_model").c_str(), &transformContinuousToDiscreteTimeSparseModel<ValueType>,
          ("Transform " + desc + "continuous time model to " + desc + "discrete time model").c_str(), py::arg("model"),
          py::arg("formulae") = std::vector<std::shared_ptr<storm::logic::Formula const>>());
    m.def(("_eliminate_non_markovian_chains" + type).c_str(), &storm::api::eliminateNonMarkovianChains<ValueType>,
          "Eliminate chains of non-Markovian states in Markov automaton.", py::arg("ma"), py::arg("formulae"), py::arg("label_behavior"));
}

void define_transformation(py::module& m) {
    define_transformation_mdef<double>(m);
    define_transformation_mdef<storm::RationalFunction>(m);

    py::class_<storm::transformer::SubsystemBuilderOptions>(m, "SubsystemBuilderOptions", "Options for constructing the subsystem")
        .def(py::init<>())
        .def_readwrite("check_transitions_outside", &storm::transformer::SubsystemBuilderOptions::checkTransitionsOutside)
        .def_readwrite("build_state_mapping", &storm::transformer::SubsystemBuilderOptions::buildStateMapping)
        .def_readwrite("build_action_mapping", &storm::transformer::SubsystemBuilderOptions::buildActionMapping)
        .def_readwrite("build_kept_actions", &storm::transformer::SubsystemBuilderOptions::buildKeptActions)
        .def_readwrite("fix_deadlocks", &storm::transformer::SubsystemBuilderOptions::fixDeadlocks);

    // Non-Markovian chain elimination
    py::native_enum<storm::transformer::EliminationLabelBehavior>(m, "EliminationLabelBehavior", "enum.Enum",
                                                                  "Behavior of labels while eliminating non-Markovian chains")
        .value("KEEP_LABELS", storm::transformer::EliminationLabelBehavior::KeepLabels)
        .value("MERGE_LABELS", storm::transformer::EliminationLabelBehavior::MergeLabels)
        .value("DELETE_LABELS", storm::transformer::EliminationLabelBehavior::DeleteLabels)
        .finalize();
}

template<typename ValueType>
void define_transformation_typed(py::module& m, std::string const& vtSuffix) {
    py::class_<storm::transformer::SubsystemBuilderReturnType<ValueType>>(m, ("SubsystemBuilderReturnType" + vtSuffix).c_str(),
                                                                          "Result of the construction of a subsystem")
        .def_readonly("model", &storm::transformer::SubsystemBuilderReturnType<ValueType>::model, "the submodel")
        .def_readonly("new_to_old_state_mapping", &storm::transformer::SubsystemBuilderReturnType<ValueType>::newToOldStateIndexMapping,
                      "for each state in result, the state index in the original model")
        .def_readonly("new_to_old_action_mapping", &storm::transformer::SubsystemBuilderReturnType<ValueType>::newToOldActionIndexMapping,
                      "for each action in result, the action index in the original model")
        .def_readonly("kept_actions", &storm::transformer::SubsystemBuilderReturnType<ValueType>::keptActions,
                      "Actions of the subsystem available in the original system")
        .def_readonly("deadlock_label", &storm::transformer::SubsystemBuilderReturnType<ValueType>::deadlockLabel,
                      "If set, deadlock states have been introduced and have been assigned this label");
    m.def(("_construct_subsystem_" + vtSuffix).c_str(), &constructSubsystem<ValueType>, "build a subsystem of a sparse model");

    py::class_<typename storm::transformer::EndComponentEliminator<ValueType>::EndComponentEliminatorReturnType>(
        m, ("EndComponentEliminatorReturnType" + vtSuffix).c_str(), "Container for result of endcomponent elimination")
        .def_readonly("matrix", &storm::transformer::EndComponentEliminator<ValueType>::EndComponentEliminatorReturnType::matrix, "The resulting matrix")
        .def_readonly("new_to_old_row_mapping", &storm::transformer::EndComponentEliminator<ValueType>::EndComponentEliminatorReturnType::newToOldRowMapping,
                      "Index mapping that gives for each row of the new matrix the corresponding row in the original matrix")
        .def_readonly("old_to_new_state_mapping",
                      &storm::transformer::EndComponentEliminator<ValueType>::EndComponentEliminatorReturnType::oldToNewStateMapping,
                      "For each state of the original matrix (and subsystem) the corresponding state in the result. Removed states are mapped to the EC.")
        .def_readonly("sink_rows", &storm::transformer::EndComponentEliminator<ValueType>::EndComponentEliminatorReturnType::sinkRows,
                      "Rows that indicate staying in the EC forever");
    m.def(("_eliminate_end_components_" + vtSuffix).c_str(), &eliminateECs<ValueType>, "Eliminate ECs in the subsystem", py::arg("matrix"),
          py::arg("subsystem"), py::arg("possible_ec_rows"), py::arg("addSinkRowStates"), py::arg("addSelfLoopAtSinkStates"));
}

template<typename ValueType>
void define_transformation_typed_only_numbers(py::module& m, std::string const& vtSuffix) {
    py::class_<storm::transformer::AddUncertainty<ValueType>>(m, ("AddUncertainty" + vtSuffix).c_str(),
                                                              "Transform model into interval model with specified uncertainty")
        .def(py::init<std::shared_ptr<storm::models::sparse::Model<ValueType>> const&>(), py::arg("model"))
        .def("transform", &storm::transformer::AddUncertainty<ValueType>::transform, "Transform the model", py::arg("additive_uncertainty"),
             py::arg("minimal_value") = storm::utility::convertNumber<ValueType>(0.0001), py::arg("max_successors") = std::optional<uint64_t>{});
}

template void define_transformation_typed<double>(py::module& m, std::string const& vtSuffix);
template void define_transformation_typed<storm::RationalNumber>(py::module& m, std::string const& vtSuffix);
template void define_transformation_typed<storm::RationalFunction>(py::module& m, std::string const& vtSuffix);
template void define_transformation_typed<storm::Interval>(py::module& m, std::string const& vtSuffix);
template void define_transformation_typed<storm::RationalInterval>(py::module& m, std::string const& vtSuffix);

template void define_transformation_typed_only_numbers<double>(py::module& m, std::string const& vtSuffix);
template void define_transformation_typed_only_numbers<storm::RationalNumber>(py::module& m, std::string const& vtSuffix);

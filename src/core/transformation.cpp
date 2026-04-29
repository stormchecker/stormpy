#include "transformation.h"

#include "storm/adapters/RationalFunctionAdapter.h"
#include "storm/api/transformation.h"
#include "storm/models/symbolic/StandardRewardModel.h"
#include "storm/transformer/SubsystemBuilder.h"
#include "storm/transformer/EndComponentEliminator.h"
#include "storm/transformer/AddUncertainty.h"

// Thin wrappers.
template<typename VT>
storm::transformer::SubsystemBuilderReturnType<VT> constructSubsystem(storm::models::sparse::Model<VT> const& originalModel, storm::storage::BitVector const& subsystemStates, storm::storage::BitVector const& subsystemActions, bool keepUnreachableStates, storm::transformer::SubsystemBuilderOptions options) {
    return storm::transformer::buildSubsystem(originalModel, subsystemStates, subsystemActions, keepUnreachableStates, options);
}

template<typename ValueType>
std::pair<std::shared_ptr<storm::models::sparse::Model<ValueType>>, std::vector<std::shared_ptr<storm::logic::Formula const>>> transformContinuousToDiscreteTimeSparseModel(std::shared_ptr<storm::models::sparse::Model<ValueType>> const& model, std::vector<std::shared_ptr<storm::logic::Formula const>> const& formulas) {
    return storm::api::transformContinuousToDiscreteTimeSparseModel(model, formulas);
}

template<typename ValueType>
typename storm::transformer::EndComponentEliminator<ValueType>::EndComponentEliminatorReturnType eliminateECs(storm::storage::SparseMatrix<ValueType> const& matrix,
                                                                                 storm::storage::BitVector const& subsystemStates,
                                                                                 storm::storage::BitVector const& possibleECRows,
                                                                                 storm::storage::BitVector const& addSinkRowStates,
                                                                                 bool addSelfLoopAtSinkStates) {
    return storm::transformer::EndComponentEliminator<ValueType>::transform(matrix, subsystemStates, possibleECRows, addSinkRowStates, addSelfLoopAtSinkStates);
}



void define_transformation(py::module& m) {
    // Transform model
    m.def("_transform_to_sparse_model", &storm::api::transformSymbolicToSparseModel<storm::dd::DdType::Sylvan, double>, "Transform symbolic model into sparse model", py::arg("model"), py::arg("formulae") = std::vector<std::shared_ptr<storm::logic::Formula const>>());
    m.def("_transform_to_sparse_parametric_model", &storm::api::transformSymbolicToSparseModel<storm::dd::DdType::Sylvan, storm::RationalFunction>, "Transform symbolic parametric model into sparse parametric model", py::arg("model"), py::arg("formulae") = std::vector<std::shared_ptr<storm::logic::Formula const>>());

    m.def("_transform_to_discrete_time_model", &transformContinuousToDiscreteTimeSparseModel<double>, "Transform continuous time model to discrete time model", py::arg("model"), py::arg("formulae") = std::vector<std::shared_ptr<storm::logic::Formula const>>());
    m.def("_transform_to_discrete_time_parametric_model", &transformContinuousToDiscreteTimeSparseModel<storm::RationalFunction>, "Transform parametric continuous time model to parametric discrete time model", py::arg("model"), py::arg("formulae") = std::vector<std::shared_ptr<storm::logic::Formula const>>());

    py::class_<storm::transformer::SubsystemBuilderOptions>(m, "SubsystemBuilderOptions", "Options for constructing the subsystem")
            .def(py::init<>())
            .def_readwrite("check_transitions_outside", &storm::transformer::SubsystemBuilderOptions::checkTransitionsOutside)
            .def_readwrite("build_state_mapping", &storm::transformer::SubsystemBuilderOptions::buildStateMapping)
            .def_readwrite("build_action_mapping", &storm::transformer::SubsystemBuilderOptions::buildActionMapping)
            .def_readwrite("build_kept_actions", &storm::transformer::SubsystemBuilderOptions::buildKeptActions)
            .def_readwrite("fix_deadlocks", &storm::transformer::SubsystemBuilderOptions::fixDeadlocks)
    ;

    // Non-Markovian chain elimination
    py::enum_<storm::transformer::EliminationLabelBehavior>(m, "EliminationLabelBehavior", "Behavior of labels while eliminating non-Markovian chains")
        .value("KEEP_LABELS", storm::transformer::EliminationLabelBehavior::KeepLabels)
        .value("MERGE_LABELS", storm::transformer::EliminationLabelBehavior::MergeLabels)
        .value("DELETE_LABELS", storm::transformer::EliminationLabelBehavior::DeleteLabels)
    ;

    m.def("_eliminate_non_markovian_chains", &storm::api::eliminateNonMarkovianChains<double>, "Eliminate chains of non-Markovian states in Markov automaton.", py::arg("ma"), py::arg("formulae"), py::arg("label_behavior"));
    m.def("_eliminate_non_markovian_chains_parametric", &storm::api::eliminateNonMarkovianChains<storm::RationalFunction>, "Eliminate chains of non-Markovian states in Markov automaton.", py::arg("ma"), py::arg("formulae"), py::arg("label_behavior"));

    py::class_<storm::transformer::EndComponentEliminator<double>::EndComponentEliminatorReturnType>(m, "EndComponentEliminatorReturnTypeDouble", "Container for result of endcomponent elimination")
            .def_readonly("matrix", &storm::transformer::EndComponentEliminator<double>::EndComponentEliminatorReturnType::matrix, "The resulting matrix")
            .def_readonly("new_to_old_row_mapping", &storm::transformer::EndComponentEliminator<double>::EndComponentEliminatorReturnType::newToOldRowMapping, "Index mapping that gives for each row fo the new matrix the corresponding row in the original matrix")
            .def_readonly("old_to_new_state_mapping", &storm::transformer::EndComponentEliminator<double>::EndComponentEliminatorReturnType::oldToNewStateMapping, "For each state of the original matrix (and subsystem) the corresponding state in the result. Removed states are mapped to the EC.")
            .def_readonly("sink_rows", &storm::transformer::EndComponentEliminator<double>::EndComponentEliminatorReturnType::sinkRows, "Rows that indicate staying in the EC forever");

    m.def("_eliminate_end_components_double", &eliminateECs<double>, "Eliminate ECs in the subystem", py::arg("matrix"), py::arg("subsystem"),  py::arg("possible_ec_rows"),py::arg("addSinkRowStates"), py::arg("addSelfLoopAtSinkStates"));

}

template<typename ValueType>
void define_transformation_typed(py::module& m, std::string const& vtSuffix) {
    py::class_<storm::transformer::SubsystemBuilderReturnType<ValueType>>(m, ("SubsystemBuilderReturnType" +
                                                                             vtSuffix).c_str(),
                                                                          "Result of the construction of a subsystem")
            .def_readonly("model", &storm::transformer::SubsystemBuilderReturnType<ValueType>::model, "the submodel")
            .def_readonly("new_to_old_state_mapping",
                          &storm::transformer::SubsystemBuilderReturnType<ValueType>::newToOldStateIndexMapping,
                          "for each state in result, the state index in the original model")
            .def_readonly("new_to_old_action_mapping",
                          &storm::transformer::SubsystemBuilderReturnType<ValueType>::newToOldActionIndexMapping,
                          "for each action in result, the action index in the original model")
            .def_readonly("kept_actions", &storm::transformer::SubsystemBuilderReturnType<ValueType>::keptActions,
                          "Actions of the subsystem available in the original system")
            .def_readonly("deadlock_label", &storm::transformer::SubsystemBuilderReturnType<ValueType>::deadlockLabel,
                          "If set, deadlock states have been introduced and have been assigned this label");
    m.def(("_construct_subsystem_" + vtSuffix).c_str(), &constructSubsystem<ValueType>, "build a subsystem of a sparse model");
}

template<typename ValueType>
void define_transformation_typed_only_numbers(py::module& m, std::string const& vtSuffix) {
    py::class_<storm::transformer::AddUncertainty<ValueType>>(m, ("AddUncertainty" + vtSuffix).c_str(), "Transform model into interval model with specified uncertainty")
        .def(py::init<std::shared_ptr<storm::models::sparse::Model<ValueType>> const&>(), py::arg("model"))
        .def("transform", &storm::transformer::AddUncertainty<ValueType>::transform, "Transform the model", py::arg("additive_uncertainty"), py::arg("minimal_value") = storm::utility::convertNumber<ValueType>(0.0001), py::arg("max_successors") = std::optional<uint64_t>{});
}

template void define_transformation_typed<double>(py::module& m, std::string const& vtSuffix);
template void define_transformation_typed<storm::RationalNumber>(py::module& m, std::string const& vtSuffix);
template void define_transformation_typed<storm::RationalFunction>(py::module& m, std::string const& vtSuffix);

template void define_transformation_typed_only_numbers<double>(py::module& m, std::string const& vtSuffix);
template void define_transformation_typed_only_numbers<storm::RationalNumber>(py::module& m, std::string const& vtSuffix);

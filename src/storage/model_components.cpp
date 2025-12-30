#include "model_components.h"

#include "storm/adapters/IntervalAdapter.h"
#include "storm/adapters/RationalFunctionAdapter.h"
#include "storm/models/sparse/StandardRewardModel.h"
#include "storm/models/symbolic/StandardRewardModel.h"
#include "storm/storage/sparse/ModelComponents.h"
#include "storm/storage/SparseMatrix.h"
#include "storm/models/sparse/StateLabeling.h"
#include "storm/storage/BitVector.h"


using StateLabeling = storm::models::sparse::StateLabeling;
using BitVector = storm::storage::BitVector;
template<typename ValueType> using SparseMatrix = storm::storage::SparseMatrix<ValueType>;
template<typename ValueType> using SparseRewardModel = storm::models::sparse::StandardRewardModel<ValueType>;

template<typename ValueType> using SparseModelComponents = storm::storage::sparse::ModelComponents<ValueType>;


template<typename ValueType>
void define_sparse_model_components(py::module& m, std::string const& vtSuffix) {

    py::class_<SparseModelComponents<ValueType>, std::shared_ptr<SparseModelComponents<ValueType>>>(m, ("Sparse" + vtSuffix + "ModelComponents").c_str(), "Components required for building a sparse model")

        .def(py::init<SparseMatrix<ValueType> const&, StateLabeling const&, std::unordered_map<std::string, SparseRewardModel<ValueType>> const&,
            bool, boost::optional<BitVector> const&, boost::optional<SparseMatrix<storm::storage::sparse::state_type>> const&>(),
            py::arg("transition_matrix") = SparseMatrix<ValueType>(),
            py::arg("state_labeling") = storm::models::sparse::StateLabeling(),
            py::arg("reward_models") =  std::unordered_map<std::string, SparseRewardModel<ValueType>>(), py::arg("rate_transitions") = false,
            py::arg("markovian_states") = boost::none, py::arg("player1_matrix") = boost::none)

        // General components (for all model types)
        .def_readwrite("transition_matrix", &SparseModelComponents<ValueType>::transitionMatrix, "The transition matrix")
        .def_readwrite("state_labeling", &SparseModelComponents<ValueType>::stateLabeling, "The state labeling")
        .def_readwrite("reward_models", &SparseModelComponents<ValueType>::rewardModels, "Reward models associated with the model")
        .def_readwrite("choice_labeling", &SparseModelComponents<ValueType>::choiceLabeling, "A list that stores a labeling for each choice")
        .def_readwrite("state_valuations", &SparseModelComponents<ValueType>::stateValuations, "A list that stores for each state to which variable valuation it belongs")
        .def_readwrite("choice_origins", &SparseModelComponents<ValueType>::choiceOrigins, "Stores for each choice from which parts of the input model description it originates")

        // POMDP specific components
        .def_readwrite("observability_classes", &SparseModelComponents<ValueType>::observabilityClasses, "The POMDP observations")

        // Continuous time specific components (CTMCs, Markov Automata):
        .def_readwrite("rate_transitions", &SparseModelComponents<ValueType>::rateTransitions, "True iff the transition values (for Markovian choices) are interpreted as rates")
        .def_readwrite("exit_rates", &SparseModelComponents<ValueType>::exitRates, "The exit rate for each state. Must be given for CTMCs and MAs, if rate_transitions is false. Otherwise, it is optional.")
        .def_readwrite("markovian_states", &SparseModelComponents<ValueType>::markovianStates, "A list that stores which states are Markovian (only for Markov Automata)")

        // Stochastic two player game specific components:
        .def_readwrite("player1_matrix", &SparseModelComponents<ValueType>::player1Matrix, "Matrix of player 1 choices (needed for stochastic two player games")

        // Stochastic multiplayer game specific components:
        .def_readwrite("state_player_indications", &SparseModelComponents<ValueType>::statePlayerIndications, "The vector mapping states to player indices")
        ;

}


template void define_sparse_model_components<double>(py::module& m, std::string const& vtSuffix);
template void define_sparse_model_components<storm::RationalNumber>(py::module& m, std::string const& vtSuffix);
template void define_sparse_model_components<storm::Interval>(py::module& m, std::string const& vtSuffix);
template void define_sparse_model_components<storm::RationalFunction>(py::module& m, std::string const& vtSuffix);

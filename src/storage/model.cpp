#include "model.h"
#include "state.h"

#include "storm/adapters/RationalFunctionAdapter.h"
#include "storm/models/ModelBase.h"
#include "storm/models/sparse/Model.h"
#include "storm/models/sparse/Dtmc.h"
#include "storm/models/sparse/Mdp.h"
#include "storm/models/sparse/Pomdp.h"
#include "storm/models/sparse/Ctmc.h"
#include "storm/models/sparse/MarkovAutomaton.h"
#include "storm/models/sparse/Smg.h"
#include "storm/models/sparse/StandardRewardModel.h"
#include "storm/models/symbolic/Model.h"
#include "storm/models/symbolic/Dtmc.h"
#include "storm/models/symbolic/Mdp.h"
#include "storm/models/symbolic/Ctmc.h"
#include "storm/models/symbolic/MarkovAutomaton.h"
#include "storm/models/symbolic/StandardRewardModel.h"
#include "storm/utility/dd.h"

#include "storm/storage/dd/DdManager.h"

#include "storm/storage/Scheduler.h"

#include <functional>
#include <string>
#include <sstream>

// Typedefs
using RationalFunction = storm::RationalFunction;
using ModelBase = storm::models::ModelBase;

template<typename ValueType> using ModelComponents = storm::storage::sparse::ModelComponents<ValueType>;
template<typename ValueType> using SparseModel = storm::models::sparse::Model<ValueType>;
template<typename ValueType> using SparseDeterministicModel = storm::models::sparse::DeterministicModel<ValueType>;
template<typename ValueType> using SparseNondeterministicModel = storm::models::sparse::NondeterministicModel<ValueType>;
template<typename ValueType> using SparseDtmc = storm::models::sparse::Dtmc<ValueType>;
template<typename ValueType> using SparseMdp = storm::models::sparse::Mdp<ValueType>;
template<typename ValueType> using SparsePomdp = storm::models::sparse::Pomdp<ValueType>;
template<typename ValueType> using SparseCtmc = storm::models::sparse::Ctmc<ValueType>;
template<typename ValueType> using SparseMarkovAutomaton = storm::models::sparse::MarkovAutomaton<ValueType>;
template<typename ValueType> using SparseSmg = storm::models::sparse::Smg<ValueType>;
template<typename ValueType> using SparseRewardModel = storm::models::sparse::StandardRewardModel<ValueType>;

template<storm::dd::DdType DdType, typename ValueType> using SymbolicModel = storm::models::symbolic::Model<DdType, ValueType>;
template<storm::dd::DdType DdType, typename ValueType> using SymbolicDtmc = storm::models::symbolic::Dtmc<DdType, ValueType>;
template<storm::dd::DdType DdType, typename ValueType> using SymbolicMdp = storm::models::symbolic::Mdp<DdType, ValueType>;
template<storm::dd::DdType DdType, typename ValueType> using SymbolicCtmc = storm::models::symbolic::Ctmc<DdType, ValueType>;
template<storm::dd::DdType DdType, typename ValueType> using SymbolicMarkovAutomaton = storm::models::symbolic::MarkovAutomaton<DdType, ValueType>;
template<storm::dd::DdType DdType, typename ValueType> using SymbolicRewardModel = storm::models::symbolic::StandardRewardModel<DdType, ValueType>;



// Thin wrappers
template<typename ValueType>
std::vector<storm::storage::sparse::state_type> getSparseInitialStates(SparseModel<ValueType> const& model) {
    std::vector<storm::storage::sparse::state_type> initialStates;
    for (auto entry : model.getInitialStates()) {
        initialStates.push_back(entry);
    }
    return initialStates;
}

template<typename ValueType>
storm::storage::SparseMatrix<ValueType>& getTransitionMatrix(SparseModel<ValueType>& model) {
    return model.getTransitionMatrix();
}

// requires pycarl.Variable
std::set<storm::RationalFunctionVariable> probabilityVariables(SparseModel<RationalFunction> const& model) {
    return storm::models::sparse::getProbabilityParameters(model);
}

std::set<storm::RationalFunctionVariable> rewardVariables(SparseModel<RationalFunction> const& model) {
    return storm::models::sparse::getRewardParameters(model);
}

std::set<storm::RationalFunctionVariable> allVariables(SparseModel<RationalFunction> const& model) {
    return storm::models::sparse::getAllParameters(model);
}

storm::storage::BitVector statesWithParameter(SparseModel<RationalFunction> const& model, storm::RationalFunctionVariable const& var) {
    storm::storage::BitVector result(model.getNumberOfStates());
    for (uint64_t s = 0; s < model.getNumberOfStates(); ++s) {
        for(auto const& entry : model.getTransitionMatrix().getRowGroup(s)) {
            if (entry.getValue().gatherVariables().count(var) > 0) {
                result.set(s);
                break;
            }
        }
    }
    return result;
}


std::string getModelInfoPrinter(ModelBase const& model) {
    std::stringstream ss;
    model.printModelInformationToStream(ss);
    return ss.str();
}

template<typename ValueType>
storm::models::sparse::StateLabeling& getLabeling(SparseModel<ValueType>& model) {
    return model.getStateLabeling();
}


// Bindings for general models
void define_model(py::module& m) {

    // ModelType
    py::enum_<storm::models::ModelType>(m, "ModelType", "Type of the model")
        .value("DTMC", storm::models::ModelType::Dtmc)
        .value("MDP", storm::models::ModelType::Mdp)
        .value("POMDP", storm::models::ModelType::Pomdp)
        .value("CTMC", storm::models::ModelType::Ctmc)
        .value("MA", storm::models::ModelType::MarkovAutomaton)
        .value("SMG", storm::models::ModelType::Smg)
    ;

    // ModelBase
    py::class_<ModelBase, std::shared_ptr<ModelBase>> modelBase(m, "_ModelBase", "Base class for all models");
    modelBase.def_property_readonly("nr_states", &ModelBase::getNumberOfStates, "Number of states")
        .def_property_readonly("nr_transitions", &ModelBase::getNumberOfTransitions, "Number of transitions")
        .def_property_readonly("nr_choices", &ModelBase::getNumberOfChoices, "Number of choices")
        .def_property_readonly("model_type", &ModelBase::getType, "Model type")
        .def_property_readonly("supports_parameters", &ModelBase::supportsParameters, "Flag whether model supports parameters")
        .def_property_readonly("has_parameters", &ModelBase::hasParameters, "Flag whether model has parameters")
        .def_property_readonly("is_exact", &ModelBase::isExact, "Flag whether model is exact")
        .def_property_readonly("is_partially_observable", &ModelBase::isPartiallyObservable, "Flag whether the model has observation labels")
        .def_property_readonly("is_sparse_model", &ModelBase::isSparseModel, "Flag whether the model is stored as a sparse model")
        .def_property_readonly("is_symbolic_model", &ModelBase::isSymbolicModel, "Flag whether the model is stored using decision diagrams")
        .def_property_readonly("is_discrete_time_model", &ModelBase::isDiscreteTimeModel, "Flag whether the model is a discrete time model")
        .def_property_readonly("is_nondeterministic_model", &ModelBase::isNondeterministicModel, "Flag whether the model contains nondeterminism")
        .def("_as_sparse_dtmc", [](ModelBase &modelbase) {
                return modelbase.as<SparseDtmc<double>>();
            }, "Get model as sparse DTMC")
        .def("_as_sparse_exact_dtmc", [](ModelBase &modelbase) {
                return modelbase.as<SparseDtmc<storm::RationalNumber>>();
            }, "Get model as sparse DTMC")
        .def("_as_sparse_pdtmc", [](ModelBase &modelbase) {
                return modelbase.as<SparseDtmc<RationalFunction>>();
            }, "Get model as sparse pDTMC")
        .def("_as_sparse_mdp", [](ModelBase &modelbase) {
                return modelbase.as<SparseMdp<double>>();
            }, "Get model as sparse MDP")
        .def("_as_sparse_exact_mdp", [](ModelBase &modelbase) {
                return modelbase.as<SparseMdp<storm::RationalNumber>>();
            }, "Get model as sparse exact MDP")
        .def("_as_sparse_pmdp", [](ModelBase &modelbase) {
                return modelbase.as<SparseMdp<RationalFunction>>();
            }, "Get model as sparse pMDP")
        .def("_as_sparse_imdp", [](ModelBase &modelbase) {
                return modelbase.as<SparseMdp<storm::Interval>>();
            }, "Get model as sparse interval MDP")
        .def("_as_sparse_pomdp", [](ModelBase &modelbase) {
                return modelbase.as<SparsePomdp<double>>();
            }, "Get model as sparse POMDP")
        .def("_as_sparse_ppomdp", [](ModelBase &modelbase) {
            return modelbase.as<SparsePomdp<RationalFunction>>();
        }, "Get model as sparse pPOMDP")
        .def("_as_sparse_ipomdp", [](ModelBase &modelbase) {
            return modelbase.as<SparsePomdp<storm::Interval>>();
        }, "Get model as sparse interval POMDP")
        .def("_as_sparse_ctmc", [](ModelBase &modelbase) {
                return modelbase.as<SparseCtmc<double>>();
            }, "Get model as sparse CTMC")
        .def("_as_sparse_pctmc", [](ModelBase &modelbase) {
                return modelbase.as<SparseCtmc<RationalFunction>>();
            }, "Get model as sparse pCTMC")
        .def("_as_sparse_ma", [](ModelBase &modelbase) {
                return modelbase.as<SparseMarkovAutomaton<double>>();
            }, "Get model as sparse MA")
        .def("_as_sparse_pma", [](ModelBase &modelbase) {
                return modelbase.as<SparseMarkovAutomaton<RationalFunction>>();
            }, "Get model as sparse pMA")
        .def("_as_sparse_smg", [](ModelBase &modelbase) {
                return modelbase.as<SparseSmg<double>>();
            }, "Get model as sparse SMG")
        .def("_as_symbolic_dtmc", [](ModelBase &modelbase) {
                return modelbase.as<SymbolicDtmc<storm::dd::DdType::Sylvan, double>>();
            }, "Get model as symbolic DTMC")
        .def("_as_symbolic_pdtmc", [](ModelBase &modelbase) {
                return modelbase.as<SymbolicDtmc<storm::dd::DdType::Sylvan, RationalFunction>>();
            }, "Get model as symbolic pDTMC")
        .def("_as_symbolic_mdp", [](ModelBase &modelbase) {
                return modelbase.as<SymbolicMdp<storm::dd::DdType::Sylvan, double>>();
            }, "Get model as symbolic MDP")
        .def("_as_symbolic_pmdp", [](ModelBase &modelbase) {
                return modelbase.as<SymbolicMdp<storm::dd::DdType::Sylvan, RationalFunction>>();
            }, "Get model as symbolic pMDP")
        .def("_as_symbolic_ctmc", [](ModelBase &modelbase) {
                return modelbase.as<SymbolicCtmc<storm::dd::DdType::Sylvan, double>>();
            }, "Get model as symbolic CTMC")
        .def("_as_symbolic_pctmc", [](ModelBase &modelbase) {
                return modelbase.as<SymbolicCtmc<storm::dd::DdType::Sylvan, RationalFunction>>();
            }, "Get model as symbolic pCTMC")
        .def("_as_symbolic_ma", [](ModelBase &modelbase) {
                return modelbase.as<SymbolicMarkovAutomaton<storm::dd::DdType::Sylvan, double>>();
            }, "Get model as symbolic MA")
        .def("_as_symbolic_pma", [](ModelBase &modelbase) {
                return modelbase.as<SymbolicMarkovAutomaton<storm::dd::DdType::Sylvan, RationalFunction>>();
            }, "Get model as symbolic pMA")
    ;
}


// Bindings for sparse models
template<typename ValueType>
void define_sparse_model(py::module& m, std::string const& vtSuffix) {

    // Models with double numbers
    py::class_<SparseModel<ValueType>, std::shared_ptr<SparseModel<ValueType>>, ModelBase> model(m, ("_Sparse" + vtSuffix + "Model").c_str(),
                                                                                           "A probabilistic model where transitions are represented by doubles and saved in a sparse matrix");
    model.def_property_readonly("supports_uncertainty", &SparseModel<ValueType>::supportsUncertainty, "Flag whether model supports uncertainty via intervals")
        .def_property_readonly("labeling", &getLabeling<ValueType>, "Labels")
        .def("has_choice_labeling", [](SparseModel<ValueType> const& model) {return model.hasChoiceLabeling();}, "Does the model have an associated choice labelling?")
        .def_property_readonly("choice_labeling", [](SparseModel<ValueType> const& model) {return model.getChoiceLabeling();}, "get choice labelling")
        .def("has_choice_origins", [](SparseModel<ValueType> const& model) {return model.hasChoiceOrigins();}, "has choice origins?")
        .def_property_readonly("choice_origins", [](SparseModel<ValueType> const& model) {return model.getChoiceOrigins();})
        .def("labels_state", &SparseModel<ValueType>::getLabelsOfState, py::arg("state"), "Get labels of state")
        .def_property_readonly("initial_states", &getSparseInitialStates<ValueType>, "Initial states")
        .def_property_readonly("initial_states_as_bitvector", [](SparseModel<ValueType> const& model) {return model.getInitialStates();})
        .def("set_initial_states", &SparseModel<ValueType>::setInitialStates, py::arg("states"), "Set initial states")
        .def_property_readonly("states", [](SparseModel<ValueType>& model) {
                return SparseModelStates<ValueType>(model);
            }, "Get states")
        .def_property_readonly("reward_models", [](SparseModel<ValueType>& model) {return model.getRewardModels(); }, "Reward models")
        .def_property_readonly("transition_matrix", &getTransitionMatrix<ValueType>, py::return_value_policy::reference, py::keep_alive<1, 0>(), "Transition matrix")
        .def_property_readonly("backward_transition_matrix", &SparseModel<ValueType>::getBackwardTransitions, py::return_value_policy::reference, py::keep_alive<1, 0>(), "Backward transition matrix")
        .def("get_reward_model", [](SparseModel<ValueType>& model, std::string const& name) -> SparseRewardModel<ValueType>& {return model.getRewardModel(name);}, py::return_value_policy::reference, py::keep_alive<1, 0>(), "Reward model")
        .def("has_reward_model", [](SparseModel<ValueType> const& model, std::string const& name) {return model.hasRewardModel(name);}, py::arg("name"))
        .def("add_reward_model", [](SparseModel<ValueType>& model, std::string const& name, SparseRewardModel<ValueType> const& rewModel) { model.addRewardModel(name, rewModel);})
        .def("has_state_valuations", [](SparseModel<ValueType> const& model) {return model.hasStateValuations();}, "has state valuation?")
        .def_property_readonly("state_valuations",  [](SparseModel<ValueType> const& model) {return model.getStateValuations();}, "state valuations")
        .def("reduce_to_state_based_rewards", &SparseModel<ValueType>::reduceToStateBasedRewards)
        .def("is_sink_state", &SparseModel<ValueType>::isSinkState, py::arg("state"))
        .def("__str__", &getModelInfoPrinter)
        .def("to_dot", [](SparseModel<ValueType>& model) { std::stringstream ss; model.writeDotToStream(ss); return ss.str(); }, "Write dot to a string")
    ;
    py::class_<SparseDeterministicModel<ValueType>, std::shared_ptr<SparseDeterministicModel<ValueType>>> detModel(m, ("_SparseDeterministic" + vtSuffix + "Model").c_str(), "Deterministic sparse model", model)
    ;
    py::class_<SparseNondeterministicModel<ValueType>, std::shared_ptr<SparseNondeterministicModel<ValueType>>> nondetModel(m, ("_SparseNondeterministic" + vtSuffix + "Model").c_str(), "Nondeterministic sparse model", model)
    ;

    py::class_<SparseDtmc<ValueType>, std::shared_ptr<SparseDtmc<ValueType>>>(m, ("Sparse" + vtSuffix + "Dtmc").c_str(), "DTMC in sparse representation", detModel)
        .def(py::init<SparseDtmc<ValueType>>(), py::arg("other_model"))
        .def(py::init<ModelComponents<ValueType> const&>(), py::arg("components"))
        .def("__str__", &getModelInfoPrinter)
    ;
    py::class_<SparseMdp<ValueType>, std::shared_ptr<SparseMdp<ValueType>>> mdp(m, ("Sparse" + vtSuffix + "Mdp").c_str(), "MDP in sparse representation", nondetModel);
    mdp.def(py::init<SparseMdp<ValueType>>(), py::arg("other_model"))
        .def(py::init<ModelComponents<ValueType> const&, storm::models::ModelType>(), py::arg("components"), py::arg("type")=storm::models::ModelType::Mdp)
        .def_property_readonly("nondeterministic_choice_indices", [](SparseMdp<ValueType> const& mdp) { return mdp.getNondeterministicChoiceIndices(); })
        .def("get_nr_available_actions", [](SparseMdp<ValueType> const& mdp, uint64_t stateIndex) { return mdp.getNondeterministicChoiceIndices()[stateIndex+1] - mdp.getNondeterministicChoiceIndices()[stateIndex] ; }, py::arg("state"))
        .def("get_choice_index", [](SparseMdp<ValueType> const& mdp, uint64_t state, uint64_t actOff) { return mdp.getNondeterministicChoiceIndices()[state]+actOff; }, py::arg("state"), py::arg("action_offset"), "gets the choice index for the offset action from the given state.")
        .def("apply_scheduler", [](SparseMdp<ValueType> const& mdp, storm::storage::Scheduler<ValueType> const& scheduler, bool dropUnreachableStates) { return mdp.applyScheduler(scheduler, dropUnreachableStates); } , "apply scheduler", "scheduler"_a, "drop_unreachable_states"_a = true)
        .def("__str__", &getModelInfoPrinter)
    ;
    py::class_<SparsePomdp<ValueType>, std::shared_ptr<SparsePomdp<ValueType>>>(m, ("Sparse" + vtSuffix + "Pomdp").c_str(), "POMDP in sparse representation", mdp)
        .def(py::init<SparsePomdp<ValueType>>(), py::arg("other_model"))
        .def(py::init<ModelComponents<ValueType> const&, bool>(), py::arg("components"), py::arg("canonic_flag")=false)
        .def("__str__", &getModelInfoPrinter)
        .def("get_observation", &SparsePomdp<ValueType>::getObservation, py::arg("state"))
        .def_property_readonly("observations", &SparsePomdp<ValueType>::getObservations)
        .def_property_readonly("nr_observations", &SparsePomdp<ValueType>::getNrObservations)
        .def("has_observation_valuations", &SparsePomdp<ValueType>::hasObservationValuations)
        .def_property_readonly("observation_valuations", &SparsePomdp<ValueType>::getObservationValuations)
    ;
    py::class_<SparseCtmc<ValueType>, std::shared_ptr<SparseCtmc<ValueType>>>(m, ("Sparse" + vtSuffix + "Ctmc").c_str(), "CTMC in sparse representation", detModel)
        .def(py::init<SparseCtmc<ValueType>>(), py::arg("other_model"))
        .def(py::init<ModelComponents<ValueType> const&>(), py::arg("components"))
        .def_property_readonly("exit_rates", [](SparseCtmc<ValueType> const& ctmc) { return ctmc.getExitRateVector(); })
        .def("__str__", &getModelInfoPrinter)
    ;
    py::class_<SparseMarkovAutomaton<ValueType>, std::shared_ptr<SparseMarkovAutomaton<ValueType>>>(m, ("Sparse" + vtSuffix + "MA").c_str(), "MA in sparse representation", nondetModel)
        .def(py::init<SparseMarkovAutomaton<ValueType>>(), py::arg("other_model"))
        .def(py::init<ModelComponents<ValueType> const&>(), py::arg("components"))
        .def_property_readonly("exit_rates", [](SparseMarkovAutomaton<ValueType> const& ma) { return ma.getExitRates(); })
        .def_property_readonly("markovian_states", [](SparseMarkovAutomaton<ValueType> const& ma) { return ma.getMarkovianStates(); })
        .def_property_readonly("nondeterministic_choice_indices", [](SparseMarkovAutomaton<ValueType> const& ma) { return ma.getNondeterministicChoiceIndices(); })
        .def("apply_scheduler", [](SparseMarkovAutomaton<ValueType> const& ma, storm::storage::Scheduler<ValueType> const& scheduler, bool dropUnreachableStates) { return ma.applyScheduler(scheduler, dropUnreachableStates); } , "apply scheduler", "scheduler"_a, "drop_unreachable_states"_a = true)
        .def("__str__", &getModelInfoPrinter)
        .def_property_readonly("convertible_to_ctmc", &SparseMarkovAutomaton<ValueType>::isConvertibleToCtmc, "Check whether the MA can be converted into a CTMC.")
        .def("convert_to_ctmc", &SparseMarkovAutomaton<ValueType>::convertToCtmc, "Convert the MA into a CTMC.")
    ;

    py::class_<SparseSmg<ValueType>, std::shared_ptr<SparseSmg<ValueType>>>(m, ("Sparse" + vtSuffix + "Smg").c_str(), "SMG in sparse representation", nondetModel)
        .def(py::init<SparseSmg<ValueType>>(), py::arg("other_model"))
        .def(py::init<ModelComponents<ValueType> const&>(), py::arg("components"))
        .def("get_state_player_indications", &SparseSmg<ValueType>::getStatePlayerIndications, "Get for each state its corresponding player")
        .def("get_player_of_state", &SparseSmg<ValueType>::getPlayerOfState, py::arg("state"), "Get player for the given state")
    ;

    py::class_<SparseRewardModel<ValueType>>(m, ("Sparse" + vtSuffix + "RewardModel").c_str(), "Reward structure for sparse models")
        .def(py::init<std::optional<std::vector<ValueType>> const&, std::optional<std::vector<ValueType>> const&,
                std::optional<storm::storage::SparseMatrix<ValueType>> const&>(), py::arg("optional_state_reward_vector") = std::nullopt,
                py::arg("optional_state_action_reward_vector") = std::nullopt,  py::arg("optional_transition_reward_matrix") = std::nullopt)
        .def_property_readonly("has_state_rewards", &SparseRewardModel<ValueType>::hasStateRewards)
        .def_property_readonly("has_state_action_rewards", &SparseRewardModel<ValueType>::hasStateActionRewards)
        .def_property_readonly("has_transition_rewards", &SparseRewardModel<ValueType>::hasTransitionRewards)
        .def_property_readonly("transition_rewards", [](SparseRewardModel<ValueType>& rewardModel) {return rewardModel.getTransitionRewardMatrix();})
        .def_property_readonly("state_rewards", [](SparseRewardModel<ValueType>& rewardModel) {return rewardModel.getStateRewardVector();})
        .def("get_state_reward", [](SparseRewardModel<ValueType>& rewardModel, uint64_t state) {return rewardModel.getStateReward(state);})
        .def("set_state_reward", [](SparseRewardModel<ValueType>& rewardModel, uint64_t state, ValueType const& value) {return rewardModel.setStateReward(state, value);})
        .def("get_zero_reward_states", &SparseRewardModel<ValueType>::template getStatesWithZeroReward<ValueType>, "get states where all rewards are zero", py::arg("transition_matrix"))
        .def("get_state_action_reward", [](SparseRewardModel<ValueType>& rewardModel, uint64_t action_index) {return rewardModel.getStateActionReward(action_index);})
        .def_property_readonly("state_action_rewards", [](SparseRewardModel<ValueType>& rewardModel) {return rewardModel.getStateActionRewardVector();})
        .def("reduce_to_state_based_rewards", [](SparseRewardModel<ValueType>& rewardModel, storm::storage::SparseMatrix<ValueType> const& transitions, bool onlyStateRewards){return rewardModel.reduceToStateBasedRewards(transitions, onlyStateRewards);},  py::arg("transition_matrix"), py::arg("only_state_rewards"), "Reduce to state-based rewards")
    ;

}

void define_sparse_parametric_model(py::module& m) {
    // Parametric models
    py::class_<SparseModel<RationalFunction>, std::shared_ptr<SparseModel<RationalFunction>>, ModelBase> modelRatFunc(m, "_SparseParametricModel", "A probabilistic model where transitions are represented by rational functions and saved in a sparse matrix");
    modelRatFunc.def("collect_probability_parameters", &probabilityVariables, "Collect parameters")
        .def("collect_reward_parameters", &rewardVariables, "Collect reward parameters")
        .def("collect_all_parameters", &allVariables, "Collect all parameters")
        .def("get_states_with_parameter", &statesWithParameter, py::arg("parameter"), "Find states with a particular parameter")
        .def("has_choice_labeling", [](SparseModel<RationalFunction> const& model) {return model.hasChoiceLabeling();}, "Does the model have an associated choice labelling?")
        .def_property_readonly("choice_labeling", [](SparseModel<RationalFunction> const& model) {return model.getChoiceLabeling();}, "get choice labelling")
        .def("has_choice_origins", [](SparseModel<RationalFunction> const& model) {return model.hasChoiceOrigins();}, "has choice origins?")
        .def_property_readonly("choice_origins", [](SparseModel<RationalFunction> const& model) {return model.getChoiceOrigins();})

        .def_property_readonly("labeling", &getLabeling<RationalFunction>, "Labels")
        .def("labels_state", &SparseModel<RationalFunction>::getLabelsOfState, py::arg("state"), "Get labels of state")
        .def_property_readonly("initial_states", &getSparseInitialStates<RationalFunction>, "Initial states")
        .def_property_readonly("initial_states_as_bitvector", [](SparseModel<RationalFunction> const& model) {return model.getInitialStates();})
        .def_property_readonly("states", [](SparseModel<RationalFunction>& model) {
                return SparseModelStates<RationalFunction>(model);
            }, "Get states")
        .def_property_readonly("reward_models", [](SparseModel<RationalFunction> const& model) {return model.getRewardModels(); }, "Reward models")
        .def_property_readonly("transition_matrix", &getTransitionMatrix<RationalFunction>, py::return_value_policy::reference, py::keep_alive<1, 0>(), "Transition matrix")
        .def_property_readonly("backward_transition_matrix", &SparseModel<RationalFunction>::getBackwardTransitions, py::return_value_policy::reference, py::keep_alive<1, 0>(), "Backward transition matrix")
        .def("get_reward_model", [](SparseModel<RationalFunction>& model, std::string const& name) -> SparseRewardModel<RationalFunction>& {return model.getRewardModel(name);}, py::return_value_policy::reference, py::keep_alive<1, 0>(), "Reward model")
        .def("add_reward_model", [](SparseModel<RationalFunction>& model, std::string const& name, SparseRewardModel<RationalFunction> const& rewModel) { model.addRewardModel(name, rewModel);})
        .def("has_state_valuations", [](SparseModel<RationalFunction> const& model) {return model.hasStateValuations();}, "has state valuation?")
        .def_property_readonly("state_valuations",  [](SparseModel<RationalFunction> const& model) {return model.getStateValuations();}, "state valuations")
        .def("reduce_to_state_based_rewards", &SparseModel<RationalFunction>::reduceToStateBasedRewards)
        .def("is_sink_state", &SparseModel<RationalFunction>::isSinkState, py::arg("state"))
        .def("__str__", &getModelInfoPrinter)
        .def("to_dot", [](SparseModel<RationalFunction>& model) { std::stringstream ss; model.writeDotToStream(ss); return ss.str(); }, "Write dot to a string")
    ;
    py::class_<SparseDeterministicModel<RationalFunction>, std::shared_ptr<SparseDeterministicModel<RationalFunction>>> detModelRatFunc(m, "_SparseParametricDeterministicModel", "Parametric deterministic sparse model", modelRatFunc)
    ;
    py::class_<SparseNondeterministicModel<RationalFunction>, std::shared_ptr<SparseNondeterministicModel<RationalFunction>>> nondetModelRatFunc(m, "_SparseParametricNondeterministicModel", "Parametric nondeterministic sparse model", modelRatFunc)
    ;

    py::class_<SparseDtmc<RationalFunction>, std::shared_ptr<SparseDtmc<RationalFunction>>>(m, "SparseParametricDtmc", "pDTMC in sparse representation", detModelRatFunc)
        .def(py::init<ModelComponents<RationalFunction> const&>(), py::arg("components"))
        .def("__str__", &getModelInfoPrinter)
    ;
    py::class_<SparseMdp<RationalFunction>, std::shared_ptr<SparseMdp<RationalFunction>>> pmdp(m, "SparseParametricMdp", "pMDP in sparse representation", nondetModelRatFunc);
    pmdp.def(py::init<ModelComponents<RationalFunction> const&>(), py::arg("components"))
        .def_property_readonly("nondeterministic_choice_indices", [](SparseMdp<RationalFunction> const& mdp) { return mdp.getNondeterministicChoiceIndices(); })
        .def("apply_scheduler", [](SparseMdp<RationalFunction> const& mdp, storm::storage::Scheduler<RationalFunction> const& scheduler, bool dropUnreachableStates) { return mdp.applyScheduler(scheduler, dropUnreachableStates); } , "apply scheduler", "scheduler"_a, "drop_unreachable_states"_a = true)
        .def("get_nr_available_actions", [](SparseMdp<RationalFunction> const& mdp, uint64_t stateIndex) { return mdp.getNondeterministicChoiceIndices()[stateIndex+1] - mdp.getNondeterministicChoiceIndices()[stateIndex] ; }, py::arg("state"))
        .def("__str__", &getModelInfoPrinter)
    ;

    py::class_<SparsePomdp<RationalFunction>, std::shared_ptr<SparsePomdp<RationalFunction>>>(m, "SparseParametricPomdp", "POMDP in sparse representation", pmdp)

        .def(py::init<SparsePomdp<RationalFunction>>(), py::arg("other_model"))
        .def(py::init<ModelComponents<RationalFunction> const&>(), py::arg("components"))
        .def("__str__", &getModelInfoPrinter)
        .def("get_observation", &SparsePomdp<RationalFunction>::getObservation, py::arg("state"))
        .def_property_readonly("observations", &SparsePomdp<RationalFunction>::getObservations)
        .def_property_readonly("nr_observations", &SparsePomdp<RationalFunction>::getNrObservations)
    ;

    py::class_<SparseCtmc<RationalFunction>, std::shared_ptr<SparseCtmc<RationalFunction>>>(m, "SparseParametricCtmc", "pCTMC in sparse representation", detModelRatFunc)
        .def(py::init<ModelComponents<RationalFunction> const&>(), py::arg("components"))
        .def("__str__", &getModelInfoPrinter)
    ;
    py::class_<SparseMarkovAutomaton<RationalFunction>, std::shared_ptr<SparseMarkovAutomaton<RationalFunction>>>(m, "SparseParametricMA", "pMA in sparse representation", nondetModelRatFunc)
        .def(py::init<ModelComponents<RationalFunction> const&>(), py::arg("components"))
        .def_property_readonly("nondeterministic_choice_indices", [](SparseMarkovAutomaton<RationalFunction> const& ma) { return ma.getNondeterministicChoiceIndices(); })
        .def("apply_scheduler", [](SparseMarkovAutomaton<RationalFunction> const& ma, storm::storage::Scheduler<RationalFunction> const& scheduler, bool dropUnreachableStates) { return ma.applyScheduler(scheduler, dropUnreachableStates); } , "apply scheduler", "scheduler"_a, "drop_unreachable_states"_a = true)
        .def("__str__", &getModelInfoPrinter)
    ;

    py::class_<SparseRewardModel<RationalFunction>>(m, "SparseParametricRewardModel", "Reward structure for parametric sparse models")
        .def(py::init<std::optional<std::vector<RationalFunction>> const&, std::optional<std::vector<RationalFunction>> const&,
                std::optional<storm::storage::SparseMatrix<RationalFunction>> const&>(), py::arg("optional_state_reward_vector") = std::nullopt,
                py::arg("optional_state_action_reward_vector") = std::nullopt,  py::arg("optional_transition_reward_matrix") = std::nullopt)
        .def_property_readonly("has_state_rewards", &SparseRewardModel<RationalFunction>::hasStateRewards)
        .def_property_readonly("has_state_action_rewards", &SparseRewardModel<RationalFunction>::hasStateActionRewards)
        .def_property_readonly("has_transition_rewards", &SparseRewardModel<RationalFunction>::hasTransitionRewards)
        .def_property_readonly("transition_rewards", [](SparseRewardModel<RationalFunction>& rewardModel) {return rewardModel.getTransitionRewardMatrix();})
        .def_property_readonly("state_rewards", [](SparseRewardModel<RationalFunction>& rewardModel) {return rewardModel.getStateRewardVector();})
        .def("get_state_reward", [](SparseRewardModel<RationalFunction>& rewardModel, uint64_t state) {return rewardModel.getStateReward(state);})
        .def("get_state_action_reward", [](SparseRewardModel<RationalFunction>& rewardModel, uint64_t action_index) {return rewardModel.getStateActionReward(action_index);})

        .def_property_readonly("state_action_rewards", [](SparseRewardModel<RationalFunction>& rewardModel) {return rewardModel.getStateActionRewardVector();})
        .def("reduce_to_state_based_rewards", [](SparseRewardModel<RationalFunction>& rewardModel, storm::storage::SparseMatrix<RationalFunction> const& transitions, bool onlyStateRewards){return rewardModel.reduceToStateBasedRewards(transitions, onlyStateRewards);},  py::arg("transition_matrix"), py::arg("only_state_rewards"), "Reduce to state-based rewards")
    ;

}


// Bindings for symbolic models
template<storm::dd::DdType DdType>
void define_symbolic_model(py::module& m, std::string vt_suffix) {

    // Set class names
    std::string prefixClassName = "Symbolic" + vt_suffix;
    std::string prefixParametricClassName = "Symbolic" + vt_suffix + "Parametric";


    // Models with double numbers
    py::class_<SymbolicModel<DdType, double>, std::shared_ptr<SymbolicModel<DdType, double>>, ModelBase> model(m, ("_"+prefixClassName+"Model").c_str(), "A probabilistic model where transitions are represented by doubles and saved in a symbolic representation");
    model.def_property_readonly("reward_models", [](SymbolicModel<DdType, double>& model) {return model.getRewardModels(); }, "Reward models")
        .def_property_readonly("dd_manager", &SymbolicModel<DdType, double>::getManager, "dd manager")
    .def_property_readonly("reachable_states", &SymbolicModel<DdType, double>::getReachableStates, "reachable states as DD")
        .def_property_readonly("initial_states", &SymbolicModel<DdType, double>::getInitialStates, "initial states as DD")
        .def("get_states", [](SymbolicModel<DdType, double> const& model, storm::expressions::Expression const& expr) {return model.getStates(expr);}, py::arg("expression"), "Get states that are described by the expression")
        .def("compute_depth", [](SymbolicModel<DdType, double> const& model) {return storm::utility::dd::computeReachableStates(model.getInitialStates(), model.getQualitativeTransitionMatrix(false), model.getRowVariables(), model.getColumnVariables()).second;}, "Computes the depth of the model, i.e., the distance to the node with the largest minimal distance from the initial states")
        .def("reduce_to_state_based_rewards", &SymbolicModel<DdType, double>::reduceToStateBasedRewards)
        .def("__str__", &getModelInfoPrinter)
    ;
    py::class_<SymbolicDtmc<DdType, double>, std::shared_ptr<SymbolicDtmc<DdType, double>>>(m, (prefixClassName+"Dtmc").c_str(), "DTMC in symbolic representation", model)
        .def("__str__", &getModelInfoPrinter)
    ;
    py::class_<SymbolicMdp<DdType, double>, std::shared_ptr<SymbolicMdp<DdType, double>>>(m, (prefixClassName+"Mdp").c_str(), "MDP in symbolic representation", model)
        .def("__str__", &getModelInfoPrinter)
    ;
    py::class_<SymbolicCtmc<DdType, double>, std::shared_ptr<SymbolicCtmc<DdType, double>>>(m, (prefixClassName+"Ctmc").c_str(), "CTMC in symbolic representation", model)
        .def("__str__", &getModelInfoPrinter)
    ;
    py::class_<SymbolicMarkovAutomaton<DdType, double>, std::shared_ptr<SymbolicMarkovAutomaton<DdType, double>>>(m, (prefixClassName+"MA").c_str(), "MA in symbolic representation", model)
        .def("__str__", &getModelInfoPrinter)
    ;

    py::class_<SymbolicRewardModel<DdType, double>>(m, (prefixClassName+"RewardModel").c_str(), "Reward structure for symbolic models")
        .def_property_readonly("has_state_rewards", &SymbolicRewardModel<DdType, double>::hasStateRewards)
        .def_property_readonly("has_state_action_rewards", &SymbolicRewardModel<DdType, double>::hasStateActionRewards)
        .def_property_readonly("has_transition_rewards", &SymbolicRewardModel<DdType, double>::hasTransitionRewards)
    ;


    // Parametric models
    py::class_<SymbolicModel<DdType, RationalFunction>, std::shared_ptr<SymbolicModel<DdType, RationalFunction>>, ModelBase> modelRatFunc(m, ("_"+prefixParametricClassName+"Model").c_str(), "A probabilistic model where transitions are represented by rational functions and saved in a symbolic representation");
    modelRatFunc.def("get_parameters", &SymbolicModel<DdType, RationalFunction>::getParameters, "Get parameters")
        .def_property_readonly("reward_models", [](SymbolicModel<DdType, RationalFunction> const& model) {return model.getRewardModels(); }, "Reward models")
        .def_property_readonly("reachable_states", &SymbolicModel<DdType, RationalFunction>::getReachableStates, "reachable states as DD")
        .def_property_readonly("initial_states", &SymbolicModel<DdType, RationalFunction>::getInitialStates, "initial states as DD")
        .def("get_states", [](SymbolicModel<DdType, RationalFunction> const& model, storm::expressions::Expression const& expr) {return model.getStates(expr);}, py::arg("expression"), "Get states that are described by the expression")
        .def("reduce_to_state_based_rewards", &SymbolicModel<DdType, RationalFunction>::reduceToStateBasedRewards)
        .def("__str__", &getModelInfoPrinter)
    ;

    py::class_<SymbolicDtmc<DdType, RationalFunction>, std::shared_ptr<SymbolicDtmc<DdType, RationalFunction>>>(m, (prefixParametricClassName+"Dtmc").c_str(), "pDTMC in symbolic representation", modelRatFunc)
        .def("__str__", &getModelInfoPrinter)
    ;
    py::class_<SymbolicMdp<DdType, RationalFunction>, std::shared_ptr<SymbolicMdp<DdType, RationalFunction>>>(m, (prefixParametricClassName+"Mdp").c_str(), "pMDP in symbolic representation", modelRatFunc)
        .def("__str__", &getModelInfoPrinter)
    ;
    py::class_<SymbolicCtmc<DdType, RationalFunction>, std::shared_ptr<SymbolicCtmc<DdType, RationalFunction>>>(m, (prefixParametricClassName+"Ctmc").c_str(), "pCTMC in symbolic representation", modelRatFunc)
        .def("__str__", &getModelInfoPrinter)
    ;
    py::class_<SymbolicMarkovAutomaton<DdType, RationalFunction>, std::shared_ptr<SymbolicMarkovAutomaton<DdType, RationalFunction>>>(m, (prefixParametricClassName+"MA").c_str(), "pMA in symbolic representation", modelRatFunc)
        .def("__str__", &getModelInfoPrinter)
    ;

    py::class_<SymbolicRewardModel<DdType, RationalFunction>>(m, (prefixParametricClassName+"RewardModel").c_str(), "Reward structure for parametric symbolic models")
        .def_property_readonly("has_state_rewards", &SymbolicRewardModel<DdType, RationalFunction>::hasStateRewards)
        .def_property_readonly("has_state_action_rewards", &SymbolicRewardModel<DdType, RationalFunction>::hasStateActionRewards)
        .def_property_readonly("has_transition_rewards", &SymbolicRewardModel<DdType, RationalFunction>::hasTransitionRewards)
    ;

}

template void define_symbolic_model<storm::dd::DdType::Sylvan>(py::module& m, std::string vt_suffix);
template void define_sparse_model<double>(py::module& m, std::string const& vt_suffix);
template void define_sparse_model<storm::RationalNumber>(py::module& m, std::string const& vt_suffix);
template void define_sparse_model<storm::Interval>(py::module& m, std::string const& vt_suffix);

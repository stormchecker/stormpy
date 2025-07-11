#include "quantitative_analysis.h"

#include "storm/adapters/RationalFunctionAdapter.h"
#include "storm/models/sparse/Pomdp.h"
#include "storm-pomdp/api/verification.h"

template<typename ValueType> using Pomdp = storm::models::sparse::Pomdp<ValueType, typename storm::models::sparse::StandardRewardModel<ValueType>>;
template<typename ValueType> using BeliefExplorationPomdpModelChecker = typename storm::pomdp::modelchecker::BeliefExplorationPomdpModelChecker<Pomdp<ValueType>, ValueType, ValueType>;
template<typename ValueType> using BeliefExplorationPomdpModelCheckerResult = typename storm::pomdp::modelchecker::BeliefExplorationPomdpModelChecker<ValueType>::Result;
template<typename ValueType> using Options = storm::pomdp::modelchecker::BeliefExplorationPomdpModelCheckerOptions<ValueType>;
template<typename ValueType> using additionalCutoffValueType = std::vector<std::vector<std::unordered_map<uint64_t, ValueType>>>;


template<typename ValueType>
void define_belief_exploration(py::module& m, std::string const& vtSuffix) {
    py::class_<BeliefExplorationPomdpModelChecker<ValueType>> belmc(m, ("BeliefExplorationModelChecker" + vtSuffix).c_str());
    belmc.def(py::init<std::shared_ptr<Pomdp<ValueType>>, Options<ValueType>>(), py::arg("model"), py::arg("options"));

    belmc.def("check", py::overload_cast<storm::logic::Formula const&,additionalCutoffValueType<ValueType> const&>(&BeliefExplorationPomdpModelChecker<ValueType>::check), py::arg("formula"), py::arg("cutoff_values"));
    belmc.def("check_with_preprocessing_environment", py::overload_cast<storm::logic::Formula const&, storm::Environment const&, additionalCutoffValueType<ValueType> const&>(&BeliefExplorationPomdpModelChecker<ValueType>::check), py::arg("formula"), py::arg("pre_processing_environment"), py::arg("cutoff_values"));
    belmc.def("check_with_environment", py::overload_cast<storm::Environment const&, storm::logic::Formula const&, additionalCutoffValueType<ValueType> const&>(&BeliefExplorationPomdpModelChecker<ValueType>::check), py::arg("environment"), py::arg("formula"), py::arg("cutoff_values"));
    belmc.def("check_with_environment_and_pre_processing_environment", py::overload_cast<storm::Environment const&, storm::logic::Formula const&, storm::Environment const&, additionalCutoffValueType<ValueType> const&>(&BeliefExplorationPomdpModelChecker<ValueType>::check), py::arg("environment"), py::arg("formula"), py::arg("pre_processing_environment"), py::arg("cutoff_values"));

    belmc.def("pause_unfolding", &BeliefExplorationPomdpModelChecker<ValueType>::pauseUnfolding);
    belmc.def("continue_unfolding", &BeliefExplorationPomdpModelChecker<ValueType>::continueUnfolding);
    belmc.def("terminate_unfolding", &BeliefExplorationPomdpModelChecker<ValueType>::terminateUnfolding);
    belmc.def("is_result_ready", &BeliefExplorationPomdpModelChecker<ValueType>::isResultReady);
    belmc.def("is_exploring", &BeliefExplorationPomdpModelChecker<ValueType>::isExploring);
    belmc.def("get_interactive_result", &BeliefExplorationPomdpModelChecker<ValueType>::getInteractiveResult);
    belmc.def("get_status", &BeliefExplorationPomdpModelChecker<ValueType>::getStatus);
    belmc.def("get_interactive_belief_explorer", &BeliefExplorationPomdpModelChecker<ValueType>::getInteractiveBeliefExplorer);
    belmc.def("has_converged", &BeliefExplorationPomdpModelChecker<ValueType>::hasConverged);
    belmc.def("set_fsc_values", &BeliefExplorationPomdpModelChecker<ValueType>::setFMSchedValueList, py::arg("value_list"));

    py::class_<typename storm::builder::BeliefMdpExplorer<Pomdp<ValueType>, ValueType>> belmdpexpl(m, ("BeliefMdpExplorer" + vtSuffix).c_str());
    belmdpexpl.def("set_fsc_values", &storm::builder::BeliefMdpExplorer<Pomdp<ValueType>, ValueType>::setFMSchedValueList, py::arg("value_list"));

    py::class_<Options<ValueType>> belexploptions(m, ("BeliefExplorationModelCheckerOptions" + vtSuffix).c_str());
    belexploptions.def(py::init<bool, bool>(), py::arg("discretize"), py::arg("unfold"));
    belexploptions.def_readwrite("use_state_elimination_cutoff", &Options<ValueType>::useStateEliminationCutoff);
    belexploptions.def_readwrite("size_threshold_init", &Options<ValueType>::sizeThresholdInit);
    belexploptions.def_readwrite("use_clipping", &Options<ValueType>::useClipping);
    belexploptions.def_readwrite("exploration_time_limit", &Options<ValueType>::explorationTimeLimit);
    belexploptions.def_readwrite("clipping_grid_res", &Options<ValueType>::clippingGridRes);
    belexploptions.def_readwrite("gap_threshold_init", &Options<ValueType>::gapThresholdInit);
    belexploptions.def_readwrite("size_threshold_factor", &Options<ValueType>::sizeThresholdFactor);
    belexploptions.def_readwrite("refine_precision", &Options<ValueType>::refinePrecision);
    belexploptions.def_readwrite("refine_step_limit", &Options<ValueType>::refineStepLimit);
    belexploptions.def_readwrite("refine", &Options<ValueType>::refine);
    belexploptions.def_readwrite("exploration_heuristic", &Options<ValueType>::explorationHeuristic);
    belexploptions.def_readwrite("skip_heuristic_schedulers", &Options<ValueType>::skipHeuristicSchedulers);
    belexploptions.def_readwrite("interactive_unfolding", &Options<ValueType>::interactiveUnfolding);
    belexploptions.def_readwrite("cut_zero_gap", &Options<ValueType>::cutZeroGap);

    py::class_<typename BeliefExplorationPomdpModelChecker<ValueType>::Result> belexplres(m, ("BeliefExplorationPomdpModelCheckerResult" + vtSuffix).c_str());
    belexplres.def_readonly("induced_mc_from_scheduler", &BeliefExplorationPomdpModelChecker<ValueType>::Result::schedulerAsMarkovChain);
    belexplres.def_readonly("cutoff_schedulers", &BeliefExplorationPomdpModelChecker<ValueType>::Result::cutoffSchedulers);
    belexplres.def_readonly("lower_bound", &BeliefExplorationPomdpModelChecker<ValueType>::Result::lowerBound);
    belexplres.def_readonly("upper_bound", &BeliefExplorationPomdpModelChecker<ValueType>::Result::upperBound);

    m.def("create_interactive_mc", &storm::pomdp::api::createInteractiveUnfoldingModelChecker<ValueType>, py::arg("env"), py::arg("pomdp"), py::arg("use_clipping"));
}

template void define_belief_exploration<double>(py::module& m, std::string const& vtSuffix);
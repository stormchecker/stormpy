#include "belief_verification.h"

#include <map>
#include <sstream>
#include <storm-pomdp/api/verification.h>
#include <storm/logic/Formula.h>

#include "src/binding_type_index.h"
#include "src/helpers.h"
#include "src/numbers.h"

template<typename ValueType>
using SparsePomdp = storm::models::sparse::Pomdp<ValueType>;
template<typename ValueType>
using Options = storm::pomdp::beliefs::BeliefBasedModelCheckerOptions<ValueType>;
template<typename ValueType>
using Result = storm::pomdp::beliefs::BeliefBasedModelCheckerResult<ValueType>;
template<typename ValueType>
using Controller = storm::pomdp::policy::ObservationBasedFiniteStateController<ValueType>;
using Statistics = storm::pomdp::beliefs::BeliefBasedModelCheckerStatistics;

template<typename ValueType>
void define_belief_verification(py::module& m) {
    auto index = stormpy::bindings::typeIndex<ValueType>();

    stormpy::bindings::bindTemplateClass<Options<ValueType>>(m, "BeliefBasedModelCheckerOptions", index, "Options for belief-based verification of POMDPs")
        .def(py::init<>())
        .def_readwrite("build_choice_labeling", &Options<ValueType>::buildChoiceLabeling, "Build choice labels for the belief MDP")
        .def_readwrite("generate_policy", &Options<ValueType>::generatePolicy, "Generate a finite-state controller")
        .def_readwrite("use_clipping", &Options<ValueType>::useClipping, "Use belief clipping")
        .def_readwrite("cut_zero_gap", &Options<ValueType>::cutZeroGap,
                       "Cut non-target beliefs whose preprocessing bounds have zero gap. Incompatible with generating a policy")
        .def_readwrite("exploration_queue_order", &Options<ValueType>::explorationQueueOrder, "Order in which discovered beliefs are explored")
        .def_readwrite("clipping_resolutions", &Options<ValueType>::clippingResolutions, "Clipping resolution for each observation")
        .def_readwrite("max_exploration_size", &Options<ValueType>::maxExplorationSize, "Maximal number of discovered beliefs, None for no limit")
        .def_readwrite("max_exploration_time", &Options<ValueType>::maxExplorationTime, "Maximal exploration time in seconds, None for no limit");

    stormpy::bindings::bindTemplateClass<Controller<ValueType>>(m, "ObservationBasedFiniteStateController", index,
                                                                "Observation-based finite-state controller for a POMDP")
        .def_property_readonly("initial_node", &Controller<ValueType>::getInitialNodeId, "Initial memory node")
        .def("is_deterministic", &Controller<ValueType>::isDeterministic, "Whether all outputs are deterministic")
        .def("has_output", &Controller<ValueType>::hasOutputForObservationInNode, "Whether an output is defined for the observation in the memory node",
             "node"_a, "observation"_a)
        .def("is_randomised", &Controller<ValueType>::outputIsRandomised, "Whether the output for the observation in the memory node is randomised", "node"_a,
             "observation"_a)
        .def("get_action", &Controller<ValueType>::getActionForObservationInNode,
             "Local action chosen for the observation in the memory node (deterministic outputs only)", "node"_a, "observation"_a)
        .def("get_successor", &Controller<ValueType>::getSuccessorForObservationInNode, "Successor memory node for the observation in the memory node",
             "node"_a, "observation"_a)
        .def(
            "get_action_distribution",
            [](Controller<ValueType> const& controller, uint64_t node, uint64_t observation) {
                std::map<uint64_t, ValueType> result;
                for (auto const& [action, probability] : controller.getActionDistributionForObservationInNode(node, observation)) {
                    result.emplace(action, probability);
                }
                return result;
            },
            "Distribution over local actions for the observation in the memory node, as a dict from action to probability", "node"_a, "observation"_a)
        .def("has_action_name", &Controller<ValueType>::hasActionName, "Whether the local action of the observation has a name", "observation"_a, "action"_a)
        .def("get_action_name", &Controller<ValueType>::getActionName, "Name of the local action of the observation", "observation"_a, "action"_a)
        .def(
            "to_dot",
            [](Controller<ValueType> const& controller) {
                std::stringstream stream;
                controller.writeDotToStream(stream);
                return stream.str();
            },
            "Graphviz DOT representation")
        .def(
            "to_json",
            [](Controller<ValueType> const& controller) {
                std::stringstream stream;
                controller.writeJsonToStream(stream);
                return stream.str();
            },
            "JSON representation")
        .def("__str__", &Controller<ValueType>::toString);

    stormpy::bindings::bindTemplateClass<Result<ValueType>>(m, "BeliefBasedModelCheckerResult", index, "Result of belief-based verification of a POMDP")
        .def_readonly("value", &Result<ValueType>::value, "Computed bound on the value")
        .def_readonly("completed_exploration", &Result<ValueType>::completedExploration, "Whether the exploration was completed")
        .def_readonly("statistics", &Result<ValueType>::statistics, "Statistics of the run")
        .def_property_readonly(
            "policy",
            [](Result<ValueType> const& result) -> Controller<ValueType> const* { return result.policy.has_value() ? &result.policy.value() : nullptr; },
            py::return_value_policy::reference_internal, "Finite-state controller, None if no policy was generated");

    // Only the same value types everywhere are bound.
    m.def(
        "verify_with_belief_unfolding",
        [](storm::Environment const& env, SparsePomdp<ValueType> const& pomdp, storm::logic::Formula const& formula, Options<ValueType> const& options) {
            return storm::pomdp::api::verifyWithBeliefUnfolding<ValueType, ValueType, ValueType, ValueType>(env, pomdp, formula, options);
        },
        "Approximate an unbounded reachability probability or expected reachability reward by unfolding the belief MDP", "env"_a, "pomdp"_a, "formula"_a,
        "options"_a);
    m.def(
        "verify_with_belief_discretization",
        [](storm::Environment const& env, SparsePomdp<ValueType> const& pomdp, storm::logic::Formula const& formula, uint64_t resolution, bool useDynamic,
           Options<ValueType> const& options) {
            return storm::pomdp::api::verifyWithBeliefDiscretization<ValueType, ValueType, ValueType, ValueType>(env, pomdp, formula, resolution, useDynamic,
                                                                                                                 options);
        },
        "Approximate an unbounded reachability probability or expected reachability reward by discretizing the belief space", "env"_a, "pomdp"_a, "formula"_a,
        "resolution"_a, "use_dynamic"_a, "options"_a);
}

template void define_belief_verification<double>(py::module& m);
template void define_belief_verification<storm::RationalNumber>(py::module& m);

void define_belief_verification_nt(py::module& m) {
    py::native_enum<storm::pomdp::beliefs::ExplorationQueueOrder>(m, "ExplorationQueueOrder", "enum.Enum", "Order in which discovered beliefs are explored")
        .value("UNORDERED", storm::pomdp::beliefs::ExplorationQueueOrder::Unordered)
        .value("FIFO", storm::pomdp::beliefs::ExplorationQueueOrder::FIFO)
        .value("LIFO", storm::pomdp::beliefs::ExplorationQueueOrder::LIFO)
        .finalize();

    py::classh<Statistics>(m, "BeliefBasedModelCheckerStatistics", "Statistics of belief-based verification")
        .def_readonly("completed_exploration", &Statistics::completedExploration, "Whether the exploration was completed")
        .def_readonly("discovered_beliefs", &Statistics::discoveredBeliefs, "Number of discovered beliefs")
        .def_readonly("explored_beliefs", &Statistics::exploredBeliefs, "Number of explored beliefs")
        .def_readonly("belief_mdp_states", &Statistics::beliefMdpStates, "Number of states of the belief MDP")
        .def_readonly("belief_mdp_choices", &Statistics::beliefMdpChoices, "Number of choices of the belief MDP")
        .def_readonly("belief_mdp_transitions", &Statistics::beliefMdpTransitions, "Number of transitions of the belief MDP")
        .def_readonly("processed_mdp_states", &Statistics::processedMdpStates, "Number of states of the processed MDP, None if not processed")
        .def_readonly("processed_mdp_choices", &Statistics::processedMdpChoices, "Number of choices of the processed MDP, None if not processed")
        .def_readonly("processed_mdp_transitions", &Statistics::processedMdpTransitions, "Number of transitions of the processed MDP, None if not processed")
        .def_readonly("exploration_time_ms", &Statistics::explorationTimeMilliseconds, "Exploration time in milliseconds")
        .def_readonly("belief_mdp_build_time_ms", &Statistics::beliefMdpBuildTimeMilliseconds, "Build time of the belief MDP in milliseconds")
        .def_readonly("belief_mdp_analysis_time_ms", &Statistics::beliefMdpAnalysisTimeMilliseconds, "Analysis time of the belief MDP in milliseconds");
}

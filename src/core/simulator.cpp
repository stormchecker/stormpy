#include "simulator.h"

#include <storm/adapters/JsonAdapter.h>
#include <storm/simulator/DiscreteTimeSparseModelSimulator.h>
#include <storm/simulator/PrismProgramSimulator.h>

template<typename ValueType>
using PLSim = storm::simulator::DiscreteTimePrismProgramSimulator<ValueType>;

template<typename ValueType>
void define_sparse_model_simulator(py::module& m, std::string const& vtSuffix) {
    py::class_<storm::simulator::DiscreteTimeSparseModelSimulator<ValueType>> dtsmsd(m, ("_DiscreteTimeSparseModelSimulator" + vtSuffix).c_str(),
                                                                                     "Simulator for sparse discrete-time models in memory (for ValueType)");
    dtsmsd.def(py::init<storm::models::sparse::Model<ValueType> const&>());
    dtsmsd.def("set_seed", &storm::simulator::DiscreteTimeSparseModelSimulator<ValueType>::setSeed, py::arg("seed"));
    dtsmsd.def("step", &storm::simulator::DiscreteTimeSparseModelSimulator<ValueType>::step, py::arg("action"));
    dtsmsd.def("random_step", &storm::simulator::DiscreteTimeSparseModelSimulator<ValueType>::randomStep);
    dtsmsd.def("get_last_reward", &storm::simulator::DiscreteTimeSparseModelSimulator<ValueType>::getLastRewards);
    dtsmsd.def("get_current_state", &storm::simulator::DiscreteTimeSparseModelSimulator<ValueType>::getCurrentState);
    dtsmsd.def("reset_to_initial_state", &storm::simulator::DiscreteTimeSparseModelSimulator<ValueType>::resetToInitial);
}

template<typename ValueType>
void define_prism_program_simulator(py::module& m, std::string const& vtSuffix) {
    py::class_<storm::simulator::DiscreteTimePrismProgramSimulator<ValueType>> dtpps(m, ("_DiscreteTimePrismProgramSimulator" + vtSuffix).c_str(),
                                                                                     "Simulator for prism programs");
    dtpps.def(py::init<storm::prism::Program const&, storm::builder::BuilderOptions const&>(), py::arg("program"), py::arg("options"));
    dtpps.def("set_seed", &storm::simulator::DiscreteTimePrismProgramSimulator<ValueType>::setSeed, py::arg("seed"));
    dtpps.def("step", &storm::simulator::DiscreteTimePrismProgramSimulator<ValueType>::step, py::arg("action_index"),
              "Make a step and randomly select the successor. The action is given as an argument, the index reflects the index of the getChoices vector that "
              "can be accessed.");
    dtpps.def(
        "get_action_indices",
        [](storm::simulator::DiscreteTimePrismProgramSimulator<ValueType> const& sim) {
            std::vector<uint64_t> actionIndices;
            for (auto const& c : sim.getChoices()) {
                actionIndices.push_back(c.getActionIndex());
            }
            return actionIndices;
        },
        "A list of choices that encode the possibilities in the current state.");
    dtpps.def("get_number_of_current_choices",
              [](storm::simulator::DiscreteTimePrismProgramSimulator<ValueType> const& sim) { return sim.getChoices().size(); });
    dtpps.def("get_current_state", &PLSim<ValueType>::getCurrentState, "Get current state");
    dtpps.def("get_current_state_as_json", [](storm::simulator::DiscreteTimePrismProgramSimulator<ValueType> const& sim) { return sim.getStateAsJson(); });
    dtpps.def("get_current_observation_as_json",
              [](storm::simulator::DiscreteTimePrismProgramSimulator<ValueType> const& sim) { return sim.getObservationAsJson(); });
    dtpps.def("get_current_state_is_sink", &storm::simulator::DiscreteTimePrismProgramSimulator<ValueType>::isSinkState);
    dtpps.def("get_current_labels", &storm::simulator::DiscreteTimePrismProgramSimulator<ValueType>::getCurrentStateLabelling,
              "What are the state labels at the current state?");
    dtpps.def("get_last_reward", &storm::simulator::DiscreteTimePrismProgramSimulator<ValueType>::getLastRewards);
    dtpps.def("reset_to_initial_state", &storm::simulator::DiscreteTimePrismProgramSimulator<ValueType>::resetToInitial, "Reset to the initial state");
    dtpps.def("_reset_to_state_from_valuation", [](PLSim<ValueType>& sim, storm::expressions::SimpleValuation const& state) { sim.resetToState(state); });
    dtpps.def("_reset_to_state_from_compressed_state", [](PLSim<ValueType>& sim, storm::generator::CompressedState const& state) { sim.resetToState(state); });
    dtpps.def("get_reward_names", &storm::simulator::DiscreteTimePrismProgramSimulator<ValueType>::getRewardNames,
              "Get names of the rewards provided by the simulator");
}

template void define_sparse_model_simulator<double>(py::module& m, std::string const& vtSuffix);
template void define_sparse_model_simulator<storm::RationalNumber>(py::module& m, std::string const& vtSuffix);

template void define_prism_program_simulator<double>(py::module& m, std::string const& vtSuffix);

#include "simulator.h"

#include <storm/adapters/JsonAdapter.h>
#include <storm/simulator/DiscreteTimeSparseModelSimulator.h>
#include <storm/simulator/PrismProgramSimulator.h>

#include "src/binding_type_index.h"

namespace stormpy {

template<typename ValueType>
void define_simulator_sparse_typed(py::module& m) {
    using Simulator = storm::simulator::DiscreteTimeSparseModelSimulator<ValueType>;
    stormpy::bindings::bindTemplateClass<Simulator>(m, "DiscreteTimeSparseModelSimulator", stormpy::bindings::typeIndex<ValueType>(),
                                                    "Simulator for sparse discrete-time models")
        .def(py::init<storm::models::sparse::Model<ValueType> const&>(), "Create simulator", py::arg("model"), py::keep_alive<1, 2>())
        .def("set_seed", &Simulator::setSeed, "Set the seed of the random generator", py::arg("seed"))
        .def("step", &Simulator::step, "Make a step with the given action", py::arg("action"))
        .def("random_step", &Simulator::randomStep, "Make a step with a randomly chosen action")
        .def("get_last_rewards", &Simulator::getLastRewards, "Get the rewards obtained in the last step")
        .def("get_current_state", &Simulator::getCurrentState, "Get the current state")
        .def("reset_to_initial", &Simulator::resetToInitial, "Reset to the initial state");
}

template<typename ValueType>
void define_simulator_prism_typed(py::module& m) {
    using Simulator = storm::simulator::DiscreteTimePrismProgramSimulator<ValueType>;
    stormpy::bindings::bindTemplateClass<Simulator>(m, "DiscreteTimePrismProgramSimulator", stormpy::bindings::typeIndex<ValueType>(),
                                                    "Simulator for Prism programs")
        .def(py::init<storm::prism::Program const&, storm::builder::BuilderOptions const&>(), "Create simulator", py::arg("program"), py::arg("options"),
             py::keep_alive<1, 2>())
        .def("set_seed", &Simulator::setSeed, "Set the seed of the random generator", py::arg("seed"))
        .def(
            // Thin wrapper as pybind11 does not support std::span
            "get_choices",
            [](Simulator const& sim) {
                auto choices = sim.getChoices();
                return std::vector<storm::generator::Choice<ValueType, uint32_t>>(choices.begin(), choices.end());
            },
            "Get the choices of the current state")
        .def("is_sink_state", &Simulator::isSinkState, "Whether the current state is a sink state")
        .def("step", &Simulator::step, "Make a step and randomly select the successor. The index of the choice is given as argument (see get_choices).",
             py::arg("action_number"))
        .def("get_last_rewards", &Simulator::getLastRewards, "Get the rewards obtained in the last step")
        .def("get_current_state", &Simulator::getCurrentState, "Get the current state", py::return_value_policy::reference_internal)
        .def("get_current_state_as_valuation", &Simulator::getCurrentStateAsValuation, "Get the current state as valuation")
        .def("get_current_state_labelling", &Simulator::getCurrentStateLabelling, "Get the labels of the current state")
        .def("get_state_as_json", &Simulator::getStateAsJson, "Get the current state as JSON")
        .def("get_observation_as_json", &Simulator::getObservationAsJson, "Get the current observation as JSON")
        .def("get_current_state_string", &Simulator::getCurrentStateString, "Get string representation of the current state")
        .def("reset_to_initial", &Simulator::resetToInitial, "Reset to the initial state")
        .def("reset_to_state", py::overload_cast<storm::generator::CompressedState const&>(&Simulator::resetToState), "Reset to the given state",
             py::arg("compressed_state"))
        .def("reset_to_state", py::overload_cast<storm::expressions::SimpleValuation const&>(&Simulator::resetToState), "Reset to the given state",
             py::arg("valuation_state"))
        .def("get_reward_names", &Simulator::getRewardNames, "Get the names of the rewards");
}

template void define_simulator_sparse_typed<double>(py::module& m);
template void define_simulator_sparse_typed<storm::RationalNumber>(py::module& m);

template void define_simulator_prism_typed<double>(py::module& m);

}  // namespace stormpy

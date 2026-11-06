#include "modelchecker.h"

#include <storm/adapters/RationalFunctionAdapter.h>
#include <storm/environment/Environment.h>
#include <storm/modelchecker/CheckTask.h>
#include <storm/modelchecker/csl/helper/SparseCtmcCslHelper.h>
#include <storm/modelchecker/hints/ExplicitModelCheckerHint.h>
#include <storm/models/sparse/Ctmc.h>
#include <storm/models/sparse/StandardRewardModel.h>
#include <storm/solver/SolveGoal.h>

#include "src/binding_type_index.h"

namespace stormpy {

template<typename ValueType>
using CheckTask = storm::modelchecker::CheckTask<storm::logic::Formula, ValueType>;
using SparseCtmcCslHelper = storm::modelchecker::helper::SparseCtmcCslHelper;

void define_modelchecker(py::module& m) {
    py::classh<storm::modelchecker::ModelCheckerHint> modelCheckerHint(m, "ModelCheckerHint", "Information that may accelerate the model checking process");
    using ExplicitHint = storm::modelchecker::ExplicitModelCheckerHint<double>;
    stormpy::bindings::bindTemplateClass<ExplicitHint>(m, "ExplicitModelCheckerHint", stormpy::bindings::typeIndex<double>(),
                                                       "Information that may accelerate an explicit state model checker", modelCheckerHint)
        .def(py::init<>(), "Create empty hint")
        .def("set_result_hint", py::overload_cast<boost::optional<std::vector<double>> const&>(&ExplicitHint::setResultHint),
             "Set a result hint close to the actual result", py::arg("result_hint"))
        .def("set_compute_only_maybe_states", &ExplicitHint::setComputeOnlyMaybeStates, "Set whether only the maybe states are computed", py::arg("value"))
        .def("set_maybe_states", py::overload_cast<storm::storage::BitVector const&>(&ExplicitHint::setMaybeStates),
             "Set the maybe states. This is assumed to be correct.", py::arg("maybe_states"))
        .def("set_scheduler_hint", py::overload_cast<boost::optional<storm::storage::Scheduler<double>> const&>(&ExplicitHint::setSchedulerHint),
             "Set a scheduler that is close to the optimal scheduler", py::arg("scheduler_hint"))
        .def("set_no_end_components_in_maybe_states", &ExplicitHint::setNoEndComponentsInMaybeStates, "Set whether the maybe states contain no end components",
             py::arg("value"));

    m.def(
        // Thin wrapper constructing the solve goal from a check task
        "compute_all_until_probabilities",
        [](storm::Environment const& env, CheckTask<double> const& task, std::shared_ptr<storm::models::sparse::Ctmc<double>> const& ctmc,
           storm::storage::BitVector const& phiStates, storm::storage::BitVector const& psiStates) {
            storm::solver::SolveGoal<double> goal(*ctmc, task);
            return SparseCtmcCslHelper::computeAllUntilProbabilities(env, std::move(goal), ctmc->getTransitionMatrix(), ctmc->getExitRateVector(),
                                                                     ctmc->getInitialStates(), phiStates, psiStates);
        },
        "Compute until probabilities for all states of a CTMC", py::arg("env"), py::arg("task"), py::arg("ctmc"), py::arg("phi_states"), py::arg("psi_states"));
    m.def("compute_all_transient_probabilities", &SparseCtmcCslHelper::computeAllTransientProbabilities<double>,
          "Compute transient probabilities for all states of a CTMC", py::arg("env"), py::arg("rate_matrix"), py::arg("initial_states"), py::arg("phi_states"),
          py::arg("psi_states"), py::arg("exit_rates"), py::arg("time_bound"));
}

template<typename ValueType>
void define_modelchecker_typed(py::module& m) {
    stormpy::bindings::bindTemplateClass<CheckTask<ValueType>>(m, "CheckTask", stormpy::bindings::typeIndex<ValueType>(), "Task for model checking")
        .def(py::init<storm::logic::Formula const&, bool, storm::solver::UncertaintyResolutionMode>(), "Create check task", py::arg("formula"),
             py::arg("only_initial_states_relevant") = false, py::arg("uncertainty_resolution_mode") = storm::solver::UncertaintyResolutionMode::Unset,
             py::keep_alive<1, 2>() /* Task keeps a reference to the formula */)
        .def("is_only_initial_states_relevant_set", &CheckTask<ValueType>::isOnlyInitialStatesRelevantSet, "Whether only initial states are relevant")
        .def("set_produce_schedulers", &CheckTask<ValueType>::setProduceSchedulers, "Set whether schedulers are produced (if possible)",
             py::arg("produce_schedulers") = true)
        .def("is_produce_schedulers_set", &CheckTask<ValueType>::isProduceSchedulersSet, "Whether schedulers are produced")
        .def("set_hint", &CheckTask<ValueType>::setHint, "Set a hint that may speed up the solver", py::arg("hint"))
        .def("set_uncertainty_resolution_mode", &CheckTask<ValueType>::setUncertaintyResolutionMode, "Set how uncertainty is resolved",
             py::arg("uncertainty_resolution_mode"));
}

template void define_modelchecker_typed<double>(py::module&);
template void define_modelchecker_typed<storm::RationalNumber>(py::module&);
template void define_modelchecker_typed<storm::RationalFunction>(py::module&);

}  // namespace stormpy

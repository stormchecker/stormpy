#include "modelchecking.h"
#include "result.h"
#include "storm/adapters/RationalFunctionAdapter.h"
#include "storm/api/verification.h"
#include "storm/environment/Environment.h"
#include "storm/environment/solver/MinMaxSolverEnvironment.h"
#include "storm/models/symbolic/StandardRewardModel.h"
#include "storm/modelchecker/results/CheckResult.h"
#include "storm/modelchecker/hints/ExplicitModelCheckerHint.h"
#include "storm/modelchecker/csl/helper/SparseCtmcCslHelper.h"
#include "storm/modelchecker/multiobjective/MultiObjectiveModelChecking.h"
#include "storm/utility/graph.h"

template<typename ValueType>
using CheckTask = storm::modelchecker::CheckTask<storm::logic::Formula, ValueType>;

// Thin wrapper for model checking using sparse engine
template<typename ValueType>
std::shared_ptr<storm::modelchecker::CheckResult> modelCheckingSparseEngine(std::shared_ptr<storm::models::sparse::Model<ValueType>> model, CheckTask<ValueType> const& task, storm::Environment const& env) {
    return storm::api::verifyWithSparseEngine<ValueType>(env, model, task);
}

template<typename ValueType>
std::shared_ptr<storm::modelchecker::CheckResult> multiObjectiveModelChecking(std::shared_ptr<storm::models::sparse::Model<ValueType>> model,
                                                                              storm::logic::MultiObjectiveFormula const& formula, storm::Environment const& env) {
    if (model->isOfType(storm::models::ModelType::Mdp)) {
        return storm::modelchecker::multiobjective::performMultiObjectiveModelChecking<storm::models::sparse::Mdp<ValueType>>(env, *(model->template as<storm::models::sparse::Mdp<ValueType>>()), formula);
    } else if (model->isOfType(storm::models::ModelType::MarkovAutomaton)) {
        return storm::modelchecker::multiobjective::performMultiObjectiveModelChecking<storm::models::sparse::MarkovAutomaton<ValueType>>(env, *(model->template as<storm::models::sparse::MarkovAutomaton<ValueType>>()), formula);
    } else {
        throw storm::exceptions::NotSupportedException("Only systems with Nondeterminism are supported");
    }
}

template<typename ValueType>
std::shared_ptr<storm::modelchecker::CheckResult> modelCheckingFullyObservableSparseEngine(std::shared_ptr<storm::models::sparse::Pomdp<ValueType>> model, CheckTask<ValueType> const& task, storm::Environment const& env) {
    return storm::api::verifyWithSparseEngine<ValueType>(env, model->template as<storm::models::sparse::Mdp<ValueType>>(), task);
}

// Thin wrapper for model checking using dd engine
template<storm::dd::DdType DdType, typename ValueType>
std::shared_ptr<storm::modelchecker::CheckResult> modelCheckingDdEngine(std::shared_ptr<storm::models::symbolic::Model<DdType, ValueType>> model, CheckTask<ValueType> const& task, storm::Environment const& env) {
    return storm::api::verifyWithDdEngine<DdType, ValueType>(env, model, task);
}

// Thin wrapper for model checking using hybrid engine
template<storm::dd::DdType DdType, typename ValueType>
std::shared_ptr<storm::modelchecker::CheckResult> modelCheckingHybridEngine(std::shared_ptr<storm::models::symbolic::Model<DdType, ValueType>> model, CheckTask<ValueType> const& task, storm::Environment const& env) {
    return storm::api::verifyWithHybridEngine<DdType, ValueType>(env, model, task);
}

std::shared_ptr<storm::modelchecker::CheckResult> checkIntervalDtmc(std::shared_ptr<storm::models::sparse::Dtmc<storm::Interval>> dtmc, CheckTask<double> const& task, storm::Environment& env) {
    auto checker = storm::modelchecker::SparseDtmcPrctlModelChecker<storm::models::sparse::Dtmc<storm::Interval>>(*dtmc);
    return checker.check(env, task);
}

std::shared_ptr<storm::modelchecker::CheckResult> checkRationalIntervalDtmc(std::shared_ptr<storm::models::sparse::Dtmc<storm::RationalInterval>> dtmc, CheckTask<storm::RationalNumber> const& task, storm::Environment& env) {
    auto checker = storm::modelchecker::SparseDtmcPrctlModelChecker<storm::models::sparse::Dtmc<storm::RationalInterval>>(*dtmc);
    return checker.check(env, task);
}

std::shared_ptr<storm::modelchecker::CheckResult> checkIntervalMdp(std::shared_ptr<storm::models::sparse::Mdp<storm::Interval>> mdp, CheckTask<double> const& task, storm::Environment& env) {
    auto checker = storm::modelchecker::SparseMdpPrctlModelChecker<storm::models::sparse::Mdp<storm::Interval>>(*mdp);
    return checker.check(env, task);
}

std::shared_ptr<storm::modelchecker::CheckResult> checkRationalIntervalMdp(std::shared_ptr<storm::models::sparse::Mdp<storm::RationalInterval>> mdp, CheckTask<storm::RationalNumber> const& task, storm::Environment& env) {
    auto checker = storm::modelchecker::SparseMdpPrctlModelChecker<storm::models::sparse::Mdp<storm::RationalInterval>>(*mdp);
    return checker.check(env, task);
}

std::vector<double> computeAllUntilProbabilities(storm::Environment const& env, CheckTask<double> const& task, std::shared_ptr<storm::models::sparse::Ctmc<double>> ctmc, storm::storage::BitVector const& phiStates, storm::storage::BitVector const& psiStates) {
    storm::solver::SolveGoal<double> goal(*ctmc, task);
    return storm::modelchecker::helper::SparseCtmcCslHelper::computeAllUntilProbabilities(env, std::move(goal), ctmc->getTransitionMatrix(), ctmc->getExitRateVector(), ctmc->getInitialStates(), phiStates, psiStates);
}

std::vector<double> computeTransientProbabilities(storm::Environment const& env, std::shared_ptr<storm::models::sparse::Ctmc<double>> ctmc, storm::storage::BitVector const& phiStates, storm::storage::BitVector const& psiStates, double timeBound) {
    return storm::modelchecker::helper::SparseCtmcCslHelper::computeAllTransientProbabilities(env, ctmc->getTransitionMatrix(), ctmc->getInitialStates(), phiStates, psiStates, ctmc->getExitRateVector(), timeBound);
}

// Thin wrapper for computing prob01 states
template<typename ValueType>
std::pair<storm::storage::BitVector, storm::storage::BitVector> computeProb01(storm::models::sparse::Dtmc<ValueType> const& model, storm::storage::BitVector const& phiStates, storm::storage::BitVector const& psiStates) {
    return storm::utility::graph::performProb01(model, phiStates, psiStates);
}

template<typename ValueType>
std::pair<storm::storage::BitVector, storm::storage::BitVector> computeProb01min(storm::models::sparse::Mdp<ValueType> const& model, storm::storage::BitVector const& phiStates, storm::storage::BitVector const& psiStates) {
    return storm::utility::graph::performProb01Min(model, phiStates, psiStates);
}

template<typename ValueType>
std::pair<storm::storage::BitVector, storm::storage::BitVector> computeProb01max(storm::models::sparse::Mdp<ValueType> const& model, storm::storage::BitVector const& phiStates, storm::storage::BitVector const& psiStates) {
    return storm::utility::graph::performProb01Max(model, phiStates, psiStates);
}

template<typename ValueType>
std::shared_ptr<storm::modelchecker::CheckResult> getExpectedNumberOfVisits(storm::Environment const& env, std::shared_ptr<storm::models::sparse::Model<ValueType>> const& model) {
    return storm::api::computeExpectedVisitingTimesWithSparseEngine(env, model);
}
template<typename ValueType>
std::shared_ptr<storm::modelchecker::CheckResult> getSteadyStateDistribution(storm::Environment const& env, std::shared_ptr<storm::models::sparse::Model<ValueType>> const& model) {
    return storm::api::computeSteadyStateDistributionWithSparseEngine(env, model);
}

template<typename ValueType>
storm::storage::BitVector getReachableStates(storm::models::sparse::Model<ValueType> const& model, storm::storage::BitVector const& initialStates, storm::storage::BitVector const& constraintStates, storm::storage::BitVector const& targetStates, boost::optional<uint64_t> maximalStep, boost::optional<storm::storage::BitVector> const& choiceFilter) {
    uint64_t steps = 0;
    if (maximalStep != boost::none) {
        steps = maximalStep.get();
    }
    return storm::utility::graph::getReachableStates(model.getTransitionMatrix(), initialStates, constraintStates, targetStates, maximalStep != boost::none, steps, choiceFilter);

}

// TODO: use consistent suffix instead of name
template<typename ValueType>
void define_check_task(py::module& m, std::string const& name) {
    // CheckTask
    py::class_<CheckTask<ValueType>, std::shared_ptr<CheckTask<ValueType>>>(m, name.c_str(), "Task for model checking")
        .def(py::init<storm::logic::Formula const&, bool>(), py::arg("formula"), py::arg("only_initial_states") = false)
        .def("set_produce_schedulers", &CheckTask<ValueType>::setProduceSchedulers, "Set whether schedulers should be produced (if possible)", py::arg("produce_schedulers") = true)
        .def("set_hint", &CheckTask<ValueType>::setHint, "Sets a hint that may speed up the solver")
        .def("set_uncertainty_resolution_mode", &CheckTask<ValueType>::setUncertaintyResolutionMode, "Sets the mode which decides how the uncertainty will be resolved.")
    ;
}

void define_modelchecking(py::module& m) {

    py::class_<storm::modelchecker::ModelCheckerHint, std::shared_ptr<storm::modelchecker::ModelCheckerHint>> mchint(m, "ModelCheckerHint", "Information that may accelerate the model checking process");
    py::class_<storm::modelchecker::ExplicitModelCheckerHint<double>>(m, "ExplicitModelCheckerHintDouble", "Information that may accelerate an explicit state model checker", mchint)
        .def(py::init<>())
        .def("set_scheduler_hint", py::overload_cast<boost::optional<storm::storage::Scheduler<double>> const&>(&storm::modelchecker::ExplicitModelCheckerHint<double>::setSchedulerHint), "scheduler_hint"_a, "Set a scheduler that is close to the optimal scheduler")
        .def("set_maybe_states", py::overload_cast<storm::storage::BitVector const&>(&storm::modelchecker::ExplicitModelCheckerHint<double>::setMaybeStates), "sets the maybe states. This is assumed to be correct.")
        .def("set_compute_only_maybe_states", &storm::modelchecker::ExplicitModelCheckerHint<double>::setComputeOnlyMaybeStates, "value")
        .def("set_result_hint", py::overload_cast<boost::optional<std::vector<double>> const&>(&storm::modelchecker::ExplicitModelCheckerHint<double>::setResultHint), "result_hint"_a);

    m.def("_get_reachable_states_double", &getReachableStates<double>, py::arg("model"), py::arg("initial_states"), py::arg("constraint_states"), py::arg("target_states"), py::arg("maximal_steps") = boost::none, py::arg("choice_filter") = boost::none);
    m.def("_get_reachable_states_exact", &getReachableStates<storm::RationalNumber>, py::arg("model"), py::arg("initial_states"), py::arg("constraint_states"), py::arg("target_states"), py::arg("maximal_steps") = boost::none, py::arg("choice_filter") = boost::none);
    m.def("_get_reachable_states_rf", &getReachableStates<storm::RationalFunction>, py::arg("model"), py::arg("initial_states"), py::arg("constraint_states"), py::arg("target_states"), py::arg("maximal_steps") = boost::none, py::arg("choice_filter") = boost::none);

    m.def("_compute_expected_number_of_visits_double", &getExpectedNumberOfVisits<double>, py::arg("env"), py::arg("model"));
    m.def("_compute_expected_number_of_visits_exact", &getExpectedNumberOfVisits<storm::RationalNumber>,  py::arg("env"), py::arg("model"));

    m.def("_compute_steady_state_distribution_double", &getSteadyStateDistribution<double>, py::arg("env"), py::arg("model"));
    m.def("_compute_steady_state_distribution_exact", &getSteadyStateDistribution<storm::RationalNumber>,  py::arg("env"), py::arg("model"));

    // Model checking
    m.def("_model_checking_fully_observable", &modelCheckingFullyObservableSparseEngine<double>, py::arg("model"), py::arg("task"), py::arg("environment")  = storm::Environment());
    m.def("_exact_model_checking_fully_observable", &modelCheckingFullyObservableSparseEngine<storm::RationalNumber>, py::arg("model"), py::arg("task"), py::arg("environment")  = storm::Environment());
    m.def("_model_checking_sparse_engine", &modelCheckingSparseEngine<double>, "Perform model checking using the sparse engine", py::arg("model"), py::arg("task"), py::arg("environment") = storm::Environment());
    m.def("_exact_model_checking_sparse_engine",  &modelCheckingSparseEngine<storm::RationalNumber>, "Perform model checking using the sparse engine", py::arg("model"), py::arg("task"), py::arg("environment") = storm::Environment());
    m.def("_parametric_model_checking_sparse_engine", &modelCheckingSparseEngine<storm::RationalFunction>, "Perform parametric model checking using the sparse engine", py::arg("model"), py::arg("task"), py::arg("environment") = storm::Environment());
    m.def("_model_checking_dd_engine", &modelCheckingDdEngine<storm::dd::DdType::Sylvan, double>, "Perform model checking using the dd engine", py::arg("model"), py::arg("task"), py::arg("environment") = storm::Environment());
    m.def("_parametric_model_checking_dd_engine", &modelCheckingDdEngine<storm::dd::DdType::Sylvan, storm::RationalFunction>, "Perform parametric model checking using the dd engine", py::arg("model"), py::arg("task"), py::arg("environment") = storm::Environment());
    m.def("_model_checking_hybrid_engine", &modelCheckingHybridEngine<storm::dd::DdType::Sylvan, double>, "Perform model checking using the hybrid engine", py::arg("model"), py::arg("task"), py::arg("environment") = storm::Environment());
    m.def("_parametric_model_checking_hybrid_engine", &modelCheckingHybridEngine<storm::dd::DdType::Sylvan, storm::RationalFunction>, "Perform parametric model checking using the hybrid engine", py::arg("model"), py::arg("task"), py::arg("environment") = storm::Environment());
    m.def("check_interval_dtmc", &checkIntervalDtmc, "Check interval DTMC");
    m.def("check_exact_interval_dtmc", &checkRationalIntervalDtmc, "Check exact interval DTMC");
    m.def("check_interval_mdp", &checkIntervalMdp, "Check interval MDP");
    m.def("check_exact_interval_mdp", &checkRationalIntervalMdp, "Check exact interval MDP");
    m.def("compute_all_until_probabilities", &computeAllUntilProbabilities, "Compute forward until probabilities");
    m.def("compute_transient_probabilities", &computeTransientProbabilities, "Compute transient probabilities");
    m.def("_compute_prob01states_double", &computeProb01<double>, "Compute prob-0-1 states", py::arg("model"), py::arg("phi_states"), py::arg("psi_states"));
    m.def("_compute_prob01states_rationalfunc", &computeProb01<storm::RationalFunction>, "Compute prob-0-1 states", py::arg("model"), py::arg("phi_states"), py::arg("psi_states"));
    m.def("_compute_prob01states_min_double", &computeProb01min<double>, "Compute prob-0-1 states (min)", py::arg("model"), py::arg("phi_states"), py::arg("psi_states"));
    m.def("_compute_prob01states_max_double", &computeProb01max<double>, "Compute prob-0-1 states (max)", py::arg("model"), py::arg("phi_states"), py::arg("psi_states"));
    m.def("_compute_prob01states_min_rationalfunc", &computeProb01min<storm::RationalFunction>, "Compute prob-0-1 states (min)", py::arg("model"), py::arg("phi_states"), py::arg("psi_states"));
    m.def("_compute_prob01states_max_rationalfunc", &computeProb01max<storm::RationalFunction>, "Compute prob-0-1 states (max)", py::arg("model"), py::arg("phi_states"), py::arg("psi_states"));
    m.def("_multi_objective_model_checking_double", &multiObjectiveModelChecking<double>, "Run multi-objective model checking",  py::arg("model"), py::arg("formula"), py::arg("environment") = storm::Environment());
    m.def("_multi_objective_model_checking_exact", &multiObjectiveModelChecking<storm::RationalNumber>, "Run multi-objective model checking", py::arg("model"), py::arg("formula"), py::arg("environment") = storm::Environment());
}

template void define_check_task<double>(py::module&, std::string const&);
template void define_check_task<storm::RationalNumber>(py::module&, std::string const&);
template void define_check_task<storm::RationalFunction>(py::module&, std::string const&);
#include "modelchecker_multiobjective.h"

#include <storm/adapters/RationalNumberAdapter.h>
#include <storm/environment/Environment.h>
#include <storm/modelchecker/multiobjective/MultiObjectiveModelChecking.h>
#include <storm/modelchecker/multiobjective/pcaa/PcaaWeightVectorChecker.h>
#include <storm/modelchecker/multiobjective/preprocessing/SparseMultiObjectivePreprocessor.h>
#include <storm/models/sparse/MarkovAutomaton.h>
#include <storm/models/sparse/Mdp.h>
#include <storm/models/sparse/StandardRewardModel.h>

#include "src/binding_type_index.h"
#include "src/interrupt.h"

namespace stormpy {

namespace multiobjective = storm::modelchecker::multiobjective;

template<typename ValueType>
void define_modelchecker_multiobjective_typed(py::module& m) {
    m.def("perform_multi_objective_model_checking",
          stormpy::interruptible(&multiobjective::performMultiObjectiveModelChecking<storm::models::sparse::Mdp<ValueType>>),
          "Perform multi-objective model checking on MDP", py::arg("env"), py::arg("model"), py::arg("formula"), py::arg("produce_scheduler") = false);
    m.def("perform_multi_objective_model_checking",
          stormpy::interruptible(&multiobjective::performMultiObjectiveModelChecking<storm::models::sparse::MarkovAutomaton<ValueType>>),
          "Perform multi-objective model checking on MA", py::arg("env"), py::arg("model"), py::arg("formula"), py::arg("produce_scheduler") = false);

    m.def(
        // Thin wrapper performing the preprocessing before creating the weight vector checker
        "create_weight_vector_checker",
        [](storm::Environment const& env, storm::models::sparse::Mdp<ValueType> const& originalModel,
           storm::logic::MultiObjectiveFormula const& originalFormula, bool produceScheduler) {
            auto const preprocessorResult = multiobjective::preprocessing::SparseMultiObjectivePreprocessor<storm::models::sparse::Mdp<ValueType>>::preprocess(
                env, originalModel, originalFormula, produceScheduler);
            return std::make_pair(multiobjective::createWeightVectorChecker(preprocessorResult), preprocessorResult.memoryIncorporationReverseData);
        },
        "Create checker for weighted sums of objectives. Also returns the data for mapping schedulers back to the original model.", py::arg("env"),
        py::arg("original_model"), py::arg("original_formula"), py::arg("produce_scheduler"));

    using PcaaWeightVectorChecker = multiobjective::PcaaWeightVectorChecker<storm::models::sparse::Mdp<ValueType>>;
    stormpy::bindings::bindTemplateClass<PcaaWeightVectorChecker>(m, "PcaaWeightVectorChecker", stormpy::bindings::typeIndex<ValueType>(),
                                                                  "Checker for weighted sums of objectives")
        .def("check", &PcaaWeightVectorChecker::check, "Optimize the weighted sum of objectives", py::arg("env"), py::arg("weight_vector"))
        .def("get_achievable_point", &PcaaWeightVectorChecker::getAchievablePoint, "Get the point achieved by the optimal scheduler")
        .def("get_optimal_weighted_sum", &PcaaWeightVectorChecker::getOptimalWeightedSum,
             "Get the optimal weighted sum. Note that this sum can be hard to interpret whenever one includes also minimization objectives.")
        .def("compute_scheduler", &PcaaWeightVectorChecker::computeScheduler,
             "Compute the optimal scheduler. Note that this is a scheduler on the preprocessed MDP.")
        .def("set_weighted_precision", &PcaaWeightVectorChecker::setWeightedPrecision, "Set precision. A smaller value means a higher precision.",
             py::arg("value"))
        .def("get_weighted_precision", &PcaaWeightVectorChecker::getWeightedPrecision, "Get precision");
}

template void define_modelchecker_multiobjective_typed<double>(py::module&);
template void define_modelchecker_multiobjective_typed<storm::RationalNumber>(py::module&);

}  // namespace stormpy

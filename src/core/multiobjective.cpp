#include "multiobjective.h"

#include "storm/modelchecker/multiobjective/MultiObjectiveModelChecking.h"
#include "storm/modelchecker/multiobjective/pcaa/PcaaWeightVectorChecker.h"
#include "storm/modelchecker/multiobjective/preprocessing/SparseMultiObjectivePreprocessor.h"
#include "storm/adapters/RationalNumberAdapter.h"
#include "storm/models/sparse/Mdp.h"
#include "storm/models/sparse/StandardRewardModel.h"
#include "storm/utility/macros.h"
#include "storm/environment/Environment.h"
//
//// Helper class to avoid that we also need to bind the preprocessing.
template<typename ValueType>
std::pair<std::unique_ptr<storm::modelchecker::multiobjective::PcaaWeightVectorChecker<storm::models::sparse::Mdp<ValueType>>>, std::optional<storm::storage::SparseModelMemoryProductReverseData>> makeWeightedObjectiveMDPModelChecker(storm::Environment const& env, storm::models::sparse::Mdp<ValueType> const& originalModel, storm::logic::MultiObjectiveFormula const& originalFormula, bool produceScheduler) {
    auto const preprocessresult = storm::modelchecker::multiobjective::preprocessing::SparseMultiObjectivePreprocessor<storm::models::sparse::Mdp<ValueType>>::preprocess(env, originalModel, originalFormula, produceScheduler);
    return std::make_pair(storm::modelchecker::multiobjective::createWeightVectorChecker(preprocessresult), preprocessresult.memoryIncorporationReverseData);
}
//
template<typename ValueType>
void define_multiobjective(py::module& m, std::string const& vtSuffix) {
    m.def(("_make_weighted_objective_mdp_model_checker_" + vtSuffix).c_str(), &makeWeightedObjectiveMDPModelChecker<ValueType>, py::arg("env"), py::arg("model"), py::arg("formula"), py::arg("compute_scheduler")=false);

    using PcaaWeightVectorChecker = storm::modelchecker::multiobjective::PcaaWeightVectorChecker<storm::models::sparse::Mdp<ValueType>>;
    py::class_<PcaaWeightVectorChecker, std::unique_ptr<PcaaWeightVectorChecker>> weightedObjectiveMdpModelChecker(m, ("WeightedObjectiveMdpModelChecker" + vtSuffix).c_str());
    weightedObjectiveMdpModelChecker.def("check", &PcaaWeightVectorChecker::check, py::arg("env"), py::arg("weight_vector"))
                           .def("get_achievable_point", &PcaaWeightVectorChecker::getAchievablePoint)
                           .def("get_optimal_weighted_sum", &PcaaWeightVectorChecker::getOptimalWeightedSum, "Note that this sum can be hard to interpret whenever one includes also minimization objectives.")
                           .def("compute_scheduler", &PcaaWeightVectorChecker::computeScheduler, "Note that this is a scheduler on the preprocessed MDP.")
                           .def("set_weighted_precision", &PcaaWeightVectorChecker::setWeightedPrecision, py::arg("value"), "A smaller value means a higher precision.");
}
//
template void define_multiobjective<double>(py::module&, std::string const&);
template void define_multiobjective<storm::RationalNumber>(py::module&, std::string const&);
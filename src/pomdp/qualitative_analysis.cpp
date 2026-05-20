#include <storm-pomdp/analysis/IterativePolicySearch.h>
#include <storm-pomdp/analysis/QualitativeAnalysisOnGraphs.h>
#include <storm-pomdp/analysis/WinningRegionQueryInterface.h>
#include <storm/logic/Formula.h>
#include "src/helpers.h"
#include "tracker.h"

template<typename ValueType>
using SparsePomdp = storm::models::sparse::Pomdp<ValueType>;

template<typename ValueType>
std::shared_ptr<storm::pomdp::IterativePolicySearch<ValueType>> createWinningRegionSolver(SparsePomdp<ValueType> const& pomdp,
                                                                                          storm::logic::Formula const& formula,
                                                                                          storm::pomdp::MemlessSearchOptions const& options) {
    STORM_LOG_TRACE("Run qualitative preprocessing...");
    storm::analysis::QualitativeAnalysisOnGraphs<ValueType> qualitativeAnalysis(pomdp);
    // After preprocessing, this might be done cheaper.
    storm::storage::BitVector targetStates = qualitativeAnalysis.analyseProb1(formula.asProbabilityOperatorFormula());
    storm::storage::BitVector surelyNotAlmostSurelyReachTarget = qualitativeAnalysis.analyseProbSmaller1(formula.asProbabilityOperatorFormula());
    storm::expressions::ExpressionManager expressionManager;
    std::shared_ptr<storm::utility::solver::SmtSolverFactory> smtSolverFactory = std::make_shared<storm::utility::solver::Z3SmtSolverFactory>();
    return std::make_shared<storm::pomdp::IterativePolicySearch<ValueType>>(pomdp, targetStates, surelyNotAlmostSurelyReachTarget, smtSolverFactory, options);
}

template<typename ValueType>
SparsePomdp<ValueType> preparePOMDPForQualitativeSearch(SparsePomdp<ValueType> const& origPomdp, storm::logic::Formula const& formula) {
    SparsePomdp<ValueType> pomdp = SparsePomdp<ValueType>(origPomdp);
    storm::analysis::QualitativeAnalysisOnGraphs<ValueType> qualitativeAnalysis(pomdp);
    // After preprocessing, this might be done cheaper.
    storm::storage::BitVector surelyNotAlmostSurelyReachTarget = qualitativeAnalysis.analyseProbSmaller1(formula.asProbabilityOperatorFormula());
    pomdp.getTransitionMatrix().makeRowGroupsAbsorbing(surelyNotAlmostSurelyReachTarget);
    return pomdp;
}

template<typename ValueType>
void define_qualitative_policy_search(py::module& m, std::string const& vtSuffix) {
    m.def(("create_iterative_qualitative_search_solver_" + vtSuffix).c_str(), &createWinningRegionSolver<ValueType>, "Create solver ", py::arg("pomdp"),
          py::arg("formula"), py::arg("options"));
    m.def(("prepare_pomdp_for_qualitative_search_" + vtSuffix).c_str(), &preparePOMDPForQualitativeSearch<ValueType>, "Preprocess POMDP", py::arg("pomdp"),
          py::arg("formula"));
    py::class_<storm::pomdp::IterativePolicySearch<ValueType>, std::shared_ptr<storm::pomdp::IterativePolicySearch<ValueType>>> mssq(
        m, ("IterativeQualitativeSearchSolver" + vtSuffix).c_str(), "Solver for POMDPs that solves qualitative queries");
    mssq.def("compute_winning_region", &storm::pomdp::IterativePolicySearch<ValueType>::computeWinningRegion, py::arg("lookahead"));
    mssq.def("compute_winning_policy_for_initial_states", &storm::pomdp::IterativePolicySearch<ValueType>::analyzeForInitialStates, py::arg("lookahead"));
    mssq.def_property_readonly("last_winning_region", &storm::pomdp::IterativePolicySearch<ValueType>::getLastWinningRegion,
                               "get the last computed winning region");

    py::class_<storm::pomdp::WinningRegionQueryInterface<ValueType>> wrqi(m, ("BeliefSupportWinningRegionQueryInterface" + vtSuffix).c_str());
    wrqi.def(py::init<SparsePomdp<ValueType> const&, storm::pomdp::WinningRegion const&>(), py::arg("pomdp"), py::arg("BeliefSupportWinningRegion"));
    wrqi.def("query_current_belief", &storm::pomdp::WinningRegionQueryInterface<ValueType>::isInWinningRegion, py::arg("current_belief"));
    wrqi.def("query_action", &storm::pomdp::WinningRegionQueryInterface<ValueType>::staysInWinningRegion, py::arg("current_belief"), py::arg("action"));
}

template void define_qualitative_policy_search<double>(py::module& m, std::string const& vtSuffix);

void define_qualitative_policy_search_nt(py::module& m) {
    py::class_<storm::pomdp::MemlessSearchOptions> mssqopts(m, "IterativeQualitativeSearchOptions", "Options for the IterativeQualitativeSearch");
    mssqopts.def(py::init<>());

    py::class_<storm::pomdp::WinningRegion> winningRegion(m, "BeliefSupportWinningRegion");
    winningRegion.def_static("load_from_file", &storm::pomdp::WinningRegion::loadFromFile, py::arg("filepath"));
    winningRegion.def("store_to_file", &storm::pomdp::WinningRegion::storeToFile, py::arg("filepath"), py::arg("preamble"), py::arg("append") = false);
}

#include "qualitative_analysis.h"

#include <storm-pomdp/analysis/IterativePolicySearch.h>
#include <storm-pomdp/analysis/QualitativeAnalysisOnGraphs.h>
#include <storm-pomdp/analysis/WinningRegionQueryInterface.h>
#include <storm/environment/Environment.h>
#include <storm/logic/Formula.h>

#include "src/binding_type_index.h"
#include "src/helpers.h"

template<typename ValueType>
using SparsePomdp = storm::models::sparse::Pomdp<ValueType>;

template<typename ValueType>
std::shared_ptr<storm::pomdp::IterativePolicySearch<ValueType>> createWinningRegionSolver(storm::Environment const& env, SparsePomdp<ValueType> const& pomdp,
                                                                                          storm::logic::Formula const& formula,
                                                                                          storm::pomdp::MemlessSearchOptions const& options) {
    STORM_LOG_TRACE("Run qualitative preprocessing...");
    storm::analysis::QualitativeAnalysisOnGraphs<ValueType> qualitativeAnalysis(pomdp);
    // After preprocessing, this might be done cheaper.
    storm::storage::BitVector targetStates = qualitativeAnalysis.analyseProb1(formula.asProbabilityOperatorFormula());
    storm::storage::BitVector surelyNotAlmostSurelyReachTarget = qualitativeAnalysis.analyseProbSmaller1(formula.asProbabilityOperatorFormula());
    storm::expressions::ExpressionManager expressionManager;
    std::shared_ptr<storm::utility::solver::SmtSolverFactory> smtSolverFactory = std::make_shared<storm::utility::solver::Z3SmtSolverFactory>();
    return std::make_shared<storm::pomdp::IterativePolicySearch<ValueType>>(env, pomdp, targetStates, surelyNotAlmostSurelyReachTarget, smtSolverFactory,
                                                                            options);
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
void define_qualitative_policy_search(py::module& m) {
    auto index = stormpy::bindings::typeIndex<ValueType>();
    m.def("create_iterative_policy_search", &createWinningRegionSolver<ValueType>, "Create the iterative policy search for a qualitative reachability query",
          "env"_a, "pomdp"_a, "formula"_a, "options"_a, py::keep_alive<0, 2>());
    m.def("prepare_pomdp_for_qualitative_search", &preparePOMDPForQualitativeSearch<ValueType>,
          "Make all states absorbing from which the target is not reached almost surely", "pomdp"_a, "formula"_a);

    using PolicySearch = storm::pomdp::IterativePolicySearch<ValueType>;
    stormpy::bindings::bindTemplateClass<PolicySearch>(
        m, "IterativePolicySearch", index,
        "Solver for POMDPs that solves qualitative queries. A solver runs a single analysis; create a new one for each further analysis.")
        .def("compute_winning_region", &PolicySearch::computeWinningRegion, "Compute the winning region with the given lookahead", "k"_a)
        .def("analyze_for_initial_states", &PolicySearch::analyzeForInitialStates, "Whether a winning policy for the initial states exists", "k"_a)
        .def_property_readonly("last_winning_region", &PolicySearch::getLastWinningRegion, "Last computed winning region");

    using QueryInterface = storm::pomdp::WinningRegionQueryInterface<ValueType>;
    stormpy::bindings::bindTemplateClass<QueryInterface>(m, "WinningRegionQueryInterface", index, "Queries on a winning region of a POMDP")
        .def(py::init<SparsePomdp<ValueType> const&, storm::pomdp::WinningRegion const&>(), "pomdp"_a, "winning_region"_a, py::keep_alive<1, 2>(),
             py::keep_alive<1, 3>())
        .def("is_in_winning_region", &QueryInterface::isInWinningRegion, "Whether the belief support is in the winning region", "belief_support"_a)
        .def("stays_in_winning_region", &QueryInterface::staysInWinningRegion, "Whether the action keeps the belief support in the winning region",
             "belief_support"_a, "action_index"_a);
}

template void define_qualitative_policy_search<double>(py::module& m);

void define_qualitative_policy_search_nt(py::module& m) {
    py::classh<storm::pomdp::MemlessSearchOptions> options(m, "MemlessSearchOptions", "Options for the iterative policy search");
    options.def(py::init<>());

    py::classh<storm::pomdp::WinningRegion> winningRegion(m, "WinningRegion", "Winning region of a POMDP in terms of belief supports");
    winningRegion.def_static("load_from_file", &storm::pomdp::WinningRegion::loadFromFile, "Load a winning region and its preamble from a file", "path"_a);
    winningRegion.def("store_to_file", &storm::pomdp::WinningRegion::storeToFile, "Store the winning region to a file", "path"_a, "preamble"_a = "",
                      "append"_a = false);
}

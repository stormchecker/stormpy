#include "pla.h"

#include <storm-pars/api/region.h>
#include <storm-pars/modelchecker/instantiation/SparseDtmcInstantiationModelChecker.h>
#include <storm-pars/modelchecker/region/SparseDtmcParameterLiftingModelChecker.h>
#include <storm-pars/modelchecker/region/SparseMdpParameterLiftingModelChecker.h>
#include <storm/api/verification.h>

#include "src/helpers.h"
#include "src/numbers.h"

typedef storm::modelchecker::SparseDtmcParameterLiftingModelChecker<storm::models::sparse::Dtmc<storm::RationalFunction>, double>
    SparseDtmcParameterLiftingModelChecker;
typedef storm::modelchecker::SparseMdpParameterLiftingModelChecker<storm::models::sparse::Mdp<storm::RationalFunction>, double>
    SparseMdpParameterLiftingModelChecker;

typedef storm::modelchecker::RegionModelChecker<storm::RationalFunction> RegionModelChecker;
typedef storm::modelchecker::RegionRefinementChecker<storm::RationalFunction> RegionRefinementChecker;
typedef storm::storage::ParameterRegion<storm::RationalFunction> Region;
typedef storm::modelchecker::AnnotatedRegion<storm::RationalFunction> AnnotatedRegion;

typedef storm::modelchecker::CheckTask<storm::logic::Formula, storm::RationalFunction> CheckTask;
typedef std::shared_ptr<storm::models::sparse::Model<storm::RationalFunction>> ParametricModel;
using storm::modelchecker::RegionCheckEngine;
using storm::modelchecker::RegionResult;
using storm::modelchecker::RegionResultHypothesis;
using storm::modelchecker::RegionSplitEstimateKind;
using storm::pars::analysis::GraphPreservationStatus;

// Thin wrappers
std::unique_ptr<RegionRefinementChecker> initializeRegionRefinementChecker(storm::Environment const& env, ParametricModel const& model, CheckTask const& task,
                                                                           RegionCheckEngine engine, bool allowModelSimplification,
                                                                           GraphPreservationStatus graphPreservationStatus, bool preconditionsValidated,
                                                                           std::set<Region::VariableType> const& discreteVars) {
    // Default splitting strategy and monotonicity settings
    storm::modelchecker::RegionSplittingStrategy strategy;
    storm::pars::modelchecker::MonotonicityOptions monotonicityOptions;
    storm::pars::modelchecker::RegionRefinementOptions<storm::RationalFunction> settings(
        model, task, engine, strategy, monotonicityOptions, discreteVars, allowModelSimplification, graphPreservationStatus, preconditionsValidated);
    return storm::api::initializeRegionRefinementChecker<storm::RationalFunction>(env, settings);
}

std::set<storm::Polynomial> gatherDerivatives(storm::models::sparse::Model<storm::RationalFunction> const& model, carl::Variable const& var) {
    std::set<storm::Polynomial> derivatives;
    for (auto it : model.getTransitionMatrix()) {
        storm::Polynomial pol = it.getValue().derivative(var, 1).nominator();
        if (!pol.isConstant()) {
            derivatives.insert(pol);
        }
    }
    return derivatives;
}

// Define python bindings
void define_pla(py::module& m) {
    // RegionResult
    py::native_enum<RegionResult>(m, "RegionResult", "enum.Enum", "Types of region check results")
        .value("EXISTS_SAT", RegionResult::ExistsSat)
        .value("EXISTS_VIOLATED", RegionResult::ExistsViolated)
        .value("EXISTS_BOTH", RegionResult::ExistsBoth)
        .value("CENTER_SAT", RegionResult::CenterSat)
        .value("CENTER_VIOLATED", RegionResult::CenterViolated)
        .value("ALL_SAT", RegionResult::AllSat)
        .value("ALL_VIOLATED", RegionResult::AllViolated)
        .value("UNKNOWN", RegionResult::Unknown)
        .finalize();
    m.attr("RegionResult").attr("friendly_name") =
        py::cpp_function(&streamToString<RegionResult>, py::name("friendly_name"), py::is_method(m.attr("RegionResult")));

    // RegionResultHypothesis
    py::native_enum<RegionResultHypothesis>(m, "RegionResultHypothesis", "enum.Enum", "Hypothesis for the result of a parameter region")
        .value("UNKNOWN", RegionResultHypothesis::Unknown)
        .value("ALL_SAT", RegionResultHypothesis::AllSat)
        .value("ALL_VIOLATED", RegionResultHypothesis::AllViolated)
        .finalize();
    m.attr("RegionResultHypothesis").attr("friendly_name") =
        py::cpp_function(&streamToString<RegionResultHypothesis>, py::name("friendly_name"), py::is_method(m.attr("RegionResultHypothesis")));

    // RegionCheckEngine
    py::native_enum<RegionCheckEngine>(m, "RegionCheckEngine", "enum.Enum", R"doc(
Region checking engines, controlling the arithmetic and supported regions.

* ``PARAMETER_LIFTING`` (default): floating-point computations on the lifted model.
* ``EXACT_PARAMETER_LIFTING``: exact rational computations on the lifted model.
* ``VALIDATING_PARAMETER_LIFTING``: floating-point computations followed by
  exact validation of the results.
* ``ROBUST_PARAMETER_LIFTING``: floating-point computations using robust models.
  Supports DTMCs only and allows graph-changing and ill-defined regions.

All engines except ``ROBUST_PARAMETER_LIFTING`` require a well-defined,
graph-preserving region.
)doc")
        .value("PARAMETER_LIFTING", RegionCheckEngine::ParameterLifting)
        .value("EXACT_PARAMETER_LIFTING", RegionCheckEngine::ExactParameterLifting)
        .value("VALIDATING_PARAMETER_LIFTING", RegionCheckEngine::ValidatingParameterLifting)
        .value("ROBUST_PARAMETER_LIFTING", RegionCheckEngine::RobustParameterLifting)
        .finalize();

    // RegionSplitEstimateKind
    py::native_enum<RegionSplitEstimateKind>(m, "RegionSplitEstimateKind", "enum.Enum", "Kinds of estimates for splitting regions")
        .value("DISTANCE", RegionSplitEstimateKind::Distance)
        .value("STATE_VALUE_DELTA", RegionSplitEstimateKind::StateValueDelta)
        .value("STATE_VALUE_DELTA_WEIGHTED", RegionSplitEstimateKind::StateValueDeltaWeighted)
        .value("DERIVATIVE", RegionSplitEstimateKind::Derivative)
        .finalize();

    // GraphPreservationStatus
    py::native_enum<GraphPreservationStatus>(m, "GraphPreservationStatus", "enum.Enum", "Guarantee whether the graph structure is preserved within a region")
        .value("NONE", GraphPreservationStatus::None)
        .value("WELL_DEFINED", GraphPreservationStatus::WellDefined)
        .value("GRAPH_PRESERVING", GraphPreservationStatus::GraphPreserving)
        .value("UNKNOWN", GraphPreservationStatus::Unknown)
        .finalize();

    // Region
    py::classh<Region>(m, "ParameterRegion", "Parameter region given by lower and upper bounds for each parameter")
        .def(py::init<Region::Valuation const&, Region::Valuation const&>(), "lower_boundaries"_a, "upper_boundaries"_a)
        .def_property_readonly("area", &Region::area, "Get area")
        .def("__str__", &streamToString<Region>);
    m.def(
        "parse_region",
        [](std::string const& inputString, std::set<Region::VariableType> const& consideredVariables) {
            return storm::api::parseRegion<storm::RationalFunction>(inputString, consideredVariables);
        },
        "input_string"_a, "considered_variables"_a, "Parse region from string, e.g. 0.3<=p<=0.5,0.1<=q<=0.4");

    // RegionModelChecker
    py::classh<RegionModelChecker> regionModelChecker(m, "RegionModelChecker", "Region model checker via parameter lifting");
    regionModelChecker
        .def("analyze_region",
             py::overload_cast<storm::Environment const&, Region const&, RegionResultHypothesis const&, bool>(&RegionModelChecker::analyzeRegion),
             "Analyze region", "environment"_a, "region"_a, "hypothesis"_a = RegionResultHypothesis::Unknown, "sample_vertices_of_region"_a = false)
        .def("get_bound_at_init_state",
             py::overload_cast<storm::Environment const&, Region const&, storm::solver::OptimizationDirection const&>(&RegionModelChecker::getBoundAtInitState),
             "Get bound at the initial state", "environment"_a, "region"_a, "dir_for_parameters"_a)
        .def("obtain_region_split_estimates", &RegionModelChecker::obtainRegionSplitEstimates, "Get region split estimates", "relevant_parameters"_a)
        .def(
            "specify",
            [](RegionModelChecker& checker, storm::Environment const& env, ParametricModel const& model, CheckTask const& task,
               std::optional<RegionSplitEstimateKind> generateRegionSplitEstimates, bool allowModelSimplifications,
               GraphPreservationStatus graphPreservationStatus) {
                checker.specify(env, model, task, generateRegionSplitEstimates, nullptr, allowModelSimplifications, graphPreservationStatus);
            },
            "Specify model and check task", "environment"_a, "model"_a, "check_task"_a, "generate_region_split_estimates"_a = std::nullopt,
            "allow_model_simplifications"_a = true, "graph_preservation_status"_a = GraphPreservationStatus::GraphPreserving);

    // RegionRefinementChecker
    py::classh<RegionRefinementChecker>(m, "RegionRefinementChecker", "Region refinement checker")
        .def(
            "specify",
            [](RegionRefinementChecker& checker, storm::Environment const& env, ParametricModel const& model, CheckTask const& task,
               bool allowModelSimplifications, GraphPreservationStatus graphPreservationStatus, std::set<Region::VariableType> const& discreteVars) {
                // Default splitting strategy
                storm::modelchecker::RegionSplittingStrategy strategy;
                checker.specify(env, model, task, strategy, discreteVars, nullptr, allowModelSimplifications, graphPreservationStatus);
            },
            "Specify model and check task", "environment"_a, "model"_a, "check_task"_a, "allow_model_simplifications"_a = true,
            "graph_preservation_status"_a = GraphPreservationStatus::GraphPreserving, "discrete_variables"_a = std::set<Region::VariableType>{})
        .def("compute_extremal_value", &RegionRefinementChecker::computeExtremalValue, "Compute extremal value and point with the given precision",
             "environment"_a, "region"_a, "dir"_a, "precision"_a, "absolute_precision"_a = false, "bound_invariant"_a = std::nullopt);

    py::classh<SparseDtmcParameterLiftingModelChecker>(m, "SparseDtmcParameterLiftingModelChecker", "Region model checker for DTMCs", regionModelChecker)
        .def(py::init<>())
        .def(
            "get_bound",
            [](SparseDtmcParameterLiftingModelChecker& checker, storm::Environment const& env, Region const& region,
               storm::solver::OptimizationDirection const& dirForParameters) {
                AnnotatedRegion annotatedRegion(region);
                return checker.getBound(env, annotatedRegion, dirForParameters)->asExplicitQuantitativeCheckResult<double>();
            },
            "Get bounds for all states", "environment"_a, "region"_a, "dir_for_parameters"_a);
    py::classh<SparseMdpParameterLiftingModelChecker>(m, "SparseMdpParameterLiftingModelChecker", "Region model checker for MDPs", regionModelChecker)
        .def(py::init<>())
        .def(
            "get_bound",
            [](SparseMdpParameterLiftingModelChecker& checker, storm::Environment const& env, Region const& region,
               storm::solver::OptimizationDirection const& dirForParameters) {
                AnnotatedRegion annotatedRegion(region);
                return checker.getBound(env, annotatedRegion, dirForParameters)->asExplicitQuantitativeCheckResult<double>();
            },
            "Get bounds for all states", "environment"_a, "region"_a, "dir_for_parameters"_a);

    m.def(
        "initialize_region_model_checker",
        [](storm::Environment const& env, ParametricModel const& model, CheckTask const& task, RegionCheckEngine engine, bool allowModelSimplification,
           GraphPreservationStatus graphPreservationStatus, bool preconditionsValidated) -> std::shared_ptr<RegionModelChecker> {
            return storm::api::initializeRegionModelChecker<storm::RationalFunction>(env, model, task, engine, allowModelSimplification,
                                                                                     graphPreservationStatus, preconditionsValidated);
        },
        "Create and specify a region model checker", "environment"_a, "model"_a, "task"_a, "engine"_a = RegionCheckEngine::ParameterLifting,
        "allow_model_simplification"_a = true, "graph_preservation_status"_a = GraphPreservationStatus::GraphPreserving, "preconditions_validated"_a = false);
    m.def("initialize_region_refinement_checker", &initializeRegionRefinementChecker, "Create and specify a region refinement checker", "environment"_a,
          "model"_a, "task"_a, "engine"_a = RegionCheckEngine::ParameterLifting, "allow_model_simplification"_a = true,
          "graph_preservation_status"_a = GraphPreservationStatus::GraphPreserving, "preconditions_validated"_a = false,
          "discrete_variables"_a = std::set<Region::VariableType>{});
    m.def("gather_derivatives", &gatherDerivatives, "Gather the nonconstant numerators of transition-probability derivatives with respect to a parameter",
          "model"_a, "parameter"_a);
}

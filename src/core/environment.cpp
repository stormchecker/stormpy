#include "environment.h"

#include <pybind11/pytypes.h>
#include <storm/environment/Environment.h>
#include <storm/environment/dd/AllDdEnvironments.h>
#include <storm/environment/exploration/ExplorationEnvironment.h>
#include <storm/environment/modelchecker/AllModelCheckerEnvironments.h>
#include <storm/environment/solver/AllSolverEnvironments.h>
#include <storm/storage/SchedulerClass.h>
#include <storm/storage/dd/cudd/CuddReorderingTechnique.h>
#include <storm/utility/constants.h>
#include <storm/utility/environment.h>

namespace stormpy {

void define_environment(py::module& m) {
    // Enums
    py::native_enum<storm::modelchecker::multiobjective::MultiObjectiveMethod>(m, "MultiObjectiveMethod", "enum.Enum", "Multi-objective model checking method")
        .value("PCAA", storm::modelchecker::multiobjective::MultiObjectiveMethod::Pcaa)
        .value("CONSTRAINT_BASED", storm::modelchecker::multiobjective::MultiObjectiveMethod::ConstraintBased)
        .finalize();

    py::native_enum<storm::SteadyStateDistributionAlgorithm>(m, "SteadyStateDistributionAlgorithm", "enum.Enum",
                                                             "Algorithm for steady state distribution computation")
        .value("AUTOMATIC", storm::SteadyStateDistributionAlgorithm::Automatic)
        .value("EQUATION_SYSTEM", storm::SteadyStateDistributionAlgorithm::EquationSystem)
        .value("EXPECTED_VISITING_TIMES", storm::SteadyStateDistributionAlgorithm::ExpectedVisitingTimes)
        .value("CLASSIC", storm::SteadyStateDistributionAlgorithm::Classic)
        .finalize();

    py::native_enum<storm::ConditionalAlgorithmSetting>(m, "ConditionalAlgorithmSetting", "enum.Enum", "Algorithm used for conditional model checking")
        .value("DEFAULT", storm::ConditionalAlgorithmSetting::Default)
        .value("RESTART", storm::ConditionalAlgorithmSetting::Restart)
        .value("BISECTION", storm::ConditionalAlgorithmSetting::Bisection)
        .value("BISECTION_ADVANCED", storm::ConditionalAlgorithmSetting::BisectionAdvanced)
        .value("BISECTION_PT", storm::ConditionalAlgorithmSetting::BisectionPolicyTracking)
        .value("BISECTION_ADVANCED_PT", storm::ConditionalAlgorithmSetting::BisectionAdvancedPolicyTracking)
        .value("POLICY_ITERATION", storm::ConditionalAlgorithmSetting::PolicyIteration)
        .finalize();

    py::native_enum<storm::MultiObjectiveModelCheckerEnvironment::PrecisionType>(m, "MultiObjectivePrecisionType", "enum.Enum",
                                                                                 "Type of precision for multi-objective model checking")
        .value("ABSOLUTE", storm::MultiObjectiveModelCheckerEnvironment::PrecisionType::Absolute)
        .value("RELATIVE_TO_DIFF", storm::MultiObjectiveModelCheckerEnvironment::PrecisionType::RelativeToDiff)
        .finalize();

    py::native_enum<storm::MultiObjectiveModelCheckerEnvironment::EncodingType>(m, "MultiObjectiveEncodingType", "enum.Enum",
                                                                                "Encoding type for multi-objective model checking")
        .value("AUTO", storm::MultiObjectiveModelCheckerEnvironment::EncodingType::Auto)
        .value("CLASSIC", storm::MultiObjectiveModelCheckerEnvironment::EncodingType::Classic)
        .value("FLOW", storm::MultiObjectiveModelCheckerEnvironment::EncodingType::Flow)
        .finalize();

    py::native_enum<storm::dd::CuddReorderingTechnique>(m, "CuddReorderingTechnique", "enum.Enum", "Reordering technique used in CUDD library")
        .value("NONE", storm::dd::CuddReorderingTechnique::None)
        .value("RANDOM", storm::dd::CuddReorderingTechnique::Random)
        .value("RANDOM_PIVOT", storm::dd::CuddReorderingTechnique::RandomPivot)
        .value("SIFT", storm::dd::CuddReorderingTechnique::Sift)
        .value("SIFT_CONV", storm::dd::CuddReorderingTechnique::SiftConv)
        .value("SYMMETRIC_SIFT", storm::dd::CuddReorderingTechnique::SymmetricSift)
        .value("SYMMETRIC_SIFT_CONV", storm::dd::CuddReorderingTechnique::SymmetricSiftConv)
        .value("GROUP_SIFT", storm::dd::CuddReorderingTechnique::GroupSift)
        .value("GROUP_SIFT_CONV", storm::dd::CuddReorderingTechnique::GroupSiftConv)
        .value("WIN2", storm::dd::CuddReorderingTechnique::Win2)
        .value("WIN2_CONV", storm::dd::CuddReorderingTechnique::Win2Conv)
        .value("WIN3", storm::dd::CuddReorderingTechnique::Win3)
        .value("WIN3_CONV", storm::dd::CuddReorderingTechnique::Win3Conv)
        .value("WIN4", storm::dd::CuddReorderingTechnique::Win4)
        .value("WIN4_CONV", storm::dd::CuddReorderingTechnique::Win4Conv)
        .value("ANNEALING", storm::dd::CuddReorderingTechnique::Annealing)
        .value("GENETIC", storm::dd::CuddReorderingTechnique::Genetic)
        .value("EXACT", storm::dd::CuddReorderingTechnique::Exact)
        .finalize();

    py::native_enum<storm::modelchecker::exploration_detail::PrecomputationType>(m, "PrecomputationType", "enum.Enum",
                                                                                 "Type of precomputation for exploration-based model checking")
        .value("LOCAL", storm::modelchecker::exploration_detail::PrecomputationType::Local)
        .value("GLOBAL", storm::modelchecker::exploration_detail::PrecomputationType::Global)
        .finalize();

    py::native_enum<storm::modelchecker::exploration_detail::NextStateHeuristic>(m, "NextStateHeuristic", "enum.Enum",
                                                                                 "Heuristic to choose the next state during exploration")
        .value("DIFFERENCE_PROBABILITY_SUM", storm::modelchecker::exploration_detail::NextStateHeuristic::DifferenceProbabilitySum)
        .value("PROBABILITY", storm::modelchecker::exploration_detail::NextStateHeuristic::Probability)
        .value("UNIFORM", storm::modelchecker::exploration_detail::NextStateHeuristic::Uniform)
        .finalize();

    // Environments
    py::classh<storm::Environment>(m, "Environment", "Environment configuring the algorithms of Storm")
        .def(py::init<>(), "Construct default environment")
        .def("dd", py::overload_cast<>(&storm::Environment::dd), "Get the dd part of the environment", py::return_value_policy::reference_internal)
        .def("exploration", py::overload_cast<>(&storm::Environment::exploration), "Get the exploration part of the environment",
             py::return_value_policy::reference_internal)
        .def("modelchecker", py::overload_cast<>(&storm::Environment::modelchecker), "Get the model checker part of the environment",
             py::return_value_policy::reference_internal)
        .def("solver", py::overload_cast<>(&storm::Environment::solver), "Get the solver part of the environment", py::return_value_policy::reference_internal)
        .def_property("model_tolerance", &storm::Environment::modelTolerance, &storm::Environment::setModelTolerance,
                      "Tolerance for numerical deviations in the model");

    py::classh<storm::ExplorationEnvironment>(m, "ExplorationEnvironment", "Environment for exploration-based model checking")
        .def_property("precomputation_type", &storm::ExplorationEnvironment::getPrecomputationType, &storm::ExplorationEnvironment::setPrecomputationType,
                      "Type of precomputation")
        .def_property("steps_until_precomputation", &storm::ExplorationEnvironment::getStepsUntilPrecomputation,
                      &storm::ExplorationEnvironment::setStepsUntilPrecomputation, "Number of exploration steps until a precomputation is performed")
        .def_property(
            // Thin wrapper mapping an unset value to None
            "sampled_paths_until_precomputation",
            [](storm::ExplorationEnvironment const& env) -> py::object {
                auto const& value = env.getSampledPathsUntilPrecomputation();
                if (value) {
                    return py::cast(*value);
                }
                return py::none();
            },
            [](storm::ExplorationEnvironment& env, py::object value) {
                if (value.is_none()) {
                    env.unsetSampledPathsUntilPrecomputation();
                } else {
                    env.setSampledPathsUntilPrecomputation(value.cast<uint64_t>());
                }
            },
            "Number of sampled paths until a precomputation is performed (None if unset)")
        .def_property("next_state_heuristic", &storm::ExplorationEnvironment::getNextStateHeuristic, &storm::ExplorationEnvironment::setNextStateHeuristic,
                      "Heuristic to choose the next state")
        .def_property("precision", &storm::ExplorationEnvironment::getPrecision, &storm::ExplorationEnvironment::setPrecision,
                      "Precision of the exploration-based model checking");

    py::classh<storm::ConditionalModelCheckerEnvironment>(m, "ConditionalModelCheckerEnvironment", "Environment for conditional model checking")
        .def_property("algorithm", &storm::ConditionalModelCheckerEnvironment::getAlgorithm, &storm::ConditionalModelCheckerEnvironment::setAlgorithm,
                      "Algorithm for conditional model checking")
        .def_property(
            "precision", &storm::ConditionalModelCheckerEnvironment::getPrecision,
            [](storm::ConditionalModelCheckerEnvironment& env, storm::RationalNumber const& value) { env.setPrecision(value, false); },
            "Precision for conditional model checking")
        .def_property("relative_precision", &storm::ConditionalModelCheckerEnvironment::isRelativePrecision,
                      &storm::ConditionalModelCheckerEnvironment::setRelativePrecision, "Whether the precision is relative");

    py::classh<storm::ModelCheckerEnvironment>(m, "ModelCheckerEnvironment", "Environment for the model checker")
        .def("conditional", py::overload_cast<>(&storm::ModelCheckerEnvironment::conditional), "Get the conditional model checking environment",
             py::return_value_policy::reference_internal)
        .def("multi", py::overload_cast<>(&storm::ModelCheckerEnvironment::multi), "Get the multi-objective model checking environment",
             py::return_value_policy::reference_internal)
        .def_property("steady_state_distribution_algorithm", &storm::ModelCheckerEnvironment::getSteadyStateDistributionAlgorithm,
                      &storm::ModelCheckerEnvironment::setSteadyStateDistributionAlgorithm, "Algorithm for steady state distributions")
        .def_property(
            // Thin wrapper mapping an unset tool to None
            "ltl2da_tool",
            [](storm::ModelCheckerEnvironment const& env) -> py::object {
                if (env.isLtl2daToolSet()) {
                    return py::cast(env.getLtl2daTool());
                }
                return py::none();
            },
            [](storm::ModelCheckerEnvironment& env, py::object value) {
                if (value.is_none()) {
                    env.unsetLtl2daTool();
                } else {
                    env.setLtl2daTool(value.cast<std::string>());
                }
            },
            "Path to external ltl2da tool (None if unset)");

    py::classh<storm::MultiObjectiveModelCheckerEnvironment>(m, "MultiObjectiveModelCheckerEnvironment", "Environment for multi-objective model checking")
        .def_property(
            "method", [](storm::MultiObjectiveModelCheckerEnvironment const& env) { return env.getMethod(); },
            &storm::MultiObjectiveModelCheckerEnvironment::setMethod, "multi-objective model checking method")
        .def_property("precision", &storm::MultiObjectiveModelCheckerEnvironment::getPrecision, &storm::MultiObjectiveModelCheckerEnvironment::setPrecision)
        .def_property("precision_type", &storm::MultiObjectiveModelCheckerEnvironment::getPrecisionType,
                      &storm::MultiObjectiveModelCheckerEnvironment::setPrecisionType)
        .def_property("encoding_type", &storm::MultiObjectiveModelCheckerEnvironment::getEncodingType,
                      &storm::MultiObjectiveModelCheckerEnvironment::setEncodingType)
        .def_property("use_indicator_constraints", &storm::MultiObjectiveModelCheckerEnvironment::getUseIndicatorConstraints,
                      &storm::MultiObjectiveModelCheckerEnvironment::setUseIndicatorConstraints)
        .def_property("use_bscc_order_encoding", &storm::MultiObjectiveModelCheckerEnvironment::getUseBsccOrderEncoding,
                      &storm::MultiObjectiveModelCheckerEnvironment::setUseBsccOrderEncoding)
        .def_property("use_redundant_bscc_constraints", &storm::MultiObjectiveModelCheckerEnvironment::getUseRedundantBsccConstraints,
                      &storm::MultiObjectiveModelCheckerEnvironment::setUseRedundantBsccConstraints)
        .def("is_export_plot_set", &storm::MultiObjectiveModelCheckerEnvironment::isExportPlotSet, "Whether plots are exported")
        .def_property(
            "plot_path_under_approximation",
            [](storm::MultiObjectiveModelCheckerEnvironment const& env) -> py::object {
                auto p = env.getPlotPathUnderApproximation();
                if (p)
                    return py::cast(*p);
                return py::none();
            },
            [](storm::MultiObjectiveModelCheckerEnvironment& env, py::object obj) {
                if (obj.is_none())
                    env.unsetPlotPathUnderApproximation();
                else
                    env.setPlotPathUnderApproximation(obj.cast<std::string>());
            })
        .def_property(
            "plot_path_over_approximation",
            [](storm::MultiObjectiveModelCheckerEnvironment const& env) -> py::object {
                auto p = env.getPlotPathOverApproximation();
                if (p)
                    return py::cast(*p);
                return py::none();
            },
            [](storm::MultiObjectiveModelCheckerEnvironment& env, py::object obj) {
                if (obj.is_none())
                    env.unsetPlotPathOverApproximation();
                else
                    env.setPlotPathOverApproximation(obj.cast<std::string>());
            })
        .def_property(
            "plot_path_pareto_points",
            [](storm::MultiObjectiveModelCheckerEnvironment const& env) -> py::object {
                auto p = env.getPlotPathParetoPoints();
                if (p)
                    return py::cast(*p);
                return py::none();
            },
            [](storm::MultiObjectiveModelCheckerEnvironment& env, py::object obj) {
                if (obj.is_none())
                    env.unsetPlotPathParetoPoints();
                else
                    env.setPlotPathParetoPoints(obj.cast<std::string>());
            })
        .def_property(
            "max_steps",
            [](storm::MultiObjectiveModelCheckerEnvironment const& env) -> py::object {
                if (env.isMaxStepsSet())
                    return py::cast(env.getMaxSteps());
                return py::none();
            },
            [](storm::MultiObjectiveModelCheckerEnvironment& env, py::object obj) {
                if (obj.is_none())
                    env.unsetMaxSteps();
                else
                    env.setMaxSteps(obj.cast<uint64_t>());
            })
        .def_property(
            "scheduler_restriction",
            [](storm::MultiObjectiveModelCheckerEnvironment const& env) -> py::object {
                if (env.isSchedulerRestrictionSet())
                    return py::cast(env.getSchedulerRestriction());
                return py::none();
            },
            [](storm::MultiObjectiveModelCheckerEnvironment& env, py::object obj) {
                if (obj.is_none())
                    env.unsetSchedulerRestriction();
                else
                    env.setSchedulerRestriction(obj.cast<storm::storage::SchedulerClass>());
            })
        .def_property("print_results", &storm::MultiObjectiveModelCheckerEnvironment::isPrintResultsSet,
                      &storm::MultiObjectiveModelCheckerEnvironment::setPrintResults);

    py::classh<storm::SolverEnvironment>(m, "SolverEnvironment", "Environment for solvers")
        .def("min_max", py::overload_cast<>(&storm::SolverEnvironment::minMax), "Get the environment for min-max solvers",
             py::return_value_policy::reference_internal)
        .def("native", py::overload_cast<>(&storm::SolverEnvironment::native), "Get the environment for native solvers",
             py::return_value_policy::reference_internal)
        .def("get_linear_equation_solver_type", &storm::SolverEnvironment::getLinearEquationSolverType, "Get the solver type for linear equation systems")
        .def("set_linear_equation_solver_type", &storm::SolverEnvironment::setLinearEquationSolverType, "Set the solver type for linear equation systems",
             py::arg("value"), py::arg("is_set_from_default") = false)
        .def_property("force_soundness", &storm::SolverEnvironment::isForceSoundness, &storm::SolverEnvironment::setForceSoundness,
                      "Whether sound results are enforced")
        .def_property("force_exact", &storm::SolverEnvironment::isForceExact, &storm::SolverEnvironment::setForceExact, "Whether exact solving is enforced");

    py::classh<storm::NativeSolverEnvironment>(m, "NativeSolverEnvironment", "Environment for native solvers")
        .def_property(
            // Thin wrapper as the setter has a default argument
            "method", &storm::NativeSolverEnvironment::getMethod,
            [](storm::NativeSolverEnvironment& env, storm::solver::NativeLinearEquationSolverMethod value) { env.setMethod(value); }, "Solution method")
        .def_property("maximal_number_of_iterations", &storm::NativeSolverEnvironment::getMaximalNumberOfIterations,
                      &storm::NativeSolverEnvironment::setMaximalNumberOfIterations, "Maximal number of iterations")
        .def_property("precision", &storm::NativeSolverEnvironment::getPrecision, &storm::NativeSolverEnvironment::setPrecision, "Precision")
        .def_property("relative_termination_criterion", &storm::NativeSolverEnvironment::getRelativeTerminationCriterion,
                      &storm::NativeSolverEnvironment::setRelativeTerminationCriterion, "Whether the termination criterion is relative");

    py::classh<storm::MinMaxSolverEnvironment>(m, "MinMaxSolverEnvironment", "Environment for min-max solvers")
        .def_property(
            "method", &storm::MinMaxSolverEnvironment::getMethod,
            [](storm::MinMaxSolverEnvironment& env, storm::solver::MinMaxMethod value) { env.setMethod(value, false); }, "Solution method")
        .def_property("maximal_number_of_iterations", &storm::MinMaxSolverEnvironment::getMaximalNumberOfIterations,
                      &storm::MinMaxSolverEnvironment::setMaximalNumberOfIterations, "Maximal number of iterations")
        .def_property("precision", &storm::MinMaxSolverEnvironment::getPrecision, &storm::MinMaxSolverEnvironment::setPrecision, "Precision")
        .def_property("relative_termination_criterion", &storm::MinMaxSolverEnvironment::getRelativeTerminationCriterion,
                      &storm::MinMaxSolverEnvironment::setRelativeTerminationCriterion, "Whether the termination criterion is relative");

    py::classh<storm::DdEnvironment>(m, "DdEnvironment", "Environment for DD libraries")
        .def("cudd", py::overload_cast<>(&storm::DdEnvironment::cudd), "Get the environment for CUDD", py::return_value_policy::reference_internal)
        .def("sylvan", py::overload_cast<>(&storm::DdEnvironment::sylvan), "Get the environment for Sylvan", py::return_value_policy::reference_internal);

    py::classh<storm::SylvanDdManagerEnvironment>(m, "SylvanDdManagerEnvironment", "Environment for Sylvan DD manager")
        .def_property("maximal_memory", &storm::SylvanDdManagerEnvironment::getMaximalMemory, &storm::SylvanDdManagerEnvironment::setMaximalMemory,
                      "Maximal memory (in MB)")
        .def_property("number_of_threads", &storm::SylvanDdManagerEnvironment::getNumberOfThreads, &storm::SylvanDdManagerEnvironment::setNumberOfThreads,
                      "Number of threads");

    py::classh<storm::CuddDdManagerEnvironment>(m, "CuddDdManagerEnvironment", "Environment for CUDD DD manager")
        .def_property("maximal_memory", &storm::CuddDdManagerEnvironment::getMaximalMemory, &storm::CuddDdManagerEnvironment::setMaximalMemory,
                      "Maximal memory (in MB)")
        .def_property("constant_precision", &storm::CuddDdManagerEnvironment::getConstantPrecision, &storm::CuddDdManagerEnvironment::setConstantPrecision,
                      "Precision for constants")
        .def_property("reordering_enabled", &storm::CuddDdManagerEnvironment::isReorderingEnabled, &storm::CuddDdManagerEnvironment::setReorderingEnabled,
                      "Whether reordering is enabled")
        .def_property("reordering_technique", &storm::CuddDdManagerEnvironment::getReorderingTechnique,
                      &storm::CuddDdManagerEnvironment::setReorderingTechnique, "Reordering technique");

    // Factories for environments
    using EnvironmentFactory = storm::utility::environment::EnvironmentFactory;
    py::classh<EnvironmentFactory>(m, "EnvironmentFactory", "Factory creating environments with default values")
        .def(py::init<>(), "Construct factory")
        .def("create", &EnvironmentFactory::create, "Create a new environment");
    py::classh<storm::utility::environment::SoundEnvironmentFactory, EnvironmentFactory>(m, "SoundEnvironmentFactory",
                                                                                         "Factory creating environments which enforce sound computations")
        .def(py::init<>(), "Construct factory");
    py::classh<storm::utility::environment::ExactEnvironmentFactory, EnvironmentFactory>(m, "ExactEnvironmentFactory",
                                                                                         "Factory creating environments which enforce exact computations")
        .def(py::init<>(), "Construct factory");
    m.def("get_sound_environment", &storm::utility::environment::getSoundEnvironment, "Create a new environment which enforces sound computations");
    m.def("get_exact_environment", &storm::utility::environment::getExactEnvironment, "Create a new environment which enforces exact computations");
}

}  // namespace stormpy

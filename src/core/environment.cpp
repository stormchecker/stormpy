#include "environment.h"

#include <pybind11/pytypes.h>
#include <storm/environment/Environment.h>
#include <storm/environment/dd/AllDdEnvironments.h>
#include <storm/environment/modelchecker/AllModelCheckerEnvironments.h>
#include <storm/environment/solver/AllSolverEnvironments.h>
#include <storm/settings/SettingsManager.h>
#include <storm/storage/SchedulerClass.h>
#include <storm/storage/dd/cudd/CuddReorderingTechnique.h>
#include <storm/utility/constants.h>

#include "src/helpers.h"

void define_environment(py::module& m) {
    py::native_enum<storm::solver::EquationSolverType>(m, "EquationSolverType", "enum.Enum", "Solver type for equation systems")
        .value("native", storm::solver::EquationSolverType::Native)
        .value("eigen", storm::solver::EquationSolverType::Eigen)
        .value("elimination", storm::solver::EquationSolverType::Elimination)
        .value("gmmxx", storm::solver::EquationSolverType::Gmmxx)
        .value("topological", storm::solver::EquationSolverType::Topological)
        .finalize();

    py::native_enum<storm::solver::NativeLinearEquationSolverMethod>(m, "NativeLinearEquationSolverMethod", "enum.Enum",
                                                                     "Method for linear equation systems with the native solver")
        .value("power_iteration", storm::solver::NativeLinearEquationSolverMethod::Power)
        .value("sound_value_iteration", storm::solver::NativeLinearEquationSolverMethod::SoundValueIteration)
        .value("optimistic_value_iteration", storm::solver::NativeLinearEquationSolverMethod::OptimisticValueIteration)
        .value("interval_iteration", storm::solver::NativeLinearEquationSolverMethod::IntervalIteration)
        .value("rational_search", storm::solver::NativeLinearEquationSolverMethod::RationalSearch)
        .value("jacobi", storm::solver::NativeLinearEquationSolverMethod::Jacobi)
        .value("SOR", storm::solver::NativeLinearEquationSolverMethod::SOR)
        .value("gauss_seidel", storm::solver::NativeLinearEquationSolverMethod::GaussSeidel)
        .value("walker_chae", storm::solver::NativeLinearEquationSolverMethod::WalkerChae)
        .finalize();

    py::native_enum<storm::solver::MinMaxMethod>(m, "MinMaxMethod", "enum.Enum", "Method for min-max equation systems")
        .value("policy_iteration", storm::solver::MinMaxMethod::PolicyIteration)
        .value("value_iteration", storm::solver::MinMaxMethod::ValueIteration)
        .value("linear_programming", storm::solver::MinMaxMethod::LinearProgramming)
        .value("topological", storm::solver::MinMaxMethod::Topological)
        .value("rational_search", storm::solver::MinMaxMethod::RationalSearch)
        .value("interval_iteration", storm::solver::MinMaxMethod::IntervalIteration)
        .value("sound_value_iteration", storm::solver::MinMaxMethod::SoundValueIteration)
        .value("optimistic_value_iteration", storm::solver::MinMaxMethod::OptimisticValueIteration)
        .finalize();

    // Multi-objective related enums
    py::native_enum<storm::modelchecker::multiobjective::MultiObjectiveMethod>(m, "MultiObjectiveMethod", "enum.Enum", "Multi-objective model checking method")
        .value("pcaa", storm::modelchecker::multiobjective::MultiObjectiveMethod::Pcaa)
        .value("constraint_based", storm::modelchecker::multiobjective::MultiObjectiveMethod::ConstraintBased)
        .finalize();

    // Added enums for model checker environment
    py::native_enum<storm::SteadyStateDistributionAlgorithm>(m, "SteadyStateDistributionAlgorithm", "enum.Enum",
                                                             "Algorithm for steady state distribution computation")
        .value("automatic", storm::SteadyStateDistributionAlgorithm::Automatic)
        .value("equation_system", storm::SteadyStateDistributionAlgorithm::EquationSystem)
        .value("expected_visiting_times", storm::SteadyStateDistributionAlgorithm::ExpectedVisitingTimes)
        .value("classic", storm::SteadyStateDistributionAlgorithm::Classic)
        .finalize();

    py::native_enum<storm::ConditionalAlgorithmSetting>(m, "ConditionalAlgorithmSetting", "enum.Enum", "Algorithm used for conditional model checking")
        .value("default", storm::ConditionalAlgorithmSetting::Default)
        .value("restart", storm::ConditionalAlgorithmSetting::Restart)
        .value("bisection", storm::ConditionalAlgorithmSetting::Bisection)
        .value("bisection_advanced", storm::ConditionalAlgorithmSetting::BisectionAdvanced)
        .value("bisection_pt", storm::ConditionalAlgorithmSetting::BisectionPolicyTracking)
        .value("bisection_advanced_pt", storm::ConditionalAlgorithmSetting::BisectionAdvancedPolicyTracking)
        .value("policy_iteration", storm::ConditionalAlgorithmSetting::PolicyIteration)
        .finalize();

    py::native_enum<storm::MultiObjectiveModelCheckerEnvironment::PrecisionType>(m, "MultiObjectivePrecisionType", "enum.Enum",
                                                                                 "Type of precision for multi-objective model checking")
        .value("absolute", storm::MultiObjectiveModelCheckerEnvironment::PrecisionType::Absolute)
        .value("relative_to_diff", storm::MultiObjectiveModelCheckerEnvironment::PrecisionType::RelativeToDiff)
        .finalize();

    py::native_enum<storm::MultiObjectiveModelCheckerEnvironment::EncodingType>(m, "MultiObjectiveEncodingType", "enum.Enum",
                                                                                "Encoding type for multi-objective model checking")
        .value("auto", storm::MultiObjectiveModelCheckerEnvironment::EncodingType::Auto)
        .value("classic", storm::MultiObjectiveModelCheckerEnvironment::EncodingType::Classic)
        .value("flow", storm::MultiObjectiveModelCheckerEnvironment::EncodingType::Flow)
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

    // Scheduler class bindings (needed for scheduler restriction)
    py::native_enum<storm::storage::SchedulerClass::MemoryPattern>(m, "SchedulerMemoryPattern", "enum.Enum", "Memory pattern of a scheduler")
        .value("arbitrary", storm::storage::SchedulerClass::MemoryPattern::Arbitrary)
        .value("goal_memory", storm::storage::SchedulerClass::MemoryPattern::GoalMemory)
        .value("counter", storm::storage::SchedulerClass::MemoryPattern::Counter)
        .finalize();

    py::class_<storm::storage::SchedulerClass>(m, "SchedulerClass", "Scheduler class restriction")
        .def(py::init<>())
        .def_property("deterministic", &storm::storage::SchedulerClass::isDeterministic,
                      [](storm::storage::SchedulerClass& sc, bool v) { sc.setIsDeterministic(v); })
        .def_property(
            "memory_states",
            [](storm::storage::SchedulerClass const& sc) -> py::object {
                if (sc.isMemoryBounded())
                    return py::cast(sc.getMemoryStates());
                return py::none();
            },
            [](storm::storage::SchedulerClass& sc, py::object obj) {
                if (obj.is_none())
                    sc.unsetMemoryStates();
                else
                    sc.setMemoryStates(obj.cast<uint64_t>());
            })
        .def_property_readonly("is_memory_bounded", &storm::storage::SchedulerClass::isMemoryBounded)
        .def_property_readonly("memory_pattern", &storm::storage::SchedulerClass::getMemoryPattern)
        .def("set_memory_pattern", [](storm::storage::SchedulerClass& sc, storm::storage::SchedulerClass::MemoryPattern p) { sc.setMemoryPattern(p); })
        .def("set_positional", &storm::storage::SchedulerClass::setPositional);

    py::class_<storm::Environment>(m, "Environment", "Environment")
        .def(py::init<>(), "Construct default environment")
        .def_property_readonly(
            "solver_environment", [](storm::Environment& env) -> auto& { return env.solver(); }, "solver part of environment")
        .def_property_readonly(
            "model_checker_environment", [](storm::Environment& env) -> auto& { return env.modelchecker(); }, "model checker part of environment")
        .def_property_readonly("dd_environment", [](storm::Environment& env) -> auto& { return env.dd(); }, "dd part of environment");

    py::class_<storm::ConditionalModelCheckerEnvironment>(m, "ConditionalModelCheckerEnvironment", "Environment for conditional model checking")
        .def_property("algorithm", &storm::ConditionalModelCheckerEnvironment::getAlgorithm, &storm::ConditionalModelCheckerEnvironment::setAlgorithm,
                      "algorithm for conditional model checking")
        .def_property(
            "precision", &storm::ConditionalModelCheckerEnvironment::getPrecision,
            [](storm::ConditionalModelCheckerEnvironment& env, storm::RationalNumber value) { env.setPrecision(value, false); },
            "precision for conditional model checking")
        .def_property("relative", &storm::ConditionalModelCheckerEnvironment::isRelativePrecision,
                      &storm::ConditionalModelCheckerEnvironment::setRelativePrecision, "whether the precision is relative");

    py::class_<storm::ModelCheckerEnvironment>(m, "ModelCheckerEnvironment", "Environment for the model checker")
        .def_property("steady_state_distribution_algorithm", &storm::ModelCheckerEnvironment::getSteadyStateDistributionAlgorithm,
                      &storm::ModelCheckerEnvironment::setSteadyStateDistributionAlgorithm, "steady state distribution algorithm used")
        .def_property(
            "ltl2da_tool",
            [](storm::ModelCheckerEnvironment const& env) -> py::object {
                if (env.isLtl2daToolSet())
                    return py::cast(env.getLtl2daTool());
                return py::none();
            },
            [](storm::ModelCheckerEnvironment& env, py::object obj) {
                if (obj.is_none())
                    env.unsetLtl2daTool();
                else
                    env.setLtl2daTool(obj.cast<std::string>());
            },
            "Path to external ltl2da tool (None to unset)")
        .def_property_readonly(
            "conditional", [](storm::ModelCheckerEnvironment& env) -> storm::ConditionalModelCheckerEnvironment& { return env.conditional(); },
            py::return_value_policy::reference, "Access conditional model checking sub-environment")
        .def_property_readonly(
            "multi", [](storm::ModelCheckerEnvironment& env) -> storm::MultiObjectiveModelCheckerEnvironment& { return env.multi(); },
            py::return_value_policy::reference, "Access multi-objective sub-environment");

    py::class_<storm::MultiObjectiveModelCheckerEnvironment>(m, "MultiObjectiveModelCheckerEnvironment", "Environment for multi-objective model checking")
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
        .def_property_readonly("export_plot_set", &storm::MultiObjectiveModelCheckerEnvironment::isExportPlotSet)
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

    py::class_<storm::SolverEnvironment>(m, "SolverEnvironment", "Environment for solvers")
        .def("set_force_sound", &storm::SolverEnvironment::setForceSoundness, "force soundness", py::arg("new_value") = true)
        .def("set_force_exact", &storm::SolverEnvironment::setForceExact, "force exact solving", py::arg("new_value") = true)
        .def("set_linear_equation_solver_type", &storm::SolverEnvironment::setLinearEquationSolverType, "set solver type to use", py::arg("new_value"),
             py::arg("set_from_default") = false)
        .def_property_readonly("minmax_solver_environment", [](storm::SolverEnvironment& senv) -> auto& { return senv.minMax(); })
        .def_property_readonly("native_solver_environment", [](storm::SolverEnvironment& senv) -> auto& { return senv.native(); });

    py::class_<storm::NativeSolverEnvironment>(m, "NativeSolverEnvironment", "Environment for Native solvers")
        .def_property("method", &storm::NativeSolverEnvironment::getMethod,
                      [](storm::NativeSolverEnvironment& nsenv, storm::solver::NativeLinearEquationSolverMethod const& m) { nsenv.setMethod(m); })
        .def_property("maximum_iterations", &storm::NativeSolverEnvironment::getMaximalNumberOfIterations,
                      [](storm::NativeSolverEnvironment& nsenv, uint64_t iters) { nsenv.setMaximalNumberOfIterations(iters); })
        .def_property("precision", &storm::NativeSolverEnvironment::getPrecision, &storm::NativeSolverEnvironment::setPrecision);

    py::class_<storm::MinMaxSolverEnvironment>(m, "MinMaxSolverEnvironment", "Environment for Min-Max-Solvers")
        .def_property("method", &storm::MinMaxSolverEnvironment::getMethod,
                      [](storm::MinMaxSolverEnvironment& mmenv, storm::solver::MinMaxMethod const& m) { mmenv.setMethod(m, false); })
        .def_property("precision", &storm::MinMaxSolverEnvironment::getPrecision, &storm::MinMaxSolverEnvironment::setPrecision);

    py::class_<storm::DdEnvironment>(m, "DdEnvironment", "Environment for DD libraries")
        .def_property_readonly("sylvan", [](storm::DdEnvironment& senv) -> auto& { return senv.sylvan(); })
        .def_property_readonly("cudd", [](storm::DdEnvironment& senv) -> auto& { return senv.cudd(); });

    py::class_<storm::SylvanDdManagerEnvironment>(m, "SylvanDdManagerEnvironment", "Environment for Sylvan Dd manager")
        .def_property("maximal_memory", &storm::SylvanDdManagerEnvironment::getMaximalMemory, &storm::SylvanDdManagerEnvironment::setMaximalMemory)
        .def_property("number_threads", &storm::SylvanDdManagerEnvironment::getNumberOfThreads, &storm::SylvanDdManagerEnvironment::setNumberOfThreads);

    py::class_<storm::CuddDdManagerEnvironment>(m, "CuddDdManagerEnvironment", "Environment for CUDD Dd manager")
        .def_property("maximal_memory", &storm::CuddDdManagerEnvironment::getMaximalMemory, &storm::CuddDdManagerEnvironment::setMaximalMemory)
        .def_property("constant_precision", &storm::CuddDdManagerEnvironment::getConstantPrecision, &storm::CuddDdManagerEnvironment::setConstantPrecision)
        .def_property("reordering_enabled", &storm::CuddDdManagerEnvironment::isReorderingEnabled, &storm::CuddDdManagerEnvironment::setReorderingEnabled)
        .def_property("reordering_technique", &storm::CuddDdManagerEnvironment::getReorderingTechnique,
                      &storm::CuddDdManagerEnvironment::setReorderingTechnique);
}

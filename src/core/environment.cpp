#include "environment.h"
#include "src/helpers.h"
#include "storm/environment/Environment.h"
#include "storm/environment/solver/SolverEnvironment.h"
#include "storm/environment/solver/AllSolverEnvironments.h"

void define_environment(py::module& m) {
    py::enum_<storm::solver::EquationSolverType>(m, "EquationSolverType", "Solver type for equation systems")
        .value("native", storm::solver::EquationSolverType::Native)
        .value("eigen", storm::solver::EquationSolverType::Eigen)
        .value("elimination", storm::solver::EquationSolverType::Elimination)
        .value("gmmxx", storm::solver::EquationSolverType::Gmmxx)
        .value("topological", storm::solver::EquationSolverType::Topological)
    ;

    py::enum_<storm::solver::NativeLinearEquationSolverMethod>(m, "NativeLinearEquationSolverMethod", "Method for linear equation systems with the native solver")
        .value("power_iteration", storm::solver::NativeLinearEquationSolverMethod::Power)
        .value("sound_value_iteration", storm::solver::NativeLinearEquationSolverMethod::SoundValueIteration)
        .value("optimistic_value_iteration", storm::solver::NativeLinearEquationSolverMethod::OptimisticValueIteration)
        .value("interval_iteration", storm::solver::NativeLinearEquationSolverMethod::IntervalIteration)
        .value("rational_search", storm::solver::NativeLinearEquationSolverMethod::RationalSearch)
        .value("jacobi", storm::solver::NativeLinearEquationSolverMethod::Jacobi)
        .value("SOR", storm::solver::NativeLinearEquationSolverMethod::SOR)
        .value("gauss_seidel", storm::solver::NativeLinearEquationSolverMethod::GaussSeidel)
        .value("walker_chae", storm::solver::NativeLinearEquationSolverMethod::WalkerChae)
    ;

    py::enum_<storm::solver::MinMaxMethod>(m, "MinMaxMethod", "Method for min-max equation systems")
        .value("policy_iteration", storm::solver::MinMaxMethod::PolicyIteration)
        .value("value_iteration", storm::solver::MinMaxMethod::ValueIteration)
        .value("linear_programming", storm::solver::MinMaxMethod::LinearProgramming)
        .value("topological", storm::solver::MinMaxMethod::Topological)
        .value("rational_search", storm::solver::MinMaxMethod::RationalSearch)
        .value("interval_iteration", storm::solver::MinMaxMethod::IntervalIteration)
        .value("sound_value_iteration", storm::solver::MinMaxMethod::SoundValueIteration)
        .value("optimistic_value_iteration", storm::solver::MinMaxMethod::OptimisticValueIteration)
    ;

    py::class_<storm::Environment>(m, "Environment", "Environment")
        .def(py::init<>(), "Construct default environment")
        .def_property_readonly("solver_environment", [](storm::Environment& env) -> auto& {return env.solver();}, "solver part of environment")
    ;

    py::class_<storm::SolverEnvironment>(m, "SolverEnvironment", "Environment for solvers")
        .def("set_force_sound", &storm::SolverEnvironment::setForceSoundness, "force soundness", py::arg("new_value") = true)
        .def("set_force_exact", &storm::SolverEnvironment::setForceExact, "force exact solving", py::arg("new_value") = true)
        .def("set_linear_equation_solver_type", &storm::SolverEnvironment::setLinearEquationSolverType, "set solver type to use", py::arg("new_value"), py::arg("set_from_default") = false)
        .def_property_readonly("minmax_solver_environment", [](storm::SolverEnvironment& senv) -> auto& { return senv.minMax(); })
        .def_property_readonly("native_solver_environment", [](storm::SolverEnvironment& senv) -> auto& {return senv.native(); })
    ;

    py::class_<storm::NativeSolverEnvironment>(m, "NativeSolverEnvironment", "Environment for Native solvers")
        .def_property("method", &storm::NativeSolverEnvironment::getMethod, [](storm::NativeSolverEnvironment& nsenv, storm::solver::NativeLinearEquationSolverMethod const& m) {nsenv.setMethod(m);})
        .def_property("maximum_iterations", &storm::NativeSolverEnvironment::getMaximalNumberOfIterations, [](storm::NativeSolverEnvironment& nsenv, uint64_t iters) {nsenv.setMaximalNumberOfIterations(iters);} )
        .def_property("precision", &storm::NativeSolverEnvironment::getPrecision, &storm::NativeSolverEnvironment::setPrecision)
    ;

    py::class_<storm::MinMaxSolverEnvironment>(m, "MinMaxSolverEnvironment", "Environment for Min-Max-Solvers")
        .def_property("method", &storm::MinMaxSolverEnvironment::getMethod, [](storm::MinMaxSolverEnvironment& mmenv, storm::solver::MinMaxMethod const& m) { mmenv.setMethod(m, false); } )
        .def_property("precision", &storm::MinMaxSolverEnvironment::getPrecision,  &storm::MinMaxSolverEnvironment::setPrecision);



}


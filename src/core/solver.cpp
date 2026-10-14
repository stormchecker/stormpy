#include "solver.h"

#include <storm/solver/OptimizationDirection.h>
#include <storm/solver/SmtSolver.h>
#include <storm/solver/SolverSelectionOptions.h>
#include <storm/solver/UncertaintyResolutionMode.h>
#include <storm/solver/Z3SmtSolver.h>
#include <storm/storage/expressions/ExpressionManager.h>
#include <storm/utility/solver.h>

namespace stormpy {

void define_solver(py::module& m) {
    py::native_enum<storm::solver::OptimizationDirection>(m, "OptimizationDirection", "enum.Enum", "Direction of optimization")
        .value("MINIMIZE", storm::solver::OptimizationDirection::Minimize)
        .value("MAXIMIZE", storm::solver::OptimizationDirection::Maximize)
        .finalize();

    py::native_enum<storm::solver::UncertaintyResolutionMode>(m, "UncertaintyResolutionMode", "enum.Enum", "How uncertainty in interval models is resolved")
        .value("MINIMIZE", storm::solver::UncertaintyResolutionMode::Minimize)
        .value("MAXIMIZE", storm::solver::UncertaintyResolutionMode::Maximize)
        .value("ROBUST", storm::solver::UncertaintyResolutionMode::Robust)
        .value("COOPERATIVE", storm::solver::UncertaintyResolutionMode::Cooperative)
        .value("UNSET", storm::solver::UncertaintyResolutionMode::Unset)
        .finalize();

    py::native_enum<storm::solver::EquationSolverType>(m, "EquationSolverType", "enum.Enum", "Solver type for equation systems")
        .value("NATIVE", storm::solver::EquationSolverType::Native)
        .value("GMMXX", storm::solver::EquationSolverType::Gmmxx)
        .value("EIGEN", storm::solver::EquationSolverType::Eigen)
        .value("ELIMINATION", storm::solver::EquationSolverType::Elimination)
        .value("TOPOLOGICAL", storm::solver::EquationSolverType::Topological)
        .value("ACYCLIC", storm::solver::EquationSolverType::Acyclic)
        .finalize();

    py::native_enum<storm::solver::NativeLinearEquationSolverMethod>(m, "NativeLinearEquationSolverMethod", "enum.Enum",
                                                                     "Method for linear equation systems with the native solver")
        .value("JACOBI", storm::solver::NativeLinearEquationSolverMethod::Jacobi)
        .value("GAUSS_SEIDEL", storm::solver::NativeLinearEquationSolverMethod::GaussSeidel)
        .value("SOR", storm::solver::NativeLinearEquationSolverMethod::SOR)
        .value("WALKER_CHAE", storm::solver::NativeLinearEquationSolverMethod::WalkerChae)
        .value("POWER", storm::solver::NativeLinearEquationSolverMethod::Power)
        .value("SOUND_VALUE_ITERATION", storm::solver::NativeLinearEquationSolverMethod::SoundValueIteration)
        .value("OPTIMISTIC_VALUE_ITERATION", storm::solver::NativeLinearEquationSolverMethod::OptimisticValueIteration)
        .value("INTERVAL_ITERATION", storm::solver::NativeLinearEquationSolverMethod::IntervalIteration)
        .value("RATIONAL_SEARCH", storm::solver::NativeLinearEquationSolverMethod::RationalSearch)
        .finalize();

    py::native_enum<storm::solver::MinMaxMethod>(m, "MinMaxMethod", "enum.Enum", "Method for min-max equation systems")
        .value("VALUE_ITERATION", storm::solver::MinMaxMethod::ValueIteration)
        .value("POLICY_ITERATION", storm::solver::MinMaxMethod::PolicyIteration)
        .value("LINEAR_PROGRAMMING", storm::solver::MinMaxMethod::LinearProgramming)
        .value("TOPOLOGICAL", storm::solver::MinMaxMethod::Topological)
        .value("RATIONAL_SEARCH", storm::solver::MinMaxMethod::RationalSearch)
        .value("INTERVAL_ITERATION", storm::solver::MinMaxMethod::IntervalIteration)
        .value("SOUND_VALUE_ITERATION", storm::solver::MinMaxMethod::SoundValueIteration)
        .value("OPTIMISTIC_VALUE_ITERATION", storm::solver::MinMaxMethod::OptimisticValueIteration)
        .finalize();
}

void define_smt_solver(py::module& m) {
    using SmtSolver = storm::solver::SmtSolver;
    using Z3SmtSolver = storm::solver::Z3SmtSolver;
    using ModelReference = storm::solver::SmtSolver::ModelReference;

    py::native_enum<SmtSolver::CheckResult>(m, "SmtCheckResult", "enum.Enum", "Result type")
        .value("SAT", SmtSolver::CheckResult::Sat)
        .value("UNSAT", SmtSolver::CheckResult::Unsat)
        .value("UNKNOWN", SmtSolver::CheckResult::Unknown)
        .finalize();

    py::classh<ModelReference> modelref(m, "ModelReference", "Lightweight Wrapper around results");
    modelref.def("get_boolean_value", &ModelReference::getBooleanValue, "Get a value for a boolean variable", py::arg("variable"))
        .def("get_integer_value", &ModelReference::getIntegerValue, "Get a value for an integer variable", py::arg("variable"))
        .def("get_rational_value", &ModelReference::getRationalValue, "Get a value (as double) for an rational variable", py::arg("variable"));

    py::classh<SmtSolver> smtsolver(m, "SmtSolver", "Generic Storm SmtSolver Wrapper");
    smtsolver.def("push", &SmtSolver::push, "Push")
        .def("pop", py::overload_cast<uint_fast64_t>(&SmtSolver::pop), "Pop", py::arg("n"))
        .def("reset", &SmtSolver::reset, "Reset")
        .def("add", py::overload_cast<storm::expressions::Expression const&>(&SmtSolver::add), "Add constraint", py::arg("assertion"))
        .def("check", &SmtSolver::check, "Check")
        .def("get_model", &SmtSolver::getModel, "Get the model");

    py::classh<Z3SmtSolver> z3solver(m, "Z3SmtSolver", "z3 API for storm smtsolver wrapper", smtsolver);
    z3solver.def(pybind11::init<storm::expressions::ExpressionManager&>(), py::arg("manager"));

    py::classh<storm::utility::solver::SmtSolverFactory> smtfactory(m, "SmtSolverFactory", "Factory for creating SMT Solvers");
    py::classh<storm::utility::solver::Z3SmtSolverFactory> z3factory(m, "Z3SmtSolverFactory", "Factory for creating z3 based SMT solvers", smtfactory);
    z3factory.def(py::init<>());
}

}  // namespace stormpy

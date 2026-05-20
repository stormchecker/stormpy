#include "smtsolver.h"
#include <storm/solver/SmtSolver.h>
#include <storm/solver/Z3SmtSolver.h>
#include <storm/utility/solver.h>
#include "storm/storage/expressions/ExpressionManager.h"

void define_smt(py::module& m) {
    using SmtSolver = storm::solver::SmtSolver;
    using Z3SmtSolver = storm::solver::Z3SmtSolver;
    using ModelReference = storm::solver::SmtSolver::ModelReference;

    py::enum_<SmtSolver::CheckResult>(m, "SmtCheckResult", "Result type")
        .value("Sat", SmtSolver::CheckResult::Sat)
        .value("Unsat", SmtSolver::CheckResult::Unsat)
        .value("Unknown", SmtSolver::CheckResult::Unknown);

    py::class_<ModelReference, std::shared_ptr<ModelReference>> modelref(m, "ModelReference", "Lightweight Wrapper around results");
    modelref.def("get_boolean_value", &ModelReference::getBooleanValue, "get a value for a boolean variable", py::arg("variable"))
        .def("get_integer_value", &ModelReference::getIntegerValue, "get a value for an integer variable", py::arg("variable"))
        .def("get_rational_value", &ModelReference::getRationalValue, "get a value (as double) for an rational variable", py::arg("variable"));

    py::class_<SmtSolver> smtsolver(m, "SmtSolver", "Generic Storm SmtSolver Wrapper");
    smtsolver.def("push", &SmtSolver::push, "push")
        .def(
            "pop", [](SmtSolver& solver, uint64_t n) { solver.pop(n); }, "pop", py::arg("levels"))
        .def("reset", &SmtSolver::reset, "reset")
        .def(
            "add", [](SmtSolver& solver, storm::expressions::Expression const& expr) { solver.add(expr); }, "addconstraint")
        .def("check", &SmtSolver::check, "check")
        .def_property_readonly("model", &SmtSolver::getModel, "get the model");

    py::class_<Z3SmtSolver> z3solver(m, "Z3SmtSolver", "z3 API for storm smtsolver wrapper", smtsolver);
    z3solver.def(pybind11::init<storm::expressions::ExpressionManager&>());

    py::class_<storm::utility::solver::SmtSolverFactory, std::shared_ptr<storm::utility::solver::SmtSolverFactory>> smtfactory(
        m, "SmtSolverFactory", "Factory for creating SMT Solvers");
    py::class_<storm::utility::solver::Z3SmtSolverFactory, std::shared_ptr<storm::utility::solver::Z3SmtSolverFactory>> z3factory(
        m, "Z3SmtSolverFactory", "Factory for creating z3 based SMT solvers", smtfactory);
    z3factory.def(py::init<>());
}
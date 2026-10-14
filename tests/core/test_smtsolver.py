import stormpy

import pytest


class TestSmtSolver:
    def test_smtsolver_init(self):
        manager = stormpy.expressions.ExpressionManager()
        solver = stormpy.developer.Z3SmtSolver(manager)

    def test_smtsolver_trivial(self):
        manager = stormpy.expressions.ExpressionManager()
        solver = stormpy.developer.Z3SmtSolver(manager)
        solver.add(manager.boolean(True))
        assert solver.check() != stormpy.developer.SmtCheckResult.UNSAT
        assert solver.check() == stormpy.developer.SmtCheckResult.SAT
        solver.add(manager.boolean(False))
        assert solver.check() == stormpy.developer.SmtCheckResult.UNSAT
        assert solver.check() != stormpy.developer.SmtCheckResult.SAT

    def test_smtsolver_arithmetic_unsat(self):
        manager = stormpy.expressions.ExpressionManager()
        x = manager.declare_integer_variable("x")
        xe = x.get_expression()
        c1 = stormpy.expressions.Expression.Geq(xe, manager.integer(1))
        c2 = stormpy.expressions.Expression.Less(xe, manager.integer(0))
        solver = stormpy.developer.Z3SmtSolver(manager)
        solver.add(c1)
        solver.add(c2)
        assert solver.check() == stormpy.developer.SmtCheckResult.UNSAT

    def test_smtsolver_arithmetic_sat(self):
        manager = stormpy.expressions.ExpressionManager()
        x = manager.declare_integer_variable("x")
        xe = x.get_expression()
        c1 = stormpy.expressions.Expression.Geq(xe, manager.integer(1))
        c2 = stormpy.expressions.Expression.Less(xe, manager.integer(2))
        solver = stormpy.developer.Z3SmtSolver(manager)
        solver.add(c1)
        solver.add(c2)
        assert solver.check() == stormpy.developer.SmtCheckResult.SAT
        assert solver.get_model().get_integer_value(x) == 1

    def test_smtsolver_keyword_arguments(self):
        manager = stormpy.expressions.ExpressionManager()
        x = manager.declare_integer_variable("x")
        solver = stormpy.developer.Z3SmtSolver(manager=manager)
        solver.add(assertion=stormpy.expressions.Expression.Eq(x.get_expression(), manager.integer(1)))
        solver.push()
        solver.add(assertion=stormpy.expressions.Expression.Eq(x.get_expression(), manager.integer(2)))
        assert solver.check() == stormpy.developer.SmtCheckResult.UNSAT
        solver.pop(n=1)
        assert solver.check() == stormpy.developer.SmtCheckResult.SAT
        assert solver.get_model().get_integer_value(x) == 1

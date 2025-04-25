import stormpy

import pytest


class TestSmtSolver:
    def test_smtsolver_init(self):
        manager = stormpy.ExpressionManager()
        solver = stormpy.utility.Z3SmtSolver(manager)

    def test_smtsolver_trivial(self):
        manager = stormpy.ExpressionManager()
        solver = stormpy.utility.Z3SmtSolver(manager)
        solver.add(manager.create_boolean(True))
        assert solver.check() != stormpy.utility.SmtCheckResult.Unsat
        assert solver.check() == stormpy.utility.SmtCheckResult.Sat
        solver.add(manager.create_boolean(False))
        assert solver.check() == stormpy.utility.SmtCheckResult.Unsat
        assert solver.check() != stormpy.utility.SmtCheckResult.Sat

    def test_smtsolver_arithmetic_unsat(self):
        manager = stormpy.ExpressionManager()
        x = manager.create_integer_variable("x")
        xe = x.get_expression()
        c1 = stormpy.Expression.Geq(xe, manager.create_integer(1))
        c2 = stormpy.Expression.Less(xe, manager.create_integer(0))
        solver = stormpy.utility.Z3SmtSolver(manager)
        solver.add(c1)
        solver.add(c2)
        assert solver.check() == stormpy.utility.SmtCheckResult.Unsat

    def test_smtsolver_arithmetic_unsat(self):
        manager = stormpy.ExpressionManager()
        x = manager.create_integer_variable("x")
        xe = x.get_expression()
        c1 = stormpy.Expression.Geq(xe, manager.create_integer(1))
        c2 = stormpy.Expression.Less(xe, manager.create_integer(0))
        solver = stormpy.utility.Z3SmtSolver(manager)
        solver.add(c1)
        solver.add(c2)
        assert solver.check() == stormpy.utility.SmtCheckResult.Unsat

    def test_smtsolver_arithmetic_unsat(self):
        manager = stormpy.ExpressionManager()
        x = manager.create_integer_variable("x")
        xe = x.get_expression()
        c1 = stormpy.Expression.Geq(xe, manager.create_integer(1))
        c2 = stormpy.Expression.Less(xe, manager.create_integer(2))
        solver = stormpy.utility.Z3SmtSolver(manager)
        solver.add(c1)
        solver.add(c2)
        assert solver.check() == stormpy.utility.SmtCheckResult.Sat
        assert solver.model.get_integer_value(x) == 1

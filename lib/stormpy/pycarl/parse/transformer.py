import importlib
from lark import Transformer

from stormpy.pycarl import Variable, VariableType, variable_with_name
from stormpy.pycarl.formula import FormulaType, Relation


class CarlParserTransformer(Transformer):
    def __init__(self, package):
        self.package = package
        self.formula_pkg = importlib.import_module(package.__name__ + ".formula")
        self._constraint_op_map = {
            "=": Relation.EQ,
            "<": Relation.LESS,
            "<=": Relation.LEQ,
            ">": Relation.GREATER,
            ">=": Relation.GEQ,
            "!=": Relation.NEQ,
        }
        self._formula_op_map = {
            "and": FormulaType.AND,
            "or": FormulaType.OR,
            "xor": FormulaType.XOR,
            "=": FormulaType.IFF,
            "=>": FormulaType.IMPLIES,
            "ite": FormulaType.ITE,
        }

    def start(self, items):
        return items[0]

    def carl_expr(self, items):
        return items[0]

    def form_expr(self, items):
        val = items[0]
        if isinstance(val, self.formula_pkg.Constraint):
            return self.formula_pkg.Formula(val)
        return val

    def formula_nary(self, items):
        formula_type = self._formula_op_map[items[0]]
        subformulas = items[1:]

        if formula_type == FormulaType.ITE:
            if len(subformulas) != 3:
                raise ValueError("ITE requires exactly 3 subformulas")
            return self.formula_pkg.Formula(formula_type, subformulas)

        if len(subformulas) == 1 and formula_type in (FormulaType.AND, FormulaType.OR):
            return subformulas[0]

        if len(subformulas) < 2:
            raise ValueError(f"{formula_type} requires at least 2 subformulas")

        if formula_type in (FormulaType.IFF, FormulaType.IMPLIES):
            # Right-associative
            result = subformulas[0]
            for sub in subformulas[1:]:
                result = self.formula_pkg.Formula(formula_type, [result, sub])
            return result

        return self.formula_pkg.Formula(formula_type, subformulas)

    def formula_unary(self, items):
        return ~items[1]

    def constraint(self, items):
        op = items[0]
        lhs = items[1]
        rhs = items[2]
        diff = self._safe_sub(lhs, rhs)
        relation = self._constraint_op_map[op]
        return self.formula_pkg.Constraint(diff, relation)

    def arith_unary(self, items):
        if items[0] == "-":
            return -items[1]
        else:
            return items[1]

    def arith_nary(self, items):
        op = items[0]
        operands = items[1:]
        result = operands[0]
        for operand in operands[1:]:
            if op == "+":
                result = self._safe_add(result, operand)
            elif op == "-":
                result = self._safe_sub(result, operand)
            elif op == "*":
                result = self._safe_mul(result, operand)
            elif op == "/":
                result = result / operand
        return result

    def _safe_add(self, a, b):
        try:
            return a + b
        except TypeError:
            try:
                return b + a
            except TypeError:
                return self.package.Polynomial(a) + self.package.Polynomial(b)

    def _safe_sub(self, a, b):
        try:
            return a - b
        except TypeError:
            try:
                return -(b - a)
            except TypeError:
                return self.package.Polynomial(a) - self.package.Polynomial(b)

    def _safe_mul(self, a, b):
        try:
            return a * b
        except TypeError:
            try:
                return b * a
            except TypeError:
                return self.package.Polynomial(a) * self.package.Polynomial(b)

    def bool_value(self, items):
        return self.formula_pkg.Formula(str(items[0]) == "true")

    def number(self, items):
        t = items[0]
        if t.type == "NUMERAL":
            return self.package.Rational(int(t.value))
        if t.type == "DECIMAL":
            return self.package.Rational(t.value)
        if t.type == "HEXADECIMAL":
            return self.package.Rational(int(t.value[2:], base=16))
        if t.type == "BINARY":
            return self.package.Rational(int(t.value[2:], base=2))
        raise ValueError(f"Unknown number {t}")

    def real_variable(self, items):
        name = str(items[0])
        v = variable_with_name(name)
        if v.is_no_variable:
            return Variable(name, VariableType.REAL)
        return v

    def bool_variable(self, items):
        name = str(items[0])
        v = variable_with_name(name)
        if v.is_no_variable:
            return self.formula_pkg.Formula(Variable(name, VariableType.BOOL))
        return self.formula_pkg.Formula(v)

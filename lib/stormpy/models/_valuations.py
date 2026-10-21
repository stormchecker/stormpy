"""Python conveniences for Storm valuations."""

from __future__ import annotations

from stormpy import Rational
from stormpy.developer import storage
from stormpy.expressions import Variable
from . import SimpleValuation, Valuations


def _get_value(self: SimpleValuation, var: Variable) -> bool | int | float:
    """
    Get the value of the given variable.
    :param var: Variable.
    :return Value of var.
    """
    if var.has_boolean_type():
        return self.get_boolean_value(var)
    elif var.has_integer_type():
        return self.get_integer_value(var)
    elif var.has_rational_type():
        return self.get_rational_value(var)
    else:
        raise ValueError(f"Variable {var} has unsupported type")


storage.SimpleValuation.get_value = _get_value


def _get_entity_value(self: Valuations, entity: int, variable: Variable) -> bool | int | Rational | str:
    """Read a variable at an entity, dispatching by its expression type.

    :param entity: State or observation index.
    :param variable: Expression variable to read.
    :return: Boolean, integer, rational or string value.
    """
    if variable.has_boolean_type():
        return self.get_boolean_value(entity, variable)
    if variable.has_integer_type():
        return self.get_int64_value(entity, variable)
    if variable.has_rational_type():
        return self.get_rational_value(entity, variable)
    if variable.has_string_type():
        return self.get_string_value(entity, variable)
    raise ValueError("Variable has unsupported type")


def _get_values(self: Valuations, variable: Variable) -> list[bool] | list[int] | list[Rational] | list[str]:
    """Read a variable for every entity, returning a list in entity order.

    :param variable: Expression variable to read.
    :return: List with one value per state or observation.
    """
    if variable.has_boolean_type():
        bits = self.get_boolean_values(variable)
        return [bits[index] for index in range(len(bits))]
    if variable.has_integer_type():
        return self.get_int64_values(variable)
    if variable.has_rational_type():
        return self.get_rational_values(variable)
    if variable.has_string_type():
        return self.get_string_values(variable)
    raise ValueError("Variable has unsupported type")


def _write_value(self: Valuations, entity: int, variable: Variable, value: bool | int | Rational | str) -> None:
    """Write a variable at an entity, dispatching by its expression type.

    :param entity: State or observation index.
    :param variable: Expression variable to write.
    :param value: Value compatible with the variable's type and storage encoding.
    """
    if variable.has_boolean_type():
        self.write_bool_value(entity, variable, value)
    elif variable.has_integer_type():
        self.write_int64_value(entity, variable, value)
    elif variable.has_rational_type():
        self.write_rational_value(entity, variable, value)
    elif variable.has_string_type():
        self.write_string_value(entity, variable, value)
    else:
        raise ValueError("Variable has unsupported type")


storage.Valuations.get_value = _get_entity_value
storage.Valuations.get_values_states = _get_values
storage.Valuations.write_value = _write_value

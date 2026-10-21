"""Values with sound bounds in model checking results."""

from __future__ import annotations

import math
from typing import Any

from stormpy import Rational
from stormpy import developer


def _infinity_sign(x: Any) -> int:
    """1 for +infinity, -1 for -infinity, 0 for finite values."""
    if isinstance(x, float) and math.isinf(x):
        return 1 if x > 0 else -1
    return 0


def _sign(x: Any) -> int:
    return _infinity_sign(x) or (x > 0) - (x < 0)


def _is_nan(*xs: Any) -> bool:
    """Whether one of the values is not a number, e.g., the result of an undefined operation such as infinity minus infinity."""
    return any(isinstance(x, float) and math.isnan(x) for x in xs)


def _add(a: Any, b: Any) -> Any:
    """Sum, or None if undefined (infinity minus infinity, or an operand is not a number)."""
    if _is_nan(a, b):
        return None
    sign_a, sign_b = _infinity_sign(a), _infinity_sign(b)
    if sign_a and sign_b and sign_a != sign_b:
        return None
    if sign_a:
        return a
    if sign_b:
        return b
    return a + b


def _mul(a: Any, b: Any) -> Any:
    """Product with the convention 0 * infinity = 0, or None if an operand is not a number."""
    if _is_nan(a, b):
        return None
    if not _infinity_sign(a) and not _infinity_sign(b):
        return a * b
    sign = _sign(a) * _sign(b)
    return 0 if sign == 0 else math.inf * sign


def _div(a: Any, b: Any) -> Any:
    """Quotient, or None if undefined (infinity divided by infinity, or an operand is not a number). Raises ZeroDivisionError for b = 0."""
    if _is_nan(a, b):
        return None
    if _sign(b) == 0:
        raise ZeroDivisionError("division by zero")
    sign_a, sign_b = _infinity_sign(a), _infinity_sign(b)
    if sign_a and sign_b:
        return None
    if sign_b:
        return 0
    if sign_a:
        return math.inf * sign_a * _sign(b)
    return a / b


def _order_key(x: Any) -> tuple:
    # Orders infinite values before or after all finite ones, without comparing them to finite values.
    sign = _infinity_sign(x)
    return (sign, 0) if sign else (0, x)


def _value(x: Any) -> Any:
    # An undefined value (infinity minus infinity) is not a number
    return math.nan if x is None else x


class BoundedValue:
    """
    Value of a single state in a model checking result, together with sound lower and upper bounds on the actual value.

    The bounds are given if the solution method could establish them, e.g., for sound methods.
    An unknown bound is ``None``. An infinite bound means the method tried but could not establish a finite bound.

    The object behaves like its value in comparisons with numbers and when converting to ``float``.
    Addition, subtraction, multiplication and division (with other values and plain numbers, which are exact) keep sound bounds on the result.
    Division only yields bounds if the bounds of the divisor exclude 0.
    Infinite values follow the convention 0 * infinity = 0. A bound which is undefined (infinity minus infinity) becomes unknown.
    """

    __slots__ = ("_value", "_lower", "_upper")

    def __init__(self, value: Any, lower: Any = None, upper: Any = None):
        """
        Create a value with bounds.

        :param value: The (approximate) value.
        :param lower: Sound lower bound on the actual value (None if not known).
        :param upper: Sound upper bound on the actual value (None if not known).
        """
        self._value = value
        # A bound which is not a number does not bound anything
        self._lower = None if _is_nan(lower) else lower
        self._upper = None if _is_nan(upper) else upper

    @property
    def value(self) -> Any:
        """The (approximate) value."""
        return self._value

    @property
    def lower(self) -> Any:
        """Sound lower bound on the actual value (None if not known)."""
        return self._lower

    @property
    def upper(self) -> Any:
        """Sound upper bound on the actual value (None if not known)."""
        return self._upper

    @property
    def has_lower(self) -> bool:
        """Whether a lower bound is known."""
        return self._lower is not None

    @property
    def has_upper(self) -> bool:
        """Whether an upper bound is known."""
        return self._upper is not None

    def __float__(self) -> float:
        return float(self._value)

    def __round__(self, ndigits: int | None = None) -> Any:
        return round(self._value, ndigits)

    def __format__(self, format_spec: str) -> str:
        # The format specification (e.g. ".6f") applies to the value and to the bounds
        return self._to_string(format_spec)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BoundedValue):
            return self._value == other._value and self._lower == other._lower and self._upper == other._upper
        return self._value == other

    def __hash__(self) -> int:
        return hash(self._value)

    @staticmethod
    def _plain(other: object) -> object:
        return other._value if isinstance(other, BoundedValue) else other

    def __lt__(self, other: object) -> bool:
        return self._value < self._plain(other)

    def __le__(self, other: object) -> bool:
        return self._value <= self._plain(other)

    def __gt__(self, other: object) -> bool:
        return self._value > self._plain(other)

    def __ge__(self, other: object) -> bool:
        return self._value >= self._plain(other)

    @staticmethod
    def _bounded(other: object) -> BoundedValue:
        # A plain number is exact, i.e., it is its own lower and upper bound
        return other if isinstance(other, BoundedValue) else BoundedValue(other, other, other)

    def __add__(self, other: object) -> BoundedValue:
        other = self._bounded(other)
        # Addition is monotone, so the sums of the bounds bound the sum.
        # A bound is only known if it is known for both summands.
        lower = None if self._lower is None or other._lower is None else _add(self._lower, other._lower)
        upper = None if self._upper is None or other._upper is None else _add(self._upper, other._upper)
        return BoundedValue(_value(_add(self._value, other._value)), lower, upper)

    def __radd__(self, other: object) -> BoundedValue:
        return self + other

    def __neg__(self) -> BoundedValue:
        # Negation swaps the bounds
        return BoundedValue(-self._value, None if self._upper is None else -self._upper, None if self._lower is None else -self._lower)

    def __sub__(self, other: object) -> BoundedValue:
        return self + (-self._bounded(other))

    def __rsub__(self, other: object) -> BoundedValue:
        return self._bounded(other) - self

    def __mul__(self, other: object) -> BoundedValue:
        other = self._bounded(other)
        value = _value(_mul(self._value, other._value))
        bounds = (self._lower, self._upper, other._lower, other._upper)
        if all(bound is not None for bound in bounds):
            # The product of intervals is bounded by the products of their bounds
            corners = [_mul(a, b) for a in (self._lower, self._upper) for b in (other._lower, other._upper)]
            return BoundedValue(value, min(corners, key=_order_key), max(corners, key=_order_key))
        if self._lower is not None and other._lower is not None and _sign(self._lower) >= 0 and _sign(other._lower) >= 0:
            # Both factors are non-negative: the product is monotone in both factors, so lower and upper bounds can be multiplied separately
            upper = None if self._upper is None or other._upper is None else _mul(self._upper, other._upper)
            return BoundedValue(value, _mul(self._lower, other._lower), upper)
        for point, factor in ((other, self), (self, other)):
            if point._lower is not None and point._lower == point._upper:
                # Scaling with a known constant (both bounds coincide): a negative constant swaps the bounds
                constant = point._lower
                if _sign(constant) == 0:
                    return BoundedValue(value, 0, 0)
                lower = None if factor._lower is None else _mul(constant, factor._lower)
                upper = None if factor._upper is None else _mul(constant, factor._upper)
                return BoundedValue(value, lower, upper) if _sign(constant) >= 0 else BoundedValue(value, upper, lower)
        return BoundedValue(value)

    def __rmul__(self, other: object) -> BoundedValue:
        return self * other

    def _reciprocal_bounds(self) -> tuple[Any, Any]:
        """Bounds on 1 / x, which are only known if the bounds exclude 0."""
        if self._lower is not None and _sign(self._lower) > 0:
            # x is positive: 1 / x is in (0, 1 / lower]
            return (0 if self._upper is None else _div(1, self._upper)), _div(1, self._lower)
        if self._upper is not None and _sign(self._upper) < 0:
            # x is negative: 1 / x is in [1 / upper, 0)
            return _div(1, self._upper), (0 if self._lower is None else _div(1, self._lower))
        # x can be 0, i.e., 1 / x is unbounded
        return None, None

    def __truediv__(self, other: object) -> BoundedValue:
        other = self._bounded(other)
        value = _value(_div(self._value, other._value))
        if other._lower is not None and other._lower == other._upper and _sign(other._lower) != 0:
            # Division by a known constant (both bounds coincide): divide the bounds directly (one rounding step for floats), a negative constant swaps them
            constant = other._lower
            lower = None if self._lower is None else _div(self._lower, constant)
            upper = None if self._upper is None else _div(self._upper, constant)
            return BoundedValue(value, lower, upper) if _sign(constant) > 0 else BoundedValue(value, upper, lower)
        # a / b = a * (1 / b) for the bounds, the value is divided directly
        lower, upper = other._reciprocal_bounds()
        bounds = self * BoundedValue(1, lower, upper)
        return BoundedValue(value, bounds._lower, bounds._upper)

    def __rtruediv__(self, other: object) -> BoundedValue:
        return self._bounded(other) / self

    def __repr__(self) -> str:
        return f"BoundedValue({self._value!r}, lower={self._lower!r}, upper={self._upper!r})"

    def __str__(self) -> str:
        return self._to_string("")

    def _to_string(self, format_spec: str) -> str:
        """Value followed by its bounds, where an unknown bound is shown as '-'."""

        def format_number(x: Any) -> str:
            if x is None:
                return "-"
            try:
                return format(x, format_spec)
            except TypeError:
                # Exact numbers (e.g. Rational) do not support format specifications such as ".6f", use their float approximation instead
                return format(float(x), format_spec)

        return f"{format_number(self._value)} [{format_number(self._lower)}, {format_number(self._upper)}]"


def _get_item_with_bounds(self, state: int) -> BoundedValue:
    """
    Get the value for the given state together with its sound bounds.

    Use :meth:`get_value` to get only the value.

    :param state: State.
    :return: Value with bounds.
    """
    return BoundedValue(self.get_value(state), self.get_lower_bound(state), self.get_upper_bound(state))


# Parametric results keep returning the plain value (defined in the bindings)
for _value_type in (float, Rational):
    developer.ExplicitQuantitativeCheckResult[_value_type].__getitem__ = _get_item_with_bounds
del _value_type

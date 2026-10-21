"""Checks for infinite values.

Infinite values of all value types (e.g. in model checking results) are given as ``float('inf')`` or ``float('-inf')``.
"""

from __future__ import annotations

import math
from typing import Any

import stormpy as _stormpy

from .developer.infinity import Infinity


def _plain_value(value: Any) -> Any:
    return _stormpy.results.BoundedValue._plain(value)


def is_infinity(value: Any) -> bool:
    """
    Check whether the value is positive infinity.

    In contrast to :func:`math.isinf`, values of exact types such as :class:`Rational` are never converted to ``float``
    and are therefore never infinite.

    :param value: Value, e.g., ``float``, :class:`Rational` or :class:`stormpy.results.BoundedValue` (checks its value).
    :return: True iff the value is positive infinity.
    """
    value = _plain_value(value)
    if isinstance(value, float):
        return value == math.inf
    if isinstance(value, Infinity):
        return not value.negated
    return False


def is_negative_infinity(value: Any) -> bool:
    """
    Check whether the value is negative infinity.

    :param value: Value, e.g., ``float``, :class:`Rational` or :class:`stormpy.results.BoundedValue` (checks its value).
    :return: True iff the value is negative infinity.
    """
    value = _plain_value(value)
    if isinstance(value, float):
        return value == -math.inf
    if isinstance(value, Infinity):
        return value.negated
    return False

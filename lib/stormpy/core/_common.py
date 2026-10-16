"""Internal helpers shared by the modules of the public API."""

from __future__ import annotations

import os
from collections.abc import Iterable
from typing import TypeAlias

from stormpy.developer import storage
from stormpy import Interval, Rational, RationalFunction, RationalInterval
from stormpy.developer import Property
from stormpy.developer.logic import Formula
from stormpy.exceptions import StormError

# File paths can be given as strings or path-like objects (e.g. pathlib.Path)
PathLike: TypeAlias = str | os.PathLike[str]


def _path(path: PathLike) -> str:
    """Convert a path given as string or path-like object (e.g. pathlib.Path) into a string."""
    if not isinstance(path, (str, os.PathLike)):
        raise TypeError(f"Expected a path as string or path-like object, got {type(path)}.")
    return os.fspath(path)


def _value_type_of_model(model) -> type:
    """Get the value type of a sparse or symbolic model."""
    if model.is_sparse_model:
        return storage.parameters_of_model(model)[0]
    if model.supports_parameters:
        return RationalFunction
    if model.is_exact:
        return Rational
    return float


def _result_value_type_of_model(model) -> type:
    """Get the value type of model checking results for a sparse or symbolic model."""
    value_type = _value_type_of_model(model)
    if value_type is Interval:
        return float
    if value_type is RationalInterval:
        return Rational
    return value_type


def _formula(property: Property | object):
    """Get the raw formula of the given property (formulas are passed through)."""
    return property.get_raw_formula() if isinstance(property, Property) else property


def _formulas(properties: Property | object | Iterable[Property | object] | None) -> list:
    """Get the raw formulas of the given property or properties (formulas are passed through)."""
    if properties is None:
        return []
    if isinstance(properties, (Property, Formula)):
        return [_formula(properties)]
    return [_formula(prop) for prop in properties]

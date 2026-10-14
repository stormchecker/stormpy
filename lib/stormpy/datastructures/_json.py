"""Python conveniences for Storm's JSON containers."""

from __future__ import annotations

from stormpy.developer import storage as _bindings
from . import JsonContainer


# Compare, hash and convert JSON containers via their string representation
def _eq(self: JsonContainer, other: object) -> bool:
    return str(self) == str(other)


def _int(self: JsonContainer) -> int:
    return int(str(self))


def _hash(self: JsonContainer) -> int:
    return hash(str(self))


for _json_class in _bindings.JsonContainer.instantiations.values():
    _json_class.__eq__ = _eq
    _json_class.__int__ = _int
    _json_class.__hash__ = _hash

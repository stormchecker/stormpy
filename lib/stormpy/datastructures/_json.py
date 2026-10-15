"""Python conveniences for Storm's JSON containers."""

from __future__ import annotations

from stormpy.developer import storage as _bindings
from . import JsonContainer


# Convert JSON containers holding a number via their string representation
def _int(self: JsonContainer) -> int:
    return int(str(self))


for _json_class in _bindings.JsonContainer.instantiations.values():
    _json_class.__int__ = _int

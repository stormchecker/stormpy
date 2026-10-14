"""Python conveniences for Storm's JSON containers."""

from stormpy.developer import storage as _bindings

# Compare, hash and convert JSON containers via their string representation
for _json_class in _bindings.JsonContainer.instantiations.values():
    _json_class.__eq__ = lambda s, o: str(s) == str(o)
    _json_class.__int__ = lambda s: int(str(s))
    _json_class.__hash__ = lambda s: str(s).__hash__()

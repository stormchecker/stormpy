from . import _utility
from ._utility import *
from stormpy._template import _TemplateClass, _deduce_default

JsonContainer = _TemplateClass("stormpy.utility.JsonContainer", _utility, parameters=("ValueType",), deduce=_deduce_default(float))


# Extend JSON containers for simplified access
for _json_class in JsonContainer.instantiations.values():
    _json_class.__eq__ = lambda s, o: str(s) == str(o)
    _json_class.__int__ = lambda s: int(str(s))
    _json_class.__hash__ = lambda s: str(s).__hash__()

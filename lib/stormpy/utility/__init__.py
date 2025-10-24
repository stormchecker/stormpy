from . import _utility
from ._utility import *

# Extend JSON container for simplified access
_utility.JsonContainerDouble.__eq__ = lambda s, o: str(s) == str(o)
_utility.JsonContainerDouble.__int__ = lambda s: int(str(s))
_utility.JsonContainerDouble.__hash__ = lambda s: str(s).__hash__()


_utility.JsonContainerRational.__eq__ = lambda s, o: str(s) == str(o)
_utility.JsonContainerRational.__int__ = lambda s: int(str(s))
_utility.JsonContainerRational.__hash__ = lambda s: str(s).__hash__()

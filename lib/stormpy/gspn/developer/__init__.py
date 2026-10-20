"""Raw pybind11 bindings for storm-gspn.

This module is only meant for developers.
Use :mod:`stormpy.gspn` for the public API.

The naming of functions and classes of the bindings mirrors the corresponding ``storm::gspn`` C++ functions and classes.
"""

from stormpy.info import _config

if not _config.STORM_WITH_GSPN:
    raise ImportError("No support for GSPNs was built in Storm.")

from . import _gspn

# Mirror _gspn's entire namespace (including private underscored classes) directly onto this package.
for _name, _value in vars(_gspn).items():
    if not _name.startswith("__"):
        globals()[_name] = _value
del _name, _value

from stormpy.info import _config

if not _config.STORM_WITH_GSPN:
    raise ImportError("No support for GSPNs was built in Storm.")

from . import _gspn
from ._gspn import *

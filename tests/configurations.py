import pytest

import stormpy.info._config as config

# Skip not supported functionality
has_spot = config.STORM_WITH_SPOT
has_xml = config.STORM_WITH_XERCES
has_dft = config.STORM_WITH_DFT
has_gspn = config.STORM_WITH_GSPN
has_pars = config.STORM_WITH_PARS
has_pomdp = config.STORM_WITH_POMDP

try:
    import numpy

    has_numpy = True
except ImportError:
    has_numpy = False

try:
    import matplotlib

    has_matplotlib = True
except ImportError:
    has_matplotlib = False

try:
    import scipy

    has_scipy = True
except ImportError:
    has_scipy = False

xml = pytest.mark.skipif(not has_xml, reason="No support for XML via xerces")
dft = pytest.mark.skipif(not has_dft, reason="No support for DFTs")
gspn = pytest.mark.skipif(not has_gspn, reason="No support for GSPNs")
pars = pytest.mark.skipif(not has_pars, reason="No support for parametric model checking")
pomdp = pytest.mark.skipif(not has_pomdp, reason="No support for POMDPs")
spot = pytest.mark.skipif(not has_spot, reason="No support for LTL via spot")
numpy_avail = pytest.mark.skipif(not has_numpy, reason="Numpy not available")
plotting = pytest.mark.skipif(not has_matplotlib or not has_scipy, reason="Libraries for plotting not available")

from stormpy import pycarl

# Skip not supported functionality
pycarl_cln = pytest.mark.skipif(not pycarl.has_cln(), reason="No support for CLN")
pycarl_parser = pytest.mark.skipif(not pycarl.has_parser(), reason="No support for carlparser")

# Parametrize available number types
from stormpy.pycarl import gmp

parameters = [pycarl.gmp]
names = ["gmp"]

if pycarl.has_cln():
    from stormpy.pycarl import cln

    parameters.append(pycarl.cln)
    names.append("cln")


class PackageSelector:
    @pytest.fixture(params=parameters, ids=names)
    def package(self, request):
        return request.param

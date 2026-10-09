import pytest
import importlib.util

import stormpy.info._config as config

has_dft = config.STORM_WITH_DFT
has_gspn = config.STORM_WITH_GSPN
has_pars = config.STORM_WITH_PARS
has_pomdp = config.STORM_WITH_POMDP


def has_package(pkg_name):
    return importlib.util.find_spec(pkg_name) is not None


has_pycarl_parser = has_package("lark")

# Skip not supported functionality
dft = pytest.mark.skipif(not has_dft, reason="No support for DFTs")
gspn = pytest.mark.skipif(not has_gspn, reason="No support for GSPNs")
pars = pytest.mark.skipif(not has_pars, reason="No support for parametric model checking")
pomdp = pytest.mark.skipif(not has_pomdp, reason="No support for POMDPs")
spot = pytest.mark.skipif(not config.STORM_WITH_SPOT, reason="No support for LTL via spot")
xml = pytest.mark.skipif(not config.STORM_WITH_XERCES, reason="No support for XML via xerces")
numpy_avail = pytest.mark.skipif(not has_package("numpy"), reason="Numpy not available")
plotting = pytest.mark.skipif(not has_package("matplotlib") or not has_package("scipy"), reason="Libraries for plotting not available")
pycarl_parser = pytest.mark.skipif(not has_pycarl_parser, reason="No support for parsing")

from stormpy import pycarl

# Skip not supported functionality
pycarl_cln = pytest.mark.skipif(not pycarl.has_cln(), reason="No support for CLN")

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

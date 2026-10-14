"""Public info package and its native developer bindings."""

import inspect

import stormpy
import stormpy.info


def test_public_exports_are_explicit():
    exported = {name for name in vars(stormpy.info) if not name.startswith("_")}
    assert exported == set(stormpy.info.__all__)
    assert all(inspect.isfunction(getattr(stormpy.info, name)) for name in stormpy.info.__all__)


def test_native_module_location():
    native = stormpy.developer.info._info
    assert native.__name__ == "stormpy.developer.info._info"
    assert stormpy.developer.info.StormVersion.__module__ == native.__name__
    assert not hasattr(stormpy.info, "Version")


def test_storm_names():
    raw = stormpy.developer.info.StormVersion
    assert isinstance(raw.version_major, int)
    assert isinstance(raw.version_minor, int)
    assert isinstance(raw.version_patch, int)
    assert isinstance(raw.version_dev, bool)
    short = f"{raw.version_major}.{raw.version_minor}.{raw.version_patch}"
    assert raw.short_version_string().startswith(short)
    assert stormpy.info.storm_long_version() == raw.long_version_string()
    assert stormpy.info.storm_build_info() == raw.build_info()

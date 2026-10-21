"""Public analysis types and their shared native developer bindings."""

import stormpy


def test_public_classes_share_native_types():
    public = stormpy.analysis.Path
    internal = stormpy.developer.utility.Path
    assert public.canonical_name == "stormpy.analysis.Path"
    assert internal.canonical_name == "stormpy.developer.utility.Path"
    assert public.instantiations == internal.instantiations


def test_native_module_location():
    native = stormpy.developer.utility._utility
    assert native.__name__ == "stormpy.developer.utility._utility"
    assert stormpy.developer.utility.ShortestPathsGenerator[float].__module__ == native.__name__
    assert not hasattr(stormpy.analysis, "ShortestPathsGenerator")
    assert "ShortestPathsGenerator" not in stormpy.analysis.__all__


def test_settings_removed_from_public_api():
    assert not hasattr(stormpy, "utility")
    for name in ("LogLevel", "set_log_level", "set_timeout", "reset_timeout"):
        assert not hasattr(stormpy, name)

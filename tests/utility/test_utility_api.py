"""Public utility package and its shared native developer bindings."""

import inspect
import types

import stormpy
from stormpy._template import _TemplateClass


def test_public_exports_are_explicit():
    module = stormpy.utility
    # Submodules (such as the optional multiobjective_plotting) are not part of __all__
    exported = {name for name, value in vars(module).items() if not name.startswith("_") and not isinstance(value, types.ModuleType)}
    assert exported == set(module.__all__)


def test_public_classes_share_native_types():
    for name in stormpy.utility.__all__:
        public = getattr(stormpy.utility, name)
        if isinstance(public, _TemplateClass):
            internal = getattr(stormpy.developer.utility, name)
            assert public.canonical_name == f"stormpy.utility.{name}"
            assert internal.canonical_name == f"stormpy.developer.utility.{name}"
            assert public.instantiations == internal.instantiations
        elif inspect.isclass(public):
            assert public is getattr(stormpy.developer.utility, name, None) or public is getattr(stormpy.developer, name)


def test_native_module_location():
    native = stormpy.developer.utility._utility
    assert native.__name__ == "stormpy.developer.utility._utility"
    assert stormpy.utility.ShortestPathsGenerator[float].__module__ == native.__name__


def test_settings_removed_from_top_level():
    for name in ("LogLevel", "set_log_level", "set_timeout", "reset_timeout"):
        assert not hasattr(stormpy, name)

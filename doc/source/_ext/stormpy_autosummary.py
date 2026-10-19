"""Helpers for selecting public and developer autosummary members."""

import sys
from types import ModuleType

import stormpy
from stormpy._template import _TemplateClass


def is_developer_api_page(docname):
    return docname.split("/", 1)[0] == "developer_api"


def public_api_modules():
    """Loaded public namespaces with an explicit export declaration."""
    package = stormpy.__name__
    prefix = package + "."
    return tuple(
        module
        for name, module in list(sys.modules.items())
        if (name == package or name.startswith(prefix))
        and not any(part == "developer" or part.startswith("_") for part in name.split("."))
        and hasattr(module, "__all__")
    )


def canonical_api_alias(fullname):
    """Find the domain owner of a top-level convenience export."""
    module, _, name = fullname.rpartition(".")
    if module != "stormpy" or name not in stormpy.__all__:
        return None
    obj = getattr(stormpy, name)
    for namespace in public_api_modules():
        if namespace is not stormpy and name in namespace.__all__ and getattr(namespace, name) is obj:
            return f"{namespace.__name__}.{name}"
    return None


def _export_key(obj):
    # publish_as() creates a new wrapper around the same native registrations.
    if isinstance(obj, _TemplateClass):
        return frozenset((arguments, id(implementation)) for arguments, implementation in obj.instantiations.items())
    return id(obj)


def _filter_api_members(module, members):
    """
    Filter the members listed on the autosummary page of a module.

    Public modules declare their API in __all__, including objects whose
    implementations live in private core modules or developer bindings.
    """
    members = [name for name in members if not name.startswith("_")]
    module_obj = sys.modules[module]
    exports = getattr(module_obj, "__all__", None)
    if exports is not None:
        members = [name for name in members if name in exports]
        if "developer" not in module.split("."):
            return members
    else:
        # Raw binding modules may re-export project types, but imported
        # third-party helpers and submodules are not API members.
        members = [
            name
            for name in members
            if not isinstance(getattr(module_obj, name), ModuleType)
            and getattr(getattr(module_obj, name), "__module__", module).split(".", 1)[0] == module.split(".", 1)[0]
        ]
    public_exports = {_export_key(getattr(namespace, name)) for namespace in public_api_modules() for name in namespace.__all__}
    return [name for name in members if _export_key(getattr(module_obj, name)) not in public_exports]

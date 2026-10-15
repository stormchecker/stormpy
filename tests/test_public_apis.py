"""Generic tests for the structure of all public APIs (stormpy, stormpy.dft, ...).

Each public module declares its API via ``__all__``. These tests check that the declared names exist, are unique and are documented.
"""

import importlib
import inspect
import types
import typing

import pytest
import stormpy
from configurations import has_dft, has_gspn, has_pars


def _core_documented_elsewhere(name):
    # Value types are documented in stormpy.numbers.
    return name in stormpy.numbers.__all__


def _numbers_documented_elsewhere(name):
    # The number types and Variable are classes of the carl bindings and are documented in stormpy.numbers.developer
    obj = getattr(stormpy.numbers, name)
    return isinstance(obj, type) and obj.__module__.startswith("stormpy.numbers.developer")


def _not_documented_elsewhere(_name):
    return False


# Public modules: name -> (available, predicate for names documented in other modules)
_PUBLIC_MODULES = {
    "stormpy": (True, _core_documented_elsewhere),
    "stormpy.dft": (has_dft, _not_documented_elsewhere),
    "stormpy.gspn": (has_gspn, _not_documented_elsewhere),
    "stormpy.pars": (has_pars, _not_documented_elsewhere),
    "stormpy.numbers": (True, _numbers_documented_elsewhere),
    "stormpy.models": (True, _not_documented_elsewhere),
    "stormpy.datastructures": (True, _not_documented_elsewhere),
    "stormpy.expressions": (True, _not_documented_elsewhere),
    "stormpy.io": (True, _not_documented_elsewhere),
    "stormpy.utility": (True, _not_documented_elsewhere),
    "stormpy.logic": (True, _not_documented_elsewhere),
    "stormpy.environments": (True, _not_documented_elsewhere),
    "stormpy.info": (True, _not_documented_elsewhere),
}

_UNAVAILABLE = pytest.mark.skip(reason="Module not available in this build of Storm")


def _modules():
    return [pytest.param(name, id=name, marks=() if available else _UNAVAILABLE) for name, (available, _) in _PUBLIC_MODULES.items()]


def _public_names(functions):
    """Parameters (module, name) for all public functions (or all other public objects) of the available modules."""
    params = []
    for module_name, (available, documented_elsewhere) in _PUBLIC_MODULES.items():
        if not available:
            params.append(pytest.param(module_name, None, id=f"{module_name}:unavailable", marks=_UNAVAILABLE))
            continue
        module = importlib.import_module(module_name)
        for name in module.__all__:
            obj = getattr(module, name, None)
            if inspect.isfunction(obj) != functions or documented_elsewhere(name):
                continue
            params.append(pytest.param(module_name, name, id=f"{module_name}:{name}"))
    return params


@pytest.mark.parametrize("module_name", _modules())
class TestAllNames:
    def test_all_names_exist(self, module_name):
        # Check that all classes/functions in __all__ exist
        module = importlib.import_module(module_name)
        missing = [name for name in module.__all__ if not hasattr(module, name)]
        assert missing == []

    def test_all_names_unique(self, module_name):
        module = importlib.import_module(module_name)
        assert len(module.__all__) == len(set(module.__all__))

    def test_no_private_or_module_names(self, module_name):
        module = importlib.import_module(module_name)
        private = [name for name in module.__all__ if name.startswith("_")]
        assert private == []
        modules = [name for name in module.__all__ if isinstance(getattr(module, name, None), types.ModuleType)]
        assert modules == []


@pytest.mark.parametrize("module_name, name", _public_names(functions=True))
def test_functions_documented(module_name, name):
    function = getattr(importlib.import_module(module_name), name)
    doc = inspect.getdoc(function)
    assert doc, f"{name} is not documented"
    # Each parameter must be documented
    for parameter in inspect.signature(function).parameters:
        assert f":param {parameter}:" in doc, f"Parameter {parameter} of {name} is not documented"


@pytest.mark.parametrize("module_name, name", _public_names(functions=True))
def test_function_annotations_resolve(module_name, name):
    # String annotations must refer to existing names
    function = getattr(importlib.import_module(module_name), name)
    typing.get_type_hints(function)


@pytest.mark.parametrize("module_name, name", _public_names(functions=False))
def test_classes_documented(module_name, name):
    obj = getattr(importlib.import_module(module_name), name)
    if isinstance(obj, stormpy._template._TemplateClass):
        # Templated classes are documented via their instantiations
        for instantiation in obj.instantiations.values():
            assert inspect.getdoc(instantiation), f"{instantiation} is not documented"
    else:
        assert inspect.getdoc(obj), f"{name} is not documented"

import importlib
import inspect

import pytest

import stormpy

NATIVE_MODULE_NAMES = (
    "stormpy._core",
    "stormpy.storage._storage",
    "stormpy.logic._logic",
    "stormpy.utility._utility",
    "stormpy.dft._dft",
    "stormpy.gspn._gspn",
    "stormpy.pars._pars",
    "stormpy.pomdp._pomdp",
    "stormpy.info._info",
    "stormpy.pycarl._pycarl_core",
    "stormpy.pycarl.gmp._gmp",
    "stormpy.pycarl.cln._cln",
    "stormpy.pycarl.formula._formula",
    "stormpy.pycarl.gmp.formula._formula",
    "stormpy.pycarl.cln.formula._formula",
)


def test_native_modules_keep_their_public_names():
    expected_modules = {
        "stormpy._core": stormpy._core,
        "stormpy.storage._storage": stormpy.storage._storage,
        "stormpy.logic._logic": stormpy.logic._logic,
        "stormpy.utility._utility": stormpy.utility._utility,
    }

    for name, module in expected_modules.items():
        assert module.__name__ == name
        assert module.__spec__.name == name
        assert module.__file__ == stormpy._bindings.__file__
        assert importlib.import_module(name) is module


@pytest.mark.parametrize(
    "binding",
    [
        stormpy.ExpressionManager.create_boolean,
        stormpy.storage._storage._ModelBase._as_sparse_dtmc,
        stormpy.storage.JaniModel.get_automaton,
        stormpy.storage.PrismProgram.to_jani,
        stormpy.storage.JaniLocationExpander.transform,
        stormpy.storage.SchedulerChoiceParametric.get_choice,
        stormpy._core._build_sparse_model_from_symbolic_description,
        stormpy._core._perform_symbolic_bisimulation,
        stormpy._core.make_sparse_model_builder_exact,
        stormpy._core.SymbolicExactQuantitativeCheckResult.get_values,
        stormpy._core.parse_properties_for_prism_program,
        stormpy.utility.SmtSolver.add,
    ],
)
def test_cross_module_signatures_use_python_type_names(binding):
    signature = binding.__doc__.splitlines()[0]

    assert "::" not in signature
    assert "stormpy." in signature


@pytest.mark.parametrize("module_name", NATIVE_MODULE_NAMES)
def test_native_callable_signatures_do_not_contain_cpp_qualified_names(module_name):
    try:
        module = importlib.import_module(module_name)
    except ImportError as error:
        pytest.skip(str(error))

    signature_lines = []

    for _, obj in inspect.getmembers(module):
        members = inspect.getmembers(obj) if inspect.isclass(obj) else ((obj.__name__, obj),) if callable(obj) else ()
        for _, member in members:
            doc = getattr(member, "__doc__", None)
            if doc:
                signature_lines.extend(line.strip() for line in doc.splitlines() if " -> " in line and not line.lstrip().startswith(":"))

    leaked_signatures = [line for line in signature_lines if "::" in line]
    assert leaked_signatures == []


@pytest.mark.parametrize("backend", ("gmp", "cln"))
def test_typed_pycarl_formulas_use_their_backend_module(backend):
    try:
        module = importlib.import_module(f"stormpy.pycarl.{backend}.formula")
    except ImportError as error:
        pytest.skip(str(error))

    assert module.Formula.__module__ == module.__name__
    assert module.Constraint.__module__ == module.__name__

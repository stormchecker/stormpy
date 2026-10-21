"""Sphinx template renderer tests; can run without importing Sphinx itself."""

import re
import runpy
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
import stormpy
from stormpy._template import _TemplateClass, _TemplateFunction, _template_function, _deduce_default

sys.path.insert(0, str(Path(__file__).parents[2] / "doc/source/_ext"))
import stormpy_templates as docs


def make_family():
    class Floating:
        def shared(self):
            pass

        def floating_only(self):
            """Only implemented for float."""

    class Integral:
        def shared(self):
            pass

    Floating.shared.__doc__ = "shared(self: test._Floating, value: float, tolerance: float) -> float\n\nShared method."
    Integral.shared.__doc__ = "shared(self: test._Integral, value: int, tolerance: float) -> int\n\nShared method."
    Floating.__module__ = "test"
    Floating.__name__ = "_Floating"
    Integral.__module__ = "test"
    Integral.__name__ = "_Integral"
    module = SimpleNamespace(_template_instantiations={"Example": {(float,): Floating, (int,): Integral}})
    return _TemplateClass("test.Example", module, parameters=["ValueType"])


def test_shared_and_fixed_types_and_conditional_members():
    family = make_family()
    output = docs.render_members(family, [family])
    assert "test.Example[ValueType]" in output
    assert "tolerance: float" in output
    assert "value: ValueType" in output
    assert "-> ValueType" in output
    assert "Available only for: ``Example[float]``." in output


def test_published_template_names_take_precedence():
    family = make_family()
    developer = family.publish_as("test.developer.Example")
    public = family.publish_as("test.models.Example")
    for families in ([public, developer], [developer, public]):
        output = docs.render_members(public, families)
        assert "test.models.Example[ValueType]" in output
        assert "test.developer.Example" not in output


def test_class_signatures_preserve_public_non_template_types():
    family = make_family()
    labeling = stormpy.models.StateLabeling
    native_name = f"{labeling.__module__}.{labeling.__qualname__}"
    for inst in family.metadata.instantiations:
        inst.implementation.shared.__doc__ = f"shared(self: {inst.native_name}, labeling: {native_name}) -> {native_name}"
    output = docs.render_members(family, [family])
    assert "labeling: stormpy.models.StateLabeling) -> stormpy.models.StateLabeling" in output
    signatures, _ = docs.constructors(stormpy.models.SparseModelComponents, docs._loaded_template_classes())
    assert any("state_labeling: stormpy.models.StateLabeling = ..." in signature for signature in signatures)


def test_python_specialization_methods_preserve_descriptors_and_defaults():
    family = make_family()

    def convert(self, value: int, /, *, value_type: type = float) -> float:
        """Convert a value."""

    def create(value_type: type = float):
        """Create a value."""

    def build(cls, value_type: type = float):
        """Build a value."""

    for inst in family.metadata.instantiations:
        inst.implementation.convert = convert
        inst.implementation.create = staticmethod(create)
        inst.implementation.build = classmethod(build)
    output = docs.render_members(family, [family])
    assert "Example.convert(self, value: int, /, *, value_type: type = float) -> float" in output
    assert "Example.create(value_type: type = float)\n   :staticmethod:" in output
    assert "Example.build(cls, value_type: type = float)\n   :classmethod:" in output
    assert "Convert a value." in output


def test_template_functions_are_listed_separately(monkeypatch):
    @_template_function("test.scale", parameters=["ValueType"], instantiations=(float, int), deduce=_deduce_default(float))
    def scale(value_type, value: int) -> int:
        """Scale a value."""
        return value

    monkeypatch.setitem(sys.modules, "test", SimpleNamespace(Example=make_family(), scale=scale, alias=scale))
    assert isinstance(scale, _TemplateFunction)
    assert docs.template_families("test") == ["Example"]
    assert docs.template_functions("test") == ["scale"]
    info = docs.template_function_info("test.scale")
    assert info["parameters"] == "ValueType"
    assert info["instantiations"] == ["scale[float]", "scale[int]"]
    assert info["signatures"] == ("(value: int) -> int",)
    assert info["overloads"] == [{"signature": "(value: int) -> int", "description": "Scale a value.", "specializations": []}]
    assert "scale[float]" in info["deduction"]


def make_native_function(monkeypatch, *, conditional=False):
    def floating():
        pass

    def integral():
        pass

    for implementation, typename, index in ((floating, "float", 1), (integral, "int", 2)):
        implementation.__name__ = f"_compute_{typename}"
        implementation.__doc__ = (
            f"_compute_{typename}(*args, **kwargs)\nOverloaded function.\n\n"
            f"1. _compute_{typename}(value: {typename}, tolerance: float, options: test._Options = <test._Options object at 0x{index:x}>) -> {typename}\n\n"
            "Compute a value.\n\n:param value: The input.\n:return: The result.\n\n"
        )
        if not conditional or implementation is floating:
            implementation.__doc__ += (
                f"2. _compute_{typename}(label: str = 'a,b') -> storm::Opaque<{typename}>\n\n" "Compute from a label; see :func:`compute`."
            )
    family = _TemplateFunction(
        "test.compute", SimpleNamespace(_template_instantiations={"compute": {(float,): floating, (int,): integral}}), parameters=["ValueType"]
    )
    monkeypatch.setitem(sys.modules, "test", SimpleNamespace(compute=family))
    return family


def test_native_function_signatures_and_prose_are_separate(monkeypatch):
    make_native_function(monkeypatch)
    info = docs.template_function_info("test.compute")
    assert info["signatures"] == ("(value: ValueType, tolerance: float, options = ...) -> ValueType", "(label: str = 'a,b')")
    assert info["overloads"] == [
        {"signature": info["signatures"][0], "description": "Compute a value.\n\n:param value: The input.\n:return: The result.", "specializations": []},
        {"signature": info["signatures"][1], "description": "Compute from a label; see :func:`compute`.", "specializations": []},
    ]
    lines = []
    docs.template_docstring(None, "function", "test.compute", sys.modules["test"].compute, None, lines)
    assert lines[0] == "Compute a value."
    assert all("_compute_" not in line and "Overloaded function." not in line for line in lines)


def test_function_overloads_only_available_for_some_specializations(monkeypatch):
    make_native_function(monkeypatch, conditional=True)
    info = docs.template_function_info("test.compute")
    assert info["signatures"] == ()
    assert len(info["overloads"]) == 2
    assert info["overloads"][0]["specializations"] == []
    assert info["overloads"][1]["specializations"] == ["compute[float]"]
    assert info["overloads"][1]["signature"] == "(label: str = 'a,b')"


def test_python_function_signatures_preserve_argument_kinds(monkeypatch):
    @_template_function("test.select", parameters=["ValueType"], instantiations=(float, int))
    def select(value_type, value: "int", /, *args: "str", option: "bool" = False, **kwargs: "int") -> "int":
        """Select a value.\n\n:param value: Input."""
        return value

    monkeypatch.setitem(sys.modules, "test", SimpleNamespace(select=select))
    info = docs.template_function_info("test.select")
    assert info["signatures"] == ("(value: int, /, *args: str, option: bool = False, **kwargs: int) -> int",)
    assert info["overloads"][0]["description"] == "Select a value.\n\n:param value: Input."


def test_real_native_function_uses_public_generic_types():
    info = docs.template_function_info("stormpy.developer.build_sparse_model")
    assert len(info["signatures"]) == 2
    signature = info["signatures"][0]
    assert "model: stormpy.io.SymbolicModelDescription" in signature
    assert "stormpy.developer.ExplicitModelBuilderOptions[ValueType] = ..." in signature
    assert "-> stormpy.models.SparseModel[ValueType]" in signature
    assert all(not docs._unresolved(overload["signature"]) for overload in info["overloads"])
    assert all("object at 0x" not in overload["signature"] for overload in info["overloads"])
    aliases = docs._public_type_names()
    assert aliases[f"{stormpy.logic.Property.__module__}.Property"] == "stormpy.logic.Property"
    assert aliases[f"{stormpy.models.ModelType.__module__}.ModelType"] == "stormpy.models.ModelType"


def test_real_python_function_resolves_forward_annotations():
    info = docs.template_function_info("stormpy.build_model")
    (signature,) = info["signatures"]
    assert "stormpy.io.PrismProgram | stormpy.io.JaniModel" in signature
    assert "collections.abc.Iterable[stormpy.logic.Property]" in signature
    assert "*, options:" in signature
    assert "engine: stormpy.Engine = stormpy.Engine.SPARSE" in signature
    assert ":param model:" in info["overloads"][0]["description"]


def test_sphinx_renders_public_and_developer_apis(monkeypatch, tmp_path):
    pytest.importorskip("sphinx")
    import pickle
    from io import StringIO
    from types import ModuleType

    from sphinx.addnodes import desc_signature
    from sphinx.application import Sphinx

    module = ModuleType("test")
    module.compute = make_native_function(monkeypatch)
    module.Example = make_family()
    module.developer = ModuleType("test.developer")
    module.developer.compute = module.compute.publish_as("test.developer.compute")
    module.developer.Example = module.Example.publish_as("test.developer.Example")
    monkeypatch.setitem(sys.modules, "test", module)
    monkeypatch.setitem(sys.modules, "test.developer", module.developer)
    monkeypatch.setitem(sys.modules, "test.extension", ModuleType("test.extension"))
    source = Path(__file__).parents[2] / "doc/source"
    config = runpy.run_path(str(source / "conf.py"))
    (tmp_path / "conf.py").write_text("")
    (tmp_path / "index.rst").write_text("Documentation\n=============\n\n.. toctree::\n\n   api\n   extensions_api\n   developer_api\n")
    (tmp_path / "api.rst").write_text(
        "API Documentation\n=================\n\n.. autosummary::\n   :toctree: api/generated\n   :template: autosummary/module.rst\n\n   test\n"
        "\n.. autosummary::\n   :toctree: api/generated\n   :template: autosummary/class.rst\n\n   stormpy.io.JaniModel\n   stormpy.datastructures.BitVector\n"
        "\n.. autosummary::\n   :toctree: api/generated\n   :template: autosummary/apiclass.rst\n\n   stormpy.datastructures.SparseMatrixBuilder\n   stormpy.models.Scheduler\n   stormpy.models.SparseModelComponents\n   stormpy.Environment\n   stormpy.environments.Environment\n"
        "\n.. autosummary::\n   :toctree: api/generated\n   :template: autosummary/apifunction.rst\n\n   stormpy.parse_property\n   stormpy.logic.parse_property\n"
        "\nSee :class:`Custom label <stormpy.developer.storage._storage.JaniModel>`.\n"
    )
    (tmp_path / "developer_api.rst").write_text(
        "Developer API Documentation\n===========================\n\n.. autosummary::\n   :toctree: developer_api/generated\n   :template: autosummary/module.rst\n\n   test.developer\n"
        "\nSee :class:`stormpy.developer.storage._storage.JaniModel`.\n"
    )
    (tmp_path / "extensions_api.rst").write_text(
        "Extensions API Documentation\n============================\n\n.. autosummary::\n   :toctree: extensions_api/generated\n   :template: autosummary/module.rst\n\n   test.extension\n"
    )
    warnings = StringIO()
    app = Sphinx(
        str(tmp_path),
        str(tmp_path),
        str(tmp_path / "html"),
        str(tmp_path / "doctrees"),
        "html",
        confoverrides={
            "extensions": ["stormpy_templates", "stormpy_developer", "sphinx.ext.autosummary"],
            "templates_path": [str(source / "_templates")],
            "autosummary_context": config["autosummary_context"],
            "autosummary_imported_members": True,
            "autoclass_content": "both",
        },
        status=StringIO(),
        warning=warnings,
        warningiserror=True,
        freshenv=True,
    )
    app.build(force_all=True)
    assert app.statuscode == 0, warnings.getvalue()
    assert warnings.getvalue() == ""
    extension_api = (tmp_path / "html/extensions_api.html").read_text()
    assert "extensions_api/generated/test.extension.html" in extension_api
    developer_api = (tmp_path / "html/developer_api.html").read_text()
    assert 'href="api/generated/stormpy.io.JaniModel.html#stormpy.io.JaniModel"' in developer_api
    cached_env = pickle.loads((tmp_path / "doctrees/environment.pickle").read_bytes())
    assert cached_env.config.autosummary_context["template_families"]("test") == ["Example"]
    assert app.env.domains["py"].objects["test.compute"].objtype == "function"
    alias = (tmp_path / "html/api/generated/stormpy.Environment.html").read_text()
    assert "Alias of" in alias
    assert 'href="stormpy.environments.Environment.html#stormpy.environments.Environment"' in alias
    alias = (tmp_path / "html/api/generated/stormpy.parse_property.html").read_text()
    assert 'href="stormpy.logic.parse_property.html#stormpy.logic.parse_property"' in alias
    function = (tmp_path / "html/api/generated/test.compute.html").read_text()
    assert "field-list" in function
    assert ":param" not in function
    assert "_compute_" not in function
    assert "object at 0x" not in function
    assert "Overloaded function." not in function
    bitvector = app.env.get_doctree("api/generated/stormpy.datastructures.BitVector")
    constructors = [sig for sig in bitvector.findall(desc_signature) if sig.get("fullname") == "BitVector"]
    assert len(constructors) == 5
    assert "other: stormpy.datastructures.BitVector" in constructors[1].astext()
    assert "*args" not in "\n".join(sig.astext() for sig in constructors)
    matrix_builder = (tmp_path / "html/api/generated/stormpy.datastructures.SparseMatrixBuilder.html").read_text()
    assert "field-list" in matrix_builder
    assert ":param" not in matrix_builder
    assert "offset+i -&gt; value of i" in matrix_builder
    scheduler = app.env.get_doctree("api/generated/stormpy.models.Scheduler")
    conversion = next(sig for sig in scheduler.findall(desc_signature) if sig.get("fullname") == "Scheduler.to_value_type")
    assert "value_type: type = float" in conversion.astext()
    components = app.env.get_doctree("api/generated/stormpy.models.SparseModelComponents")
    constructor = next(sig for sig in components.findall(desc_signature) if sig.get("fullname") == "SparseModelComponents")
    assert "state_labeling: stormpy.models.StateLabeling" in constructor.astext()
    api = (tmp_path / "html/api.html").read_text()
    assert 'href="api/generated/stormpy.io.JaniModel.html#stormpy.io.JaniModel"' in api
    assert "Custom label" in re.sub(r"<[^>]*>", "", api)
    disclaimer = "The stormpy developer API is internal and can be subject to change."
    for docname in app.env.found_docs:
        html = (tmp_path / f"html/{docname}.html").read_text()
        if docname == "developer_api" or docname.startswith("developer_api/"):
            assert html.count(disclaimer) == 1
        elif docname.startswith("api/"):
            assert disclaimer not in html
            text = app.env.get_doctree(docname).astext()
            assert "storm::" not in text
            assert "_compute_" not in text
            assert "test.developer" not in text


def test_public_api_filter_includes_refactored_implementations(monkeypatch):
    config = runpy.run_path(str(Path(__file__).parents[2] / "doc/source/conf.py"))
    implementation = type("Public", (), {"__module__": "test.developer._core"})
    monkeypatch.setitem(sys.modules, "test.public", SimpleNamespace(__all__=["Public"], Public=implementation, Imported=object(), _private=object()))
    assert config["_filter_api_members"]("test.public", ["Public", "Imported", "_private"]) == ["Public"]


def test_developer_api_filter_omits_published_aliases(monkeypatch):
    config = runpy.run_path(str(Path(__file__).parents[2] / "doc/source/conf.py"))

    family = make_family().publish_as("stormpy.docs_test.developer.Example")
    wrapped = make_family().publish_as("stormpy.docs_test.developer.Wrapped")
    shared = object()
    raw = object()
    monkeypatch.setitem(
        sys.modules,
        "stormpy.docs_test.developer",
        SimpleNamespace(__all__=["Example", "Shared", "Raw", "Wrapped"], Example=family, Shared=shared, Raw=raw, Wrapped=wrapped),
    )
    monkeypatch.setitem(
        sys.modules,
        "stormpy.docs_test",
        SimpleNamespace(
            __all__=["Published", "Alias", "Wrapped"],
            Published=family.publish_as("stormpy.docs_test.Published"),
            Alias=shared,
            Wrapped=make_family().publish_as("stormpy.docs_test.Wrapped"),
        ),
    )
    # Private modules and developer modules do not establish public ownership.
    monkeypatch.setitem(sys.modules, "stormpy._docs_test", SimpleNamespace(__all__=["Raw"], Raw=raw))
    # A same-named wrapper with different implementations does not replace
    # the raw binding's documentation (e.g. build_symbolic_model).
    assert config["_filter_api_members"]("stormpy.docs_test.developer", ["Example", "Shared", "Raw", "Wrapped"]) == ["Raw", "Wrapped"]


def test_raw_binding_filter_keeps_project_reexports(monkeypatch):
    from stormpy_autosummary import _filter_api_members

    # GMP and CLN formula types report a shared module, outside the backend.
    formula = type("Formula", (), {"__module__": "stormpy.numbers.developer.formula"})
    imported = type("Imported", (), {"__module__": "third_party"})
    monkeypatch.setitem(sys.modules, "stormpy.docs_test.developer.formula", SimpleNamespace(Formula=formula, Imported=imported))
    assert _filter_api_members("stormpy.docs_test.developer.formula", ["Formula", "Imported"]) == ["Formula"]


def test_constructor_descriptions_in_class_body():
    family = make_family()
    for inst in family.metadata.instantiations:

        def constructor(self):
            pass

        typ = docs.argument_name(inst.arguments[0])
        constructor.__doc__ = f"__init__(self: {inst.native_name}, value: {typ}) -> None\n\nCreate an example.\n\n:param value: Initial value."
        inst.implementation.__init__ = constructor
    assert docs.constructor_descriptions(family, [family]) == [("Create an example.\n\n:param value: Initial value.", [])]
    assert docs.constructors(family, [family]) == (("(value: ValueType)",), [])
    assert "Example.__init__" not in docs.render_members(family, [family])


def test_constructor_descriptions_preserve_specialization_differences():
    family = make_family()
    for inst in family.metadata.instantiations:

        def constructor(self):
            pass

        typ = docs.argument_name(inst.arguments[0])
        constructor.__doc__ = f"__init__(self: {inst.native_name}) -> None\n\nCreate the {typ} specialization."
        inst.implementation.__init__ = constructor
    assert docs.constructor_descriptions(family, [family]) == [
        ("Create the float specialization.", ["Example[float]"]),
        ("Create the int specialization.", ["Example[int]"]),
    ]


def test_unresolved_annotations_are_omitted_not_overloads():
    assert (
        docs._public_signature(
            "run(self: stormpy._core._CheckResult, components: storm::Components<std::pair<int, int>>, limit: int = 5) -> storm::Result<int>"
        )
        == "run(self, components, limit: int = 5)"
    )
    assert docs._public_signature("run(self: stormpy.models.SparseMdp[ValueType]) -> float") == "run(self: stormpy.models.SparseMdp[ValueType]) -> float"


def test_constructor_deduction_descriptions():
    assert "SparseMatrix[float]" in docs.deduction_description(stormpy.datastructures.SparseMatrix)
    inferred = docs.deduction_description(stormpy.models.SparseMdp)
    assert "first positional constructor argument" in inferred
    assert "``components`` or ``other_model``" in inferred
    assert "[float]" not in inferred
    second = docs.deduction_description(stormpy.models.MemoryStructureBuilder)
    assert "second positional constructor argument" in second
    assert "``model``" in second
    fallback = docs.deduction_description(stormpy.models.SparseModelComponents)
    assert "``transition_matrix``" in fallback
    assert "If none is supplied, ``SparseModelComponents[float]``" in fallback
    assert docs.deduction_description(stormpy.developer.storage.Add) is None


def test_object_defaults_do_not_split_generic_signatures():
    family = make_family()
    for index, inst in enumerate(family.metadata.instantiations):

        def constructor(self):
            pass

        constructor.__doc__ = f"__init__(self: {inst.native_name}, options: test._Options = <test._Options object at 0x{index + 1:x}>) -> None"
        inst.implementation.__init__ = constructor
    signatures, variants = docs.constructors(family, [family])
    assert signatures == ("(options = ...)",)
    assert variants == []


def test_specialization_specific_constructors_are_retained():
    family = stormpy.models.SparseRewardModel
    signatures, variants = docs.constructors(family, [family])
    assert not signatures
    assert variants
    assert all("SparseRewardModel[" in specialization for specialization, _ in variants)
    assert all("ValueType" not in signature for _, signature in variants)

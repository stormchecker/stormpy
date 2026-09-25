"""Sphinx template renderer tests; can run without importing Sphinx itself."""

import importlib.util
from pathlib import Path
from types import SimpleNamespace

import stormpy
import stormpy.dft
from stormpy._template import TemplateClass

_spec = importlib.util.spec_from_file_location("stormpy_templates", Path(__file__).parents[2] / "doc/source/_ext/stormpy_templates.py")
docs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(docs)


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
    return TemplateClass("test.Example", module, parameters=["ValueType"])


def test_shared_and_fixed_types_and_conditional_members():
    family = make_family()
    output = docs.render_members(family, [family])
    assert "test.Example[ValueType]" in output
    assert "tolerance: float" in output
    assert "value: ValueType" in output
    assert "-> ValueType" in output
    assert "Available only for: ``Example[float]``." in output


def test_public_aliases():
    assert docs.argument_name(stormpy.Rational) == "stormpy.Rational"
    assert docs.argument_name(stormpy.Interval) == "stormpy.Interval"
    assert docs.argument_name(stormpy.RationalInterval) == "stormpy.RationalInterval"
    assert docs.argument_name(stormpy.RationalFunction) == "stormpy.RationalFunction"
    assert docs.argument_name(stormpy.storage.DdType.Sylvan) == "stormpy.DdType.Sylvan"
    assert all("_storage" not in docs.specialization_name(stormpy.SparseMdp, inst) for inst in stormpy.SparseMdp.metadata.instantiations)


def test_pybind_overloads():
    doc = """get(self: test._Floating, value: float) -> float\nOverloaded function.\n\n1. get(self: test._Floating, value: float) -> float\n\n2. get(self: test._Floating, value: int) -> float\n\nDescription."""
    indexes = docs.signature_lines(doc, "get")
    assert indexes == [0, 3, 5]
    assert docs.signature_lines("get(self: test.Example[ValueType])\n\nDescription.", "get") == [0]
    assert "Description." not in [doc.splitlines()[i] for i in indexes]


def test_overload_substitution_and_unrecognized_cpp_types():
    family = make_family()
    entries = []
    for inst in family.metadata.instantiations:
        typ = docs.argument_name(inst.arguments[0])
        entries.append(
            (
                inst,
                f"""shared(*args, **kwargs)\nOverloaded function.\n\n1. shared(self: {inst.native_name}, value: {typ}) -> {typ}\n\n2. shared(self: {inst.native_name}, value: int) -> storm::opaque<{typ}>\n\nShared method.""",
            )
        )
    variants = docs.generic_docs(family, entries, [family], "shared")
    assert all("1. shared(self: test.Example[ValueType], value: ValueType) -> ValueType" in text for _, text in variants)
    assert all("storm::opaque<" not in text for _, text in variants)
    assert all("2. shared(self: test.Example[ValueType], value: int)" in text for _, text in variants)
    assert all("Shared method." in text for _, text in variants)


def test_unresolved_annotations_are_omitted_not_overloads():
    assert (
        docs._public_signature(
            "run(self: stormpy._core._CheckResult, components: storm::Components<std::pair<int, int>>, limit: int = 5) -> storm::Result<int>"
        )
        == "run(self, components, limit: int = 5)"
    )
    assert docs._public_signature("run(self: stormpy.storage.SparseMdp[ValueType]) -> float") == "run(self: stormpy.storage.SparseMdp[ValueType]) -> float"


def test_constructor_deduction_descriptions():
    assert "SparseMatrix[float]" in docs.deduction_description(stormpy.storage.SparseMatrix)
    inferred = docs.deduction_description(stormpy.storage.SparseMdp)
    assert "first positional constructor argument" in inferred
    assert "``components`` or ``other_model``" in inferred
    assert "[float]" not in inferred
    second = docs.deduction_description(stormpy.storage.MemoryStructureBuilder)
    assert "second positional constructor argument" in second
    assert "``model``" in second
    fallback = docs.deduction_description(stormpy.storage.SparseModelComponents)
    assert "``transition_matrix``" in fallback
    assert "If none is supplied, ``SparseModelComponents[float]``" in fallback
    assert "first positional constructor argument" in docs.deduction_description(stormpy.dft.DFTSimulator)
    assert "``dft``" in docs.deduction_description(stormpy.dft.DFTSimulator)
    assert docs.deduction_description(stormpy.storage.Add) is None


def test_real_constructor_overloads_are_not_dropped():
    family = stormpy.storage.SparseCtmc
    output = docs.render_members(family, [family, stormpy.storage.SparseModel])
    signatures, variants = docs.constructors(family, [family, stormpy.storage.SparseModel])
    assert signatures == ("(other_model: stormpy.storage.SparseCtmc[ValueType])", "(components)")
    assert variants == []
    assert "SparseCtmc.__init__" not in output
    assert "SparseCtmc.__str__" not in output
    assert ".. py:method:: SparseCtmc.collect_reward_parameters(self: stormpy.storage.SparseModel[stormpy.RationalFunction])" in output
    assert ".. code-block:: text\n\n      collect_reward_parameters(" not in output


def test_object_defaults_do_not_split_generic_signatures():
    family = stormpy.dft.ExplicitDFTModelBuilder
    output = docs.render_members(family, [family])
    signatures, variants = docs.constructors(family, [family])
    assert signatures == ("(dft, symmetries = ...)",)
    assert variants == []
    assert "ExplicitDFTModelBuilder.__init__" not in output
    assert "object at 0x" not in output


def test_specialization_specific_constructors_are_retained():
    family = stormpy.storage.SparseRewardModel
    signatures, variants = docs.constructors(family, [family])
    assert not signatures
    assert variants
    assert all("SparseRewardModel[" in specialization for specialization, _ in variants)
    assert all("ValueType" not in signature for _, signature in variants)


def test_real_conditional_methods_and_unrecognized_signatures():
    output = docs.render_members(stormpy.Scheduler, [stormpy.Scheduler])
    section = output.split(".. py:method:: Scheduler.cast_to_double_datatype", 1)[1].split(".. py:", 1)[0]
    assert "Available only for:" in section
    assert "Scheduler[stormpy.Interval]" not in section
    assert "-> stormpy.storage.Scheduler[float]" in section
    assert "-> stormpy.storage.Scheduler[ValueType]" not in section
    check = docs.render_members(stormpy.ExplicitQualitativeCheckResult, [stormpy.ExplicitQualitativeCheckResult])
    assert ".. py:method:: ExplicitQualitativeCheckResult.as_explicit_exact_qualitative(self)" in check
    assert "storm::modelchecker::ExplicitQualitativeCheckResult" not in check
    matrix = docs.render_members(stormpy.SparseMatrix, [stormpy.SparseMatrix, stormpy.SparseMatrixRows, stormpy.SparseMatrixEntry])
    assert "stormpy.storage.SparseMatrixEntry[ValueType]" in matrix
    assert ".. py:property:: SparseMatrix.nr_rows" in matrix
    ma = docs.render_members(stormpy.storage.SparseMA, [stormpy.storage.SparseMA])
    assert ".. py:property:: SparseMA.supports_parameters" in ma
    assert "Type: ``bool``" not in ma
    state = docs.render_members(stormpy.storage.SparseModelState, [stormpy.storage.SparseModelState])
    assert "SparseModelState.__int__" not in state
    assert "SparseModelState.__new__" not in state

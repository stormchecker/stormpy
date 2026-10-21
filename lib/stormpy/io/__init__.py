"""Format-specific model descriptions, parsing, exporting and their options."""

import os as _os
from collections.abc import Iterable as _Iterable

import stormpy as _stormpy
from stormpy.core._common import _path
from stormpy.developer import storage as _bindings
from stormpy import developer as _developer
from stormpy.core._parsing import parse_prism_program, parse_jani_model, parse_jani_model_from_string, instantiate_constants
from stormpy.core._io import export_to_drn, export_to_umb

SymbolicModelDescription = _developer.SymbolicModelDescription
JaniModelType = _developer.JaniModelType
DirectEncodingParserOptions = _developer.DirectEncodingParserOptions
ExplicitModelParserOptions = _developer.ExplicitModelParserOptions
DirectEncodingExporterOptions = _developer.DirectEncodingExporterOptions

PrismProgram = _bindings.PrismProgram
PrismModule = _bindings.PrismModule
PrismCommand = _bindings.PrismCommand
PrismUpdate = _bindings.PrismUpdate
PrismAssignment = _bindings.PrismAssignment
PrismLabel = _bindings.PrismLabel
PrismModelType = _bindings.PrismModelType
PrismConstant = _bindings.PrismConstant
PrismVariable = _bindings.PrismVariable
PrismIntegerVariable = _bindings.PrismIntegerVariable
PrismBooleanVariable = _bindings.PrismBooleanVariable
PrismRewardModel = _bindings.PrismRewardModel
JaniModel = _bindings.JaniModel
JaniAutomaton = _bindings.JaniAutomaton
JaniEdge = _bindings.JaniEdge
JaniTemplateEdge = _bindings.JaniTemplateEdge
JaniEdgeDestination = _bindings.JaniEdgeDestination
JaniTemplateEdgeDestination = _bindings.JaniTemplateEdgeDestination
JaniOrderedAssignments = _bindings.JaniOrderedAssignments
JaniAssignment = _bindings.JaniAssignment
JaniLocation = _bindings.JaniLocation
JaniVariableSet = _bindings.JaniVariableSet
JaniType = _bindings.JaniType
BasicType = _bindings.BasicType
BoundedType = _bindings.BoundedType
ClockType = _bindings.ClockType
ArrayType = _bindings.ArrayType
ContinuousType = _bindings.ContinuousType
JaniVariable = _bindings.JaniVariable
JaniConstant = _bindings.JaniConstant
CompressionMode = _bindings.CompressionMode
UmbImportValueType = _bindings.UmbImportValueType
UmbImportOptions = _bindings.UmbImportOptions
UmbExportValueType = _bindings.UmbExportValueType
UmbExportOptions = _bindings.UmbExportOptions
UmbModel = _bindings.UmbModel

__all__ = [
    "PrismProgram",
    "PrismModule",
    "PrismCommand",
    "PrismUpdate",
    "PrismAssignment",
    "PrismLabel",
    "PrismModelType",
    "PrismConstant",
    "PrismVariable",
    "PrismIntegerVariable",
    "PrismBooleanVariable",
    "PrismRewardModel",
    "JaniModel",
    "JaniAutomaton",
    "JaniEdge",
    "JaniTemplateEdge",
    "JaniEdgeDestination",
    "JaniTemplateEdgeDestination",
    "JaniOrderedAssignments",
    "JaniAssignment",
    "JaniLocation",
    "JaniVariableSet",
    "JaniType",
    "BasicType",
    "BoundedType",
    "ClockType",
    "ArrayType",
    "ContinuousType",
    "JaniVariable",
    "JaniConstant",
    "CompressionMode",
    "UmbImportValueType",
    "UmbImportOptions",
    "UmbExportValueType",
    "UmbExportOptions",
    "UmbModel",
    "import_umb",
    "umb_to_archive",
    "export_jani_to_file",
    "sparse_model_to_umb",
    "SymbolicModelDescription",
    "JaniModelType",
    "DirectEncodingParserOptions",
    "ExplicitModelParserOptions",
    "DirectEncodingExporterOptions",
    "parse_prism_program",
    "parse_jani_model",
    "parse_jani_model_from_string",
    "instantiate_constants",
    "export_to_drn",
    "export_to_umb",
]


def import_umb(path: str | _os.PathLike[str], *, options: UmbImportOptions | None = None) -> UmbModel:
    """Read a UMB archive into an intermediate UMB model.

    :param path: Archive filename as a string or path-like object.
    :param options: Optional UmbImportOptions controlling imported values and metadata.
    :return: The intermediate UmbModel; use build_model_from_umb to build a sparse model.
    """
    return _bindings.import_umb(_path(path), options if options is not None else UmbImportOptions())


def umb_to_archive(umb_model: UmbModel, path: str | _os.PathLike[str], options: UmbExportOptions | None = None) -> None:
    """Write an intermediate UMB model to an archive.

    :param umb_model: UMB model to export.
    :param path: Archive filename as a string or path-like object.
    :param options: Optional UmbExportOptions controlling values and compression.
    """
    _bindings.to_archive(umb_model, _path(path), options if options is not None else UmbExportOptions())


def export_jani_to_file(
    filename: str | _os.PathLike[str],
    model: JaniModel,
    properties: "_Iterable[_stormpy.logic.Property] | None" = None,
    *,
    check_valid: bool = True,
    compact: bool = False,
) -> None:
    """Write a JANI model and its properties as JSON.

    :param filename: Output filename as a string or path-like object.
    :param model: JANI model to export.
    :param properties: Optional iterable of properties to include.
    :param check_valid: Whether to validate the model before exporting it.
    :param compact: Whether to omit JSON indentation.
    """
    _bindings.JsonExporter.to_file(model, list(properties) if properties is not None else [], _path(filename), check_valid, compact)


def sparse_model_to_umb(model: "_stormpy.models.SparseModel", *, options: UmbExportOptions | None = None) -> UmbModel:
    """Convert a sparse model to the intermediate UMB representation.

    :param model: Sparse model with floating point, exact or interval values.
    :param options: Optional UmbExportOptions controlling output value encoding.
    :return: Intermediate UmbModel for inspection or archive export.
    """
    return _bindings.sparse_model_to_umb(model, options if options is not None else UmbExportOptions())

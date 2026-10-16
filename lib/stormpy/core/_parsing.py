"""Parsing of symbolic model descriptions and properties."""

from __future__ import annotations

from collections.abc import Iterable, Mapping

from stormpy import developer
from stormpy.developer import storage
from stormpy import Rational
from stormpy.core._common import PathLike, _path
from stormpy.developer import Property, SymbolicModelDescription
from stormpy.exceptions import StormError

# Import classes from developer (and republish them under stormpy.X.)
PrismProgram = storage.PrismProgram
JaniModel = storage.JaniModel


def parse_prism_program(path: PathLike, *, prism_compatibility: bool = False, simplify: bool = True) -> PrismProgram:
    """
    Parse a Prism program from file.

    :param path: Path to the Prism file (string or path-like object).
    :param prism_compatibility: If True, the parser is more lenient and accepts all models accepted by the original Prism model checker.
    :param simplify: If True, the program is simplified after parsing.
    :return: The Prism program.
    """
    return developer.parse_program(_path(path), prism_compatibility=prism_compatibility, simplify=simplify)


def parse_jani_model(path: PathLike, *, property_filter: Iterable[str] | None = None) -> tuple[JaniModel, list[Property]]:
    """
    Parse a Jani model and the properties contained in it from file.

    :param path: Path to the Jani file (string or path-like object).
    :param property_filter: (optional) Names of the properties to parse. If None, all properties are parsed.
    :return: Tuple of the Jani model and the list of properties.
    """
    return developer.parse_jani_model(_path(path), property_filter=list(property_filter) if property_filter is not None else None)


def parse_jani_model_from_string(json_string: str, *, property_filter: Iterable[str] | None = None) -> tuple[JaniModel, list[Property]]:
    """
    Parse a Jani model and the properties contained in it from a string.

    :param json_string: The Jani model in JSON format.
    :param property_filter: (optional) Names of the properties to parse. If None, all properties are parsed.
    :return: Tuple of the Jani model and the list of properties.
    """
    return developer.parse_jani_model_from_string(json_string, property_filter=list(property_filter) if property_filter is not None else None)


def parse_properties(
    properties: str, context: PrismProgram | JaniModel | SymbolicModelDescription | None = None, *, property_filter: Iterable[str] | None = None
) -> list[Property]:
    """
    Parse properties given in the Prism property format.

    Multiple properties are separated by semicolons or newlines.
    Use :func:`parse_property` to parse a single property.

    :param properties: String containing the properties.
    :param context: (optional) Symbolic model (Prism program or Jani model) defining the variables, constants and labels referenced in the properties.
    :param property_filter: (optional) Names of the properties to keep. If None, all properties are kept.
    :return: List of the parsed properties.
    """
    property_filter = set(property_filter) if property_filter is not None else None
    if context is None:
        return developer.parse_properties(properties, property_filter)
    if isinstance(context, PrismProgram):
        return developer.parse_properties_for_prism_program(properties, context, property_filter)
    if isinstance(context, JaniModel):
        return developer.parse_properties_for_jani_model(properties, context, property_filter)
    if isinstance(context, SymbolicModelDescription):
        return developer.parse_properties_for_symbolic_model_description(properties, context, property_filter)
    raise StormError(f"Unsupported context of type {type(context)} for parsing properties. Use a Prism program or a Jani model.")


def parse_property(property: str, context: PrismProgram | JaniModel | SymbolicModelDescription | None = None) -> Property:
    """
    Parse a single property given in the Prism property format.

    Use :func:`parse_properties` to parse several properties at once.

    :param property: String containing exactly one property.
    :param context: (optional) Symbolic model (Prism program or Jani model) defining the variables, constants and labels referenced in the property.
    :return: The parsed property.
    :raises StormError: If the string does not contain exactly one property.
    """
    properties = parse_properties(property, context)
    if len(properties) != 1:
        hint = " Use parse_properties for several properties." if len(properties) > 1 else ""
        raise StormError(f"Expected exactly one property, but {len(properties)} were given.{hint}")
    return properties[0]


def _constant_definitions(
    description: SymbolicModelDescription, constants: str | Mapping[str | storage.Variable, bool | int | float | Rational | storage.Expression]
) -> dict:
    """Convert constant definitions given as string or mapping into a mapping from variables to expressions."""
    if isinstance(constants, str):
        return description.parse_constant_definitions(constants)
    if not isinstance(constants, Mapping):
        raise StormError(f"Unsupported constant definitions of type {type(constants)}. Use a string or a mapping.")
    manager = description.as_prism_program().expression_manager if description.is_prism_program() else description.as_jani_model().expression_manager
    definitions = {}
    for name, value in constants.items():
        if isinstance(name, storage.Variable):
            variable = name
        elif isinstance(name, str):
            if not manager.has_variable(name):
                raise StormError(f"Unknown constant '{name}'.")
            variable = manager.get_variable(name)
        else:
            raise StormError(f"Unsupported constant {name!r} of type {type(name)}. Use the name or the variable.")
        # bool must be checked before int as bool is a subclass of int
        if isinstance(value, storage.Expression):
            expression = value
        elif isinstance(value, bool):
            expression = manager.boolean(value)
        elif isinstance(value, int):
            expression = manager.integer(value)
        elif isinstance(value, float):
            # Use the decimal representation to obtain the exact rational (e.g. 0.1 -> 1/10)
            expression = manager.rational(Rational(repr(value)))
        elif isinstance(value, Rational):
            expression = manager.rational(value)
        else:
            raise StormError(f"Unsupported value {value!r} of type {type(value)} for constant '{variable.name}'.")
        definitions[variable] = expression
    return definitions


def instantiate_constants(
    model: PrismProgram | JaniModel | SymbolicModelDescription,
    constants: str | Mapping[str | storage.Variable, bool | int | float | Rational | storage.Expression],
    properties: Property | Iterable[Property] | None = None,
) -> tuple[PrismProgram | JaniModel | SymbolicModelDescription, list[Property]]:
    """
    Instantiate undefined constants in a symbolic model and the corresponding properties.

    :param model: Symbolic model (Prism program, Jani model or symbolic model description).
    :param constants: Constant definitions, either as comma-separated string, e.g. ``"N=3,p=0.5"``,
        or as mapping from constants (given by name or variable) to values, e.g. ``{"N": 3, "p": 0.5}``.
        Values can be Booleans, integers, floats, rationals or expressions.
    :param properties: (optional) Property or properties in which the constants are instantiated as well.
    :return: Tuple of the instantiated model (of the same kind as the given model) and the list of instantiated properties.
    """
    description = model if isinstance(model, SymbolicModelDescription) else SymbolicModelDescription(model)
    definitions = _constant_definitions(description, constants)
    instantiated = description.preprocess(definitions)
    if isinstance(properties, Property):
        properties = [properties]
    instantiated_properties = developer.substitute_constants_in_properties(list(properties), definitions) if properties else []
    if isinstance(model, PrismProgram):
        return instantiated.as_prism_program(), instantiated_properties
    if isinstance(model, JaniModel):
        return instantiated.as_jani_model(), instantiated_properties
    return instantiated, instantiated_properties

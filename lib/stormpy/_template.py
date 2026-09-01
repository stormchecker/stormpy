"""Runtime representation and metadata for native C++ template families.

C++ template specializations still need to be compiled and bound separately.
``TemplateClass`` groups those concrete Python classes behind one public,
subscriptable object and exposes their structure to documentation and stub
generation tools.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator, Mapping, Sequence
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Literal, TypeAlias

TemplateParameterKind: TypeAlias = Literal["type", "value"]


@dataclass(frozen=True)
class TemplateParameter:
    """Description of one public template parameter.

    ``type`` parameters select a Python or native type. ``value`` parameters
    select a runtime value, such as a ``ModelType`` enum member.
    """

    name: str
    kind: TemplateParameterKind = "type"


@dataclass(frozen=True)
class TemplateInstantiation:
    """Description of one concrete native template specialization."""

    arguments: tuple[object, ...]
    implementation: type
    native_name: str


@dataclass(frozen=True)
class TemplateMetadata:
    """Tooling-oriented description of a complete template family."""

    name: str
    canonical_name: str
    parameters: tuple[TemplateParameter, ...]
    instantiations: tuple[TemplateInstantiation, ...]
    deduction_guide: str | None


DeductionGuide: TypeAlias = Callable[["TemplateClass", tuple[Any, ...], Mapping[str, Any]], object]


def deduce_from_first_argument(source: "TemplateClass | None" = None, *, keyword: str | None = None) -> DeductionGuide:
    """Create a guide that copies template arguments from an instance.

    The first positional constructor argument is used when present. ``keyword``
    optionally identifies the same argument for keyword-only calls. If
    ``source`` is omitted, the instance is matched against the family being
    constructed; otherwise it is matched against ``source``.
    """

    def deduction(family: TemplateClass, args: tuple[Any, ...], kwargs: Mapping[str, Any]) -> object:
        if args:
            instance = args[0]
        elif keyword is not None and keyword in kwargs:
            instance = kwargs[keyword]
        else:
            argument = f" {keyword!r}" if keyword is not None else " first positional"
            raise TypeError(f"Cannot deduce template parameters without the{argument} argument")
        return (source or family).parameters_of(instance)

    deduction.__name__ = "deduce_from_first_argument"
    deduction.__qualname__ = "deduce_from_first_argument"
    return deduction


class TemplateClass:
    """Native C++ template family exposed as a subscriptable Python object.

    ``family[parameters]`` returns a registered concrete Python class.
    ``family(*args, **kwargs)`` constructs a class selected by a configured
    deduction guide.
    """

    def __init__(
        self,
        canonical_name: str,
        module: object,
        *,
        parameters: Sequence[str | TemplateParameter],
        deduce: DeductionGuide | None = None,
    ) -> None:
        """Load a native template family.

        :param canonical_name: Fully qualified public family name used for
            native registration lookup, tooling, and representations. Its last
            component is the native template-family name.
        :param module: Native module containing the registered specializations.
        :param parameters: Ordered descriptions or names of the public
            template parameters. A bare name describes a type parameter.
        :param deduce: Optional constructor deduction guide. It receives this
            family, the positional constructor arguments, and a read-only
            mapping of keyword arguments, and returns the complete template
            parameter tuple. Deduction guides may inspect any constructor
            argument and may provide defaults or transform parameters.
        :raises RuntimeError: If the module has no registrations for ``name``,
            has an empty registration table, or mixes parameter arities.
        :raises ValueError: If parameter metadata or the canonical name is
            invalid.
        """
        canonical_module, separator, name = canonical_name.rpartition(".")
        if not separator or not canonical_module or not name.isidentifier():
            raise ValueError("Canonical template name must be fully qualified")

        try:
            implementations = module._template_instantiations[name]
        except (AttributeError, KeyError):
            raise RuntimeError(f"Native module has no registrations for {name}") from None
        if not implementations:
            raise RuntimeError(f"Native module has no registrations for {name}")

        arities = {len(arguments) for arguments in implementations}
        if len(arities) != 1:
            raise RuntimeError(f"Native module has inconsistent registrations for {name}")

        parameter_metadata = tuple(parameter if isinstance(parameter, TemplateParameter) else TemplateParameter(parameter) for parameter in parameters)
        arity = arities.pop()
        if len(parameter_metadata) != arity:
            raise ValueError(f"{name} has {arity} native template parameters, but {len(parameter_metadata)} parameter names were provided")
        if any(not parameter.name or not parameter.name.isidentifier() for parameter in parameter_metadata):
            raise ValueError(f"Invalid template parameter name for {name}")
        if any(parameter.kind not in ("type", "value") for parameter in parameter_metadata):
            raise ValueError(f"Invalid template parameter kind for {name}")
        if len({parameter.name for parameter in parameter_metadata}) != arity:
            raise ValueError(f"Template parameter names for {name} must be unique")

        self.__name__ = name
        self.__qualname__ = name
        self.__module__ = canonical_module
        self._canonical_name = canonical_name
        self._parameters = parameter_metadata
        self._arity = arity
        self._deduction_guide = deduce
        self._instantiations: dict[tuple[object, ...], type] = {}
        for arguments, implementation in implementations.items():
            self.register(arguments, implementation)

    def _normalize(self, parameters: object) -> tuple[object, ...]:
        """Convert subscription parameters to a validated tuple."""
        key = parameters if isinstance(parameters, tuple) else (parameters,)
        if len(key) != self._arity:
            raise TypeError(f"{self.__name__} expects {self._arity} template " f"parameter{'s' if self._arity != 1 else ''}, got {len(key)}")
        return key

    def register(self, parameters: object, implementation: type) -> None:
        """Add a concrete specialization to this family.

        :param parameters: One parameter or a tuple containing the complete
            template-parameter list.
        :param implementation: Concrete Python class for those parameters.
        :raises TypeError: If the parameter count is wrong or ``implementation``
            is not a class.
        :raises ValueError: If the parameter tuple is already registered.
        """
        key = self._normalize(parameters)
        if not isinstance(implementation, type):
            raise TypeError("A template implementation must be a class")
        if key in self._instantiations:
            raise ValueError(f"{self.__name__}{key!r} is already registered")
        self._instantiations[key] = implementation

    def __getitem__(self, parameters: object) -> type:
        """Return the concrete class registered for ``parameters``.

        A single parameter may be written directly as ``family[T]``; multiple
        parameters use normal subscription tuple syntax, ``family[T, U]``.

        :raises TypeError: If the parameter count is wrong or no matching
            specialization is registered.
        """
        key = self._normalize(parameters)
        try:
            return self._instantiations[key]
        except KeyError:
            raise TypeError(f"{self.__name__} has no instantiation for {key!r}") from None

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Construct the specialization selected by the deduction guide.

        :raises TypeError: If no deduction guide is configured or the deduced
            specialization is unavailable.
        """
        if self._deduction_guide is None:
            raise TypeError(f"{self.__name__} requires explicit template parameters")
        parameters = self._deduction_guide(self, args, MappingProxyType(kwargs))
        return self[parameters](*args, **kwargs)

    def parameters_of(self, instance: object) -> tuple[object, ...]:
        """Return the complete parameter tuple of a registered instance.

        :raises TypeError: If the instance matches zero or multiple registered
            specializations.
        """
        matches = [parameters for parameters, implementation in self._instantiations.items() if isinstance(instance, implementation)]
        if len(matches) != 1:
            raise TypeError(f"Cannot infer {self.__name__} template parameters from {type(instance)!r}")
        return matches[0]

    @property
    def canonical_name(self) -> str:
        """Fully qualified public name of this template family."""
        return self._canonical_name

    @property
    def metadata(self) -> TemplateMetadata:
        """Return an immutable, current description for documentation tools."""
        instantiations = tuple(
            TemplateInstantiation(arguments, implementation, f"{implementation.__module__}.{implementation.__name__}")
            for arguments, implementation in self._instantiations.items()
        )
        guide = None
        if self._deduction_guide is not None:
            guide = getattr(self._deduction_guide, "__qualname__", type(self._deduction_guide).__qualname__)
        return TemplateMetadata(self.__name__, self._canonical_name, self._parameters, instantiations, guide)

    @property
    def instantiations(self) -> Mapping[tuple[object, ...], type]:
        """Map registered parameter tuples to classes without allowing mutation."""
        return MappingProxyType(self._instantiations)

    def is_instantiation(self, instance: object) -> bool:
        """Return whether ``instance`` belongs to any registered specialization."""
        return isinstance(instance, tuple(self._instantiations.values()))

    def __iter__(self) -> Iterator[tuple[object, ...]]:
        """Iterate over registered parameter tuples in registration order."""
        return iter(self._instantiations)

    def __repr__(self) -> str:
        """Return a concise template-family representation."""
        return f"<template class {self._canonical_name}>"

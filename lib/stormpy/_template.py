"""Runtime representation of C++ template families.

C++ template specializations still need to be compiled and bound separately.
``TemplateClass`` groups those concrete Python classes behind one public,
subscriptable object.
"""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from types import MappingProxyType
from typing import Any


class TemplateClass:
    """Native C++ template family exposed as a subscriptable Python object.

    ``family[parameters]`` returns a registered concrete Python class.
    ``family(*args, **kwargs)`` constructs a class selected by a configured
    deduction rule.
    """

    def __init__(
        self,
        name: str,
        module: object,
        *,
        deduce_from: TemplateClass | None = None,
    ) -> None:
        """Load a native template family.

        :param name: Family name used by the native registration table.
        :param module: Native module containing the registered specializations.
        :param deduce_from: Optional constructor deduction guide. For an
            unsubscripted call, copy the complete parameter tuple of the first
            argument from this template family. For example,
            ``deduce_from=DFT`` makes ``Builder(dft)`` select
            ``Builder[float]`` when ``dft`` is a ``DFT[float]``. Source and
            target families must have equivalent parameter tuples; no defaults
            or partial deduction are performed.
        :raises RuntimeError: If the module has no registrations for ``name``,
            has an empty registration table, or mixes parameter arities.
        """
        try:
            implementations = module._template_instantiations[name]
        except (AttributeError, KeyError):
            raise RuntimeError(f"Native module has no registrations for {name}") from None
        if not implementations:
            raise RuntimeError(f"Native module has no registrations for {name}")

        arities = {len(parameters) for parameters in implementations}
        if len(arities) != 1:
            raise RuntimeError(f"Native module has inconsistent registrations for {name}")

        self.__name__ = name
        self._arity = arities.pop()
        self._deduction_source = deduce_from
        self._instantiations: dict[tuple[object, ...], type] = {}
        for parameters, implementation in implementations.items():
            self.register(parameters, implementation)

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
        :raises TypeError: If the parameter count differs from the family's
            native arity.
        :raises ValueError: If the parameter tuple is already registered.
        """
        key = self._normalize(parameters)
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
        """Construct an instance of the specialization selected from the first argument.

        The first positional argument is matched against ``deduce_from``. If no
        deduction source is configured, it is matched against this family,
        enabling copy-like construction such as ``DFT(existing_dft)``.

        :raises TypeError: If no arguments permit deduction, the first argument
            is not a uniquely registered instance, or the resulting
            specialization is unavailable.
        """
        if args:
            parameters = (self._deduction_source or self).parameters_of(args[0])
        else:
            raise TypeError(f"{self.__name__} requires explicit template parameters")
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
        return f"<template class {self.__name__}>"

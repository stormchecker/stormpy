"""Public wrapper and JSON serialization for DFT module decomposition."""

from . import developer
from . import DFT, DFTElement


class DftIndependentModule:
    """An independent module of a DFT: a subtree that can be analyzed in isolation.

    Wraps :class:`stormpy.dft.developer.DftIndependentModule`, resolving element
    indices to their :class:`~stormpy.dft.DFTElement` objects.
    """

    def __init__(self, native: developer.DftIndependentModule, dft: DFT) -> None:
        self._native = native
        self._dft = dft

    @property
    def is_static(self) -> bool:
        """:return: True iff the module contains only static elements (except in submodules)."""
        return self._native.is_static()

    @property
    def is_fully_static(self) -> bool:
        """:return: True iff the module contains only static elements (also in submodules)."""
        return self._native.is_fully_static()

    @property
    def is_single_be(self) -> bool:
        """:return: True iff the module consists of a single BE (trivial module)."""
        return self._native.is_single_be()

    @property
    def representative(self) -> DFTElement:
        """:return: The DFT element representing this module."""
        return self._dft.get_element(self._native.get_representative())

    @property
    def elements(self) -> list[DFTElement]:
        """:return: The elements directly contained in this module (excluding submodules)."""
        return [self._dft.get_element(index) for index in self._native.get_elements()]

    @property
    def submodules(self) -> list["DftIndependentModule"]:
        """:return: The submodules nested within this module."""
        return [DftIndependentModule(submodule, self._dft) for submodule in self._native.get_submodules()]

    def subtree(self) -> DFT:
        """:return: The DFT restricted to this module's subtree."""
        return self._native.get_subtree(self._dft)


def modules(dft: DFT) -> DftIndependentModule:
    """Compute the independent-module decomposition of a DFT.

    :param dft: The DFT to decompose.
    :return: The top-level :class:`DftIndependentModule`.
    """
    return DftIndependentModule(dft.modules(), dft)


def _element_json(element: DFTElement) -> dict[str, str]:
    """
    Get JSON representation of an element.

    :param element: DFT element.
    :return: Dict with 'id' and 'name'.
    """
    return {"id": str(element.id), "name": element.name}


def _module_json(module: DftIndependentModule) -> dict[str, object]:
    """
    Create JSON representation of a DFT module.

    :param module: Module.
    :return: JSON object containing the module and its submodules in a recursive hierarchy.
    """
    data = dict()
    data["representative"] = _element_json(module.representative)
    data["elements"] = [_element_json(elem) for elem in module.elements]
    data["submodules"] = [_module_json(submodule) for submodule in module.submodules]
    return data


def modules_json(dft: DFT) -> dict[str, object]:
    """
    Create JSON representation of DFT modules.

    :param dft: DFT.
    :return: JSON object containing all modules in a recursive hierarchy.
    """
    return _module_json(modules(dft))

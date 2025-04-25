import stormpy.dft


def _get_tuple(dft, index):
    """
    Get json representation of element.

    :param dft: DFT.
    :param index: Index (Id).
    :return: Dict with 'name' and 'index'.
    """
    return {"id": str(index), "name": dft.get_element(index).name}


def _modules_json(dft, module):
    """
    Create JSON representation of DFT modules.

    :param dft: DFT.
    :param module: Module.
    :return: JSON object containing all modules in a recursive hierarchy.
    """
    data = dict()
    data["representative"] = _get_tuple(dft, module.representative())
    data["elements"] = [_get_tuple(dft, elem) for elem in module.elements()]
    submodules = []
    for submodule in module.submodules():
        submodules.append(_modules_json(dft, submodule))
    data["submodules"] = submodules
    return data


def modules_json(dft):
    """
    Create JSON representation of DFT modules.

    :param dft: DFT.
    :return: JSON object containing all modules in a recursive hierarchy.
    """
    return _modules_json(dft, dft.modules())

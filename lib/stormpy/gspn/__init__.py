"""API for Generalized Stochastic Petri Nets (GSPNs).

Makes the functionality of ``storm::gspn::`` available.
"""

from . import developer
from stormpy.logic import Property
from stormpy.core._common import PathLike, _path
from stormpy.io import JaniModel

# Import classes from developer
GSPN = developer.GSPN
GspnBuilder = developer.GspnBuilder
Place = developer.Place
Transition = developer.Transition
TimedTransition = developer.TimedTransition
ImmediateTransition = developer.ImmediateTransition
TransitionPartition = developer.TransitionPartition
LayoutInfo = developer.LayoutInfo


def load_gspn_file(path: PathLike, *, constant_definitions: str = "") -> GSPN:
    """
    Load a GSPN from a file in the PNML or PNPRO format.

    The format is determined by the file extension (``.pnml`` or ``.pnpro``).

    :param path: Path to the GSPN file (string or path-like object).
    :param constant_definitions: Definitions of undefined constants, e.g. ``"N=3,rate=0.5"``.
    :return: The GSPN.
    """
    return developer.GspnParser.parse(_path(path), constant_definitions)


def export_gspn_pnpro_file(gspn: GSPN, path: PathLike) -> None:
    """
    Export a GSPN to a file in the PNPRO format.

    :param gspn: GSPN.
    :param path: Path of the output file (string or path-like object).
    """
    developer.export_gspn_to_pnpro(gspn, _path(path))


def export_gspn_pnml_file(gspn: GSPN, path: PathLike) -> None:
    """
    Export a GSPN to a file in the PNML format.

    :param gspn: GSPN.
    :param path: Path of the output file (string or path-like object).
    """
    developer.export_gspn_to_pnml(gspn, _path(path))


def build_jani_model(gspn: GSPN, *, automaton_name: str = "gspn_automaton", add_deadlock_properties: bool = False) -> tuple[JaniModel, list[Property]]:
    """
    Translate a GSPN into a JANI model.

    :param gspn: GSPN.
    :param automaton_name: Name of the JANI automaton.
    :param add_deadlock_properties: Whether to create the standard properties for deadlocks
        (reachability, time-bounded reachability with the constant ``TIME_BOUND``, and expected time).
        This adds transient variables for deadlocks to the model.
    :return: The JANI model and the deadlock properties (empty if not requested).
    """
    builder = developer.JaniGSPNBuilder(gspn)
    model = builder.build(automaton_name)
    properties = builder.get_deadlock_properties(model) if add_deadlock_properties else []
    return model, properties


__all__ = [
    # GSPN data structures
    "GSPN",
    "GspnBuilder",
    "Place",
    "Transition",
    "TimedTransition",
    "ImmediateTransition",
    "TransitionPartition",
    "LayoutInfo",
    # Input/output
    "load_gspn_file",
    "export_gspn_pnpro_file",
    "export_gspn_pnml_file",
    "build_jani_model",
]

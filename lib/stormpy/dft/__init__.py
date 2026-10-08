"""API for Dynamic Fault Tree (DFT) analysis.

Makes the functionality of ``storm::dft::`` available.
"""

import warnings
from collections.abc import Iterable

from . import developer
from stormpy import Property, RationalFunction
from stormpy.exceptions import StormError, StormWarning
from stormpy.storage import SparseCtmc, SparseMA

# Import classes from developer (and republish them under stormpy.dft.X.)
DFT = developer.DFT.publish_as("stormpy.dft.DFT")


# Extend parametric DFT with a convenience method to collect its parameters
def _get_parameters(self):
    """Return the parameters occurring in this parametric DFT."""
    return developer.get_parameters(self)


DFT.instantiations[(RationalFunction,)].get_parameters = _get_parameters

DFTElementType = developer.DFTElementType
DFTElement = developer.DFTElement.publish_as("stormpy.dft.DFTElement")
DFTBE = developer.DFTBE.publish_as("stormpy.dft.DFTBE")
DFTDependency = developer.DFTDependency.publish_as("stormpy.dft.DFTDependency")
DFTState = developer.DFTState.publish_as("stormpy.dft.DFTState")

DftInstantiator = developer.DftInstantiator.publish_as("stormpy.dft.DftInstantiator")

DftEnvironment = developer.DftEnvironment
AnalysisEnvironment = developer.AnalysisEnvironment
ModelBuilderEnvironment = developer.ModelBuilderEnvironment
TransformationEnvironment = developer.TransformationEnvironment

ApproximationHeuristic = developer.ApproximationHeuristic

RelevantEvents = developer.RelevantEvents
DftSymmetries = developer.DftSymmetries

# Import functions from developer
load_dft_galileo_file = developer.load_dft_galileo_file
load_parametric_dft_galileo_file = developer.load_parametric_dft_galileo_file
load_dft_json_file = developer.load_dft_json_file
load_dft_json_string = developer.load_dft_json_string
load_parametric_dft_json_file = developer.load_parametric_dft_json_file
load_parametric_dft_json_string = developer.load_parametric_dft_json_string
export_dft_json_file = developer.export_dft_json_file
export_dft_json_string = developer.export_dft_json_string

# Additional Python classes and functions
# Require some of the public classes and need to be imported after them
from ._module import DftIndependentModule, modules, modules_json
from ._simulator import DFTSimulator, SimulationStepResult, SimulationTraceResult

# Add additional functions


# Define helper functions
def check_dft_validity(dft: DFT) -> bool:
    """
    Check validity of DFT.
    Checks whether the DFT is well-formed, can be analyzed via Markov model analysis and points out potential modeling issues.
    :param dft: DFT.
    :return: True iff DFT is valid.
    """
    valid, output = developer.is_well_formed(dft, check_valid_for_analysis=True)
    if not valid:
        raise StormError("DFT is not well formed and cannot be analysed: {}".format(output))
    issue, output = developer.has_potential_modeling_issues(dft)
    if issue:
        # Modeling issues do not prevent analysis but could lead to unexpected analysis results
        warnings.warn("DFT has modeling issue which could lead to unexpected results: {}".format(output), StormWarning)
    return valid and not issue


# API functions
def analyze_dft(
    env: DftEnvironment,
    dft: DFT,
    properties: Iterable[Property],
    relevant_events: RelevantEvents | None = None,
) -> list[float | tuple[float, float]] | list[RationalFunction | tuple[RationalFunction, RationalFunction]]:
    """
    Analyze the DFT with respect to the given properties.

    :param env: Environment configuring the analysis.
    :param dft: DFT.
    :param properties: Properties to check.
    :param relevant_events: (optional) relevant events which should be observed.
    :return: List of results corresponding to the given properties.
        Each entry is a single value for exact analysis, or a tuple (lower, upper) for approximate analysis.
        For approximate analysis, the difference between the bounds satisfies the (relative) error given by env.analysis_environment.approximation_error.
    """
    check_dft_validity(dft)
    return developer.analyze_dft(
        env,
        dft,
        [(prop.raw_formula if isinstance(prop, Property) else prop) for prop in properties],
        relevant_events if relevant_events is not None else developer.RelevantEvents(),
    )


def build_model(
    env: DftEnvironment,
    dft: DFT,
    symmetries: DftSymmetries | None = None,
    relevant_events: RelevantEvents | None = None,
) -> SparseCtmc[float] | SparseCtmc[RationalFunction] | SparseMA[float] | SparseMA[RationalFunction]:
    """
    Build state-space model (CTMC or MA) for the given DFT.

    :param env: Environment configuring the build.
    :param dft: DFT.
    :param symmetries: (optional) symmetries in the DFT to exploit.
    :param relevant_events: (optional) relevant events which should be observed.
    :return: The built model as either a CTMC or an MA.
    """
    return developer.build_model(
        env,
        dft,
        symmetries if symmetries is not None else developer.DftSymmetries(),
        relevant_events if relevant_events is not None else developer.RelevantEvents(),
    )


def prepare_for_analysis(dft: DFT) -> DFT:
    """
    Prepare a DFT for analysis.
    Marks FDEP conflicts and applies the standard set of DFT-to-CTMC/MA transformations expected by the model builder.

    :param dft: The DFT to prepare.
    :return: The prepared DFT.
    """
    developer.compute_dependency_conflicts(dft, use_smt=False)
    return developer.transform_dft(dft, unique_constant_be=True, binary_fdeps=True, exponential_distributions=True)

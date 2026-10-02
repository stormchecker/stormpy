"""Public API for Dynamic Fault Tree (DFT) analysis.

This is a curated, documented façade over the raw pybind11 bindings in
:mod:`stormpy.dft.developer`. It re-exports the parts of the native API that
are already good public names, adds a few hand-written convenience wrappers
(:class:`DftIndependentModule`, :class:`DFTSimulator`), and otherwise leaves
low-level/advanced functionality (e.g. :class:`~stormpy.dft.developer.RandomGenerator`,
raw ``ValueType``-specific overloads) to :mod:`stormpy.dft.developer`.
"""

from . import developer

# Template families: re-exported unmodified, since each is already a clean,
# well-scoped query/data object.
DFT = developer.DFT
DFTElement = developer.DFTElement
DFTBE = developer.DFTBE
DFTDependency = developer.DFTDependency
DFTState = developer.DFTState
ExplicitDFTModelBuilder = developer.ExplicitDFTModelBuilder

# Renamed for public clarity: matches the DftEnvironment/DftSymmetries capitalization
# convention used elsewhere in this API (the native binding follows storm-dft's own,
# inconsistent, all-caps "DFT" spelling for this one class).
DFTInstantiator = developer.DftInstantiator

# Non-template classes and enums, already well-named: re-exported unmodified.
DftSymmetries = developer.DftSymmetries
DftEnvironment = developer.DftEnvironment
AnalysisEnvironment = developer.AnalysisEnvironment
ModelBuilderEnvironment = developer.ModelBuilderEnvironment
TransformationEnvironment = developer.TransformationEnvironment
RelevantEvents = developer.RelevantEvents
DFTElementType = developer.DFTElementType
ApproximationHeuristic = developer.ApproximationHeuristic
SimulationStepResult = developer.SimulationStepResult
SimulationTraceResult = developer.SimulationTraceResult


# Analysis functions.
#
# analyze_dft/build_model restore a Python-level default for relevant_events/symmetries:
# the native developer.analyze_dft/developer.build_model require them explicitly (developer
# mirrors the C++ API 1:1, with no conveniences), so the default lives here instead.
def analyze_dft(env, dft, properties, relevant_events=None):
    """
    Analyze the DFT.

    :param env: Environment for the analysis.
    :param dft: DFT.
    :param properties: PCTL formulas capturing the properties to check.
    :param relevant_events: Relevant events which should be observed, or ``None`` for none.
    :return: Results.
    """
    return developer.analyze_dft(env, dft, properties, relevant_events if relevant_events is not None else developer.RelevantEvents())


def build_model(env, dft, symmetries=None, relevant_events=None):
    """
    Build state-space model (CTMC or MA) for DFT.

    :param env: Environment for the analysis.
    :param dft: DFT.
    :param symmetries: Symmetries in the DFT, or ``None`` for none.
    :param relevant_events: Relevant events which should be observed, or ``None`` for none.
    :return: The built model.
    """
    return developer.build_model(
        env,
        dft,
        symmetries if symmetries is not None else developer.DftSymmetries(),
        relevant_events if relevant_events is not None else developer.RelevantEvents(),
    )


transform_dft = developer.transform_dft
compute_dependency_conflicts = developer.compute_dependency_conflicts
is_well_formed = developer.is_well_formed
has_potential_modeling_issues = developer.has_potential_modeling_issues
compute_relevant_events = developer.compute_relevant_events
get_parameters = developer.get_parameters

# Input/output
load_dft_galileo_file = developer.load_dft_galileo_file
load_parametric_dft_galileo_file = developer.load_parametric_dft_galileo_file
load_dft_json_file = developer.load_dft_json_file
load_dft_json_string = developer.load_dft_json_string
load_parametric_dft_json_file = developer.load_parametric_dft_json_file
load_parametric_dft_json_string = developer.load_parametric_dft_json_string
export_dft_json_file = developer.export_dft_json_file
export_dft_json_string = developer.export_dft_json_string

# Hand-written curated wrappers
from ._module import DftIndependentModule, modules, modules_json
from ._simulator import DFTSimulator


def prepare_for_analysis(dft):
    """
    Prepare a DFT for analysis: mark FDEP conflicts and apply the standard
    set of DFT-to-CTMC/MA transformations expected by the model builder.

    :param dft: The DFT to prepare.
    :return: The prepared DFT.
    """
    compute_dependency_conflicts(dft, use_smt=False)
    return transform_dft(dft, unique_constant_be=True, binary_fdeps=True, exponential_distributions=True)

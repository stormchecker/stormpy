import math

import stormpy
from stormpy.tests.helpers.helper import get_example_path
from stormpy.tests.configurations import dft


@dft
class TestDftEnvironment:
    def test_dft_environment_subenvironments(self):
        env = stormpy.dft.DftEnvironment()
        assert isinstance(env.analysis_environment, stormpy.dft.AnalysisEnvironment)
        assert isinstance(env.model_builder_environment, stormpy.dft.ModelBuilderEnvironment)
        assert isinstance(env.transformation_environment, stormpy.dft.TransformationEnvironment)

    def test_analysis_environment_properties(self):
        env = stormpy.dft.DftEnvironment()
        analysis_env = env.analysis_environment

        analysis_env.use_modularisation = True
        assert analysis_env.use_modularisation
        analysis_env.solve_with_smt = True
        assert analysis_env.solve_with_smt
        analysis_env.chunksize = 7
        assert analysis_env.chunksize == 7
        analysis_env.mttf_precision = 1e-3
        assert math.isclose(analysis_env.mttf_precision, 1e-3)
        analysis_env.mttf_stepsize = 0.5
        assert math.isclose(analysis_env.mttf_stepsize, 0.5)
        assert analysis_env.approximation_error is None
        analysis_env.approximation_error = 0.1
        assert math.isclose(analysis_env.approximation_error, 0.1)
        analysis_env.approximation_error = None
        assert analysis_env.approximation_error is None

    def test_model_builder_environment_properties(self):
        env = stormpy.dft.DftEnvironment()
        builder_env = env.model_builder_environment

        builder_env.use_symmetry_reduction = False
        assert not builder_env.use_symmetry_reduction
        builder_env.allow_dc_for_relevant_events = True
        assert builder_env.allow_dc_for_relevant_events
        builder_env.add_labels_claiming = True
        assert builder_env.add_labels_claiming
        assert builder_env.max_depth is None
        builder_env.max_depth = 5
        assert builder_env.max_depth == 5
        builder_env.max_depth = None
        assert builder_env.max_depth is None
        builder_env.take_first_dependency = True
        assert builder_env.take_first_dependency
        builder_env.unique_failed_be = True
        assert builder_env.unique_failed_be

    def test_transformation_environment_properties(self):
        env = stormpy.dft.DftEnvironment()
        transformation_env = env.transformation_environment

        transformation_env.use_bisimulation = True
        assert transformation_env.use_bisimulation
        transformation_env.eliminate_chains = True
        assert transformation_env.eliminate_chains

        for label_behavior in (
            stormpy.EliminationLabelBehavior.KEEP_LABELS,
            stormpy.EliminationLabelBehavior.EXTEND_LABELS,
            stormpy.EliminationLabelBehavior.MERGE_LABELS,
            stormpy.EliminationLabelBehavior.DELETE_LABELS,
        ):
            transformation_env.label_behavior = label_behavior
            assert transformation_env.label_behavior == label_behavior

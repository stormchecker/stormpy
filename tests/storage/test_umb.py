import os
import tempfile

import pytest
import stormpy
from helpers.helper import get_example_path


@pytest.fixture
def dtmc():
    program = stormpy.parse_prism_program(get_example_path("dtmc", "brp-16-2.pm"))
    return stormpy.build_sparse_model_with_options(program, stormpy.BuilderOptions(True, True))


@pytest.fixture
def mdp():
    program = stormpy.parse_prism_program(get_example_path("mdp", "coin2-2.nm"))
    return stormpy.build_sparse_model_with_options(program, stormpy.BuilderOptions(True, True))


@pytest.fixture
def tmp_umb(tmp_path):
    return str(tmp_path / "test.umb")


class TestUmbOptions:
    def test_import_options_defaults(self):
        opts = stormpy.UmbImportOptions()
        assert opts.build_choice_labeling is True
        assert opts.build_state_valuations is True
        assert opts.value_type == stormpy.UmbImportValueType.Default

    def test_export_options_defaults(self):
        opts = stormpy.UmbExportOptions()
        assert opts.allow_choice_labeling_as_actions is True
        assert opts.allow_choice_origins_as_actions is False
        assert opts.canonicize_pomdp is True
        assert opts.compression == stormpy.CompressionMode.Default
        assert opts.value_type == stormpy.UmbExportValueType.Default

    def test_import_options_set(self):
        opts = stormpy.UmbImportOptions()
        opts.value_type = stormpy.UmbImportValueType.Double
        opts.build_choice_labeling = False
        opts.build_state_valuations = False
        assert opts.value_type == stormpy.UmbImportValueType.Double
        assert opts.build_choice_labeling is False
        assert opts.build_state_valuations is False

    def test_export_options_set(self):
        opts = stormpy.UmbExportOptions()
        opts.compression = stormpy.CompressionMode.Gzip
        opts.value_type = stormpy.UmbExportValueType.Rational
        assert opts.compression == stormpy.CompressionMode.Gzip
        assert opts.value_type == stormpy.UmbExportValueType.Rational

    def test_compression_mode_enum(self):
        assert stormpy.CompressionMode.Default
        assert stormpy.CompressionMode.Gzip
        assert stormpy.CompressionMode.Xz
        assert stormpy.CompressionMode.NoCompression

    def test_import_value_type_enum(self):
        assert stormpy.UmbImportValueType.Default
        assert stormpy.UmbImportValueType.Rational
        assert stormpy.UmbImportValueType.Double

    def test_export_value_type_enum(self):
        assert stormpy.UmbExportValueType.Default
        assert stormpy.UmbExportValueType.Rational
        assert stormpy.UmbExportValueType.Double
        assert stormpy.UmbExportValueType.DoubleInterval
        assert stormpy.UmbExportValueType.RationalInterval


class TestUmbModel:
    def test_str(self, dtmc):
        umb = stormpy.sparse_model_to_umb(dtmc)
        assert isinstance(str(umb), str)

    def test_get_short_model_information(self, dtmc):
        umb = stormpy.sparse_model_to_umb(dtmc)
        assert isinstance(umb.get_short_model_information(), str)

    def test_get_model_information(self, dtmc):
        umb = stormpy.sparse_model_to_umb(dtmc)
        info = umb.get_model_information()
        assert isinstance(info, str)
        assert len(info) > 0

    def test_validate(self, dtmc):
        umb = stormpy.sparse_model_to_umb(dtmc)
        valid, errors = umb.validate()
        assert valid is True
        assert errors == ""

    def test_validate_or_throw(self, dtmc):
        umb = stormpy.sparse_model_to_umb(dtmc)
        umb.validate_or_throw()  # should not raise


class TestUmbConvenienceFunctions:
    def test_export_and_build_dtmc(self, dtmc, tmp_umb):
        stormpy.export_to_umb(dtmc, tmp_umb)
        assert os.path.isfile(tmp_umb)
        model2 = stormpy.build_from_umb(tmp_umb)
        assert type(dtmc) == type(model2)
        assert dtmc.nr_states == model2.nr_states
        assert dtmc.nr_transitions == model2.nr_transitions

    def test_export_and_build_mdp(self, mdp, tmp_umb):
        stormpy.export_to_umb(mdp, tmp_umb)
        model2 = stormpy.build_from_umb(tmp_umb)
        assert type(mdp) == type(model2)
        assert mdp.nr_states == model2.nr_states
        assert mdp.nr_transitions == model2.nr_transitions

    def test_export_with_gzip(self, dtmc, tmp_umb):
        opts = stormpy.UmbExportOptions()
        opts.compression = stormpy.CompressionMode.Gzip
        stormpy.export_to_umb(dtmc, tmp_umb, opts)
        model2 = stormpy.build_from_umb(tmp_umb)
        assert type(dtmc) == type(model2)
        assert dtmc.nr_states == model2.nr_states


class TestUmbRoundTrip:
    def _assert_same_structure(self, model, model2):
        assert model.model_type == model2.model_type
        assert model.nr_states == model2.nr_states
        assert model.nr_transitions == model2.nr_transitions
        assert model.nr_choices == model2.nr_choices

    def test_dtmc_short_round_trip(self, dtmc):
        umb = stormpy.sparse_model_to_umb(dtmc)
        model2 = stormpy.sparse_model_from_umb(umb)
        self._assert_same_structure(dtmc, model2)

    def test_mdp_short_round_trip(self, mdp):
        umb = stormpy.sparse_model_to_umb(mdp)
        model2 = stormpy.sparse_model_from_umb(umb)
        self._assert_same_structure(mdp, model2)

    def test_dtmc_file_round_trip(self, dtmc, tmp_umb):
        umb = stormpy.sparse_model_to_umb(dtmc)
        stormpy.umb_to_archive(umb, tmp_umb)
        assert os.path.isfile(tmp_umb)
        assert os.path.getsize(tmp_umb) > 0
        umb2 = stormpy.import_umb(tmp_umb)
        valid, errors = umb2.validate()
        assert valid, errors
        model2 = stormpy.sparse_model_from_umb(umb2)
        self._assert_same_structure(dtmc, model2)

    def test_mdp_file_round_trip(self, mdp, tmp_umb):
        umb = stormpy.sparse_model_to_umb(mdp)
        stormpy.umb_to_archive(umb, tmp_umb)
        umb2 = stormpy.import_umb(tmp_umb)
        model2 = stormpy.sparse_model_from_umb(umb2)
        self._assert_same_structure(mdp, model2)

    def test_dtmc_gzip_round_trip(self, dtmc, tmp_umb):
        export_opts = stormpy.UmbExportOptions()
        export_opts.compression = stormpy.CompressionMode.Gzip
        umb = stormpy.sparse_model_to_umb(dtmc, export_opts)
        stormpy.umb_to_archive(umb, tmp_umb, export_opts)
        assert os.path.getsize(tmp_umb) > 0
        umb2 = stormpy.import_umb(tmp_umb)
        model2 = stormpy.sparse_model_from_umb(umb2)
        self._assert_same_structure(dtmc, model2)

    def test_dtmc_xz_round_trip(self, dtmc, tmp_umb):
        export_opts = stormpy.UmbExportOptions()
        export_opts.compression = stormpy.CompressionMode.Xz
        umb = stormpy.sparse_model_to_umb(dtmc, export_opts)
        stormpy.umb_to_archive(umb, tmp_umb, export_opts)
        assert os.path.getsize(tmp_umb) > 0
        umb2 = stormpy.import_umb(tmp_umb)
        model2 = stormpy.sparse_model_from_umb(umb2)
        self._assert_same_structure(dtmc, model2)

    def test_import_options_no_state_valuations(self, dtmc, tmp_umb):
        umb = stormpy.sparse_model_to_umb(dtmc)
        stormpy.umb_to_archive(umb, tmp_umb)
        import_opts = stormpy.UmbImportOptions()
        import_opts.build_state_valuations = False
        umb2 = stormpy.import_umb(tmp_umb, import_opts)
        model2 = stormpy.sparse_model_from_umb(umb2, import_opts)
        self._assert_same_structure(dtmc, model2)
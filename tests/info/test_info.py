import stormpy.info


class TestInfo:
    def test_version(self):
        raw = stormpy.developer.info.StormVersion
        # Short version
        assert isinstance(raw.short_version_string(), str)
        assert "." in raw.short_version_string()
        # Long version
        assert isinstance(stormpy.info.storm_long_version(), str)
        assert stormpy.info.storm_long_version().startswith("Version ")
        assert raw.short_version_string() in stormpy.info.storm_long_version()
        # storm_version()
        assert stormpy.info.storm_version() in raw.short_version_string()
        assert "." in stormpy.info.storm_version()
        # Development version
        assert stormpy.info.storm_development_version() == raw.version_dev
        assert (raw.version_dev and raw.short_version_string().endswith(" (dev)")) or not raw.version_dev

    def test_build_info(self):
        assert isinstance(stormpy.info.storm_build_info(), str)
        assert "Compiled" in stormpy.info.storm_build_info()
        assert stormpy.info.storm_build_type() in ("Debug", "Release")

    def test_origin_info(self):
        assert isinstance(stormpy.info.storm_from_system(), bool)
        assert stormpy.info.storm_from_system() == (stormpy.info.storm_directory() is not None)
        repo, tag, hsh = stormpy.info.storm_origin_info()
        assert repo is None or isinstance(repo, str)
        assert tag is None or isinstance(tag, str)
        if stormpy.info.storm_from_system():
            assert repo is None and tag is None
        else:
            assert isinstance(repo, str) and isinstance(tag, str)
        assert isinstance(hsh, str)
        assert hsh == stormpy.developer.info.StormVersion.git_revision_hash

    def test_number_representations(self):
        assert isinstance(stormpy.info.storm_exact_use_cln(), bool)
        assert isinstance(stormpy.info.storm_ratfunc_use_cln(), bool)

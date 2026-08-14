import stormpy.info


class TestInfo:
    def test_version(self):
        # Short version
        assert isinstance(stormpy.info.Version.short, str)
        assert "." in stormpy.info.Version.short
        # Long version
        assert isinstance(stormpy.info.Version.long, str)
        assert stormpy.info.Version.long.startswith("Version ")
        assert stormpy.info.Version.short in stormpy.info.Version.long
        # storm_version()
        assert stormpy.info.storm_version() in stormpy.info.Version.short
        assert "." in stormpy.info.storm_version()
        # Development version
        assert stormpy.info.storm_development_version() == stormpy.info.Version.development
        assert (stormpy.info.Version.development and stormpy.info.Version.short.endswith(" (dev)")) or not stormpy.info.Version.development

    def test_build_info(self):
        assert isinstance(stormpy.info.Version.build_info, str)
        assert "Compiled" in stormpy.info.Version.build_info
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
        assert hsh == stormpy.info.Version.git_hash

    def test_number_repressentations(self):
        assert isinstance(stormpy.info.storm_exact_use_cln(), bool)
        assert isinstance(stormpy.info.storm_ratfunc_use_cln(), bool)

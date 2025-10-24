import stormpy.info


class TestInfo:
    def test_version(self):
        assert isinstance(stormpy.info.Version.short, str) and "." in stormpy.info.Version.short
        assert isinstance(stormpy.info.Version.long, str) and "Version" in stormpy.info.Version.long
        assert isinstance(stormpy.info.Version.build_info, str) and "Compiled" in stormpy.info.Version.build_info

    def test_version_equal(self):
        assert stormpy.info.storm_version() in stormpy.info.Version.short
        assert (stormpy.info.Version.development and stormpy.info.Version.short.endswith(" (dev)")) or not stormpy.info.Version.development

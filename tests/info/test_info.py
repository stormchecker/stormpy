import stormpy.info


class TestInfo:
    def test_version(self):
        assert isinstance(stormpy.info.Version.short, str) and "." in stormpy.info.Version.short
        assert isinstance(stormpy.info.Version.long, str) and "Version" in stormpy.info.Version.long
        assert isinstance(stormpy.info.Version.build_info, str) and "Compiled" in stormpy.info.Version.build_info

    def test_version_equal(self):
        assert stormpy.info.storm_version() in stormpy.info.Version.short
        assert (stormpy.info.Version.development and stormpy.info.Version.short.endswith(" (dev)")) or not stormpy.info.Version.development

    def test_origin_info(self):
        repo, tag, h = stormpy.info.storm_origin_info()
        assert repo is None or isinstance(repo, str)
        assert tag is None or isinstance(tag, str)
        assert isinstance(h, str)

"""GSPN-specific tests for the public GSPN API (stormpy.gspn).

Generic checks of all public APIs (names exist, documentation) are in tests/test_public_apis.py.
"""

from configurations import gspn


@gspn
class TestPublicGspnApi:
    def test_internal_imports_not_public(self):
        import stormpy.gspn

        for name in ["JaniModel", "PathLike", "Property"]:
            assert name not in stormpy.gspn.__all__

    def test_removed_names(self):
        import stormpy.gspn

        for name in ["GSPNParser", "GSPNToJaniBuilder", "GSPNBuilder"]:
            assert not hasattr(stormpy.gspn, name)
            assert not hasattr(stormpy.gspn.developer, name)
        for name in ["export_gspn_pnpro_file", "export_gspn_pnml_file"]:
            assert not hasattr(stormpy.gspn.GSPN, name)

    def test_developer_bindings(self):
        import stormpy.gspn

        for name in ["GspnParser", "JaniGSPNBuilder", "export_gspn_to_pnpro", "export_gspn_to_pnml"]:
            assert hasattr(stormpy.gspn.developer, name)
            assert name not in stormpy.gspn.__all__
        assert stormpy.gspn.GSPN is stormpy.gspn.developer.GSPN

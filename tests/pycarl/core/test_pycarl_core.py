from configurations import pycarl_cln


class TestPycarlCore:
    def pickle(self, mod):
        import inspect
        import enum
        import builtins

        for name, obj in inspect.getmembers(mod):
            if inspect.isclass(obj):
                assert (
                    issubclass(obj, enum.Enum)
                    or issubclass(obj, builtins.Exception)
                    or (hasattr(obj, "__getstate__") and inspect.isroutine(getattr(obj, "__getstate__")))
                )
                assert (
                    issubclass(obj, enum.Enum)
                    or issubclass(obj, builtins.Exception)
                    or (hasattr(obj, "__setstate__") and inspect.isroutine(getattr(obj, "__setstate__")))
                )

    def test_init(self):
        from stormpy import pycarl

    def test_import(self):
        from stormpy import pycarl
        from stormpy.pycarl import formula

    def test_config(self):
        from stormpy import pycarl

        assert pycarl.has_parser() == True or pycarl.has_parser() == False
        assert pycarl.has_cln() == True or pycarl.has_cln() == False

    def test_pickle(self):
        from stormpy import pycarl
        from stormpy.pycarl import formula

        for mod in [pycarl, pycarl.formula]:
            self.pickle(mod)

    def test_pickle_gmp(self):
        from stormpy import pycarl
        from stormpy.pycarl import gmp

        self.pickle(pycarl.gmp)

    @pycarl_cln
    def test_pickle_cln(self):
        from stormpy import pycarl
        from stormpy.pycarl import cln

        self.pickle(pycarl.cln)

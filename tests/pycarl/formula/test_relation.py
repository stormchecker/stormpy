from stormpy import pycarl
from stormpy.pycarl.formula import Relation


class TestRelation:
    def test_to_string(self):
        r = Relation.LESS
        assert str(r) == "<"
        assert str(Relation.GEQ) == ">="

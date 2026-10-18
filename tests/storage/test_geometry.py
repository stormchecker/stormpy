import pytest
import stormpy
from stormpy.developer.storage import Halfspace, Polytope


@pytest.mark.parametrize("value_type", [float, stormpy.Rational])
def test_downward_closure(value_type):
    one, two = value_type(1), value_type(2)
    polytope = Polytope[value_type].create_downward_closure([[one, two], [two, one]])
    assert not polytope.is_empty()
    assert not polytope.is_universal()
    assert polytope.contains([one, one])
    assert not polytope.contains([two, two])
    # Halfspaces bounding the polytope from above
    assert all(halfspace.contains([one, one]) for halfspace in polytope.halfspaces)
    assert any(not halfspace.contains([two, two]) for halfspace in polytope.halfspaces)

    point, exists = polytope.optimize([one, one])
    assert exists
    assert sum(point) == 3
    # Downward closures are unbounded in negative directions
    _, exists = polytope.optimize([-one, -one])
    assert not exists

    smaller = Polytope[value_type].create_downward_closure([[one, one]])
    assert polytope.contains(smaller)
    assert not smaller.contains(polytope)


def test_halfspace():
    halfspace = Halfspace[float]([1.0, 1.0], 2.0)
    assert halfspace.normal_vector == [1.0, 1.0]
    assert halfspace.offset == 2.0
    assert halfspace.contains([1.0, 1.0])
    assert not halfspace.contains([2.0, 1.0])
    assert halfspace.distance([1.0, 1.0]) == 0
    assert halfspace.distance([2.0, 1.0]) == 1

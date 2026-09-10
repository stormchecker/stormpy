from types import SimpleNamespace

import pytest

from stormpy._template import TemplateClass, deduce_from_first_argument


class BaseImplementation:
    def __init__(self, source=None):
        self.source = source


class DerivedImplementation(BaseImplementation):
    pass


def make_family(*, deduce=None) -> TemplateClass:
    module = SimpleNamespace(_template_instantiations={"Example": {("base",): BaseImplementation}})
    return TemplateClass("test.Example", module, parameters=["kind"], deduce=deduce)


def test_deduction_selects_exact_registered_subclass():
    family = make_family(deduce=deduce_from_first_argument())
    family.register("derived", DerivedImplementation)
    source = DerivedImplementation()

    result = family(source)

    assert type(result) is DerivedImplementation
    assert result.source is source


def test_deduction_rejects_unregistered_subclass():
    class UnregisteredImplementation(BaseImplementation):
        pass

    family = make_family(deduce=deduce_from_first_argument())
    source = UnregisteredImplementation()

    with pytest.raises(TypeError, match="Cannot infer Example template parameters"):
        family(source)
    assert not family.is_instantiation(source)


def test_cannot_register_implementation_for_multiple_parameters():
    family = make_family()

    with pytest.raises(ValueError, match="already registered for .*base"):
        family.register("duplicate", BaseImplementation)

    assert ("duplicate",) not in family.instantiations
    assert family.parameters_of(BaseImplementation()) == ("base",)

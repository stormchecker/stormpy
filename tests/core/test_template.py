from types import SimpleNamespace

import pytest

from stormpy._template import TemplateClass, deduce_default, deduce_from_first_argument, deduce_from_object


class BaseImplementation:
    def __init__(self, source=None):
        self.source = source


class DerivedImplementation(BaseImplementation):
    pass


def make_family(*, deduce=None) -> TemplateClass:
    module = SimpleNamespace(_template_instantiations={"Example": {("base",): BaseImplementation}})
    return TemplateClass("test.Example", module, parameters=["kind"], deduce=deduce)


def call_guide(guide, *args, **kwargs):
    return guide(None, args, kwargs)


def test_builtin_deduction_sources_are_exposed_as_metadata():
    from stormpy._template import DeductionSource

    module = SimpleNamespace(_template_instantiations={"Example": {("base",): BaseImplementation}})
    from_object = TemplateClass(
        "test.Example",
        module,
        parameters=["kind"],
        deduce=deduce_from_object(lambda value: value, keyword=("model", "source"), position=1),
    )
    assert from_object.metadata.deduction_source == DeductionSource(1, ("model", "source"))
    from_first = TemplateClass("test.Example", module, parameters=["kind"], deduce=deduce_from_first_argument(keyword="source"))
    assert from_first.metadata.deduction_source == DeductionSource(0, ("source",))
    assert make_family(deduce=deduce_default("base")).metadata.deduction_source is None


def test_deduction_selects_exact_registered_subclass():
    family = make_family(deduce=deduce_from_first_argument())
    family.register("derived", DerivedImplementation)
    source = DerivedImplementation()

    result = family(source)

    assert type(result) is DerivedImplementation
    assert result.source is source


def test_default_deduction_selects_configured_instantiation():
    family = make_family(deduce=deduce_default("base"))

    result = family()

    assert type(result) is BaseImplementation


def test_default_deduction_rejects_unregistered_instantiation():
    family = make_family(deduce=deduce_default("missing"))

    with pytest.raises(TypeError, match=r"Example has no instantiation for \('missing',\)"):
        family()


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


def test_object_deduction_transforms_argument():
    family = make_family(deduce=deduce_from_object(lambda obj: obj.kind, keyword="source"))
    family.register("derived", DerivedImplementation)
    source = SimpleNamespace(kind="derived")

    for result in (family(source), family(source=source)):
        assert type(result) is DerivedImplementation
        assert result.source is source


def test_object_deduction_argument_selection():
    guide = deduce_from_object(lambda obj: float if obj is None else obj.kind, keyword="model")
    source = SimpleNamespace(kind=int)
    alternate = SimpleNamespace(kind=str)

    assert call_guide(guide, source, model=alternate) is int
    assert call_guide(guide, model=alternate) is str
    with pytest.raises(TypeError, match="missing argument.*model"):
        call_guide(guide)
    assert call_guide(guide, model=None) is float


def test_object_deduction_keyword_aliases():
    guide = deduce_from_object(type, keyword=("components", "other_model"))

    assert call_guide(guide, other_model=1) is int
    assert call_guide(guide, components=1.0, other_model=1) is float
    assert call_guide(guide, components=None, other_model=1) is type(None)
    assert call_guide(guide, 1, components=1.0) is int


def test_object_deduction_second_argument():
    guide = deduce_from_object(type, keyword="model", position=1)

    assert call_guide(guide, 2, 1.0, model=1) is float
    assert call_guide(guide, 2, model=1.0) is float
    assert call_guide(guide, model=1.0) is float
    with pytest.raises(TypeError, match="missing argument.*position 1.*model"):
        call_guide(guide, 2)


def test_object_deduction_rejects_misspelled_required_argument():
    family = make_family(deduce=deduce_from_object(lambda obj: obj.kind, keyword="source"))

    with pytest.raises(TypeError, match="Cannot deduce template parameters: missing argument.*source"):
        family(soruce=SimpleNamespace(kind="base"))


def test_object_deduction_explicit_default_only_applies_to_missing_argument():
    guide = deduce_from_object(type, keyword="source", default=(float,))

    assert call_guide(guide) == (float,)
    assert call_guide(guide, source=1) is int
    assert call_guide(guide, None) is type(None)
    assert call_guide(guide, source=None) is type(None)

import inspect
from types import SimpleNamespace

import pytest

from stormpy._template import _TemplateClass, _TemplateFunction, _deduce_default, _template_function, _deduce_from_first_argument, _deduce_from_object


# Helper functions
class BaseImplementation:
    def __init__(self, source=None):
        self.source = source


class DerivedImplementation(BaseImplementation):
    pass


def _double(value):
    return 2 * value


def _triple(value):
    return 3 * value


def make_family(*, deduce=None) -> _TemplateClass:
    module = SimpleNamespace(_template_instantiations={"Example": {("base",): BaseImplementation}})
    return _TemplateClass("test.Example", module, parameters=["kind"], deduce=deduce)


def make_function_family() -> _TemplateFunction:
    module = SimpleNamespace(_template_instantiations={"scale": {("double",): _double, ("triple",): _triple}})
    return _TemplateFunction("test.scale", module, parameters=["kind"], deduce=_deduce_default("double"))


def call_guide(guide, *args, **kwargs):
    return guide(None, args, kwargs)


class TestTemplates:
    def test_cannot_register_implementation_for_multiple_parameters(self):
        family = make_family()

        with pytest.raises(ValueError, match="already registered for .*base"):
            family.register("duplicate", BaseImplementation)

        assert ("duplicate",) not in family.instantiations
        assert family.parameters_of(BaseImplementation()) == ("base",)

    def test_template_function_subscription(self):
        family = make_function_family()
        assert family["triple"] is _triple
        assert family["triple"](2) == 6

    def test_template_function_default_deduction(self):
        family = make_function_family()
        assert family(2) == 4

    def test_template_function_rejects_non_callable(self):
        family = make_function_family()
        with pytest.raises(TypeError):
            family.register("other", 42)

    def test_template_function_publish_as(self):
        published = make_function_family().publish_as("public.scale")
        assert isinstance(published, _TemplateFunction)
        assert repr(published) == "<template function public.scale>"
        assert published["triple"] is _triple


class TestDeduction:
    def test_deduction_selects_exact_registered_subclass(self):
        family = make_family(deduce=_deduce_from_first_argument())
        family.register("derived", DerivedImplementation)
        source = DerivedImplementation()

        result = family(source)

        assert type(result) is DerivedImplementation
        assert result.source is source

    def test_default_deduction_selects_configured_instantiation(self):
        family = make_family(deduce=_deduce_default("base"))

        result = family()

        assert type(result) is BaseImplementation

    def test_default_deduction_rejects_unregistered_instantiation(self):
        family = make_family(deduce=_deduce_default("missing"))

        with pytest.raises(TypeError, match=r"Example has no instantiation for \('missing',\)"):
            family()

    def test_deduction_rejects_unregistered_subclass(self):
        class UnregisteredImplementation(BaseImplementation):
            pass

        family = make_family(deduce=_deduce_from_first_argument())
        source = UnregisteredImplementation()

        with pytest.raises(TypeError, match="Cannot infer Example template parameters"):
            family(source)
        assert not family.is_instantiation(source)

    def test_object_deduction_transforms_argument(self):
        family = make_family(deduce=_deduce_from_object(lambda obj: obj.kind, keyword="source"))
        family.register("derived", DerivedImplementation)
        source = SimpleNamespace(kind="derived")

        for result in (family(source), family(source=source)):
            assert type(result) is DerivedImplementation
            assert result.source is source

    def test_object_deduction_argument_selection(self):
        guide = _deduce_from_object(lambda obj: float if obj is None else obj.kind, keyword="model")
        source = SimpleNamespace(kind=int)
        alternate = SimpleNamespace(kind=str)

        assert call_guide(guide, source, model=alternate) is int
        assert call_guide(guide, model=alternate) is str
        with pytest.raises(TypeError, match="missing argument.*model"):
            call_guide(guide)
        assert call_guide(guide, model=None) is float

    def test_object_deduction_keyword_aliases(self):
        guide = _deduce_from_object(type, keyword=("components", "other_model"))

        assert call_guide(guide, other_model=1) is int
        assert call_guide(guide, components=1.0, other_model=1) is float
        assert call_guide(guide, components=None, other_model=1) is type(None)
        assert call_guide(guide, 1, components=1.0) is int

    def test_object_deduction_second_argument(self):
        guide = _deduce_from_object(type, keyword="model", position=1)

        assert call_guide(guide, 2, 1.0, model=1) is float
        assert call_guide(guide, 2, model=1.0) is float
        assert call_guide(guide, model=1.0) is float
        with pytest.raises(TypeError, match="missing argument.*position 1.*model"):
            call_guide(guide, 2)

    def test_object_deduction_rejects_misspelled_required_argument(self):
        family = make_family(deduce=_deduce_from_object(lambda obj: obj.kind, keyword="source"))

        with pytest.raises(TypeError, match="Cannot deduce template parameters: missing argument.*source"):
            family(soruce=SimpleNamespace(kind="base"))

    def test_object_deduction_explicit_default_only_applies_to_missing_argument(self):
        guide = _deduce_from_object(type, keyword="source", default=(float,))

        assert call_guide(guide) == (float,)
        assert call_guide(guide, source=1) is int
        assert call_guide(guide, None) is type(None)
        assert call_guide(guide, source=None) is type(None)


def test_missing_instantiation_lists_supported_instantiations():
    family = make_family()
    family.register("derived", DerivedImplementation)

    with pytest.raises(TypeError, match=r"Supported are: 'base', 'derived'"):
        family["missing"]


def test_python_template_function():
    @_template_function("test.scale_by", parameters=["factor"], instantiations=(2, 3), deduce=_deduce_default(2))
    def scale_by(factor, value, *, offset=0):
        """Scale the value."""
        return factor * value + offset

    assert isinstance(scale_by, _TemplateFunction)
    assert scale_by[3](2, offset=1) == 7
    assert scale_by(2) == 4
    assert str(inspect.signature(scale_by)) == "(value, *, offset=0)"
    assert inspect.signature(scale_by) == inspect.signature(scale_by[3])
    assert list(inspect.signature(scale_by[3]).parameters) == ["value", "offset"]
    assert scale_by[3].__name__ == "scale_by"
    assert inspect.getdoc(scale_by[3]) == "Scale the value."
    with pytest.raises(TypeError, match="Supported are: 2, 3"):
        scale_by[4]

    published = scale_by.publish_as("public.scale_by")
    assert inspect.signature(published) == inspect.signature(scale_by)
    assert published(2, offset=1) == 5
    assert published[3](2, offset=1) == 7


def test_builtin_deduction_sources_are_exposed_as_metadata():
    from stormpy._template import DeductionSource

    module = SimpleNamespace(_template_instantiations={"Example": {("base",): BaseImplementation}})
    from_object = _TemplateClass(
        "test.Example",
        module,
        parameters=["kind"],
        deduce=_deduce_from_object(lambda value: value, keyword=("model", "source"), position=1),
    )
    assert from_object.metadata.deduction_source == DeductionSource(1, ("model", "source"))
    from_first = _TemplateClass("test.Example", module, parameters=["kind"], deduce=_deduce_from_first_argument(keyword="source"))
    assert from_first.metadata.deduction_source == DeductionSource(0, ("source",))
    assert make_family(deduce=_deduce_default("base")).metadata.deduction_source is None

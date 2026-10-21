"""Public logic package and its shared native developer bindings."""

import inspect

import stormpy


def test_public_exports_are_explicit():
    exported = {name for name in vars(stormpy.logic) if not name.startswith("_")}
    assert exported == set(stormpy.logic.__all__)


def test_public_classes_share_native_types():
    for name in stormpy.logic.__all__:
        public = getattr(stormpy.logic, name)
        if inspect.isfunction(public):
            continue
        assert inspect.isclass(public)
        # Property and OptimizationDirection are bound with the core library
        assert public is getattr(stormpy.developer.logic, name, None) or public is getattr(stormpy.developer, name)


def test_native_module_location():
    native = stormpy.developer.logic._logic
    assert native.__name__ == "stormpy.developer.logic._logic"
    assert stormpy.logic.Formula.__module__ == native.__name__


def test_storm_names():
    raw = stormpy.developer.logic
    for name in ("ProbabilityOperator", "RewardOperator", "TimeOperator", "LongRunAvarageOperator", "BooleanBinaryStateFormula"):
        assert not hasattr(raw, name)
    for name in ("TimeOperatorFormula", "LongRunAverageOperatorFormula", "BinaryBooleanStateFormula"):
        assert hasattr(raw, name)
    assert not hasattr(raw.RewardOperatorFormula, "has_reward_name")
    assert hasattr(raw.BoundedUntilFormula, "is_multi_dimensional")
    assert str(raw.BooleanLiteralFormula(value=True)) == "true"

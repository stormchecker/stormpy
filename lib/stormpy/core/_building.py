"""Building of models from symbolic descriptions and explicit input formats."""

from __future__ import annotations

from collections.abc import Iterable

from stormpy import developer
from stormpy.developer import storage
from stormpy.core._common import PathLike, _formulas, _path
from stormpy.core._modelchecking import Engine
from stormpy import Interval, Rational, RationalFunction, RationalInterval
from stormpy._template import _deduce_default, _template_function
from stormpy.developer import (
    DirectEncodingParserOptions,
    Environment,
    ExplicitModelParserOptions,
    Property,
    SymbolicModelDescription,
)
from stormpy.exceptions import StormError


class BuilderOptions(developer.BuilderOptions):
    """
    Options for building a model from a symbolic description.

    The options can be created preserving the given properties via e.g. ``BuilderOptions(properties)``,
    or they can be created for the full model via ``BuilderOptions(build_full=True)``.
    Single flags can be set afterwards, e.g. ``options.set_build_all_labels()`` or ``options.set_build_state_valuations()``.

    :param properties: (optional) Property or properties (or formulas) whose labels and reward models are preserved.
    :param model_description: (optional) Symbolic model description used to resolve the properties.
    :param build_full: Whether the full model is built, i.e., all reward models, all labels, state valuations, choice labels
        and choice origins (in addition to the labels and reward models required by the properties).
    """

    def __init__(
        self,
        properties: Property | Iterable[Property] | None = None,
        model_description: SymbolicModelDescription | None = None,
        *,
        build_full: bool = False,
    ) -> None:
        if isinstance(properties, bool):
            raise TypeError("The flag build_full of BuilderOptions is keyword-only, use BuilderOptions(build_full=True).")
        if properties is None:
            super().__init__()
        elif model_description is None:
            super().__init__(_formulas(properties))
        else:
            super().__init__(_formulas(properties), model_description)
        if build_full:
            self.set_build_all_reward_models()
            self.set_build_all_labels()
            self.set_build_state_valuations()
            self.set_build_choice_labels()
            self.set_build_choice_origins()


def _check_constants(model) -> None:
    """Raise an error if the symbolic model has undefined constants which would change the graph structure."""
    if isinstance(model, SymbolicModelDescription):
        model = model.as_prism_program() if model.is_prism_program() else model.as_jani_model()
    if not model.undefined_constants_are_graph_preserving:
        raise StormError("Model still contains undefined constants which influence the graph structure. Use instantiate_constants() first.")


_VALUE_TYPES = (float, Rational, RationalFunction, Interval, RationalInterval)


@_template_function("stormpy.build_model", parameters=("ValueType",), instantiations=_VALUE_TYPES, deduce=_deduce_default(float))
def build_model(
    value_type: type,
    model: storage.PrismProgram | storage.JaniModel | SymbolicModelDescription,
    properties: Property | Iterable[Property] | None = None,
    *,
    options: BuilderOptions | None = None,
    engine: Engine = Engine.SPARSE,
    environment: Environment | None = None,
):
    """
    Build a model from a symbolic model description.

    The engine determines the representation of the model and should match the engine later used for :func:`model_checking`:
    ``Engine.SPARSE`` (default) builds a sparse (explicit) model, ``Engine.DD`` and ``Engine.HYBRID`` build a symbolic model
    (using decision diagrams, see also :func:`build_symbolic_model`).

    The value type of the model is selected via subscript, e.g. ``build_model[stormpy.Rational](program)``:
    float (default), Rational (exact), RationalFunction (parametric), Interval or RationalInterval (exact interval).
    Symbolic models do not support the interval value types.

    :param model: Symbolic model (Prism program, Jani model or symbolic model description).
    :param properties: (optional) Property or properties which should be checkable on the built model.
        Only the labels and reward models required by the properties are built.
        If None or empty (and no options are given), all labels and reward models are built.
    :param options: (optional) Builder options for full control of the building process. Cannot be combined with properties.
        Only supported for ``Engine.SPARSE``.
    :param engine: Engine for which the model is built.
    :param environment: (optional) Environment configuring the decision diagram libraries. Only supported for ``Engine.DD`` and ``Engine.HYBRID``.
    :return: The model in sparse representation (e.g. a sparse DTMC) or in symbolic representation (e.g. a symbolic DTMC).
    :raises TypeError: If the value type is not supported.
    """
    if engine != Engine.SPARSE:
        if options is not None:
            raise StormError("Builder options are only supported for sparse models (Engine.SPARSE).")
        return build_symbolic_model[value_type](model, properties, environment=environment)
    if environment is not None:
        raise StormError("An environment is only used for building symbolic models (Engine.DD or Engine.HYBRID).")
    build = developer.build_sparse_model[value_type]
    if value_type is not RationalFunction:
        _check_constants(model)
    if options is not None:
        if properties:
            raise StormError("Either properties or builder options can be given, but not both.")
        return build(model, options)
    if properties:
        # Storm derives the builder options from the formulas and the model (e.g., choice labels for POMDPs)
        return build(model, _formulas(properties))
    # Only all labels and reward models are built, but no additional information such as state valuations
    return build(model, developer.BuilderOptions(build_all_reward_models=True, build_all_labels=True))


@_template_function(
    "stormpy.build_symbolic_model", parameters=("ValueType",), instantiations=(float, Rational, RationalFunction), deduce=_deduce_default(float)
)
def build_symbolic_model(
    value_type: type,
    model: storage.PrismProgram | storage.JaniModel | SymbolicModelDescription,
    properties: Property | Iterable[Property] | None = None,
    *,
    environment: Environment | None = None,
):
    """
    Build a model in symbolic representation (using decision diagrams) from a symbolic model.

    The value type of the model is selected via subscript, e.g. ``build_symbolic_model[stormpy.Rational](program)``:
    float (default), Rational (exact) or RationalFunction (parametric). Interval value types are not supported.

    :param model: Symbolic model (Prism program, Jani model or symbolic model description).
    :param properties: (optional) Property or properties which should be checkable on the built model. If None, the full model is built.
    :param environment: (optional) Environment configuring the decision diagram libraries.
    :return: The model in symbolic representation, e.g. a symbolic DTMC.
    :raises TypeError: If the value type is not supported.
    """
    build = developer.build_symbolic_model[value_type]
    if value_type is not RationalFunction:
        _check_constants(model)
    formulas = _formulas(properties)
    environment = environment if environment is not None else Environment()
    return build(environment, model, formulas, build_full_model=not formulas)


@_template_function("stormpy.build_model_from_drn", parameters=("ValueType",), instantiations=_VALUE_TYPES, deduce=_deduce_default(float))
def build_model_from_drn(value_type: type, path: PathLike, *, options: DirectEncodingParserOptions | None = None):
    """
    Build a model in sparse representation from a file in the explicit DRN format.

    The value type of the model is selected via subscript, e.g. ``build_model_from_drn[stormpy.Rational](path)``:
    float (default), Rational (exact), RationalFunction (parametric), Interval or RationalInterval (exact interval).

    :param path: Path to the DRN file (string or path-like object).
    :param options: (optional) Options for the DRN parser.
    :return: The model in sparse representation.
    :raises TypeError: If the value type is not supported.
    """
    build = developer.build_explicit_drn_model[value_type]
    return build(_path(path), options if options is not None else DirectEncodingParserOptions())


def build_model_from_explicit(
    transitions: PathLike,
    labeling: PathLike,
    *,
    state_rewards: PathLike | None = None,
    transition_rewards: PathLike | None = None,
    choice_labeling: PathLike | None = None,
    options: ExplicitModelParserOptions | None = None,
):
    """
    Build a model in sparse representation from files in the explicit format (.tra, .lab, ...).
    All paths can be given as strings or path-like objects.

    :param transitions: Path to the file containing the transitions (.tra).
    :param labeling: Path to the file containing the state labeling (.lab).
    :param state_rewards: (optional) Path to the file containing state rewards.
    :param transition_rewards: (optional) Path to the file containing transition rewards.
    :param choice_labeling: (optional) Path to the file containing the choice labeling.
    :param options: (optional) Options for the explicit parser.
    :return: The model in sparse representation.
    """
    model = developer.build_explicit_model(
        _path(transitions),
        _path(labeling),
        _path(state_rewards) if state_rewards is not None else None,
        _path(transition_rewards) if transition_rewards is not None else None,
        _path(choice_labeling) if choice_labeling is not None else None,
        options if options is not None else ExplicitModelParserOptions(),
    )
    return model


def build_model_from_umb(path: PathLike, *, options: storage.UmbImportOptions | None = None):
    """
    Build a model in sparse representation from a UMB archive.

    :param path: Path to the UMB archive (string or path-like object).
    :param options: (optional) Options controlling the value type and which parts of the model are built.
    :return: The model in sparse representation.
    """
    options = options if options is not None else storage.UmbImportOptions()
    umb = storage.import_umb(_path(path), options)
    return storage.sparse_model_from_umb(umb, options)

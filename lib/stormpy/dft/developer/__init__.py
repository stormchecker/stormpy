"""Raw pybind11 bindings for storm-dft.

Every name here mirrors the corresponding ``storm::dft::`` C++ method or
class 1:1 (same name transliterated to snake_case, same arguments). This
module is not meant for everyday use: :mod:`stormpy.dft` builds a smaller,
curated, documented public API on top of it. Reach for
:mod:`stormpy.dft.developer` only when the public API does not expose
something you need, e.g. low-level access to ``ValueType``-specific
overloads or template-family metadata.
"""

from stormpy.info import _config

if not _config.STORM_WITH_DFT:
    raise ImportError("No support for DFTs was built in Storm.")

from . import _dft

# Mirror _dft's entire namespace directly onto this package -- including the
# underscore-prefixed concrete template specializations (e.g. _DFT_Double) and
# the _template_instantiations registry -- so callers never need to know the
# compiled extension is nested one level deeper as `_dft`. (`developer._dft` is
# still reachable for anyone who wants the raw module object itself, e.g. for
# the TemplateClass construction below.) This does not change a bound class's
# own __module__ (set by pybind11 to "stormpy.dft.developer._dft" at binding
# time), so TemplateClass.metadata.instantiations[...].native_name still
# correctly reports where a specialization is actually defined.
for _name, _value in vars(_dft).items():
    if not _name.startswith("__"):
        globals()[_name] = _value
del _name, _value

from stormpy._template import TemplateClass, deduce_from_first_argument, deduce_from_object

# Unify the per-ValueType compiled specializations of each C++ template family
# behind one subscriptable, deducible Python name. This is required just to
# obtain a usable Python name for a C++ template -- it mirrors C++ template
# argument deduction, and is not a curation decision (see stormpy._template).

DFT = TemplateClass(
    "stormpy.dft.developer.DFT",
    _dft,
    parameters=("ValueType",),
    deduce=deduce_from_first_argument(keyword="dft"),
)

DFTElement = TemplateClass(
    "stormpy.dft.developer.DFTElement",
    _dft,
    parameters=("ValueType",),
)

DFTBE = TemplateClass(
    "stormpy.dft.developer.DFTBE",
    _dft,
    parameters=("ValueType",),
)

DFTDependency = TemplateClass(
    "stormpy.dft.developer.DFTDependency",
    _dft,
    parameters=("ValueType",),
)

DFTState = TemplateClass(
    "stormpy.dft.developer.DFTState",
    _dft,
    parameters=("ValueType",),
)

DFTTraceSimulator = TemplateClass(
    "stormpy.dft.developer.DFTTraceSimulator",
    _dft,
    parameters=("ValueType",),
    deduce=deduce_from_first_argument(DFT, keyword="dft"),
)

ExplicitDFTModelBuilder = TemplateClass(
    "stormpy.dft.developer.ExplicitDFTModelBuilder",
    _dft,
    parameters=("ValueType",),
    deduce=deduce_from_object(DFT.parameters_of, position=1, keyword="dft"),
)

_deduce_dft_parameters = deduce_from_first_argument(DFT, keyword="dft")


def _deduce_dft_instantiator(family, args, kwargs):
    return (*_deduce_dft_parameters(family, args, kwargs), float)


DftInstantiator = TemplateClass(
    "stormpy.dft.developer.DftInstantiator",
    _dft,
    parameters=("SourceValueType", "TargetValueType"),
    deduce=_deduce_dft_instantiator,
)

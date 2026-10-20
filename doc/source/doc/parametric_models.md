---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Parametric Models

Parametric models contain parameters in their transition probabilities, rates, or rewards.
Stormpy can instantiate these parameters, compute property values as rational functions
of the parameters, verify properties throughout a parameter region, or search for
satisfying parameter values.

## Building parametric models

[01-parametric-models.py](https://github.com/stormchecker/stormpy/blob/master/examples/parametric_models/01-parametric-models.py)

Parameters are undefined constants in a PRISM program. Constants that determine the
model's structure, such as variable bounds, must be defined before building.
We use the parametric die model, whose transition probabilities depend on `p` and `q`.
Selecting `RationalFunction` in `build_model` builds a parametric DTMC:

```{code-cell} python3
import math

import stormpy
import stormpy.pars
import stormpy.examples.files

program = stormpy.parse_prism_program(stormpy.examples.files.prism_pdtmc_die)
property = stormpy.parse_property("P<=0.5 [F s=7 & d=2]", program)
model = stormpy.build_model[stormpy.RationalFunction](program, property)
parameters = model.collect_all_parameters()
for parameter in parameters:
    print(parameter.name)
```

The property asks whether the probability of eventually rolling a two is at most `0.5`.
`collect_all_parameters()` returns the parameters occurring in the model.

[03-parametric-models.py](https://github.com/stormchecker/stormpy/blob/master/examples/parametric_models/03-parametric-models.py)
shows three ways to inspect the model's transitions and count those with probability one.

## Instantiating parametric models

Use `ModelInstantiator` to replace the parameters with concrete values and obtain a
model that can be checked numerically. Here, we set both parameters to `2/5`.
To compute the resulting probability, clone the property and remove the bound from its formula:

```{code-cell} python3
instantiator = stormpy.pars.ModelInstantiator(model)
point = {parameter: stormpy.RationalFunctionCoefficient("2/5") for parameter in parameters}
instantiated_model = instantiator.instantiate(point)

probability_property = property.clone()
probability_property.get_raw_formula().remove_bound()
result = stormpy.model_checking(instantiated_model, probability_property)
probability = result[instantiated_model.initial_states[0]].value
print("Probability of rolling a two:", probability)
assert math.isclose(probability, 4 / 35, rel_tol=1e-6)
```

Use `ModelInstantiator[stormpy.models.ModelType.DTMC, stormpy.Rational](model)`
to instantiate with exact rational values. The resulting model can be checked with
`stormpy.model_checking` in the same way.

## Model checking parametric models

[02-parametric-models.py](https://github.com/stormchecker/stormpy/blob/master/examples/parametric_models/02-parametric-models.py)

Model checking a parametric model directly computes a rational function of the
parameters, rather than a probability for one valuation:

```{code-cell} python3
result = stormpy.model_checking(model, probability_property)
probability_function = result[model.initial_states[0]]
print("Probability as a function of the parameters:", probability_function)
```

The rational functions can grow rapidly with the number of states and parameters.

## Regions

A parameter region assigns an inclusive lower and upper bound to each parameter.
For example, let both `p` and `q` range from `0.2` to `0.8`:

```{code-cell} python3
region = stormpy.pars.parse_region("0.2<=p<=0.8,0.2<=q<=0.8", parameters)
```

Alternatively, construct a region from a dictionary of bounds. We will also use this
smaller region, where both parameters range from `0.2` to `0.6`:

```{code-cell} python3
lower = stormpy.RationalFunctionCoefficient("1/5")
upper = stormpy.RationalFunctionCoefficient("3/5")
smaller_region = stormpy.pars.create_region({parameter: (lower, upper) for parameter in parameters})
```

### Region requirements

A region is:

- **Well-defined** if, for every valuation and each state and enabled action, the
  instantiated outgoing transition values lie in `[0, 1]` and sum to `1`.
- **Graph-preserving** if it is well-defined and every valuation preserves the
  parametric model's existing transition graph.

For example, outgoing probabilities `p` and `1-p` form a valid distribution for
`p` in `[0, 1]`, but one transition disappears at either endpoint. The region
`0.2 <= p <= 0.8` preserves both transitions.

`ConstraintCollector` exposes the constraints for well-definedness and graph preservation:

```{code-cell} python3
collector = stormpy.pars.ConstraintCollector(model)
print("Well-definedness constraints:")
for constraint in collector.get_wellformed_constraints():
    print(constraint)
print("Graph-preservation constraints:")
for constraint in collector.get_graph_preserving_constraints():
    print(constraint)
```

### Region bounds and engines

Verification and feasibility also accept `region_bound` instead of an explicit region.
This uses `[region_bound, 1-region_bound]` for every parameter. Floats are interpreted
using their decimal representation, so `0.2` means exactly `1/5`.
Provide exactly one of the keyword arguments `region` or `region_bound`.

Select a `RegionCheckEngine` using `region_engine` for verification and
feasibility (`PLA` only). The choice affects arithmetic and which regions are supported:

| Engine | Arithmetic | Region requirements |
| --- | --- | --- |
| `PARAMETER_LIFTING` (default) | Floating point | Well-defined and graph-preserving |
| `EXACT_PARAMETER_LIFTING` | Exact rational, potentially more expensive | Well-defined and graph-preserving |
| `VALIDATING_PARAMETER_LIFTING` | Floating point followed by exact validation | Well-defined and graph-preserving |
| `ROBUST_PARAMETER_LIFTING` | Floating point using robust models | Can include graph-changing valuations; DTMCs only |

## Verifying parametric models

[04-parameter-synthesis.py](https://github.com/stormchecker/stormpy/blob/master/examples/parametric_models/04-parameter-synthesis.py)

Function `verify` checks whether a bounded probability or reward property holds for **every**
well-defined parameter valuation in a region. It supports sparse parametric DTMCs and
MDPs with one initial state.

For our die model, the property asks whether the probability of rolling a two is at
most `0.5`. This does not hold throughout the original region:

```{code-cell} python3
holds_everywhere = stormpy.pars.verify(model, property, region=region)
print("Property holds throughout the region:", holds_everywhere)
assert not holds_everywhere
```

Some valuations exceed the bound. Restricting both parameters to `[0.2, 0.6]` makes
the property hold everywhere:

```{code-cell} python3
assert stormpy.pars.verify(model, property, region=smaller_region)
```

We can also use uniform bounds. Here, `region_bound=0.4` restricts both parameters to
`[0.4, 0.6]`:

```{code-cell} python3
assert stormpy.pars.verify(model, property, region_bound=0.4)
```

### Computing extremal values

`compute_extremal_value` minimizes or maximizes a quantitative probability or reward
over an explicit region. It returns the value and a parameter valuation achieving it,
within the requested precision. Floats must be finite and are interpreted using their
decimal representation, so `1e-4` means exactly `1/10000`. The wrapper handles the
conversion required by Storm:

```{code-cell} python3
value, valuation = stormpy.pars.compute_extremal_value(
    model,
    probability_property,
    region=region,
    direction=stormpy.logic.OptimizationDirection.MAXIMIZE,
    precision=1e-4,
    absolute_precision=True,
)
print("Maximum probability:", value)
print("Parameter valuation:", valuation)
```

For MDPs, the property's `min` or `max` selects the scheduler optimization, while
`direction` selects the optimization over parameters.

## Feasibility

Function `check_feasibility` searches for a well-defined parameter valuation satisfying a
bounded probability or reward property. It supports sparse parametric DTMCs and MDPs
with one initial state.

Verification failed on the original region, but some valuations still satisfy the property.
The result includes a satisfying valuation and the corresponding probability as a witness.
Select the search method with the `method` argument:

- `FeasibilityMethod.PLA`: parameter lifting, the default, for DTMCs and MDPs.
- `FeasibilityMethod.GD`: gradient descent for DTMCs.
- `FeasibilityMethod.SCP`: sequential convex programming for DTMCs and MDPs.

We can try all three methods on the same model, property, and region:

```{code-cell} python3
methods = [
    stormpy.pars.FeasibilityMethod.PLA,
    stormpy.pars.FeasibilityMethod.GD,
    stormpy.pars.FeasibilityMethod.SCP,
]
results = {}
for method in methods:
    result = stormpy.pars.check_feasibility(model, property, region=region, method=method)
    results[method] = result
    print(method.name, "feasibility:", result.status)
    assert result.status == stormpy.pars.RegionResult.EXISTS_SAT
    assert result.witness is not None
    witness = result.witness
    print("Parameter valuation:", {parameter.name: str(value) for parameter, value in witness.valuation.items()})
    print("Probability at the initial state:", witness.value)
```

All three methods find a satisfying valuation in this example. Their witnesses can differ;
for reference, `p=q=0.5` gives probability `1/6`, satisfying our bound.
Check each witness by instantiating the original model and computing its probability:

```{code-cell} python3
for method, result in results.items():
    witness = result.witness
    instantiated_model = instantiator.instantiate(witness.valuation)
    checked = stormpy.model_checking(instantiated_model, probability_property, only_initial_states=True)
    probability = checked[instantiated_model.initial_states[0]].value
    print(method.name, "probability on the instantiated model:", probability)
    assert math.isclose(probability, witness.value, rel_tol=1e-6)
    assert probability <= 0.5
```

### Establishing infeasibility

A stronger property can be infeasible throughout the original region. Here, no valuation
achieves probability at least `0.9`. We use PLA to establish infeasibility, so the result
is `ALL_VIOLATED` and has no witness:

```{code-cell} python3
stronger_property = stormpy.parse_property("P>=0.9 [F s=7 & d=2]", program)
infeasible = stormpy.pars.check_feasibility(model, stronger_property, region=region, method=stormpy.pars.FeasibilityMethod.PLA)
print("Feasibility of the stronger property:", infeasible.status)
assert infeasible.status == stormpy.pars.RegionResult.ALL_VIOLATED
assert infeasible.witness is None
```

A feasibility method can also return `RegionResult.UNKNOWN` when it cannot decide.
SCP can return this status when it fails to find a satisfying valuation. GD can keep
searching on an infeasible region, so use PLA when you need to establish infeasibility.
Only `EXISTS_SAT` includes a witness.

The lower-level checkers and model simplifiers are available through
`stormpy.pars.developer`.

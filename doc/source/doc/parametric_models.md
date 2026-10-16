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

## Verification and feasibility

The public `stormpy.pars` API provides model instantiation, region creation, verification, and feasibility synthesis
for sparse parametric DTMCs and MDPs with one initial state. Both analyses require a bounded
probability or reward property.

[04-parameter-synthesis.py](https://github.com/stormchecker/stormpy/blob/master/examples/parametric_models/04-parameter-synthesis.py)

### Building the parametric model

We use the parametric die model, whose transition probabilities depend on `p` and `q`.
The property asks whether the probability of eventually rolling a two is at most `0.5`.
Leaving the parameters undefined and selecting `RationalFunction` builds a parametric DTMC:

```{code-cell} python3
import stormpy
import stormpy.pars
import stormpy.examples.files

program = stormpy.parse_prism_program(stormpy.examples.files.prism_pdtmc_die)
property = stormpy.parse_property("P<=0.5 [F s=7 & d=2]", program)
model = stormpy.build_model[stormpy.RationalFunction](program, property)
parameters = model.collect_all_parameters()
```

### Verifying a region

First, let both parameters range from `0.2` to `0.8`. `verify` checks whether the property
holds for **every** well-defined valuation in this region:

```{code-cell} python3
region = stormpy.pars.parse_region("0.2<=p<=0.8,0.2<=q<=0.8", parameters)
holds_everywhere = stormpy.pars.verify(model, property, region)
print("Property holds throughout the region:", holds_everywhere)
assert not holds_everywhere
```

The result is `False`: some valuations exceed the probability bound. We can restrict the
region to `[0.2, 0.6]` for both parameters, where the property does hold everywhere.
This time, we construct the region from a dictionary of exact rational bounds:

```{code-cell} python3
lower = stormpy.RationalFunctionCoefficient("1/5")
upper = stormpy.RationalFunctionCoefficient("3/5")
smaller_region = stormpy.pars.create_region({parameter: (lower, upper) for parameter in parameters})
assert stormpy.pars.verify(model, property, smaller_region)
```

### Finding and checking a satisfying valuation

Verification failed on the original region, but some valuations still satisfy the property.
`check_feasibility` searches for one and returns its valuation and probability as a witness.
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
    result = stormpy.pars.check_feasibility(model, property, region, method=method)
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
To check each returned witness independently, instantiate the original model using
`ModelInstantiator` and compute the probability on the resulting DTMC:

```{code-cell} python3
import math

instantiator = stormpy.pars.ModelInstantiator(model)
probability_property = stormpy.parse_property("P=? [F s=7 & d=2]", program)
for method, result in results.items():
    witness = result.witness
    instantiated_model = instantiator.instantiate(witness.valuation)
    checked = stormpy.model_checking(instantiated_model, probability_property, only_initial_states=True)
    probability = checked[instantiated_model.initial_states[0]].value
    print(method.name, "probability on the instantiated model:", probability)
    assert math.isclose(probability, witness.value)
    assert probability <= 0.5
```

### Establishing infeasibility

A stronger property can be infeasible throughout the original region. Here, no valuation
achieves probability at least `0.9`. We use PLA to establish infeasibility, so the result
is `ALL_VIOLATED` and has no witness:

```{code-cell} python3
stronger_property = stormpy.parse_property("P>=0.9 [F s=7 & d=2]", program)
infeasible = stormpy.pars.check_feasibility(model, stronger_property, region, method=stormpy.pars.FeasibilityMethod.PLA)
print("Feasibility of the stronger property:", infeasible.status)
assert infeasible.status == stormpy.pars.RegionResult.ALL_VIOLATED
assert infeasible.witness is None
```

A feasibility method can also return `RegionResult.UNKNOWN` when it cannot decide.
SCP can return this status when it fails to find a satisfying valuation. GD can keep
searching on an infeasible region, so use PLA when you need to establish infeasibility.
Only `EXISTS_SAT` includes a witness.

### Uniform bounds and analysis options

Both analysis functions also accept `region_bound` instead of an explicit region. This
uses `[region_bound, 1-region_bound]` for every parameter. Floats are interpreted using
their decimal representation, so `0.2` means exactly `1/5`. For example, `0.4` restricts
both parameters to `[0.4, 0.6]`, where our original property holds everywhere:

```{code-cell} python3
assert stormpy.pars.verify(model, property, region_bound=0.4)
```

Provide exactly one of `region` or `region_bound`.

The default engine requires a well-defined, graph-preserving region and validates this
requirement. To include graph-changing valuations in a DTMC, select
`RegionCheckEngine.ROBUST_PARAMETER_LIFTING` using `engine` for verification or `region_engine`
for feasibility. The `region_engine` argument applies only to the `PLA` method.

For MDPs, bounds without `min` or `max` apply to every scheduler. For example,
`Pmin>=0.8 [F "target"]` requires the bound for every scheduler, while
`Pmax>=0.8 [F "target"]` asks for some scheduler. SCP requires universal scheduler quantification.

The lower-level checkers and model simplifiers are available through
`stormpy.pars.developer`.

## Instantiating parametric models

[01-parametric-models.py](https://github.com/stormchecker/stormpy/blob/master/examples//parametric_models/01-parametric-models.py)

Input formats such as prism allow to specify programs with open constants. We refer to these open constants as parameters.
If the constants only influence the probabilities or rates, but not the topology of the underlying model, we can build these models as parametric models:

```{code-cell} python3
import stormpy
import stormpy.examples
import stormpy.examples.files

path = stormpy.examples.files.prism_pdtmc_die
prism_program = stormpy.parse_prism_program(path)
formula_str = "P=? [F s=7 & d=2]"
prop = stormpy.parse_property(formula_str, prism_program)
model = stormpy.build_model[stormpy.RationalFunction](prism_program, prop)
parameters = model.collect_all_parameters()
for x in parameters:
    print(x)
```

To obtain a standard DTMC, MDP or other Markov model, use the public model instantiator:

```{code-cell} python3
import stormpy.pars

instantiator = stormpy.pars.ModelInstantiator[stormpy.models.ModelType.DTMC, float](model)
```

Use `ModelInstantiator[stormpy.models.ModelType.DTMC, stormpy.Rational](model)`
to instantiate with exact rational values. The resulting model can be checked with
`stormpy.model_checking` in the same way.

Before we obtain an instantiated model, we need to map parameters to values: We build such a dictionary as follows:

```{code-cell} python3
point = dict()
for x in parameters:
    print(x.name)
    point[x] = stormpy.RationalFunctionCoefficient(0.4)
instantiated_model = instantiator.instantiate(point)
result = stormpy.model_checking(instantiated_model, prop)
print(result[model.initial_states[0]])
```

Initial states and labels are set as for the parameter-free case.

## Checking parametric models

[02-parametric-models.py](https://github.com/stormchecker/stormpy/blob/master/examples//parametric_models/02-parametric-models.py)

It is also possible to check the parametric model directly, similar as before in [Checking properties](../getting_started.md#checking-properties):

```{code-cell} python3
result = stormpy.model_checking(model, prop)
initial_state = model.initial_states[0]
func = result[initial_state]
print(func)
```

We collect the constraints ensuring that underlying model is well-formed and the graph structure does not change:

```{code-cell} python3
collector = stormpy.ConstraintCollector(model)
for constraint in collector.get_wellformed_constraints():
    print(constraint)
for constraint in collector.get_graph_preserving_constraints():
    print(constraint)
```

## Collecting information about the parametric models

[03-parametric-models.py](https://github.com/stormchecker/stormpy/blob/master/examples//parametric_models/03-parametric-models.py)

This example shows three implementations to obtain the number of transitions with probability one in a parametric model.

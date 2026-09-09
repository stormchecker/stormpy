---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.19.5
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Parametric Models

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
properties = stormpy.parse_properties(formula_str, prism_program)
model = stormpy.build_parametric_model(prism_program, properties)
parameters = model.collect_all_parameters()
for x in parameters:
    print(x)
```

In order to obtain a standard DTMC, MDP or other Markov model, we need to instantiate these models by means of a model instantiator:

```{code-cell} python3
import stormpy.pars

instantiator = stormpy.pars.PDtmcInstantiator(model)
```

Before we obtain an instantiated model, we need to map parameters to values: We build such a dictionary as follows:

```{code-cell} python3
point = dict()
for x in parameters:
    print(x.name)
    point[x] = stormpy.RationalFunctionCoefficient(0.4)
instantiated_model = instantiator.instantiate(point)
result = stormpy.model_checking(instantiated_model, properties[0])
print(result.at(model.initial_states[0]))
```

Initial states and labels are set as for the parameter-free case.

## Checking parametric models

[02-parametric-models.py](https://github.com/stormchecker/stormpy/blob/master/examples//parametric_models/02-parametric-models.py)

It is also possible to check the parametric model directly, similar as before in [Checking properties](../getting_started.md#checking-properties):

```{code-cell} python3
result = stormpy.model_checking(model, properties[0])
initial_state = model.initial_states[0]
func = result.at(initial_state)
print(func)
```

We collect the constraints ensuring that underlying model is well-formed and the graph structure does not change:

```{code-cell} python3
import stormpy.info

if stormpy.info.storm_ratfunc_use_cln():
    import stormpy.pycarl.cln.formula
else:
    import stormpy.pycarl.gmp.formula
collector = stormpy.ConstraintCollector(model)
for formula in collector.wellformed_constraints:
    print(formula)
for formula in collector.graph_preserving_constraints:
    print(formula)
```

## Collecting information about the parametric models

[03-parametric-models.py](https://github.com/stormchecker/stormpy/blob/master/examples//parametric_models/03-parametric-models.py)

This example shows three implementations to obtain the number of transitions with probability one in a parametric model.

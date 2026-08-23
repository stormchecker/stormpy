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

# Exploring Models

## Background

Often, stormpy is used as a testbed for new algorithms.
An essential step is to transfer the (low-level) descriptions of an MDP or other state-based model into
an own algorithm. In this section, we discuss some of the functionality.

## Reading MDPs

[01-exploration.py](https://github.com/stormchecker/stormpy/blob/master/examples/exploration/01-exploration.py)

In [Getting Started](../getting_started.ipynb), we briefly iterated over a DTMC. In this section, we explore an MDP:

```{code-cell} ipython3
import doctest

import stormpy
import stormpy.examples
import stormpy.examples.files

program = stormpy.parse_prism_program(stormpy.examples.files.prism_mdp_maze)
prop = 'R=? [F "goal"]'

properties = stormpy.parse_properties_for_prism_program(prop, program, None)
model = stormpy.build_model(program, properties)
```

The iteration over the model is as before, but now, for every action, we can have several transitions:

```{code-cell} ipython3
for state in model.states:
    if state.id in model.initial_states:
        print("State {} is initial".format(state.id))
    for action in state.actions:
        for transition in action.transitions:
            print("From state {} by action {}, with probability {}, go to state {}".format(state, action, transition.value(), transition.column))
```

Internally, storm can hold hints to the origin of the actions, which may be helpful to give meaning and for debugging.
As the availability and the encoding of this data depends on the input model, we discuss these features in highlevel_models.

Storm currently supports deterministic rewards on states or actions. More information can be found in [Reward Models](reward_models.ipynb).

## Reading POMDPs

[02-exploration.py](https://github.com/stormchecker/stormpy/blob/master/examples/exploration/02-exploration.py)

Internally, POMDPs extend MDPs. Thus, iterating over the POMDP is done as before.

```{code-cell} ipython3
import stormpy
import stormpy.examples
import stormpy.examples.files

program = stormpy.parse_prism_program(stormpy.examples.files.prism_pomdp_maze)
prop = 'R=? [F "goal"]'
properties = stormpy.parse_properties_for_prism_program(prop, program, None)
model = stormpy.build_model(program, properties)
```

Indeed, all that changed in the code above is the example we use.
And, that the model type now is a POMDP:

```{code-cell} ipython3
print(model.model_type)
```

Additionally, POMDPs have a set of observations, which are internally just numbered by an integer from 0 to the number of observations -1

```{code-cell} ipython3
print(model.nr_observations)
for state in model.states:
    print("State {} has observation id {}".format(state.id, model.observations[state.id]))
```

## Sorting states

[03-exploration.py](https://github.com/stormchecker/stormpy/blob/master/examples/exploration/03-exploration.py)

Often, one may sort the states according to the graph structure.
Storm supports some of these sorting algorithms, e.g., topological sort.

## Reading MAs

To be continued…

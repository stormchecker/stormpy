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

# Continuous-time Markov chains (CTMCs)

## Background

In this section, we explain how Stormpy can be used to build a simple CTMC.
Building CTMCs works similar to building DTMCs as in [Discrete-time Markov chains (DTMCs)](building_dtmcs.md), however instead of transition probabilities we use transition rates.

[01-building-ctmcs.py](https://github.com/stormchecker/stormpy/blob/master/examples/building_ctmcs/01-building-ctmcs.py)

First, we import Stormpy:

```{code-cell} python3
import stormpy
```

## Transition Matrix

In this example, we build the transition matrix using a numpy array

```{code-cell} python3
import numpy as np

transitions = np.array(
    [
        [0, 1.5, 0, 0],
        [3, 0, 1.5, 0],
        [0, 3, 0, 1.5],
        [0, 0, 3, 0],
    ],
    dtype="float64",
)
```

The following function call returns a sparse matrix with default row groups:

```{code-cell} python3
transition_matrix = stormpy.build_sparse_matrix(transitions)
print(transition_matrix)
```

## Labeling

The state labeling is created analogously to the previous example in [building DTMCs](building_dtmcs.md#labeling):

```{code-cell} python3
state_labeling = stormpy.storage.StateLabeling(4)
state_labels = {"empty", "init", "deadlock", "full"}
for label in state_labels:
    state_labeling.add_label(label)
state_labeling.add_label_to_state("init", 0)
state_labeling.add_label_to_state("empty", 0)
state_labeling.add_label_to_state("full", 3)
```

## Building the Model

Now, we can collect all components, including the choice labeling.
To let the transition values be interpreted as rates we set rate_transitions to True:

```{code-cell} python3
components = stormpy.SparseModelComponents(transition_matrix=transition_matrix, state_labeling=state_labeling, rate_transitions=True)
```

And finally, we can build the model:

```{code-cell} python3
ctmc = stormpy.storage.SparseCtmc(components)
print(ctmc)
```

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

# Markov automata (MAs)

## Background

We already saw the process of building [CTMCs](building_ctmcs.ipynb) and [MDPs](building_mdps.ipynb) via Stormpy.

Markov automata use states that are probabilistic, i.e. like the states of an MDP, or Markovian, i.e. like the states of a CTMC.

In this section, we build a small MA with five states from which the first four are Markovian.

[01-building-mas.py](https://github.com/stormchecker/stormpy/blob/master/examples/building_mas/01-building-mas.py)

First, we import Stormpy:

```{code-cell} ipython3
import stormpy
```

## Transition Matrix

For [building MDPS](building_mdps.ipynb#transition-matrix), we used the SparseMatrixBuilder to create a matrix with a custom row grouping.
In this example, we use the numpy library.

In the beginning, we create a numpy array that will be used to build the transition matrix of our model.:

```{code-cell} ipython3
import numpy as np

transitions = np.array([[0, 1, 0, 0, 0], [0.8, 0, 0.2, 0, 0], [0.9, 0, 0, 0.1, 0], [0, 0, 0, 0, 1], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]], dtype="float64")
```

When building the matrix we define a custom row grouping by passing a list containing the starting row of each row group in ascending order:

```{code-cell} ipython3
transition_matrix = stormpy.build_sparse_matrix(transitions, [0, 2, 3, 4, 5])
print(transition_matrix)
```

## Labeling
The labeling is similar the ones already covered in the previous examples.

```{code-cell} ipython3
state_labeling = stormpy.storage.StateLabeling(5)
state_labels = {"init", "deadlock"}
for label in state_labels:
    state_labeling.add_label(label)
state_labeling.add_label_to_state("init", 0)

choice_labeling = stormpy.storage.ChoiceLabeling(6)
choice_labels = {"alpha", "beta"}
for label in choice_labels:
    choice_labeling.add_label(label)
choice_labeling.add_label_to_choice("alpha", 0)
choice_labeling.add_label_to_choice("beta", 1)
```

## Markovian States

In order to define which states have only one probability distribution over the successor states,
we build a BitVector that contains the respective Markovian states:

```{code-cell} ipython3
markovian_states = stormpy.BitVector(5, [1, 2, 3, 4])
```

## Exit Rates

Lastly, we initialize a list to equip every (Markovian) state with an exit rate > 0:

```{code-cell} ipython3
exit_rates = [0.0, 10.0, 12.0, 1.0, 1.0]
```

## Building the Model

Now, we can collect all components:

```{code-cell} ipython3
components = stormpy.SparseModelComponents(transition_matrix=transition_matrix, state_labeling=state_labeling, markovian_states=markovian_states)
components.choice_labeling = choice_labeling
components.exit_rates = exit_rates
```

Finally, we can build the model:

```{code-cell} ipython3
ma = stormpy.storage.SparseMA(components)
print(ma)
```

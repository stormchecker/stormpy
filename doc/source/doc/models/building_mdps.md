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

# Markov decision processes (MDPs)

## Background

In [Discrete-time Markov chains (DTMCs)](building_dtmcs.ipynb) we modelled Knuth-Yao’s model of a fair die by the means of a DTMC.
In the following we extend this model with nondeterministic choice by building a Markov decision process.

[01-building-mdps.py](https://github.com/stormchecker/stormpy/blob/master/examples/building_mdps/01-building-mdps.py)

First, we import Stormpy:

```{code-cell} ipython3
import stormpy
```

## Transition Matrix

Since we want to build a nondeterminstic model, we create a transition matrix with a custom row group for each state:

```{code-cell} ipython3
builder = stormpy.SparseMatrixBuilder(rows=0, columns=0, entries=0, force_dimensions=False, has_custom_row_grouping=True, row_groups=0)
```

We need more than one row for the transitions starting in state 0 because a nondeterministic choice over the actions is available.
Therefore, we start a new group that will contain the rows representing actions of state 0.
Note that the row group needs to be added before any entries are added to the group:

```{code-cell} ipython3
builder.new_row_group(0)
builder.add_next_value(0, 1, 0.5)
builder.add_next_value(0, 2, 0.5)
builder.add_next_value(1, 1, 0.2)
builder.add_next_value(1, 2, 0.8)
```

In this example, we have two nondeterministic choices in state 0.
With choice 0 we have probability 0.5 to got to state 1 and probability 0.5 to got to state 2.
With choice 1 we got to state 1 with probability 0.2 and go to state 2 with probability 0.8.

For the remaining states, we need to specify the starting rows of each row group:

```{code-cell} ipython3
builder.new_row_group(2)
builder.add_next_value(2, 3, 0.5)
builder.add_next_value(2, 4, 0.5)
builder.new_row_group(3)
builder.add_next_value(3, 5, 0.5)
builder.add_next_value(3, 6, 0.5)
builder.new_row_group(4)
builder.add_next_value(4, 7, 0.5)
builder.add_next_value(4, 1, 0.5)
builder.new_row_group(5)
builder.add_next_value(5, 8, 0.5)
builder.add_next_value(5, 9, 0.5)
builder.new_row_group(6)
builder.add_next_value(6, 10, 0.5)
builder.add_next_value(6, 11, 0.5)
builder.new_row_group(7)
builder.add_next_value(7, 2, 0.5)
builder.add_next_value(7, 12, 0.5)

for s in range(8, 14):
    builder.new_row_group(s)
    builder.add_next_value(s, s - 1, 1)
```

Finally, we build the transition matrix:

```{code-cell} ipython3
transition_matrix = builder.build()
```

## Labeling

The state labeling is similar to the one in the previous example for [building a DTMC](building_dtmcs.ipynb).

```{code-cell} ipython3
state_labeling = stormpy.storage.StateLabeling(13)
labels = {"init", "one", "two", "three", "four", "five", "six", "done", "deadlock"}
for label in labels:
    state_labeling.add_label(label)

state_labeling.add_label_to_state("init", 0)
state_labeling.add_label_to_state("one", 7)
state_labeling.add_label_to_state("two", 8)
state_labeling.add_label_to_state("three", 9)
state_labeling.add_label_to_state("four", 10)
state_labeling.add_label_to_state("five", 11)
state_labeling.add_label_to_state("six", 12)
state_labeling.set_states("done", stormpy.BitVector(13, [7, 8, 9, 10, 11, 12]))
```

### Choice labeling
We focus on the labeling of choices.
Since in state 0 a nondeterministic choice over two actions is available, the total number of choices is 14.
To distinguish those we can define a choice labeling:

```{code-cell} ipython3
choice_labeling = stormpy.storage.ChoiceLabeling(14)
choice_labels = {"a", "b"}

for label in choice_labels:
    choice_labeling.add_label(label)
```

We assign the label ‘a’ to the first action of state 0 and ‘b’ to the second.
Recall that those actions where defined in row one and two of the transition matrix respectively:

```{code-cell} ipython3
choice_labeling.add_label_to_choice("a", 0)
choice_labeling.add_label_to_choice("b", 1)
print(choice_labeling)
```

## Reward models

In this reward model the length of the action rewards coincides with the number of choices:

```{code-cell} ipython3
reward_models = {}
action_reward = [0.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
reward_models["coin_flips"] = stormpy.SparseRewardModel(optional_state_action_reward_vector=action_reward)
```

## Building the Model

We collect the components:

```{code-cell} ipython3
components = stormpy.SparseModelComponents(
    transition_matrix=transition_matrix, state_labeling=state_labeling, reward_models=reward_models, rate_transitions=False
)
components.choice_labeling = choice_labeling
```

We build the model:

```{code-cell} ipython3
mdp = stormpy.storage.SparseMdp(components)
print(mdp)
```

## Partially observable Markov decision process (POMDPs)

To build a partially observable Markov decision process (POMDP),
`components.observability_classes` can be set to a list of numbers that defines the status of the observables in each state.

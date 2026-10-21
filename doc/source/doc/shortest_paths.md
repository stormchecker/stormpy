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

# Working with Shortest Paths

Storm can enumerate the most probable paths of a model, leading from the initial state to a defined set of target states, which we refer to as shortest paths.
In particular, the model states visited along those paths are available as sets and can be accumulated, yielding a *sub-model*.

## Background

The underlying implementation uses the *recursive enumeration algorithm* [[JM1999]](#jm1999), substituting distance for probability – which is why we refer to the most probable paths as the *shortest* paths.

This algorithm computes the shortest paths recursively and in order, i.e., to find the 7th shortest path, the 1st through 6th shortest paths are computed as precursors.

It is crucial to note that *any* path is eligible, including those that (repeatedly) traverse loops (i.e., *non-simple* paths). This is a common case in practice: Often a large number of similar paths that differ only in the order and number of loop traversals occur successively in the sequence of shortest paths. (For applications that are only interested in simple paths, this is rather unfortunate.)

## Examining Shortest Paths

[01-shortest-paths.py](https://github.com/stormchecker/stormpy/blob/master/examples/shortest_paths/01-shortest-paths.py)

As in [Getting Started](../getting_started.md), we import some required modules and build a model from the example files:

```{code-cell} python3
import stormpy.examples
import stormpy.examples.files

path = stormpy.examples.files.prism_dtmc_die
prism_program = stormpy.parse_prism_program(path)
model = stormpy.build_model(prism_program)
```

We choose a target state (by its ID) to which we want to compute the shortest paths:

```{code-cell} python3
state_id = 8
```

It is also possible to specify a set of target states (as a list, e.g., `[8, 10, 11]`) or a label in the model if applicable (e.g., `"observe0Greater1"`).
For simplicity, we will stick to using a single state for now.

To compute one path, use {func}`stormpy.analysis.shortest_path`. It returns the state IDs in order from the initial state to the target, together with the path's probability:

```{code-cell} python3
states, probability = stormpy.analysis.shortest_path(model, state_id)
print(states, probability)
```

Pass ``k=3`` to obtain the third most probable path. Exact models return an exact rational probability.
Path ranks are one-based, so the third most probable path corresponds to ``k=3``.
We can inspect the first three paths by calling the function for each rank:

```{code-cell} python3
for k in range(1, 4):
    states, probability = stormpy.analysis.shortest_path(model, state_id, k=k)
    print(f"{k}-shortest path to state #{state_id}: {states}, with probability {probability}")
```

Each call computes the requested path independently. The returned states run from the initial state to the target.

<a id='jm1999'></a>
\[JM1999\] Víctor M. Jiménez, Andrés Marzal. [Computing the K Shortest Paths: A New Algorithm and an Experimental Comparison](https://scholar.google.com/scholar?q=Computing+the+k+shortest+paths%3A+A+new+algorithm+and+an+experimental+comparison). International Workshop on Algorithm Engineering, 1999

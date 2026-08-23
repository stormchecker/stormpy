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

# Working with Shortest Paths

Storm can enumerate the most probable paths of a model, leading from the initial state to a defined set of target states, which we refer to as shortest paths.
In particular, the model states visited along those paths are available as sets and can be accumulated, yielding a *sub-model*.

## Background

The underlying implementation uses the *recursive enumeration algorithm* [[JM1999]](#jm1999), substituting distance for probability – which is why we refer to the most probable paths as the *shortest* paths.

This algorithm computes the shortest paths recursively and in order, i.e., to find the 7th shortest path, the 1st through 6th shortest paths are computed as precursors. The next (i.e., 8th shortest) path can then be computed efficiently.

It is crucial to note that *any* path is eligible, including those that (repeatedly) traverse loops (i.e., *non-simple* paths). This is a common case in practice: Often a large number of similar paths that differ only in the order and number of loop traversals occur successively in the sequence of shortest paths. (For applications that are only interested in simple paths, this is rather unfortunate.)

## Examining Shortest Paths

[01-shortest-paths.py](https://github.com/stormchecker/stormpy/blob/master/examples/shortest_paths/01-shortest-paths.py)

As in [Getting Started](../getting_started.ipynb), we import some required modules and build a model from the example files:

```{code-cell} ipython3
import stormpy.examples
import stormpy.examples.files

path = stormpy.examples.files.prism_dtmc_die
prism_program = stormpy.parse_prism_program(path)
model = stormpy.build_model(prism_program)
```

We also import the `ShortestPathsGenerator`:

```{code-cell} ipython3
from stormpy.utility import ShortestPathsGenerator
```

and choose a target state (by its ID) to which we want to compute the shortest paths:

```{code-cell} ipython3
state_id = 8
```

It is also possible to specify a set of target states (as a list, e.g., `[8, 10, 11]`) or a label in the model if applicable (e.g., `"observe0Greater1"`).
For simplicity, we will stick to using a single state for now.

We initialize a `ShortestPathsGenerator` instance:

```{code-cell} ipython3
spg = ShortestPathsGenerator(model, state_id)
```

Now we can query the k-shortest path by index. Note that 1-based indices are used, so that the 3rd shortest path indeed corresponds to index `k=3`.
Let us inspect the first three shortest paths:

```{code-cell} ipython3
for k in range(1, 4):
    path = spg.get_path_as_list(k)
    distance = spg.get_distance(k)
    print("{}-shortest path to state #{}: {}, with distance {}".format(k, state_id, path, distance))
```

As you can see, the distance (i.e., probability of the path) is also available.
Note that the paths are displayed as a backward-traversal from the target to the initial state.

<a id='jm1999'></a>
\[JM1999\] Víctor M. Jiménez, Andrés Marzal. [Computing the K Shortest Paths: A New Algorithm and an Experimental Comparison](https://scholar.google.com/scholar?q=Computing+the+k+shortest+paths%3A+A+new+algorithm+and+an+experimental+comparison). International Workshop on Algorithm Engineering, 1999

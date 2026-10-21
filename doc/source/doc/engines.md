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

# Engines

## Background

Storm supports different engines for building and checking a model. A detailed comparison of the different engines provided in Storm can be found on the [Storm website](https://www.stormchecker.org/documentation/usage/engines.html).

## Sparse engine

In all of the examples so far we used the default sparse engine:

```{code-cell} python3
import stormpy.examples
import stormpy.examples.files

prism_program = stormpy.parse_prism_program(stormpy.examples.files.prism_dtmc_die)
prop = stormpy.parse_property('P=? [F "one"]', prism_program)
sparse_model = stormpy.build_model(prism_program, prop)
print(type(sparse_model))
```

```{code-cell} python3
print("Number of states: {}".format(sparse_model.nr_states))
```

```{code-cell} python3
print("Number of transitions: {}".format(sparse_model.nr_transitions))
```

```{code-cell} python3
sparse_result = stormpy.model_checking(sparse_model, prop)
initial_state = sparse_model.initial_states[0]
print(sparse_result[initial_state])
```

## Symbolic engine

Instead of using the sparse engine, one can also use a symbolic representation in terms of binary decision diagrams (BDDs).
To use the symbolic (dd) engine, we pass the engine to the building and model checking:

```{code-cell} python3
symbolic_model = stormpy.build_model(prism_program, prop, engine=stormpy.Engine.DD)
print(type(symbolic_model))
```

```{code-cell} python3
print("Number of states: {}".format(symbolic_model.nr_states))
```

```{code-cell} python3
print("Number of transitions: {}".format(symbolic_model.nr_transitions))
```

```{code-cell} python3
symbolic_result = stormpy.model_checking(symbolic_model, prop, engine=stormpy.Engine.DD)
print(symbolic_result)
```

We can also filter the computed results and only consider the initial states:

```{code-cell} python3
stormpy.filter_initial_states(symbolic_result, symbolic_model)
print(symbolic_result.get_min())
```

It is also possible to first build the model symbolically and then transform it into a sparse model:

```{code-cell} python3
print(type(symbolic_model))
```

```{code-cell} python3
transformed_model = stormpy.transformations.transform_to_sparse_model(symbolic_model)
print(type(transformed_model))
```

## Hybrid engine

A third possibility is to use the hybrid engine, a combination of sparse and dd engines.
It first builds the model symbolically.
The actual model checking is then performed with the engine which is deemed most suitable for the given task.

```{code-cell} python3
print(type(symbolic_model))
```

```{code-cell} python3
hybrid_result = stormpy.model_checking(symbolic_model, prop, engine=stormpy.Engine.HYBRID)
stormpy.filter_initial_states(hybrid_result, symbolic_model)
print(hybrid_result)
```

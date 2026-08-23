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

# Engines

## Background

Storm supports different engines for building and checking a model. A detailed comparison of the different engines provided in Storm can be found on the [Storm website](https://www.stormchecker.org/documentation/usage/engines.html).

## Sparse engine

In all of the examples so far we used the default sparse engine:

```{code-cell} ipython3
import stormpy.examples
import stormpy.examples.files

prism_program = stormpy.parse_prism_program(stormpy.examples.files.prism_dtmc_die)
properties = stormpy.parse_properties('P=? [F "one"]', prism_program)
sparse_model = stormpy.build_sparse_model(prism_program, properties)
print(type(sparse_model))
```

```{code-cell} ipython3
print("Number of states: {}".format(sparse_model.nr_states))
```

```{code-cell} ipython3
print("Number of transitions: {}".format(sparse_model.nr_transitions))
```

```{code-cell} ipython3
sparse_result = stormpy.check_model_sparse(sparse_model, properties[0])
initial_state = sparse_model.initial_states[0]
print(sparse_result.at(initial_state))
```

## Symbolic engine

Instead of using the sparse engine, one can also use a symbolic representation in terms of binary decision diagrams (BDDs).
To use the symbolic (dd) engine, we use the symbolic versions for the building and model checking:

```{code-cell} ipython3
symbolic_model = stormpy.build_symbolic_model(prism_program, properties)
print(type(symbolic_model))
```

```{code-cell} ipython3
print("Number of states: {}".format(symbolic_model.nr_states))
```

```{code-cell} ipython3
print("Number of transitions: {}".format(symbolic_model.nr_transitions))
```

```{code-cell} ipython3
symbolic_result = stormpy.check_model_dd(symbolic_model, properties[0])
print(symbolic_result)
```

We can also filter the computed results and only consider the initial states:

```{code-cell} ipython3
filter = stormpy.create_filter_initial_states_symbolic(symbolic_model)
symbolic_result.filter(filter)
print(symbolic_result.min)
```

It is also possible to first build the model symbolically and then transform it into a sparse model:

```{code-cell} ipython3
print(type(symbolic_model))
```

```{code-cell} ipython3
transformed_model = stormpy.transform_to_sparse_model(symbolic_model)
print(type(transformed_model))
```

## Hybrid engine

A third possibility is to use the hybrid engine, a combination of sparse and dd engines.
It first builds the model symbolically.
The actual model checking is then performed with the engine which is deemed most suitable for the given task.

```{code-cell} ipython3
print(type(symbolic_model))
```

```{code-cell} ipython3
hybrid_result = stormpy.check_model_hybrid(symbolic_model, properties[0])
filter = stormpy.create_filter_initial_states_symbolic(symbolic_model)
hybrid_result.filter(filter)
print(hybrid_result)
```

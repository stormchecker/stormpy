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

# Analysis

## Background

Storm supports various model checking approaches that we consider in this section on analysis.

As always:

```{code-cell} python3
import stormpy
import stormpy.examples
import stormpy.examples.files

path = stormpy.examples.files.prism_dtmc_die
prism_program = stormpy.parse_prism_program(path)
formula_str = "P=? [F s=7 & d=2]"
properties = stormpy.parse_properties(formula_str, prism_program)
```

## Qualitative Analysis

## Adapting the model checking engine

[02-analysis.py](https://github.com/stormchecker/stormpy/blob/master/examples/analysis/02-analysis.py)

Instead of using the sparse representation, models can also be built symbolically:

```{code-cell} python3
model = stormpy.build_symbolic_model(prism_program, properties)
result = stormpy.model_checking(model, properties[0])
```

To access the result, the result has to be filtered:

```{code-cell} python3
filter = stormpy.create_filter_initial_states_symbolic(model)
result.filter(filter)
assert result.min == result.max
```

Then, result.min (or result.max) contains the result. Notice that if there are multiple initial states, result.min will not be equal to result.max.

Besides this analysis on the DD, there are approaches that combine both representation.
Stormpy does support them, but we have not yet documented them.

## Adapting model checking algorithms

[03-analysis.py](https://github.com/stormchecker/stormpy/blob/master/examples/analysis/03-analysis.py)

Reconsider the model checking example from the getting started guide:

```{code-cell} python3
model = stormpy.build_model(prism_program, properties)
result = stormpy.model_checking(model, properties[0])
```

We can also vary the model checking algorithm:

```{code-cell} python3
env = stormpy.Environment()
env.solver_environment.set_linear_equation_solver_type(stormpy.EquationSolverType.native)
env.solver_environment.native_solver_environment.method = stormpy.NativeLinearEquationSolverMethod.power_iteration
result = stormpy.model_checking(model, properties[0], environment=env)
```

Finally, we allow to change some parameters of the algorithms. E.g., in iterative approaches,
we allow to change the number of iterations:

```{code-cell} python3
env.solver_environment.native_solver_environment.maximum_iterations = 3
result = stormpy.model_checking(model, properties[0])
```

Notice that by setting such parameters, the result may be off from the actual model checking algorithm.

Environments can be used likewise for symbolic model checking. See the example for more information.

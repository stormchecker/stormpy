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

# Working with Schedulers

In non-deterministic models the notion of a scheduler (or policy) is important.
The scheduler determines which action to take at each state.

For a given reachability property, Storm can return the scheduler realizing the resulting probability.

## Examining Schedulers for MDPs

[01-schedulers.py](https://github.com/stormchecker/stormpy/blob/master/examples/schedulers/01-schedulers.py)

As in [Getting Started](../getting_started.ipynb), we import some required modules and build a model from the example files:

```{code-cell} ipython3
import stormpy
import stormpy.examples
import stormpy.examples.files

path = stormpy.examples.files.prism_mdp_coin_2_2
formula_str = 'Pmin=? [F "finished" & "all_coins_equal_1"]'
program = stormpy.parse_prism_program(path)
formulas = stormpy.parse_properties(formula_str, program)
options = stormpy.BuilderOptions(True, True)
options.set_build_state_valuations()
options.set_build_choice_labels()
options.set_build_with_choice_origins()
model = stormpy.build_sparse_model_with_options(program, options)
```

Next we check the model and make sure to extract the scheduler:

```{code-cell} ipython3
result = stormpy.model_checking(model, formulas[0], extract_scheduler=True)
```

The result then contains the scheduler we want:

```{code-cell} ipython3
assert result.has_scheduler
scheduler = result.scheduler
assert scheduler.memoryless
assert scheduler.deterministic
print(scheduler)
```

To get the information which action the scheduler chooses in which state, we can simply iterate over the states:

```{code-cell} ipython3
for state in model.states:
    choice = scheduler.get_choice(state)
    action_index = choice.get_deterministic_choice()
    action = state.actions[action_index]
    print("In state {} ({}) choose action {} ({})".format(state, ", ".join(state.labels), action, ", ".join(action.labels)))
    print(state.valuations)
```

## Examining Schedulers for Markov automata

[02-schedulers.py](https://github.com/stormchecker/stormpy/blob/master/examples/schedulers/02-schedulers.py)

Currently there is no support yet for scheduler extraction on MAs.
However, if the timing information is not relevant for the property, we can circumvent this lack by first transforming the MA to an MDP.

We build the model as before:

```{code-cell} ipython3
path = stormpy.examples.files.prism_ma_simple
formula_str = "Tmin=? [ F s=4 ]"

program = stormpy.parse_prism_program(path, False, True)
formulas = stormpy.parse_properties_for_prism_program(formula_str, program)
ma = stormpy.build_model(program, formulas)
```

Next we transform the continuous-time model into a discrete-time model.
Note that all timing information is lost at this point:

```{code-cell} ipython3
mdp, mdp_formulas = stormpy.transform_to_discrete_time_model(ma, formulas)
assert mdp.model_type == stormpy.ModelType.MDP
```

After the transformation we have obtained an MDP where we can extract the scheduler as shown before:

```{code-cell} ipython3
result = stormpy.model_checking(mdp, mdp_formulas[0], extract_scheduler=True)
scheduler = result.scheduler
print(scheduler)
```

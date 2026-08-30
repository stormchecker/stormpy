---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.19.5
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Working with Simulators

The simulators in stormpy are meant to mimic access to unknown models,
but they can also be used to explore the model.

All simulators implement the abstract class `stormpy.simulator.Simulator`.

The simulators differ in the model representation they use in the background and in the representation of the states and actions exposed to the user. We will go through some options by example!

```{code-cell} python3
import stormpy
import stormpy.examples
import stormpy.examples.files
import stormpy.simulator
```

## Model-based simulation

We first start with an explicit model-based simulation. This means that we have a model of the DTMC in memory. This is fast and convenient if the model is available, but limits the size of models that we support.

### DTMCs
We first discuss the interface for DTMCs, without any nondeterminism.

#### Explicit state-representations
After importing some parts of stormpy as above, we start with creating a model, in this case a DTMC:

```{code-cell} python3
path = stormpy.examples.files.prism_dtmc_die
prism_program = stormpy.parse_prism_program(path)
model = stormpy.build_model(prism_program)

simulator = stormpy.simulator.create_simulator(model, seed=42)
```

Let us simulate a path.

```{code-cell} python3
simulator.restart()
```

```{code-cell} python3
simulator.step()
```

```{code-cell} python3
simulator.step()
```

```{code-cell} python3
simulator.step()
```

We start the simulator by restarting. We then do 3 steps. Every step returns a triple (state, reward, labels). In particular, the simulation above reflects a path s0, s2, s5, s11. Taking the transitions in-between yields the reward as shown above. While states s2 and s5 are not labelled, state s0 is labelled with `init` and state s11 is labelled with `done` and `five`. Indeed we can check this information on the model that we used for the simulator:

```{code-cell} python3
model.labeling.get_labels_of_state(11)
```

We can continue sampling.

```{code-cell} python3
simulator.step()
```

```{code-cell} python3
simulator.step()
```

Indeed, we are not leaving the state. In this case, we can never leave the state as state s11 is absorbing. The simulator detects and exposes this information via `simulator.is_done()`

```{code-cell} python3
simulator.is_done()
```

We can sample more paths, yielding (potentially) different final states:

```{code-cell} python3
simulator.restart()
final_outcomes = dict()
for n in range(100):
    while not simulator.is_done():
        observation, reward, labels = simulator.step()
    if observation not in final_outcomes:
        final_outcomes[observation] = 1
    else:
        final_outcomes[observation] += 1
    simulator.restart()
final_outcomes
```

#### Program-level representations

We can run the same simulator but represent states symbolically, referring to the high-level description of the state rather than on its internal index. The advantage of this is that the process becomes independent of the underlying representation of the model. We first need to build the model with the required annotations.

```{code-cell} python3
options = stormpy.BuilderOptions()
options.set_build_state_valuations()
model = stormpy.build_sparse_model_with_options(prism_program, options)
```

Then, we create simulator that uses program-level state observations.

```{code-cell} python3
simulator = stormpy.simulator.create_simulator(model, seed=42)
simulator.set_observation_mode(stormpy.simulator.SimulatorObservationMode.PROGRAM_LEVEL)
```

```{code-cell} python3
state, reward, label = simulator.restart()
str(state)
```

Indeed, the state is now an object that describes the state in terms of the variables of prism program, in this case variables "s" and "d".

We can use the simulator as before, e.g.,

```{code-cell} python3
simulator.restart()
final_outcomes = dict()
print(simulator.get_reward_names())
for n in range(100):
    while not simulator.is_done():
        observation, reward, labels = simulator.step()
    if observation not in final_outcomes:
        final_outcomes[observation] = 1
    else:
        final_outcomes[observation] += 1
    simulator.restart()
print(", ".join([f"{str(k)}: {v}" for k, v in final_outcomes.items()]))
```

### MDPs

#### Explicit representations

As above, we can represent states both explicitly or symbolically. We only discuss the explicit representation here. With nondeterminism, we now must resolve this nondeterminism externally. That is, the step argument now takes an argument, which we may pick randomly or in a more intelligent manner.

```{code-cell} python3
import random

random.seed(23)
path = stormpy.examples.files.prism_mdp_slipgrid
prism_program = stormpy.parse_prism_program(path)

model = stormpy.build_model(prism_program)
simulator = stormpy.simulator.create_simulator(model, seed=42)
# 3 paths of at most 20 steps.
paths = []
for m in range(3):
    path = []
    state, reward, labels = simulator.restart()
    path = [f"{state}"]
    for n in range(20):
        actions = simulator.available_actions()
        select_action = random.randint(0, len(actions) - 1)
        path.append(f"--act={actions[select_action]}-->")
        state, reward, labels = simulator.step(actions[select_action])
        path.append(f"{state}")
        if simulator.is_done():
            break
    paths.append(path)
for path in paths:
    print(" ".join(path))
    print("------")
```

In the example above, the actions are internal numbers. Often, a program gives semantically meaningful names, such as moving `north`, `east`, `west` and `south` in a grid with program variables reflecting the `x` and `y` location.

```{code-cell} python3
options = stormpy.BuilderOptions()
options.set_build_choice_labels()
options.set_build_state_valuations()
model = stormpy.build_sparse_model_with_options(prism_program, options)
simulator = stormpy.simulator.create_simulator(model, seed=42)
simulator.set_action_mode(stormpy.simulator.SimulatorActionMode.GLOBAL_NAMES)
simulator.set_observation_mode(stormpy.simulator.SimulatorObservationMode.PROGRAM_LEVEL)
# 3 paths of at most 20 steps.
paths = []
for m in range(3):
    path = []
    state, reward, labels = simulator.restart()
    path = [f"({state['x']},{state['y']})"]
    for n in range(20):
        actions = simulator.available_actions()
        select_action = random.randint(0, len(actions) - 1)
        path.append(f"--{actions[select_action]}-->")
        state, reward, labels = simulator.step(actions[select_action])
        path.append(f"({state['x']},{state['y']})")
        if simulator.is_done():
            break
    paths.append(path)
for path in paths:
    print(" ".join(path))
```

## Program-level simulator

We can also use a program-level simulator, which does not require putting the model into memory.

```{code-cell} python3
simulator = stormpy.simulator.create_simulator(prism_program, seed=42)
```

```{code-cell} python3
# 3 paths of at most 20 steps.
paths = []
for m in range(3):
    path = []
    state, reward, labels = simulator.restart()
    path = [f"({state['x']},{state['y']})"]
    for n in range(20):
        actions = simulator.available_actions()
        select_action = random.randint(0, len(actions) - 1)
        path.append(f"--{actions[select_action]}-->")
        state, reward, labels = simulator.step(actions[select_action])
        path.append(f"({state['x']},{state['y']})")
        if simulator.is_done():
            break
    paths.append(path)
for path in paths:
    print(" ".join(path))
```

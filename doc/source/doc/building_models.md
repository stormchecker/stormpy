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

# Building Models

## Background

Storm supports a wide range of formalisms to specify Markov models.
Stormpy can be used to build models from some of these formalisms.
Moreover, during construction, various options can be set.
This document yields information about the most important options.

## Building from explicit models

We use some standard examples:

```{code-cell} python3
import stormpy.examples
import stormpy.examples.files
```

### DRN
Storm supports the explicit [DRN format](https://www.stormchecker.org/documentation/background/drn.html). From this, models can be built directly:

```{code-cell} python3
path = stormpy.examples.files.drn_ctmc_dft
model = stormpy.build_model_from_drn(path)
print(model.model_type)
```

And the same for parametric models:

```{code-cell} python3
path = stormpy.examples.files.drn_pdtmc_die
model = stormpy.build_parametric_model_from_drn(path)
print(model.model_type)
```

### UMB
Support for [UMB](https://pmc-tools.github.io/umb/) will follow once the UMB-support for Storm is part of a stable release.

## Building from symbolic models

### PRISM
For the moment, see the getting started.

### JANI
Another option are JANI descriptions. These are another high-level description format.
Building models from JANI is done in two steps. First the Jani-description is parsed, and then the model is built from this description:

```{code-cell} python3
path = stormpy.examples.files.jani_dtmc_die
jani_program, properties = stormpy.parse_jani_model(path)
model = stormpy.build_model(jani_program)
print(model.model_type)
```

Notice that parsing JANI files also returns properties. In JANI, properties can be embedded in the model file.

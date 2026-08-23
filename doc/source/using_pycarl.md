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

# Getting Started with Pycarl
Pycarl is shipped with the stormpy library and can be installed following the [general installation instructions](installation).

## A Quick Tour through pycarl
First we import pycarl:

```{code-cell} ipython3
from stormpy import pycarl
```

Pycarl can use two different number types: `gmp` and `cln`.
In this example we will use `gmp` numbers and therefore import the corresponding module:

```{code-cell} ipython3
from stormpy.pycarl import gmp
```

### Simple arithmetic operations
[01-getting-started.py](https://github.com/stormchecker/stormpy/blob/master/examples/pycarl/01-pycarl-getting-started.py)

We start by doing some simple arithmetic operations.
First we create two variables `x` and `y`:

```{code-cell} ipython3
pycarl.clear_variable_pool()
x = pycarl.Variable("x")
y = pycarl.Variable("y")
```

We perform some operations on polynomials by using the common arithmetic operations of Python:

```{code-cell} ipython3
pol1 = x * x + pycarl.gmp.Integer(2)
pol2 = y + pycarl.gmp.Integer(1)
result = pol1 * pol2
print("({}) * ({}) = {}".format(pol1, pol2, result))
```

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

# Dynamic Fault Trees

## Building DFTs

[01-dfts.py](https://github.com/stormchecker/stormpy/blob/master/examples/dfts/01-dfts.py)

Dynamic fault trees can be loaded from either the Galileo format or from a custom JSON form.
A file containing the DFT in the Galileo format can be loaded via `load_dft_galileo_file(path)`.
The custom JSON format can be loaded from a file via `load_dft_json_file(path)` or directly from a string via `load_dft_json_string(path)`.
We start by loading a simple DFT containing an AND gate from JSON:

```{code-cell} ipython3
import stormpy
import stormpy.dft
import stormpy.examples
import stormpy.examples.files

path_json = stormpy.examples.files.dft_json_and
dft_small = stormpy.dft.load_dft_json_file(path_json)
print(dft_small)
```

Next we load a more complex DFT from the Galileo format:

```{code-cell} ipython3
path_galileo = stormpy.examples.files.dft_galileo_hecs
dft = stormpy.dft.load_dft_galileo_file(path_galileo)
```

After loading the DFT, we can display some common statistics about the model:

```{code-cell} ipython3
print("DFT with {} elements.".format(dft.nr_elements()))
print("DFT has {} BEs and {} dynamic elements.".format(dft.nr_be(), dft.nr_dynamic()))
```

## Analyzing DFTs

[01-dfts.py](https://github.com/stormchecker/stormpy/blob/master/examples/dfts/01-dfts.py)

The next step is to analyze the DFT via `analyze_dft(dft, formula)`.
Here we can use all standard properties as described in [Building properties](../getting_started.ipynb#building-properties).
In our example we compute the Mean-time-to-failure (MTTF):

```{code-cell} ipython3
formula_str = 'T=? [ F "failed" ]'
formulas = stormpy.parse_properties(formula_str)
results = stormpy.dft.analyze_dft(dft, [formulas[0].raw_formula])
result = results[0]
print("MTTF: {:.2f}".format(result))
```

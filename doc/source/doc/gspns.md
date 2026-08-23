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

# Generalized Stochastic Petri Nets

## Loading GSPNs

[01-gspns.py](https://github.com/stormchecker/stormpy/blob/master/examples/gspns/01-gspns.py)

Generalized stochastic Petri nets can be given either in the PNPRO format or in the PNML format.
We start by loading a GSPN stored in the PNML format:

```{code-cell} python3
import stormpy
import stormpy.gspn
import stormpy.examples
import stormpy.examples.files

import_path = stormpy.examples.files.gspn_pnml_simple
gspn_parser = stormpy.gspn.GSPNParser()
gspn = gspn_parser.parse(import_path)
```

After loading, we can display some properties of the GSPN:

```{code-cell} python3
print("Name of GSPN: {}.".format(gspn.get_name()))
```

```{code-cell} python3
print("Number of places: {}.".format(gspn.get_number_of_places()))
```

```{code-cell} python3
print("Number of immediate transitions: {}.".format(gspn.get_number_of_immediate_transitions()))
```

```{code-cell} python3
print("Number of timed transitions: {}.".format(gspn.get_number_of_timed_transitions()))
```

## Building GSPNs

[02-gspns.py](https://github.com/stormchecker/stormpy/blob/master/examples/gspns/02-gspns.py)

In the following, we describe how to construct GSPNs via the `GSPNBuilder`.
First, we create an instance of the `GSPNBuilder` and set the name of the GSPN:

```{code-cell} python3
builder = stormpy.gspn.GSPNBuilder()
builder.set_name("my_gspn")
```

In the next step, we add an immediate transition to the GSPN.
Additionally, we define the position of the transition by setting its layout information:

```{code-cell} python3
it_1 = builder.add_immediate_transition(1, 0.0, "it_1")
it_layout = stormpy.gspn.LayoutInfo(1.5, 2.0)
builder.set_transition_layout_info(it_1, it_layout)
```

We add a timed transition and set its layout information:

```{code-cell} python3
tt_1 = builder.add_timed_transition(0, 0.4, "tt_1")
tt_layout = stormpy.gspn.LayoutInfo(12.5, 2.0)
builder.set_transition_layout_info(tt_1, tt_layout)
```

Next, we add two places to the GSPN and set their layouts:

```{code-cell} python3
place_1 = builder.add_place(1, 1, "place_1")
p1_layout = stormpy.gspn.LayoutInfo(6.5, 2.0)
builder.set_place_layout_info(place_1, p1_layout)

place_2 = builder.add_place(1, 0, "place_2")
p2_layout = stormpy.gspn.LayoutInfo(18.5, 2.0)
builder.set_place_layout_info(place_2, p2_layout)
```

Places and transitions can be linked by input, output and inhibition arcs.
We add the arcs of our GSPN as follows:

```{code-cell} python3
builder.add_output_arc(it_1, place_1)
builder.add_inhibition_arc(place_1, it_1)
builder.add_input_arc(place_1, tt_1)
builder.add_output_arc(tt_1, place_2)
```

We can now build the GSPN:

```{code-cell} python3
gspn = builder.build_gspn()
```

After building, we export the GSPN.
GSPNs can be saved in the PNPRO format via `export_gspn_pnpro_file(path)` and in the PNML format via `export_gspn_pnml_file(path)`.
We export the GSPN into the PNPRO format:

```{code-cell} python3
export_path = stormpy.examples.files.gspn_pnpro_simple
gspn.export_gspn_pnpro_file(export_path)
```

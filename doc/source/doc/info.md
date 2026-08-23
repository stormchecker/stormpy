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

# Storm(py) Information

Stormpy links against a particular installation of Storm.
The module `stormpy.info` provides information about this installation.
This is especially useful for debugging and for writing bug reports.

First, we import the relevant modules:

```{code-cell} python3
import stormpy
import stormpy.info
```

## Storm Version

The Storm version that stormpy is linked against is available via `storm_version()`:

```{code-cell} python3
stormpy.info.storm_version()
```

The flag `storm_development_version()` tells whether the linked Storm is a development version, i.e. modified since the last release:

```{code-cell} python3
stormpy.info.storm_development_version()
```

Further information about the Storm build is available through `Version.long` and `Version.build_info`.
These are particularly useful when reporting issues, as they also list the compiler and the build date:

```{code-cell} python3
stormpy.info.Version.long
```

```{code-cell} python3
stormpy.info.Version.build_info
```

## Build Configuration

The build type of Storm states how the library was originally compiled.
`Debug` builds are often slower, but easier to debug, while `Release` builds are the standard choice:

```{code-cell} python3
stormpy.info.storm_build_type()
```

## Origin of the Storm Installation

The function `storm_from_system()` reports whether stormpy relies on a pre-existing system installation of Storm, or whether Storm was fetched and installed during the build of stormpy:

```{code-cell} python3
stormpy.info.storm_from_system()
```

The function `storm_origin_info()` provides the origin of the Storm installation: the repository URL, the repository tag and the commit hash.
If a system installation was used, the repository and the tag are `None`.
If Storm was installed as part of the build of stormpy, repository and tag are given; for a local source directory, the tag reads `__local-source-dir__`:

```{code-cell} python3
repo, tag, hash = stormpy.info.storm_origin_info()
print("Repository:", repo)
print("Tag:", tag)
print("Commit hash:", hash)
```

If a system installation of Storm was used, `storm_directory()` returns the path to this installation. Otherwise, `None` is returned:

```{code-cell} python3
stormpy.info.storm_directory()
```

## Number representations

Storm can use different libraries for exact arithmetic.
This is relevant if you compute with exact numbers or rational functions, as the performance may be influenced by the library.
The functions `storm_exact_use_cln()` and `storm_ratfunc_use_cln()` report whether CLN (instead of GMP) is used for exact numbers and rational functions, respectively:

```{code-cell} python3
print("Represent exact numbers using " + ("CLN" if stormpy.info.storm_exact_use_cln() else "GMP"))
print("Represent rational functions using " + ("CLN" if stormpy.info.storm_ratfunc_use_cln() else "GMP"))
```

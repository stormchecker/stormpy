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

# How to write a stormpy binding

The following tutorial teaches you how to write a binding for stormpy. It helps to also read the [pybind11 documentation](https://pybind11.readthedocs.io/en/stable/advanced/classes.html), however, there are some stormpy-specific things in this document.

File paths below are relative to the stormpy repository root unless explicitly marked as belonging to the Storm repository. C++ `#include` paths remain relative to their include search paths.

## General architecture of bindings

Stormpy employs a two-layer implementation of bindings. 

- The bottom layer uses pybind11 to provide the bindings of the Storm side. All Storm bindings need to be declared on the C++ side in `src`. These bindings will be declared in stormpy as _private_ methods/classes in `_binding`. They are hidden from the public API.
- The second (higher) layer provides the public Python API and makes use of the pybind11 layer. The public Python API is defined on the Python side in `lib/stormpy`, which re-exports the private bindings from C++ and/or defines new Python abstractions. The Python API then explicitly calls the private bindings.

## Step 1: Creating a C++ binding

Suppose that we want to bind the following class in Storm to Python. Inspired by the [pybind11 tutorial](https://pybind11.readthedocs.io/en/stable/advanced/classes.html), we are going to add a dog:

```{code-block} cpp
:caption: `src/storm-animal/Dog.h` (Storm repository)

#include <cstdint>
#include <string>

namespace storm::animal {
class Dog {
   public:
    Dog(std::string name, uint64_t age);
    bool isHappy();
    std::string bark(uint64_t numberOfBarks);
    // ...
};
} // namespace storm::animal
```

Suppose `Dog` is declared in the hypothetical header {file}`src/storm-animal/Dog.h` in the Storm repository, in the module `storm-animal`. In {file}`src/animal/`, you will find the list of bindings for this Storm module.
Let's create a new binding for dog by creating {file}`src/animal/dog.h` and {file}`src/animal/dog.cpp`.


```{code-block} cpp
:caption: `src/animal/dog.h`

#pragma once

#include "src/core/common.h"

void define_dog(py::module& m);
```

The following code applies if your `Dog` is not generic, i.e., is not a template class. If it _is_ a template class, see {ref}`binding-template-classes`.

```{code-block} cpp
:caption: `src/animal/dog.cpp`

#include "dog.h"

#include <storm-animal/Dog.h>

// Define python bindings
void define_dog(py::module& m) {
    py::classh<storm::animal::Dog>(m, "Dog", "A dog is an interesting animal")
        .def(py::init<std::string, uint64_t>(), py::arg("name"), py::arg("age")) // Exposes the constructor
        .def_property_readonly("is_happy", &storm::animal::Dog::isHappy, "Whether the dog is happy") // Creates a property calling this method
        .def("bark", &storm::animal::Dog::bark, py::arg("number_of_barks"), "Make the dog bark the given number of times"); // Creates a method
}
```

That's done! Note that we use `py::classh` instead of `py::class_` to make use of pybind11's [smart holder](https://pybind11.readthedocs.io/en/stable/advanced/smart_ptrs.html#py-smart-holder).
We still need to include {file}`src/animal/dog.h` and call `define_dog` in {file}`src/mod_animal.cpp`:

```{code-block} cpp
:caption: `src/mod_animal.cpp`

#include "animal/dog.h"

PYBIND11_MODULE(_animal, m) {
    m.doc() = "animal";
    // ...

    define_cat(m);
    define_dog(m); // <-- put this here!

    // ...
}
```

## Step 2: Re-exporting to Stormpy

The `Dog` is now defined in the path `stormpy.animal._animal.Dog`. We still need to re-export it to the public Python namespace by adding the following to {file}`lib/stormpy/animal/__init__.py`:

```{code-block} python
:caption: `lib/stormpy/animal/__init__.py`

from ._animal import Dog
```

## Step 3: Adding tests

The last step is to add tests for your bindings. The tests are in {file}`tests/animal/` (files named `test_*.py`). Either create a new file or add your tests to an appropriate existing one. What an appropriate test is is usually more specific to what you are actually binding. For example:

```{code-block} python
:caption: `tests/animal/test_animals.py`

from stormpy.animal import Dog


class TestAnimals:
    def test_dog_bark(self):
        dog = Dog("Bob the Railway Dog", 148)
        assert dog.bark(2) == "Bark Bark"
```

After adding the binding and its tests, rebuild stormpy and run the tests from the repository root in your activated development environment:

```bash
pip install -e '.[test]'
pytest tests/animal/test_animals.py
```

(binding-template-classes)=
## Adding bindings to template classes

Suppose our `Dog` takes one template parameter `ValueType` and uses it for the age instead of `uint64_t`. Its declaration in {file}`src/storm-animal/Dog.h` in the Storm repository would now be:

```{code-block} cpp
:caption: `src/storm-animal/Dog.h` (Storm repository)

#include <cstdint>
#include <string>

namespace storm::animal {
template<typename ValueType>
class Dog {
   public:
    Dog(std::string name, ValueType age);
    bool isHappy();
    std::string bark(uint64_t numberOfBarks);
    // ...
};
} // namespace storm::animal
```

Let's bind it generically! Define the binding like this:

```{code-block} cpp
:caption: `src/animal/dog.h`

#pragma once

#include "src/core/common.h"

template<typename ValueType> // <- add this
void define_dog(py::module& m);
```

```{code-block} cpp
:caption: `src/animal/dog.cpp`

#include "dog.h"

#include <storm-animal/Dog.h>

#include "src/binding_type_index.h"

template<typename ValueType> // <- add this
void define_dog(py::module& m) {
    // next line calls a different binding function
    stormpy::bindings::bindTemplateClass<storm::animal::Dog<ValueType>>(
        m, "Dog", stormpy::bindings::typeIndex<ValueType>(), "A dog is an interesting animal")
        .def(py::init<std::string, ValueType>(), py::arg("name"), py::arg("age")) // Exposes the constructor
        .def_property_readonly("is_happy", &storm::animal::Dog<ValueType>::isHappy, "Whether the dog is happy") // Creates a property calling this method
        .def("bark", &storm::animal::Dog<ValueType>::bark, py::arg("number_of_barks"), "Make the dog bark the given number of times"); // Creates a method
}

// Explicitly instantiate all of the types you want to support
template void define_dog<double>(py::module& m);
template void define_dog<storm::RationalNumber>(py::module& m);
```

In `mod_animal.cpp`, call `define_dog` on all `ValueType`s that you want to support:


```{code-block} cpp
:caption: `src/mod_animal.cpp`

#include "animal/dog.h"

PYBIND11_MODULE(_animal, m) {
    m.doc() = "animal";
    // ...

    define_cat(m);
    define_dog<double>(m); // <-- put this here!
    define_dog<storm::RationalNumber>(m); // <-- put this here!

    // ...
}
```

Re-export it in Python as follows:

```{code-block} python
:caption: `lib/stormpy/animal/__init__.py`

from . import _animal
from stormpy._template import TemplateClass

Dog = TemplateClass("stormpy.animal.Dog", _animal, parameters=("ValueType",))
```

The first argument `stormpy.animal.Dog` corresponds to the full Python path of the class, the second argument `_animal` gives the containing module and the third argument `("ValueType",)` names all template parameters.

### Deduction guides

You can now instantiate typed dogs with `Dog[float]` and `Dog[RationalNumber]`.

For our Dog, it would be redundant to construct it like this:

```py
d = Dog[float]("Bonn-Oberkassel dog", 14000.5)
```

As `14000.5` is clearly a float, the following should work as well and automatically give us a `Dog[float]`:

```py
d = Dog("Bonn-Oberkassel dog", 14000.5)
```

By default, stormpy can automatically deduce the right type based on the first argument.
However, in our case, the first argument does not provide the type, but the second argument does. We therefore need to provide a custom _deduction guide_ which returns the right type.

In {file}`lib/stormpy/animal/__init__.py`, replace the earlier `Dog` declaration with:

```{code-block} python
:caption: `lib/stormpy/animal/__init__.py`

from stormpy._template import TemplateClass


def _deduce_dog(_family, args, kwargs):
    if len(args) >= 2:
        age = args[1]
    elif "age" in kwargs:
        age = kwargs["age"]
    else:
        raise TypeError("Cannot deduce Dog's ValueType without the age argument")
    return (type(age),)


Dog = TemplateClass(
    "stormpy.animal.Dog",
    _animal,
    parameters=("ValueType",),
    deduce=_deduce_dog,
)
```

Then we can do this:

```py
d = Dog("Bonn-Oberkassel dog", 14000.5)
assert type(d) is Dog[float]

d = Dog(name="Bonn-Oberkassel dog", age=14000.5)
assert type(d) is Dog[float]
```

There are also some pre-defined deduction guides in {file}`lib/stormpy/_template.py`:

- `deduce_from_first_argument` deduces from the type of the first argument.

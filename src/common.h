#pragma once

#include "config.h"

#include <pybind11/operators.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <tuple>

namespace py = pybind11;
using namespace pybind11::literals;

#if PY_MAJOR_VERSION >= 3
#define PY_DIV "__truediv__"
#define PY_RDIV "__rtruediv__"
#else
#define PY_DIV "__div__"
#define PY_RDIV "__rdiv__"
#endif

PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>)
PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T const>)

#include "boost.h"

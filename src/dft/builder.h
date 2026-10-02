#pragma once

#include "src/dft/common.h"

void define_builder(py::module& m);

template<typename ValueType>
void define_builder_typed(py::module& m);

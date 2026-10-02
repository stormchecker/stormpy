#pragma once

#include "src/dft/common.h"

void define_storage_elements(py::module& m);

template<typename ValueType>
void define_storage_elements_typed(py::module& m);

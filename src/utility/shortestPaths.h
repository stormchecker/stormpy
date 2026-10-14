#pragma once

#include "src/common.h"

void define_ksp(py::module& m);

template<typename ValueType>
void define_ksp_typed(py::module& m);

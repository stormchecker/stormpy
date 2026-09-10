#pragma once

#include "src/dft/common.h"

template<typename ValueType>
void define_dft_state(py::module& m);

void define_failable_elements(py::module& m);

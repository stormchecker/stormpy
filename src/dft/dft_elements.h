#pragma once

#include "src/dft/common.h"

void define_dft_elements(py::module& m);

template<typename ValueType>
void define_dft_elements_typed(py::module& m, std::string const& vt_suffix);

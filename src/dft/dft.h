#pragma once

#include "src/dft/common.h"

void define_dft(py::module& m);

template<typename ValueType>
void define_dft_typed(py::module& m, std::string const& vt_suffix);

void define_symmetries(py::module& m);

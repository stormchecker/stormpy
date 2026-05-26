#pragma once

#include "src/common.h"

void define_maximal_end_components(py::module& m);

template<typename ValueType>
void define_maximal_end_component_decomposition(py::module& m, std::string const& vt_suffix);

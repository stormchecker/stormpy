#pragma once

#include "src/dft/common.h"

void define_analysis(py::module& m);

template<typename ValueType>
void define_analysis_typed(py::module& m);

void define_input(py::module& m);
void define_output(py::module& m);

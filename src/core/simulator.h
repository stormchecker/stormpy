#pragma once

#include "src/core/common.h"

template<typename ValueType>
void define_sparse_model_simulator(py::module& m);

template<typename ValueType>
void define_prism_program_simulator(py::module& m);
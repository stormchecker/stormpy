#pragma once

#include "src/pomdp/common.h"

void define_transformations_nt(py::module& m);
template<typename ValueType>
void define_transformations(py::module& m);
template<typename ValueType>
void define_observation_trace_unfolder(py::module& m);

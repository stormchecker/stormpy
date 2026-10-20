#pragma once

#include <storm/dd/DdType.h>

#include "src/common.h"

void define_model(py::module& m);
template<typename ValueType>
void define_sparse_model(py::module& m);
template<storm::dd::DdType DdType, typename ValueType>
void define_symbolic_model(py::module& m);

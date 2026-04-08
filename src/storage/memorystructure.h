#pragma once
#include "common.h"

void define_memorystructure_untyped(py::module& m);
template<typename ValueType>
void define_memorystructure_typed(py::module& m, std::string const& vt);
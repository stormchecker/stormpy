#pragma once

#include "src/core/common.h"

void define_result(py::module& m);

template<typename ValueType>
void define_typed_result(py::module& m, std::string const& vtSuffix);

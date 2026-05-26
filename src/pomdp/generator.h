#pragma once

#include "src/pomdp/common.h"

template<typename ValueType>
void define_verimon_generator(py::module& m, std::string const& vtSuffix);

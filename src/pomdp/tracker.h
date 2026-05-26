#pragma once

#include "src/pomdp/common.h"

template<typename ValueType>
void define_tracker(py::module& m, std::string const& vtSuffix);

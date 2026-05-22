#pragma once

#include "src/pomdp/common.h"

template<typename VT>
void define_belief_exploration(py::module& m, std::string const& vtSuffix);
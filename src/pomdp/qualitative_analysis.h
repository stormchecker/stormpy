#pragma once

#include "src/pomdp/common.h"

template<typename VT>
void define_qualitative_policy_search(py::module& m, std::string const& vtSuffix);
void define_qualitative_policy_search_nt(py::module& m);
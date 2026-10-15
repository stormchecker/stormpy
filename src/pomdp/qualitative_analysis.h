#pragma once

#include "src/pomdp/common.h"

template<typename ValueType>
void define_qualitative_policy_search(py::module& m);
void define_qualitative_policy_search_nt(py::module& m);

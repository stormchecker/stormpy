#pragma once

#include "src/pomdp/common.h"

template<typename ValueType>
void define_belief_verification(py::module& m);
void define_belief_verification_nt(py::module& m);

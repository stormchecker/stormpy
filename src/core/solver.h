#pragma once

#include "src/core/common.h"

namespace stormpy {

void define_solver(py::module& m);
void define_smt_solver(py::module& m);

}  // namespace stormpy

#pragma once

#include "src/core/common.h"

void define_core(py::module& m);
void define_parse(py::module& m);
void define_build(py::module& m);
void define_export(py::module& m);
void define_optimality_type(py::module& m);
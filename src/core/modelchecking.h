#pragma once

#include "common.h"

template<typename ValueType>
void define_check_task(py::module& m, std::string const& name);

void define_modelchecking(py::module& m);

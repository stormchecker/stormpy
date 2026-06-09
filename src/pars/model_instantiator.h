#pragma once

#include "src/pars/common.h"

template<typename ValueType>
void define_model_instantiator(py::module& m);

template<typename ValueType>
void define_model_instantiation_checker(py::module& m);

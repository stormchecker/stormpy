#pragma once

#include "common.h"

void define_transformation(py::module& m);
template<typename ValueType>
void define_transformation_typed(py::module& m, std::string const& suffix);
template<typename ValueType>
void define_transformation_typed_only_numbers(py::module& m, std::string const& vtSuffix);

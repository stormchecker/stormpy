#pragma once

#include "common.h"

void define_transformations_nt(py::module &m);
template <typename VT>
void define_transformations(py::module &m, std::string const &vtSuffix);
template <typename VT>
void define_transformations_int(py::module &m, std::string const &vtSuffix);

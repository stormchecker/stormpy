#pragma once

#include <storm/storage/dd/DdType.h>
#include "common.h"

template<storm::dd::DdType DdType>
void define_dd(py::module& m, std::string const& libname);
void define_dd_nt(py::module& m);
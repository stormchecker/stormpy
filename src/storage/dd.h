#pragma once

#include <storm/storage/dd/Dd.h>
#include <storm/storage/dd/DdType.h>

#include "src/common.h"

template<storm::dd::DdType DdType>
py::class_<storm::dd::Dd<DdType>> define_dd(py::module& m, std::string const& libname);
template<storm::dd::DdType DdType, typename ValueType>
void define_dd_typed(py::module& m, std::string const& libstring, std::string const& valueSuffix, py::class_<storm::dd::Dd<DdType>> const& dd);

void define_dd_nt(py::module& m);

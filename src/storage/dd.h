#pragma once

#include <storm/dd/Dd.h>
#include <storm/dd/DdType.h>

#include "src/common.h"

template<storm::dd::DdType DdType>
py::classh<storm::dd::Dd<DdType>> define_dd(py::module& m);
template<storm::dd::DdType DdType, typename ValueType>
void define_dd_typed(py::module& m, py::classh<storm::dd::Dd<DdType>> const& dd);

void define_dd_nt(py::module& m);

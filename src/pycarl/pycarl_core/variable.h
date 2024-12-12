/*
 * variable.h
 *
 *  Created on: 16 Apr 2016
 *      Author: harold
 */

#ifndef PYTHON_PYCARL_CORE_VARIABLE_H_
#define PYTHON_PYCARL_CORE_VARIABLE_H_

#include "src/pycarl/common.h"

void define_variabletype(py::module& m);
void define_variable(py::module& m);

#endif /* PYTHON_PYCARL_CORE_VARIABLE_H_ */

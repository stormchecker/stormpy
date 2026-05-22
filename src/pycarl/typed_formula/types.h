#pragma once

#include <carl/core/SimpleConstraint.h>
#include <carl/formula/Constraint.h>
#include <carl/formula/Formula.h>

#include "src/pycarl/types.h"

typedef carl::Constraint<Polynomial> Constraint;
typedef carl::SimpleConstraint<Polynomial> SimpleConstraint;
typedef carl::SimpleConstraint<FactorizedRationalFunction> SimpleConstraintRatFunc;
typedef carl::Formula<Polynomial> Formula;

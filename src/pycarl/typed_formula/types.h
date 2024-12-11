
#include "src/pycarl/types.h"

#include <carl/formula/Constraint.h>
#include <carl/core/SimpleConstraint.h>
#include <carl/formula/Formula.h>

typedef carl::Constraint<Polynomial> Constraint;
typedef carl::SimpleConstraint<Polynomial> SimpleConstraint;
typedef carl::SimpleConstraint<FactorizedRationalFunction> SimpleConstraintRatFunc;
typedef carl::Formula<Polynomial> Formula;


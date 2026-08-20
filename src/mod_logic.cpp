#include "src/logic/formulae.h"
#include "src/module_bindings.h"

namespace stormpy::bindings {

void bindLogic(py::module& m) {
    define_formulae(m);
}

}  // namespace stormpy::bindings

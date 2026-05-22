#include "src/common.h"
#include "src/gspn/gspn.h"
#include "src/gspn/gspn_io.h"

PYBIND11_MODULE(_gspn, m) {
    m.doc() = "Support for GSPNs";

#ifdef STORMPY_DISABLE_SIGNATURE_DOC
    py::options options;
    options.disable_function_signatures();
#endif

    define_gspn(m);
    define_gspn_io(m);
}

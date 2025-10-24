#include "common.h"
#include "storm-version-info/storm-version.h"

PYBIND11_MODULE(_info, m) {
    m.doc() = "Storm information";

#ifdef STORMPY_DISABLE_SIGNATURE_DOC
    py::options options;
    options.disable_function_signatures();
#endif

    py::class_<storm::StormVersion>(m, "Version", "Version information for Storm")
        // static properties are still called with self as argument (which we ignore), see
        // https://pybind11.readthedocs.io/en/stable/advanced/classes.html#static-properties
        .def_property_readonly_static("major", [](py::object /* self */){ return storm::StormVersion::versionMajor; }, "Storm major version.")
        .def_property_readonly_static("minor", [](py::object /* self */){ return storm::StormVersion::versionMinor; }, "Storm minor version.")
        .def_property_readonly_static("patch", [](py::object /* self */){ return storm::StormVersion::versionPatch; }, "Storm patch version.")
        .def_property_readonly_static("development", [](py::object /* self */){ return storm::StormVersion::versionDev; }, "Flag if Storm is development version.")
        .def_property_readonly_static("short", [](py::object /* self */){ return storm::StormVersion::shortVersionString(); }, "Storm version in short representation.")
        .def_property_readonly_static("long", [](py::object /* self */){ return storm::StormVersion::longVersionString(); }, "Storm version in long representation.")
        .def_property_readonly_static("build_info", [](py::object /* self */){ return storm::StormVersion::buildInfo(); }, "Build info for Storm.")
    ;
}

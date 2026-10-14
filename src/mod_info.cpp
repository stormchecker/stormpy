#include <storm-version-info/storm-version.h>

#include "src/common.h"

PYBIND11_MODULE(_info, m) {
    m.doc() = "Storm information";

#ifdef STORMPY_DISABLE_SIGNATURE_DOC
    py::options options;
    options.disable_function_signatures();
#endif

    py::classh<storm::StormVersion>(m, "StormVersion", "Version information for Storm")
        // static properties are still called with self as argument (which we ignore), see
        // https://pybind11.readthedocs.io/en/stable/advanced/classes.html#static-properties
        .def_property_readonly_static(
            "version_major", [](py::object /* self */) { return storm::StormVersion::versionMajor; }, "Storm major version.")
        .def_property_readonly_static(
            "version_minor", [](py::object /* self */) { return storm::StormVersion::versionMinor; }, "Storm minor version.")
        .def_property_readonly_static(
            "version_patch", [](py::object /* self */) { return storm::StormVersion::versionPatch; }, "Storm patch version.")
        .def_property_readonly_static(
            "version_dev", [](py::object /* self */) { return storm::StormVersion::versionDev; }, "Flag if Storm is development version.")
        .def_property_readonly_static(
            "git_revision_hash", [](py::object /* self */) { return storm::StormVersion::gitRevisionHash; }, "Git commit hash from which Storm was built.")
        .def_static("short_version_string", &storm::StormVersion::shortVersionString, "Storm version in short representation.")
        .def_static("long_version_string", &storm::StormVersion::longVersionString, "Storm version in long representation.")
        .def_static("build_info", &storm::StormVersion::buildInfo, "Build info for Storm.");
}

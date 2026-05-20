#include "gspn_io.h"
#include "src/helpers.h"
#include "storm-gspn/parser/GspnParser.h"
#include "storm-gspn/storage/gspn/GSPN.h"

using GSPN = storm::gspn::GSPN;
using GSPNParser = storm::parser::GspnParser;
using GSPNJaniBuilder = storm::builder::JaniGSPNBuilder;

void define_gspn_io(py::module& m) {
    // GspnParser class
    py::class_<GSPNParser, std::shared_ptr<GSPNParser>>(m, "GSPNParser")
        .def(py::init<>())
        .def(
            "parse",
            [](GSPNParser& p, std::string const& filename, std::string const& constantDefinitions) -> GSPN& {
                return *(p.parse(filename, constantDefinitions));
            },
            "filename"_a, "constant_definitions"_a = "");

    // GspnToJani builder
    py::class_<GSPNJaniBuilder, std::shared_ptr<GSPNJaniBuilder>>(m, "GSPNToJaniBuilder")
        .def(py::init<GSPN const&>(), py::arg("gspn"))
        .def("build", &GSPNJaniBuilder::build, py::arg("automaton_name") = "gspn_automaton", "Build Jani model from GSPN")
        .def("create_deadlock_properties", &GSPNJaniBuilder::getDeadlockProperties, py::arg("jani_model"), "Create standard properties for deadlocks");
}

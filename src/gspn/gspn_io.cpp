#include "gspn_io.h"

#include <storm-gspn/parser/GspnParser.h>
#include <storm-gspn/storage/gspn/GSPN.h>

#include "src/helpers.h"

using GSPN = storm::gspn::GSPN;
using GspnParser = storm::parser::GspnParser;
using JaniGSPNBuilder = storm::builder::JaniGSPNBuilder;

void define_gspn_io(py::module& m) {
    // GspnParser class
    py::classh<GspnParser>(m, "GspnParser", "Parser for GSPNs in the PNML or PNPRO format")
        .def_static(
            "parse",
            [](std::string const& filename, std::string const& constantDefinitions) {
                return std::unique_ptr<GSPN>(GspnParser::parse(filename, constantDefinitions));
            },
            "filename"_a, "constant_definitions"_a = "", "Parse a GSPN from a file");

    // JaniGSPNBuilder class
    py::classh<JaniGSPNBuilder>(m, "JaniGSPNBuilder", "Builder translating a GSPN into a JANI model")
        // The builder keeps a reference to the GSPN
        .def(py::init<GSPN const&>(), "gspn"_a, py::keep_alive<1, 2>())
        .def("build", &JaniGSPNBuilder::build, "automaton_name"_a = "gspn_automaton", "Build Jani model from GSPN")
        .def("get_deadlock_properties", &JaniGSPNBuilder::getDeadlockProperties, "model"_a,
             "Get standard properties (reachability, time bounded reachability, expected time) for deadlocks");
}

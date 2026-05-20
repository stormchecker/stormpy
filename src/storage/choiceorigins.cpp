#include "choiceorigins.h"
#include "storm/adapters/JsonAdapter.h"
#include "storm/storage/jani/Model.h"
#include "storm/storage/sparse/JaniChoiceOrigins.h"
#include "storm/storage/sparse/PrismChoiceOrigins.h"

using ChoiceOrigins = storm::storage::sparse::ChoiceOrigins;
using JaniChoiceOrigins = storm::storage::sparse::JaniChoiceOrigins;
using PrismChoiceOrigins = storm::storage::sparse::PrismChoiceOrigins;

void define_origins(py::module& m) {
    py::class_<ChoiceOrigins, std::shared_ptr<ChoiceOrigins>> co(m, "ChoiceOrigins",
                                                                 "This class represents the origin of choices of a model in terms of the input model spec.");
    co.def("is_prism_choice_origins", &ChoiceOrigins::isPrismChoiceOrigins)
        .def("is_jani_choice_origins", &ChoiceOrigins::isJaniChoiceOrigins)
        .def("as_prism_choice_origins", [](ChoiceOrigins& co) -> PrismChoiceOrigins& { return co.asPrismChoiceOrigins(); })
        .def("as_jani_choice_origins", [](ChoiceOrigins& co) -> JaniChoiceOrigins& { return co.asJaniChoiceOrigins(); })
        .def("get_identifier_info", &ChoiceOrigins::getIdentifierInfo, "identifier"_a, "human readable string")
        .def("get_choice_info", &ChoiceOrigins::getChoiceInfo, "identifier"_a, "human readable string")
        .def("get_number_of_identifiers", &ChoiceOrigins::getNumberOfIdentifiers, "the number of considered identifier");

    py::class_<JaniChoiceOrigins, std::shared_ptr<JaniChoiceOrigins>>(m, "JaniChoiceOrigins",
                                                                      "This class represents for each choice the origin in the jani spec.", co)
        .def(py::init<std::shared_ptr<storm::jani::Model const> const&, std::vector<uint_fast64_t> const&,
                      std::vector<JaniChoiceOrigins::EdgeIndexSet> const&>(),
             "jani_model"_a, "index_to_identifier_mapping"_a, "identifier_to_edge_index__set_mapping"_a)
        .def_property_readonly("model", &JaniChoiceOrigins::getModel, "retrieves the associated JANI model")
        .def(
            "get_edge_index_set", [](JaniChoiceOrigins const& co, uint64_t choice) -> auto& { return co.getEdgeIndexSet(choice); },
            "returns the set of edges that induced the choice", py::arg("choice_index"));

    py::class_<PrismChoiceOrigins, std::shared_ptr<PrismChoiceOrigins>>(
        m, "PrismChoiceOrigins", "This class represents for each choice the set of prism commands that induced the choice.", co)
        .def(py::init<std::shared_ptr<storm::prism::Program const> const&, std::vector<uint_fast64_t> const&,
                      std::vector<PrismChoiceOrigins::CommandSet> const&>(),
             "prism_program"_a, "index_to_identifier_mapping"_a, "identifier_to_command_set_mapping"_a)
        .def_property_readonly("program", &PrismChoiceOrigins::getProgram, "retrieves the associated Prism program")
        .def(
            "get_command_set", [](PrismChoiceOrigins const& co, uint64_t choice) -> auto& { return co.getCommandSet(choice); },
            "Returns the set of prism commands that induced the choice", py::arg("choice_index"));
}
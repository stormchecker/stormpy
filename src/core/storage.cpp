#include "storage.h"

#include <storm/languages/SymbolicModelDescription.h>
#include <storm/languages/jani/Model.h>
#include <storm/languages/jani/ModelType.h>
#include <storm/languages/jani/Property.h>
#include <storm/languages/prism/Program.h>
#include <storm/storage/BoostTypes.h>
#include <storm/storage/scheduler/SchedulerClass.h>

#include "src/helpers.h"

namespace stormpy {

using SymbolicModelDescription = storm::languages::SymbolicModelDescription;
using ConstantDefinitions = std::map<storm::expressions::Variable, storm::expressions::Expression>;

void define_storage(py::module& m) {
    using FlatSet = storm::storage::FlatSet<uint64_t>;
    py::classh<FlatSet>(m, "FlatSet", "Flat set of integers")
        .def(py::init<>())
        .def(py::init<FlatSet>(), "other"_a)
        .def(
            "insert", [](FlatSet& flatset, uint64_t value) { flatset.insert(value); }, "Insert value", py::arg("value"))
        .def(
            "is_subset_of", [](FlatSet const& left, FlatSet const& right) { return std::includes(right.begin(), right.end(), left.begin(), left.end()); },
            "Whether this set is a subset of the other set", py::arg("other"))
        .def(
            "insert_set", [](FlatSet& left, FlatSet const& additional) { left.insert(additional.begin(), additional.end()); },
            "Insert all values of the other set", py::arg("other"))
        .def("__str__", &storm::storage::toString<uint64_t>)
        .def("__len__", &FlatSet::size)
        .def(
            "__iter__", [](FlatSet& v) { return py::make_iterator(v.begin(), v.end()); }, py::keep_alive<0, 1>()) /* Keep set alive while iterator is used */
        ;

    py::classh<storm::jani::Property>(m, "Property", "Property consisting of a name and a formula")
        .def(py::init<std::string const&, std::shared_ptr<storm::logic::Formula const> const&, std::set<storm::expressions::Variable> const&,
                      std::string const&>(),
             "Construct property from formula", py::arg("name"), py::arg("formula"), py::arg("undefined_constants"), py::arg("comment") = "")
        .def(py::init<storm::jani::Property>(), "Copy property", py::arg("other"))
        .def("clone", &storm::jani::Property::clone, "Return a deep copy of the property, preserving its name, comment, filter, and undefined constants")
        .def("get_name", &storm::jani::Property::getName, "Get the name of the property")
        .def("get_comment", &storm::jani::Property::getComment, "Get the comment of the property")
        .def("get_raw_formula", &storm::jani::Property::getRawFormula, "Get the formula of the property")
        .def("get_undefined_constants", &storm::jani::Property::getUndefinedConstants, "Get the undefined constants occurring in the property")
        .def("contains_undefined_constants", &storm::jani::Property::containsUndefinedConstants, "Whether the property contains undefined constants")
        .def("substitute", py::overload_cast<ConstantDefinitions const&>(&storm::jani::Property::substitute, py::const_), "Substitute variables by expressions",
             py::arg("substitution"))
        .def("__str__", &streamToString<storm::jani::Property>);

    py::native_enum<storm::jani::ModelType>(m, "JaniModelType", "enum.Enum", "Type of the Jani model")
        .value("UNDEFINED", storm::jani::ModelType::UNDEFINED)
        .value("LTS", storm::jani::ModelType::LTS)
        .value("DTMC", storm::jani::ModelType::DTMC)
        .value("CTMC", storm::jani::ModelType::CTMC)
        .value("MDP", storm::jani::ModelType::MDP)
        .value("CTMDP", storm::jani::ModelType::CTMDP)
        .value("MA", storm::jani::ModelType::MA)
        .value("TA", storm::jani::ModelType::TA)
        .value("PTA", storm::jani::ModelType::PTA)
        .value("STA", storm::jani::ModelType::STA)
        .value("HA", storm::jani::ModelType::HA)
        .value("PHA", storm::jani::ModelType::PHA)
        .value("SHA", storm::jani::ModelType::SHA)
        .finalize();

    py::classh<SymbolicModelDescription>(m, "SymbolicModelDescription", "Symbolic description of a model (Prism program or Jani model)")
        .def(py::init<>(), "Create empty description")
        .def(py::init<storm::prism::Program const&>(), "Construct from Prism program", py::arg("program"))
        .def(py::init<storm::jani::Model const&>(), "Construct from Jani model", py::arg("model"))
        .def("has_model", &SymbolicModelDescription::hasModel, "Whether the description contains a model")
        .def("is_prism_program", &SymbolicModelDescription::isPrismProgram, "Whether the description is a Prism program")
        .def("is_jani_model", &SymbolicModelDescription::isJaniModel, "Whether the description is a Jani model")
        .def("as_prism_program", py::overload_cast<>(&SymbolicModelDescription::asPrismProgram, py::const_), "Get the Prism program")
        .def("as_jani_model", py::overload_cast<>(&SymbolicModelDescription::asJaniModel, py::const_), "Get the Jani model")
        .def("get_parameter_names", &SymbolicModelDescription::getParameterNames, "Get the names of the parameters")
        .def("has_undefined_constants", &SymbolicModelDescription::hasUndefinedConstants, "Whether the description has undefined constants")
        .def("get_undefined_constants", &SymbolicModelDescription::getUndefinedConstants, "Get the undefined constants")
        .def("parse_constant_definitions", &SymbolicModelDescription::parseConstantDefinitions, "Parse a string of constant definitions",
             py::arg("constant_definition_string"))
        .def("preprocess", py::overload_cast<ConstantDefinitions const&>(&SymbolicModelDescription::preprocess, py::const_),
             "Substitute the given constant definitions", py::arg("constant_definitions"))
        .def("preprocess", py::overload_cast<std::string const&>(&SymbolicModelDescription::preprocess, py::const_),
             "Substitute the constant definitions given as string", py::arg("constant_definition_string") = "")
        .def("__str__", &streamToString<SymbolicModelDescription>);

    // Prism programs and Jani models can be converted into SymbolicModelDescription
    py::implicitly_convertible<storm::prism::Program, SymbolicModelDescription>();
    py::implicitly_convertible<storm::jani::Model, SymbolicModelDescription>();

    m.def("parse_constant_definition_string", &storm::languages::parseConstantDefinitionString, "Parse a string of constant definitions", py::arg("manager"),
          py::arg("constant_definition_string"));

    py::native_enum<storm::storage::SchedulerClass::MemoryPattern>(m, "SchedulerMemoryPattern", "enum.Enum", "Memory pattern of a scheduler")
        .value("ARBITRARY", storm::storage::SchedulerClass::MemoryPattern::Arbitrary)
        .value("GOAL_MEMORY", storm::storage::SchedulerClass::MemoryPattern::GoalMemory)
        .value("COUNTER", storm::storage::SchedulerClass::MemoryPattern::Counter)
        .finalize();

    py::classh<storm::storage::SchedulerClass>(m, "SchedulerClass", "Class of schedulers")
        .def(py::init<>(), "Create class of arbitrary schedulers")
        .def_property(
            "is_deterministic", &storm::storage::SchedulerClass::isDeterministic,
            [](storm::storage::SchedulerClass& sc, bool value) { sc.setIsDeterministic(value); }, "Whether schedulers are deterministic")
        .def_property(
            // Thin wrapper mapping unbounded memory to None
            "memory_states",
            [](storm::storage::SchedulerClass const& sc) -> py::object {
                if (sc.isMemoryBounded()) {
                    return py::cast(sc.getMemoryStates());
                }
                return py::none();
            },
            [](storm::storage::SchedulerClass& sc, py::object value) {
                if (value.is_none()) {
                    sc.unsetMemoryStates();
                } else {
                    sc.setMemoryStates(value.cast<uint64_t>());
                }
            },
            "Number of memory states (None if unbounded)")
        .def("is_memory_bounded", &storm::storage::SchedulerClass::isMemoryBounded, "Whether the memory is bounded")
        .def("is_positional", &storm::storage::SchedulerClass::isPositional, "Whether schedulers are positional")
        .def("get_memory_pattern", &storm::storage::SchedulerClass::getMemoryPattern, "Get the memory pattern")
        .def(
            "set_memory_pattern",
            [](storm::storage::SchedulerClass& sc, storm::storage::SchedulerClass::MemoryPattern pattern) { sc.setMemoryPattern(pattern); },
            "Set the memory pattern", py::arg("pattern"))
        .def("set_positional", [](storm::storage::SchedulerClass& sc) { sc.setPositional(); }, "Restrict to positional schedulers");
}

}  // namespace stormpy

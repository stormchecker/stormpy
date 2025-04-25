#include "gspn.h"
#include "src/helpers.h"
#include "storm-gspn/storage/gspn/GSPN.h"
#include "storm-gspn/storage/gspn/GspnBuilder.h"
#include "storm/settings/SettingsManager.h"
#include "storm/io/file.h"

using GSPN = storm::gspn::GSPN;
using GSPNBuilder = storm::gspn::GspnBuilder;
using LayoutInfo = storm::gspn::LayoutInfo;
using Place = storm::gspn::Place;
using TimedTransition = storm::gspn::TimedTransition<GSPN::RateType>;
using ImmediateTransition = storm::gspn::ImmediateTransition<GSPN::WeightType>;
using Transition = storm::gspn::Transition;
using TransitionPartition = storm::gspn::TransitionPartition;


void gspnToFile(GSPN const& gspn, std::string const& filepath, bool toPnpro) {
    std::ofstream fs;
    storm::io::openFile(filepath, fs);

    if(toPnpro) {
        gspn.toPnpro(fs);
    }
    else {
        gspn.toPnml(fs);
    }
    storm::io::closeFile(fs);
}


void define_gspn(py::module& m) {

    // GSPN_Builder class
    py::class_<GSPNBuilder, std::shared_ptr<GSPNBuilder>>(m, "GSPNBuilder", "Generalized Stochastic Petri Net Builder")
        .def(py::init(), "Constructor")
        .def("set_name", &GSPNBuilder::setGspnName, "Set name of GSPN", "name"_a)

        .def("add_place", &GSPNBuilder::addPlace, "Add a place to the GSPN", py::arg("capacity") = 1, py::arg("initial_tokens") = 0, py::arg("name") = "")
        .def("set_place_layout_info", &GSPNBuilder::setPlaceLayoutInfo, py::arg("place_id"), py::arg("layout_info"), R"doc(
             Set place layout information.

            :param uint64_t id: The ID of the place.
            :param stormpy.LayoutInfo layout_info: The layout information.
        )doc")

        .def("add_immediate_transition", &GSPNBuilder::addImmediateTransition, "Add an immediate transition to the GSPN", "priority"_a = 0, "weight"_a = 0, "name"_a = "")
        .def("add_timed_transition", py::overload_cast<uint_fast64_t const&, double const& , std::string const&>(&GSPNBuilder::addTimedTransition), "Add a timed transition to the GSPN", "priority"_a, "rate"_a, "name"_a = "")
        .def("add_timed_transition", py::overload_cast<uint_fast64_t const&, double const& , boost::optional<uint64_t> const&, std::string const&>(&GSPNBuilder::addTimedTransition), "priority"_a, "rate"_a, "num_servers"_a, "name"_a = "")
        .def("set_transition_layout_info", &GSPNBuilder::setTransitionLayoutInfo, "transition_id"_a, "layout_info"_a, R"doc(
             Set transition layout information.

            :param uint64_t id: The ID of the transition.
            :param stormpy.LayoutInfo layout_info: The layout information.
        )doc")

        .def("add_input_arc", py::overload_cast<uint_fast64_t const&, uint_fast64_t const&, uint_fast64_t const&>(&GSPNBuilder::addInputArc), "from"_a , "to"_a,  "multiplicity"_a = 1, R"doc(
             Add a new input arc from a place to a transition

            :param from: The ID or name of the place from which the arc is originating.
            :type from: uint_64_t or str
            :param uint_64_t to: The ID or name of the transition to which the arc goes to.
            :type from: uint_64_t or str
            :param uint64_t multiplicity: The multiplicity of the arc, default = 1.
        )doc")
        .def("add_input_arc", py::overload_cast<std::string const&, std::string const&, uint64_t>(&GSPNBuilder::addInputArc), "from"_a,  "to"_a, "multiplicity"_a = 1)
        .def("add_inhibition_arc", py::overload_cast<uint_fast64_t const&, uint_fast64_t const&, uint_fast64_t const&>(&GSPNBuilder::addInhibitionArc), "from"_a,  "to"_a,  "multiplicity"_a = 1, R"doc(
             Add an new inhibition arc from a place to a transition.

            :param from: The ID or name of the place from which the arc is originating.
            :type from: uint_64_t or str
            :param to: The ID or name of the transition to which the arc goes to.
            :type to: uint_64_t or str
            :param uint64_t multiplicity: The multiplicity of the arc, default = 1.
        )doc")
        .def("add_inhibition_arc", py::overload_cast<std::string const&, std::string const&, uint64_t>(&GSPNBuilder::addInhibitionArc), "from"_a,  "to"_a,  "multiplicity"_a = 1)
        .def("add_output_arc", py::overload_cast<uint_fast64_t const&, uint_fast64_t const&, uint_fast64_t const&>(&GSPNBuilder::addOutputArc), "from"_a,  "to"_a,  "multiplicity"_a = 1, R"doc(
             Add an new output arc from a transition to a place.

            :param from: The ID or name of the transition from which the arc is originating.
            :type from: uint_64_t or str
            :param to: The ID or name of the place to which the arc goes to.
            :type to: uint_64_t or str
            :param uint64_t multiplicity: The multiplicity of the arc, default = 1.
        )doc")
        .def("add_output_arc", py::overload_cast<std::string const&, std::string const&, uint64_t>(&GSPNBuilder::addOutputArc), "from"_a,  "to"_a,  "multiplicity"_a)
        .def("add_normal_arc", &GSPNBuilder::addNormalArc, "from"_a, "to"_a, "multiplicity"_a = 1, R"doc(
             Add an arc from a named element to a named element.
             Can be both input or output arc, but not an inhibition arc.
             Convenience function for textual format parsers.

            :param str from: Source element in the GSPN from where this arc starts.
            :param str to: Target element in the GSPN where this arc ends.
            :param uint64_t multiplicity: Multiplicity of the arc, default = 1.
        )doc")

        .def("build_gspn", &GSPNBuilder::buildGspn, "Construct GSPN", "expression_manager"_a = nullptr, "constants_substitution"_a = std::map<storm::expressions::Variable, storm::expressions::Expression>())
    ;

    // GSPN class
    py::class_<GSPN, std::shared_ptr<GSPN>>(m, "GSPN", "Generalized Stochastic Petri Net")
        // Constructor
        .def(py::init<std::string const&, std::vector<Place> const&, std::vector<ImmediateTransition> const&,
                     std::vector<TimedTransition> const&, std::vector<TransitionPartition> const&, std::shared_ptr<storm::expressions::ExpressionManager> const&, std::map<storm::expressions::Variable,
                     storm::expressions::Expression> const&>(), "name"_a, "places"_a, "immediate_transitions"_a, "timed_transitions"_a, "partitions"_a, "expression_manager"_a, "constants_substitution"_a = std::map<storm::expressions::Variable, storm::expressions::Expression>())

        .def("get_name", &GSPN::getName, "Get name of GSPN")
        .def("set_name", &GSPN::setName, "Set name of GSPN")

        .def("get_number_of_places", &GSPN::getNumberOfPlaces, "Get the number of places in this GSPN")
        .def("get_number_of_immediate_transitions", &GSPN::getNumberOfImmediateTransitions, "Get the number of immediate transitions in this GSPN")
        .def("get_number_of_timed_transitions", &GSPN::getNumberOfTimedTransitions, "Get the number of timed transitions in this GSPN")

        .def("get_place", [](GSPN const& g, uint64_t id) -> const Place& {return *(g.getPlace(id)); }, "id"_a, R"doc(
             Returns the place with the corresponding id.

            :param uint64_t id: The ID of the place.
            :rtype: stormpy.Place
        )doc")
        .def("get_place", [](GSPN const& g, std::string const& name) -> const Place& {return *(g.getPlace(name)); }, "name"_a)
        .def("get_timed_transition", [](GSPN const& g, std::string const& name) -> const TimedTransition& {return *(g.getTimedTransition(name)); }, "name"_a, "Returns the timed transition with the corresponding name")
        .def("get_immediate_transition", [](GSPN const& g, std::string const& name) -> const ImmediateTransition& {return *(g.getImmediateTransition(name)); }, "name"_a, "Returns the immediate transition with the corresponding name")
        .def("get_transition",[](GSPN const& g, std::string const& name) -> const Transition& {return *(g.getTransition(name)); }, "name"_a, "Returns the transition with the corresponding name")

        .def("get_partitions", &GSPN::getPartitions, "Get the partitions of this GSPN")
        .def("get_places", &GSPN::getPlaces, R"doc(
             Returns a vector of the places of this GSPN.

            :rtype: list[stormpy.Place]
        )doc")
        .def("get_timed_transitions", &GSPN::getTimedTransitions, R"doc(
             Returns a vector of the timed transitions of this GSPN.

            :rtype: list[stormpy.TimedTransition]
        )doc")
        .def("get_immediate_transitions", &GSPN::getImmediateTransitions, R"doc(
             Returns the immediate transitions of this GSPN.

            :rtype: list[stormpy.ImmediateTransition]
        )doc")
        .def("get_initial_marking", &GSPN::getInitialMarking, "Computes the initial marking of this GSPN")

        .def("is_valid", &GSPN::isValid, "Perform some checks")

        // GSPN export
        .def("export_gspn_pnpro_file", [](GSPN& g, std::string const& filepath) -> void { gspnToFile(g, filepath, true); }, "filepath"_a, "Export GSPN to PNPRO file")
        .def("export_gspn_pnml_file", [](GSPN& g, std::string const& filepath) -> void { gspnToFile(g, filepath, false); }, "filepath"_a, "Export GSPN to PNML file")

        .def_static("timed_transition_id_to_transition_id", &GSPN::timedTransitionIdToTransitionId)
        .def_static("immediate_transition_id_to_transition_id", &GSPN::immediateTransitionIdToTransitionId)
        .def_static("transition_id_to_timed_transition_id", &GSPN::transitionIdToTimedTransitionId)
        .def_static("transition_id_to_immediate_transition_id", &GSPN::transitionIdToImmediateTransitionId)
    ;


    // LayoutInfo class
    py::class_<LayoutInfo>(m, "LayoutInfo")
        .def(py::init<>())
        .def(py::init<double, double, double>(), "x"_a, "y"_a, "rotation"_a = 0.0)
        .def_readwrite("x", &LayoutInfo::x)
        .def_readwrite("y", &LayoutInfo::y)
        .def_readwrite("rotation", &LayoutInfo::rotation)
    ;

    // Place class
    py::class_<Place, std::shared_ptr<Place>>(m, "Place", "Place in a GSPN")
        .def(py::init<uint64_t>(), "id"_a)
        .def("get_name", &Place::getName, "Get name of this place")
        .def("set_name", &Place::setName, "name"_a, "Set name of this place")
        .def("get_id", &Place::getID, "Get the id of this place")
        .def("set_number_of_initial_tokens", &Place::setNumberOfInitialTokens, "tokens"_a, "Set the number of initial tokens of this place")
        .def("get_number_of_initial_tokens", &Place::getNumberOfInitialTokens, "Get the number of initial tokens of this place")
        .def("set_capacity", &Place::setCapacity, "cap"_a, "Set the capacity of tokens of this place")  // problem: boost or lambda [](..
        .def("get_capacity", &Place::getCapacity, "Get the capacity of tokens of this place")
        .def("has_restricted_capacity", &Place::hasRestrictedCapacity, "Is capacity of this place restricted")
    ;

    // Transition class
    py::class_<Transition, std::shared_ptr<Transition>>(m, "Transition", "Transition in a GSPN")
        .def(py::init<>())
        .def("get_id", &Transition::getID, "Get id of this transition")
        .def("set_name", &Transition::setName, "name"_a, "Set name of this transition")
        .def("get_name", &Transition::getName, "Get name of this transition")
        .def("set_priority", &Transition::setPriority, "priority"_a, "Set priority of this transition")
        .def("get_priority", &Transition::getPriority, "Get priority of this transition")

        .def("set_input_arc_multiplicity", &Transition::setInputArcMultiplicity, "place"_a, "multiplicity"_a, "Set the multiplicity of the input arc originating from the place.")
        .def("remove_input_arc", &Transition::removeInputArc, "place"_a, "Remove an input arc connected to a given place.")
        .def("exists_input_arc", &Transition::existsInputArc, "place"_a, "Check whether the given place is connected to this transition via an input arc.")

        .def("set_output_arc_multiplicity", &Transition::setOutputArcMultiplicity, "place"_a, "multiplicity"_a, "Set the multiplicity of the output arc going to the place.")
        .def("remove_output_arc", &Transition::removeOutputArc, "place"_a, "Remove an output arc connected to a given place.")
        .def("exists_output_arc", &Transition::existsOutputArc, "place"_a, "Check whether the given place is connected to this transition via an output arc.")

        .def("set_inhibition_arc_multiplicity", &Transition::setInhibitionArcMultiplicity,  "place"_a, "multiplicity"_a, "Set the multiplicity of the inhibition arc originating from the place.")
        .def("remove_inhibition_arc", &Transition::removeInhibitionArc, "place"_a, "Remove an inhibition arc connected to a given place.")
        .def("exists_inhibition_arc", &Transition::existsInhibitionArc, "place"_a, "Check whether the given place is connected to this transition via an inhibition arc.")

        .def("get_input_places", &Transition::getInputPlaces)
        .def("get_output_places", &Transition::getOutputPlaces)
        .def("get_inhibition_places", &Transition::getInhibitionPlaces)

        .def("get_input_arc_multiplicity", &Transition::getInputArcMultiplicity, "place"_a, "Returns the corresponding multiplicity.")
        .def("get_inhibition_arc_multiplicity", &Transition::getInhibitionArcMultiplicity, "place"_a, "Returns the corresponding multiplicity.")
        .def("get_output_arc_multiplicity", &Transition::getOutputArcMultiplicity, "place"_a, "Returns the corresponding multiplicity.")

        .def("is_enabled", &Transition::isEnabled, "marking"_a, "Check if the given marking enables the transition.")
        .def("fire", &Transition::fire, "marking"_a, "Fire the transition if possible.")

    ;

    // TimedTransition class
    py::class_<TimedTransition, Transition, std::shared_ptr<TimedTransition>>(m, "TimedTransition", "TimedTransition in a GSPN")
        .def(py::init<>())
        .def("get_rate", &TimedTransition::getRate, "Get rate of this transition")
        .def("set_rate", &TimedTransition::setRate, "rate"_a, "Set rate of this transition")
        .def("set_k_server_semantics", &TimedTransition::setKServerSemantics, "k"_a, "Set semantics of this transition")
        .def("set_single_server_semantics", &TimedTransition::setSingleServerSemantics, "Set semantics of this transition")
        .def("set_infinite_server_semantics", &TimedTransition::setInfiniteServerSemantics, "Set semantics of this transition")
        .def("has_k_server_semantics", &TimedTransition::hasKServerSemantics, "Get semantics of this transition")
        .def("has_single_server_semantics", &TimedTransition::hasSingleServerSemantics, "Get semantics of this transition")
        .def("has_infinite_server_semantics", &TimedTransition::hasInfiniteServerSemantics, "Get semantics of this transition")
        .def("get_number_of_servers", &TimedTransition::getNumberOfServers, "Get number of servers")
    ;

    // ImmediateTransition class
    py::class_<ImmediateTransition, Transition, std::shared_ptr<ImmediateTransition>>(m, "ImmediateTransition", "ImmediateTransition in a GSPN")
        .def(py::init<>())
        .def("get_weight", &ImmediateTransition::getWeight, "Get weight of this transition")
        .def("set_weight", &ImmediateTransition::setWeight, "weight"_a, "Set weight of this transition")
        .def("no_weight_attached", &ImmediateTransition::noWeightAttached, "True iff no weight is attached")
    ;

    // TransitionPartition class
    py::class_<TransitionPartition>(m, "TransitionPartition")
         .def(py::init<>())
         .def_readwrite("priority", &TransitionPartition::priority)
         .def_readwrite("transitions", &TransitionPartition::transitions)
         .def("nr_transitions", &TransitionPartition::nrTransitions, "Get number of transitions")
    ;

}

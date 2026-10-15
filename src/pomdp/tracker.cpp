#include "tracker.h"

#include <storm-pomdp/generator/BeliefSupportTracker.h>
#include <storm-pomdp/generator/NondeterministicBeliefTracker.h>
#include <storm/adapters/RationalFunctionAdapter.h>

#include "src/binding_type_index.h"
#include "src/helpers.h"

template<typename ValueType>
using SparsePomdp = storm::models::sparse::Pomdp<ValueType>;

template<typename ValueType>
void define_tracker(py::module& m) {
    auto index = stormpy::bindings::typeIndex<ValueType>();

    using SupportTracker = storm::generator::BeliefSupportTracker<ValueType>;
    stormpy::bindings::bindTemplateClass<SupportTracker>(m, "BeliefSupportTracker", index, "Tracker for belief supports")
        .def(py::init<SparsePomdp<ValueType> const&>(), "pomdp"_a, py::keep_alive<1, 2>())
        .def("get_current_belief_support", &SupportTracker::getCurrentBeliefSupport, "What is the support given the trace so far")
        .def("track", &SupportTracker::track, "Update the belief support with the given action and observation", "action"_a, "observation"_a)
        .def("reset", &SupportTracker::reset, "Reset the tracker to the initial belief support");

    using BeliefState = storm::generator::SparseBeliefState<ValueType>;
    stormpy::bindings::bindTemplateClass<BeliefState>(m, "SparseBeliefState", index, "Belief state in sparse format")
        .def("get", &BeliefState::get, "Probability of the given state", "state"_a)
        .def_property_readonly("risk", &BeliefState::getRisk, "Risk of the belief state")
        .def("__str__", &BeliefState::toString)
        .def_property_readonly("is_valid", &BeliefState::isValid, "Whether the belief state is valid");

    using Tracker = storm::generator::NondeterministicBeliefTracker<ValueType, BeliefState>;
    stormpy::bindings::bindTemplateClass<typename Tracker::Options>(m, "NondeterministicBeliefTrackerOptions", index,
                                                                    "Options for the nondeterministic belief tracker")
        .def(py::init<>())
        .def_readwrite("track_time_out", &Tracker::Options::trackTimeOut, "Timeout for tracking in milliseconds, 0 for no timeout")
        .def_readwrite("time_out", &Tracker::Options::timeOut, "Timeout for the reduction in milliseconds, 0 for no timeout")
        .def_readwrite("wiggle", &Tracker::Options::wiggle, "Tolerance used in the reduction");

    stormpy::bindings::bindTemplateClass<Tracker>(m, "NondeterministicBeliefTracker", index,
                                                  "Tracker for belief states (in sparse format) and uncontrollable actions")
        .def(py::init<SparsePomdp<ValueType> const&, typename Tracker::Options>(), "pomdp"_a, "options"_a = typename Tracker::Options(), py::keep_alive<1, 2>())
        .def("reset", &Tracker::reset, "Start tracking with the given initial observation", "observation"_a)
        .def("set_risk", &Tracker::setRisk, "Set the risk of each state", "risk"_a)
        .def("get_current_risk", &Tracker::getCurrentRisk, "Maximal (or minimal) risk of the current beliefs", "max"_a = true)
        .def("track", &Tracker::track, "Update the beliefs with the given observation", "new_observation"_a)
        .def("get_current_beliefs", &Tracker::getCurrentBeliefs, "Current beliefs")
        .def("get_number_of_beliefs", &Tracker::getNumberOfBeliefs, "Number of current beliefs")
        .def("get_current_dimension", &Tracker::getCurrentDimension, "Dimension of the current beliefs")
        .def("get_current_observation", &Tracker::getCurrentObservation, "Last observation")
        .def("reduce", &Tracker::reduce, "Reduce the set of beliefs")
        .def("has_timed_out", &Tracker::hasTimedOut, "Whether the last reduction timed out");
}

template void define_tracker<double>(py::module& m);
template void define_tracker<storm::RationalNumber>(py::module& m);

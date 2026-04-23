#include "tracker.h"
#include "src/helpers.h"

#include <storm/adapters/RationalFunctionAdapter.h>
#include <storm-pomdp/generator/BeliefSupportTracker.h>
#include <storm-pomdp/generator/NondeterministicBeliefTracker.h>


template<typename ValueType> using SparsePomdp = storm::models::sparse::Pomdp<ValueType>;
template<typename ValueType> using SparsePomdpTracker = storm::generator::BeliefSupportTracker<ValueType>;

template<typename ValueType> using NDPomdpTrackerSparse = storm::generator::NondeterministicBeliefTracker<ValueType, storm::generator::SparseBeliefState<ValueType>>;


template<typename ValueType>
void define_tracker(py::module& m, std::string const& vtSuffix) {
    py::class_<storm::generator::BeliefSupportTracker<ValueType>> tracker(m, ("BeliefSupportTracker" + vtSuffix).c_str(), "Tracker for BeliefSupports");
    tracker.def(py::init<SparsePomdp<ValueType> const&>(), py::arg("pomdp"));
    tracker.def("get_current_belief_support", &SparsePomdpTracker<ValueType>::getCurrentBeliefSupport, "What is the support given the trace so far");
    tracker.def("track", &SparsePomdpTracker<ValueType>::track, py::arg("action"), py::arg("observation"));

    py::class_<storm::generator::SparseBeliefState<ValueType>> sbel(m, ("SparseBeliefState" + vtSuffix).c_str(), "Belief state in sparse format");
    sbel.def("get", &storm::generator::SparseBeliefState<ValueType>::get, py::arg("state"));
    sbel.def_property_readonly("risk", &storm::generator::SparseBeliefState<ValueType>::getRisk);
    sbel.def("__str__", &storm::generator::SparseBeliefState<ValueType>::toString);
    sbel.def_property_readonly("is_valid", &storm::generator::SparseBeliefState<ValueType>::isValid);

    py::class_<typename NDPomdpTrackerSparse<ValueType>::Options> opts(m, ("NondeterministicBeliefTracker" + vtSuffix + "SparseOptions").c_str(), "Options for the corresponding tracker");
    opts.def(py::init<>());
    opts.def_readwrite("track_timeout", &NDPomdpTrackerSparse<ValueType>::Options::trackTimeOut);
    opts.def_readwrite("reduction_timeout", &NDPomdpTrackerSparse<ValueType>::Options::timeOut);
    opts.def_readwrite("reduction_wiggle", &NDPomdpTrackerSparse<ValueType>::Options::wiggle);

    py::class_<NDPomdpTrackerSparse<ValueType>> ndetbelieftracker(m, ("NondeterministicBeliefTracker" + vtSuffix + "Sparse").c_str(), "Tracker for belief states and uncontrollable actions");
    ndetbelieftracker.def(py::init<SparsePomdp<ValueType> const&, typename NDPomdpTrackerSparse<ValueType>::Options>(), py::arg("pomdp"), py::arg("options"));
    ndetbelieftracker.def("reset", &NDPomdpTrackerSparse<ValueType>::reset);
    ndetbelieftracker.def("set_risk", &NDPomdpTrackerSparse<ValueType>::setRisk, py::arg("risk"));
    ndetbelieftracker.def("obtain_current_risk",&NDPomdpTrackerSparse<ValueType>::getCurrentRisk, py::arg("max")=true);
    ndetbelieftracker.def("track", &NDPomdpTrackerSparse<ValueType>::track, py::arg("observation"));
    ndetbelieftracker.def("obtain_beliefs", &NDPomdpTrackerSparse<ValueType>::getCurrentBeliefs);
    ndetbelieftracker.def("size", &NDPomdpTrackerSparse<ValueType>::getNumberOfBeliefs);
    ndetbelieftracker.def("dimension", &NDPomdpTrackerSparse<ValueType>::getCurrentDimension);
    ndetbelieftracker.def("obtain_last_observation", &NDPomdpTrackerSparse<ValueType>::getCurrentObservation);
    ndetbelieftracker.def("reduce",&NDPomdpTrackerSparse<ValueType>::reduce);
    ndetbelieftracker.def("reduction_timed_out", &NDPomdpTrackerSparse<ValueType>::hasTimedOut);
}

template void define_tracker<double>(py::module& m, std::string const& vtSuffix);
template void define_tracker<storm::RationalNumber>(py::module& m, std::string const& vtSuffix);

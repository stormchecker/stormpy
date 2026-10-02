#include "utility.h"

#include <storm-dft/utility/RelevantEvents.h>

void define_relevant_events(py::module& m) {
    // RelevantEvents
    py::classh<storm::dft::utility::RelevantEvents>(m, "RelevantEvents", "Relevant events which should be observed")
        .def(py::init<>(), "Create empty list of relevant events")
        .def("is_relevant", &storm::dft::utility::RelevantEvents::isRelevant, "Check whether the given name is a relevant event", py::arg("name"));
}

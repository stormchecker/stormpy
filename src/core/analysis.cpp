#include "analysis.h"

#include <storm/analysis/GraphConditions.h>

#include "src/binding_type_index.h"

// Define python bindings
void define_graph_constraints(py::module& m) {
    // ConstraintCollector
    stormpy::bindings::bindTemplateClass<storm::analysis::ConstraintCollector<storm::RationalFunction>>(
        m, "ConstraintCollector", stormpy::bindings::typeIndex<storm::RationalFunction>(), "Collector for constraints on parametric Markov chains")
        .def(py::init<storm::models::sparse::Model<storm::RationalFunction> const&>(), py::arg("model"))
        .def_property_readonly("wellformed_constraints", &storm::analysis::ConstraintCollector<storm::RationalFunction>::getWellformedConstraints,
                               "Get the constraints ensuring a wellformed model")
        .def_property_readonly("graph_preserving_constraints", &storm::analysis::ConstraintCollector<storm::RationalFunction>::getGraphPreservingConstraints,
                               "Get the constraints ensuring the graph is preserved");
}

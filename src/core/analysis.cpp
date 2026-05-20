#include "analysis.h"

#include "storm/analysis/GraphConditions.h"

// Define python bindings
void define_graph_constraints(py::module& m) {
    // ConstraintCollector
    py::class_<storm::analysis::ConstraintCollector<storm::RationalFunction>, std::shared_ptr<storm::analysis::ConstraintCollector<storm::RationalFunction>>>(
        m, "ConstraintCollector", "Collector for constraints on parametric Markov chains")
        .def(py::init<storm::models::sparse::Model<storm::RationalFunction> const&>(), py::arg("model"))
        .def_property_readonly("wellformed_constraints", &storm::analysis::ConstraintCollector<storm::RationalFunction>::getWellformedConstraints,
                               "Get the constraints ensuring a wellformed model")
        .def_property_readonly("graph_preserving_constraints", &storm::analysis::ConstraintCollector<storm::RationalFunction>::getGraphPreservingConstraints,
                               "Get the constraints ensuring the graph is preserved");
}

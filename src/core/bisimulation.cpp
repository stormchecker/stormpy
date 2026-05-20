#include "bisimulation.h"
#include "storm/adapters/RationalFunctionAdapter.h"
#include "storm/models/symbolic/StandardRewardModel.h"

template<storm::dd::DdType DdType, typename ValueType>
std::shared_ptr<storm::models::Model<ValueType>> performBisimulationMinimization(
    std::shared_ptr<storm::models::symbolic::Model<DdType, ValueType>> const& model, std::vector<std::shared_ptr<storm::logic::Formula const>> const& formulas,
    storm::storage::BisimulationType const& bisimulationType, storm::dd::bisimulation::QuotientFormat const& quotientFormat) {
    return storm::api::performBisimulationMinimization<DdType, ValueType, ValueType>(model, formulas, bisimulationType,
                                                                                     storm::dd::bisimulation::SignatureMode::Eager, quotientFormat);
}

// Define python bindings
void define_bisimulation(py::module& m) {
    // Bisimulation
    m.def("_perform_bisimulation", &storm::api::performBisimulationMinimization<double>, "Perform bisimulation", py::arg("model"), py::arg("formulas"),
          py::arg("bisimulation_type"), py::arg("graph_preserving"));
    m.def("_perform_parametric_bisimulation", &storm::api::performBisimulationMinimization<storm::RationalFunction>, "Perform bisimulation on parametric model",
          py::arg("model"), py::arg("formulas"), py::arg("bisimulation_type"), py::arg("graph_preserving"));
    m.def("_perform_symbolic_bisimulation", &performBisimulationMinimization<storm::dd::DdType::Sylvan, double>, "Perform bisimulation", py::arg("model"),
          py::arg("formulas"), py::arg("bisimulation_type"), py::arg("quotient_format"));
    m.def("_perform_symbolic_parametric_bisimulation", &performBisimulationMinimization<storm::dd::DdType::Sylvan, storm::RationalFunction>,
          "Perform bisimulation on parametric model", py::arg("model"), py::arg("formulas"), py::arg("bisimulation_type"), py::arg("quotient_format"));

    // BisimulationType
    py::enum_<storm::storage::BisimulationType>(m, "BisimulationType", "Types of bisimulation")
        .value("STRONG", storm::storage::BisimulationType::Strong)
        .value("WEAK", storm::storage::BisimulationType::Weak);

    // QuotientFormat
    py::enum_<storm::dd::bisimulation::QuotientFormat>(m, "QuotientFormat", "Return format of bisimulation quotient")
        .value("SPARSE", storm::dd::bisimulation::QuotientFormat::Sparse)
        .value("DD", storm::dd::bisimulation::QuotientFormat::Dd);
}

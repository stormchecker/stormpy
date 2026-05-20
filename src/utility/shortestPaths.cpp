#include "shortestPaths.h"
#include "src/helpers.h"
#include "storm/utility/shortestPaths.h"

// only forward declaring Model leads to pybind compilation error
// this may be avoidable. but including certainly works.
#include "storm/models/sparse/Model.h"
#include "storm/models/sparse/StandardRewardModel.h"

void define_ksp(py::module& m) {
    // long types shortened for readability
    //
    // this could be templated rather than hardcoding double, but the actual
    // bindings must refer to instantiated versions anyway (i.e., overloaded
    // for each template instantiation) -- and double is enough for me
    using BitVector = storm::storage::BitVector;
    using MatrixFormat = storm::utility::ksp::MatrixFormat;
    using Path = storm::utility::ksp::Path<double>;
    using ShortestPathsGenerator = storm::utility::ksp::ShortestPathsGenerator<double>;
    using state_t = storm::utility::ksp::state_t;
    using Matrix = ShortestPathsGenerator::Matrix;
    using Model = ShortestPathsGenerator::Model;
    using StateProbMap = ShortestPathsGenerator::StateProbMap;

    py::class_<Path>(m, "Path")
        // overload constructor rather than dealing with boost::optional
        .def(py::init([](state_t preNode, unsigned long preK, double distance) { return Path{boost::optional<state_t>(preNode), preK, distance}; }),
             "predecessorNode"_a, "predecessorK"_a, "distance"_a)

        .def(py::init([](unsigned long preK, double distance) { return Path{boost::none, preK, distance}; }), "predecessorK"_a, "distance"_a)

        .def(py::self == py::self, "Compares predecessor node and index, ignoring distance")

        //.def("__str__", &streamToString<Path>)

        .def_readwrite("predecessorNode", &Path::predecessorNode)  // TODO (un-)wrap boost::optional so it's usable
        .def_readwrite("predecessorK", &Path::predecessorK)
        .def_readwrite("distance", &Path::distance);

    py::enum_<MatrixFormat>(m, "MatrixFormat").value("Straight", MatrixFormat::straight).value("I_Minus_P", MatrixFormat::iMinusP);

    py::class_<ShortestPathsGenerator>(m, "ShortestPathsGenerator")
        .def(py::init<Model const&, BitVector>(), "model"_a, "target_bitvector"_a)
        .def(py::init<Model const&, state_t>(), "model"_a, "target_state"_a)
        .def(py::init<Model const&, std::vector<state_t> const&>(), "model"_a, "target_state_list"_a)
        .def(py::init<Model const&, std::string>(), "model"_a, "target_label"_a)
        .def(py::init<Matrix const&, std::vector<double> const&, BitVector const&, MatrixFormat>(), "transition_matrix"_a, "target_prob_vector"_a,
             "initial_states"_a, "matrix_format"_a)
        .def(py::init<Matrix const&, StateProbMap const&, BitVector const&, MatrixFormat>(), "transition_matrix"_a, "target_prob_map"_a, "initial_states"_a,
             "matrix_format"_a)

        .def("get_distance", &ShortestPathsGenerator::getDistance, "k"_a)
        .def("get_states", &ShortestPathsGenerator::getStates, "k"_a)
        .def("get_path_as_list", &ShortestPathsGenerator::getPathAsList, "k"_a);
}

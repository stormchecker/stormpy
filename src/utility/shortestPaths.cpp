#include "shortestPaths.h"

#include <storm/adapters/RationalNumberAdapter.h>
// storm/utility/shortestPaths.h only forward declares Model, but pybind11 needs the complete type for the constructor arguments
#include <storm/models/sparse/Model.h>
#include <storm/utility/shortestPaths.h>

#include "src/binding_type_index.h"
#include "src/helpers.h"

void define_ksp(py::module& m) {
    using namespace storm::utility::ksp;

    py::native_enum<MatrixFormat>(m, "MatrixFormat", "enum.Enum", "Format of a given transition matrix: either P itself or I-P")
        .value("STRAIGHT", MatrixFormat::straight)
        .value("I_MINUS_P", MatrixFormat::iMinusP)
        .finalize();
}

template<typename ValueType>
void define_ksp_typed(py::module& m) {
    using namespace storm::utility::ksp;

    stormpy::bindings::bindTemplateClass<Path<ValueType>>(
        m, "Path", stormpy::bindings::typeIndex<ValueType>(),
        "Entry of the shortest path tree: the k-th shortest path to a state via its predecessor and the path's probability")
        // overload constructor rather than dealing with boost::optional
        .def(py::init(
                 [](state_t preNode, unsigned long preK, ValueType distance) { return Path<ValueType>{boost::optional<state_t>(preNode), preK, distance}; }),
             "predecessor_node"_a, "predecessor_k"_a, "distance"_a)
        .def(py::init([](unsigned long preK, ValueType distance) { return Path<ValueType>{boost::none, preK, distance}; }), "predecessor_k"_a, "distance"_a)

        .def(py::self == py::self, "Compares predecessor node and index, ignoring distance")

        .def_readwrite("predecessor_node", &Path<ValueType>::predecessorNode)  // TODO (un-)wrap boost::optional so it's usable
        .def_readwrite("predecessor_k", &Path<ValueType>::predecessorK)
        .def_readwrite("distance", &Path<ValueType>::distance)
        .def("__str__", &streamToString<Path<ValueType>>);

    stormpy::bindings::bindTemplateClass<ShortestPathsGenerator<ValueType>>(
        m, "ShortestPathsGenerator", stormpy::bindings::typeIndex<ValueType>(),
        "Computes the k most probable paths from the initial states to a set of target states")
        .def(py::init<typename ShortestPathsGenerator<ValueType>::Model const&, BitVector>(), "model"_a, "target_bv"_a)
        .def(py::init<typename ShortestPathsGenerator<ValueType>::Model const&, state_t>(), "model"_a, "single_target"_a)
        .def(py::init<typename ShortestPathsGenerator<ValueType>::Model const&, std::vector<state_t> const&>(), "model"_a, "target_list"_a)
        .def(py::init<typename ShortestPathsGenerator<ValueType>::Model const&, std::string>(), "model"_a, "target_label"_a = "target")
        .def(py::init<typename ShortestPathsGenerator<ValueType>::Matrix const&, std::vector<ValueType> const&, BitVector const&, MatrixFormat>(),
             "transition_matrix"_a, "target_prob_vector"_a, "initial_states"_a, "matrix_format"_a)
        .def(py::init<typename ShortestPathsGenerator<ValueType>::Matrix const&, typename ShortestPathsGenerator<ValueType>::StateProbMap const&,
                      BitVector const&, MatrixFormat>(),
             "maybe_transition_matrix"_a, "target_prob_map"_a, "initial_states"_a, "matrix_format"_a)

        .def("get_distance", &ShortestPathsGenerator<ValueType>::getDistance, "k"_a, "Get the probability of the k-th shortest path")
        .def("get_states", &ShortestPathsGenerator<ValueType>::getStates, "k"_a, "Get the states occurring in the k-th shortest path")
        .def("get_path_as_list", &ShortestPathsGenerator<ValueType>::getPathAsList, "k"_a,
             "Get the states of the k-th shortest path as back-to-front traversal");
}

template void define_ksp_typed<double>(py::module& m);
template void define_ksp_typed<storm::RationalNumber>(py::module& m);

#include "state.h"

#include <storm/adapters/IntervalAdapter.h>

template<typename ValueType>
void define_state(py::module& m, std::string const& vtSuffix) {
    // SparseModelStates
    py::classh<SparseModelStates<ValueType>>(m, ("Sparse" + vtSuffix + "ModelStates").c_str(), "States in sparse model")
        .def("__getitem__", &SparseModelStates<ValueType>::getState)
        .def("__len__", &SparseModelStates<ValueType>::getSize);

    // SparseModelState
    py::classh<SparseModelState<ValueType>>(m, ("Sparse" + vtSuffix + "ModelState").c_str(), "State in sparse model")
        .def("__str__", &SparseModelState<ValueType>::toString)
        .def_property_readonly("id", &SparseModelState<ValueType>::getIndex, "Id")
        .def_property_readonly("labels", &SparseModelState<ValueType>::getLabels, "Get state labels")
        .def_property_readonly("valuations", &SparseModelState<ValueType>::getValuations, "Get state valuations")
        .def_property_readonly("actions", &SparseModelState<ValueType>::getActions, "Get actions")
        .def("__int__", &SparseModelState<ValueType>::getIndex);

    // SparseModelActions
    py::classh<SparseModelActions<ValueType>>(m, ("Sparse" + vtSuffix + "ModelActions").c_str(), "Actions for state in sparse model")
        .def("__getitem__", &SparseModelActions<ValueType>::getAction)
        .def("__len__", &SparseModelActions<ValueType>::getSize);

    // SparseModelAction
    py::classh<SparseModelAction<ValueType>>(m, ("Sparse" + vtSuffix + "ModelAction").c_str(), "Action for state in sparse model")
        .def("__str__", &SparseModelAction<ValueType>::toString)
        .def_property_readonly("id", &SparseModelAction<ValueType>::getIndex, "Id")
        .def_property_readonly("transitions", &SparseModelAction<ValueType>::getTransitions, "Get transitions")
        .def_property_readonly("labels", &SparseModelAction<ValueType>::getLabels, "Get choice labels")
        .def_property_readonly("origins", &SparseModelAction<ValueType>::getOrigins, "Get choice origins");
}

template void define_state<double>(py::module& m, std::string const& vtSuffix);
template void define_state<storm::RationalNumber>(py::module& m, std::string const& vtSuffix);
template void define_state<storm::Interval>(py::module& m, std::string const& vtSuffix);
template void define_state<storm::RationalInterval>(py::module& m, std::string const& vtSuffix);
template void define_state<storm::RationalFunction>(py::module& m, std::string const& vtSuffix);

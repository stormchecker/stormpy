#pragma once

#include "common.h"

#include "storm/models/sparse/Model.h"
#include "storm/storage/SparseMatrix.h"

// Forward declaration
template<typename ValueType>
class SparseModelActions;

// State definition
template<typename ValueType>
class SparseModelState {
    using s_index = typename storm::storage::SparseMatrix<ValueType>::index_type;

   public:
    SparseModelState(storm::models::sparse::Model<ValueType>& model, s_index stateIndex) : model(model), stateIndex(stateIndex) {}

    s_index getIndex() const {
        return stateIndex;
    }

    std::set<std::string> getLabels() const {
        return this->model.getStateLabeling().getLabelsOfState(this->stateIndex);
    }

    std::string getValuations() const {
        if (!this->model.hasStateValuations()) {
            throw std::invalid_argument("No state valuations available");
        }
        return this->model.getStateValuations().getStateInfo(this->stateIndex);
    }

    SparseModelActions<ValueType> getActions() const {
        return SparseModelActions<ValueType>(this->model, stateIndex);
    }

    std::string toString() const {
        std::stringstream stream;
        stream << stateIndex;
        return stream.str();
    }

   private:
    s_index stateIndex;
    storm::models::sparse::Model<ValueType>& model;
};

template<typename ValueType>
class SparseModelStates {
    using s_index = typename storm::storage::SparseMatrix<ValueType>::index_type;

   public:
    SparseModelStates(storm::models::sparse::Model<ValueType>& model) : model(model) {
        length = model.getNumberOfStates();
    }

    s_index getSize() const {
        return length;
    }

    SparseModelState<ValueType> getState(s_index index) const {
        if (index < length) {
            return SparseModelState<ValueType>(model, index);
        } else {
            throw py::index_error();
        }
    }

   private:
    s_index length;
    storm::models::sparse::Model<ValueType>& model;
};

// Action definition
template<typename ValueType>
class SparseModelAction {
    using s_index = typename storm::storage::SparseMatrix<ValueType>::index_type;

   public:
    SparseModelAction(storm::models::sparse::Model<ValueType>& model, s_index stateIndex, s_index actionIndex)
        : model(model), stateIndex(stateIndex), actionIndex(actionIndex) {}

    s_index getIndex() const {
        return this->actionIndex;
    }

    typename storm::storage::SparseMatrix<ValueType>::rows getTransitions() {
        return model.getTransitionMatrix().getRow(stateIndex, actionIndex);
    }

    std::set<std::string> getLabels() const {
        if (!this->model.hasChoiceLabeling()) {
            throw std::invalid_argument("No choice labeling available");
        }
        return this->model.getChoiceLabeling().getLabelsOfChoice(getActionIndex());
    }

    std::string getOrigins() const {
        if (!this->model.hasChoiceOrigins()) {
            throw std::invalid_argument("No choice origins available");
        }
        return this->model.getChoiceOrigins()->getChoiceInfo(getActionIndex());
    }

    std::string toString() const {
        std::stringstream stream;
        stream << actionIndex;
        return stream.str();
    }

   private:
    s_index getActionIndex() const {
        return model.getTransitionMatrix().getRowGroupIndices()[stateIndex] + actionIndex;
    }

    s_index stateIndex;
    s_index actionIndex;
    storm::models::sparse::Model<ValueType>& model;
};

template<typename ValueType>
class SparseModelActions {
    using s_index = typename storm::storage::SparseMatrix<ValueType>::index_type;

   public:
    SparseModelActions(storm::models::sparse::Model<ValueType>& model, s_index stateIndex) : model(model), stateIndex(stateIndex) {
        length = model.getTransitionMatrix().getRowGroupSize(stateIndex);
    }

    s_index getSize() const {
        return length;
    }

    SparseModelAction<ValueType> getAction(size_t index) const {
        if (index < length) {
            return SparseModelAction<ValueType>(model, stateIndex, index);
        } else {
            throw py::index_error();
        }
    }

   private:
    s_index stateIndex;
    s_index length;
    storm::models::sparse::Model<ValueType>& model;
};

template<typename ValueType>
void define_state(py::module& m, std::string const& vtSuffix);

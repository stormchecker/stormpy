#pragma once

#include <storm/adapters/RationalFunctionAdapter.h>
#include <storm/adapters/RationalNumberAdapter.h>
#include <storm/models/ModelType.h>

#include "src/template_binding.h"

namespace stormpy::bindings {

template<typename ValueType>
struct BindingTypeArgument;

template<>
struct BindingTypeArgument<double> {
    static TemplateArgument get() {
        return {pybind11::module_::import("builtins").attr("float"), "Double"};
    }
};

template<>
struct BindingTypeArgument<storm::RationalNumber> {
    static TemplateArgument get() {
        return {pybind11::module_::import("stormpy").attr("Rational"), "Rational"};
    }
};

template<>
struct BindingTypeArgument<storm::RationalFunction> {
    static TemplateArgument get() {
        return {pybind11::module_::import("stormpy").attr("RationalFunction"), "RationalFunction"};
    }
};

template<typename ValueType>
TemplateArgument bindingTypeArgument() {
    return BindingTypeArgument<ValueType>::get();
}

template<storm::models::ModelType ModelKind>
struct BindingModelTypeArgument;

template<>
struct BindingModelTypeArgument<storm::models::ModelType::Dtmc> {
    static TemplateArgument get() {
        return {pybind11::cast(storm::models::ModelType::Dtmc), "DTMC"};
    }
};

template<>
struct BindingModelTypeArgument<storm::models::ModelType::Mdp> {
    static TemplateArgument get() {
        return {pybind11::cast(storm::models::ModelType::Mdp), "MDP"};
    }
};

template<>
struct BindingModelTypeArgument<storm::models::ModelType::Ctmc> {
    static TemplateArgument get() {
        return {pybind11::cast(storm::models::ModelType::Ctmc), "CTMC"};
    }
};

template<>
struct BindingModelTypeArgument<storm::models::ModelType::MarkovAutomaton> {
    static TemplateArgument get() {
        return {pybind11::cast(storm::models::ModelType::MarkovAutomaton), "MA"};
    }
};

template<typename... ValueTypes>
TemplateIndex typeIndex() {
    return makeTemplateIndex({bindingTypeArgument<ValueTypes>()...});
}

template<storm::models::ModelType ModelKind, typename... ValueTypes>
TemplateIndex typeIndex() {
    return makeTemplateIndex({BindingModelTypeArgument<ModelKind>::get(), bindingTypeArgument<ValueTypes>()...});
}

}  // namespace stormpy::bindings

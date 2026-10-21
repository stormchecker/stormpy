#pragma once

#include <storm/adapters/IntervalAdapter.h>
#include <storm/adapters/RationalFunctionAdapter.h>
#include <storm/adapters/RationalNumberAdapter.h>
#include <storm/dd/DdType.h>
#include <storm/models/ModelType.h>

#include "src/template_binding.h"

namespace stormpy::bindings {

template<typename ValueType>
struct BindingValueTypeArgument;

template<>
struct BindingValueTypeArgument<double> {
    static TemplateArgument get() {
        return {pybind11::module_::import("builtins").attr("float"), "Double"};
    }
};

template<>
struct BindingValueTypeArgument<storm::RationalNumber> {
    static TemplateArgument get() {
        return {pybind11::module_::import("stormpy").attr("Rational"), "Rational"};
    }
};

template<>
struct BindingValueTypeArgument<storm::RationalFunction> {
    static TemplateArgument get() {
        return {pybind11::module_::import("stormpy").attr("RationalFunction"), "RationalFunction"};
    }
};

template<>
struct BindingValueTypeArgument<storm::Interval> {
    static TemplateArgument get() {
        return {pybind11::module_::import("stormpy").attr("Interval"), "Interval"};
    }
};

template<>
struct BindingValueTypeArgument<storm::RationalInterval> {
    static TemplateArgument get() {
        return {pybind11::module_::import("stormpy").attr("RationalInterval"), "RationalInterval"};
    }
};

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

template<storm::dd::DdType DdKind>
struct BindingDdTypeArgument;

template<>
struct BindingDdTypeArgument<storm::dd::DdType::Sylvan> {
    static TemplateArgument get() {
        return {pybind11::cast(storm::dd::DdType::Sylvan), "Sylvan"};
    }
};

template<>
struct BindingDdTypeArgument<storm::dd::DdType::CUDD> {
    static TemplateArgument get() {
        return {pybind11::cast(storm::dd::DdType::CUDD), "CUDD"};
    }
};

template<typename... ValueTypes>
TemplateIndex typeIndex() {
    return makeTemplateIndex({BindingValueTypeArgument<ValueTypes>::get()...});
}

template<storm::models::ModelType ModelKind, typename... ValueTypes>
TemplateIndex typeIndex() {
    return makeTemplateIndex({BindingModelTypeArgument<ModelKind>::get(), BindingValueTypeArgument<ValueTypes>::get()...});
}

template<storm::dd::DdType DdKind, typename... ValueTypes>
TemplateIndex typeIndex() {
    return makeTemplateIndex({BindingDdTypeArgument<DdKind>::get(), BindingValueTypeArgument<ValueTypes>::get()...});
}

}  // namespace stormpy::bindings

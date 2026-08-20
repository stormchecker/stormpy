#pragma once

#include <memory>
#include <utility>

namespace stormpy::registration {

// This facade lets the existing binding functions participate in two global
// passes without duplicating their declarations. The declaration pass creates
// every Python class and enum; the definition pass looks those classes up and
// attaches methods and free functions. Binding argument expressions are still
// evaluated in both passes, so binding functions must otherwise be declarative.
using namespace pybind11;

enum class Phase { Declare, Define };

class module {
   public:
    module(pybind11::module_ const& implementation, Phase phase) :implementation_(implementation), phase_(phase) {}

    Phase phase() const {
        return phase_;
    }
    pybind11::module_ const& raw() const {
        return implementation_;
    }

    auto attr(char const* name) const {
        return implementation_.attr(name);
    }

    template<typename... Args>
    void def(Args&&... args) {
        if (phase_ == Phase::Define) {
            implementation_.def(std::forward<Args>(args)...);
        }
    }

   private:
    pybind11::module_ implementation_;
    Phase phase_;
};

template<typename BindingFunction>
void bindModule(pybind11::module_ const& implementation, BindingFunction&& bind) {
    module declarations(implementation, Phase::Declare);
    bind(declarations);

    module definitions(implementation, Phase::Define);
    bind(definitions);
}

template<typename Type, typename... Options>
class class_;

template<typename Value>
Value const& unwrap(Value const& value) {
    return value;
}

template<typename Type, typename... Options>
pybind11::handle unwrap(class_<Type, Options...> const& value);

template<typename Type, typename... Options>
class class_ {
   public:
    using RawClass = pybind11::class_<Type, Options...>;

    template<typename... Extra>
    class_(module const& parent, char const* name, Extra const&... extra) : implementation_(acquire(parent, name, extra...)), phase_(parent.phase()) {}

    Phase phase() const {
        return phase_;
    }
    RawClass const& raw() const {
        return implementation_;
    }

#define STORMPY_FORWARD_CLASS_METHOD(method)                     \
    template<typename... Args>                                   \
    class_& method(Args&&... args) {                             \
        if (phase_ == Phase::Define) {                           \
            implementation_.method(std::forward<Args>(args)...); \
        }                                                        \
        return *this;                                            \
    }

    STORMPY_FORWARD_CLASS_METHOD(def)
    STORMPY_FORWARD_CLASS_METHOD(def_property)
    STORMPY_FORWARD_CLASS_METHOD(def_property_readonly)
    STORMPY_FORWARD_CLASS_METHOD(def_readonly)
    STORMPY_FORWARD_CLASS_METHOD(def_readwrite)
    STORMPY_FORWARD_CLASS_METHOD(def_static)

#undef STORMPY_FORWARD_CLASS_METHOD

   private:
    template<typename... Extra>
    static RawClass acquire(module const& parent, char const* name, Extra const&... extra) {
        if (parent.phase() == Phase::Declare) {
            return RawClass(parent.raw(), name, unwrap(extra)...);
        }
        // Reuse the Python type registered in the declaration pass. Constructing
        // another pybind11::class_ would attempt to register the C++ type twice.
        return pybind11::reinterpret_borrow<RawClass>(parent.raw().attr(name));
    }

    RawClass implementation_;
    Phase phase_;
};

template<typename Type, typename... Options>
pybind11::handle unwrap(class_<Type, Options...> const& value) {
    return value.raw();
}

template<typename EnumType>
class native_enum {
   public:
    template<typename Parent>
    native_enum(Parent const& parent, char const* name, char const* nativeTypeName, char const* classDoc = "") {
        if (parent.phase() == Phase::Declare) {
            implementation_ = std::make_unique<pybind11::native_enum<EnumType>>(parent.raw(), name, nativeTypeName, classDoc);
        }
    }

    native_enum& value(char const* name, EnumType value, char const* doc = nullptr) {
        if (implementation_) {
            implementation_->value(name, value, doc);
        }
        return *this;
    }

    native_enum& export_values() {
        if (implementation_) {
            implementation_->export_values();
        }
        return *this;
    }

    void finalize() {
        if (implementation_) {
            implementation_->finalize();
        }
    }

   private:
    std::unique_ptr<pybind11::native_enum<EnumType>> implementation_;
};

}  // namespace stormpy::registration

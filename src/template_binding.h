#pragma once

#include <initializer_list>
#include <pybind11/pybind11.h>
#include <stdexcept>
#include <string>
#include <string_view>
#include <utility>

namespace stormpy::bindings {

/**
 * Python lookup key and stable native-name component for one template
 * parameter.
 *
 * The key is used by Python subscription, for example `float` in `DFT[float]`.
 * The label is used only in the descriptive native class name, for example
 * `Double` in `_DFT_Double`. Labels are explicit so implementation-specific
 * Python type names do not leak into the binding API.
 */
struct TemplateArgument {
    /// Object accepted as this parameter in Python template subscription.
    pybind11::object key;

    /// Identifier fragment used in the concrete native class name.
    std::string label;
};

/** Complete lookup key and native-name suffix for one specialization. */
struct TemplateIndex {
    /// Ordered Python template-parameter tuple.
    pybind11::tuple key;

    /// Concatenated label fragments, each prefixed by an underscore.
    std::string label;
};

/**
 * Combine individual template arguments into a specialization index.
 *
 * Argument order is preserved in both the Python key and native label. For
 * example, arguments `(ModelType.DTMC, float)` with labels `(DTMC, Double)`
 * produce the key `(ModelType.DTMC, float)` and label `_DTMC_Double`.
 *
 * @param arguments Ordered template arguments.
 * @return Complete index used for lookup, naming, and registration.
 */
inline TemplateIndex makeTemplateIndex(std::initializer_list<TemplateArgument> arguments) {
    pybind11::tuple key(arguments.size());
    std::string label;
    std::size_t position = 0;
    for (auto const& argument : arguments) {
        key[position++] = argument.key;
        label += "_" + argument.label;
    }
    return {std::move(key), std::move(label)};
}

/**
 * Produce the stable native name of a concrete template specialization.
 *
 * Native names intentionally begin with an underscore because the generic
 * `TemplateClass` object is the public API. The concrete class remains
 * directly accessible from the native module for inspection and advanced use.
 *
 * @param family Public template-family name.
 * @param index Specialization index.
 * @return A name such as `_DFT_Double`.
 */
inline std::string templateClassName(std::string_view family, TemplateIndex const& index) {
    return "_" + std::string(family) + index.label;
}

/**
 * Bind a descriptively named native class without registering a template
 * specialization.
 *
 * This is used for implementation classes such as specialization-specific
 * bases that Python users do not select through `TemplateClass`.
 *
 * @tparam Class Bound C++ class.
 * @tparam Options Additional `pybind11::class_` options, such as holder types.
 * @tparam Extra Types of additional constructor arguments forwarded to
 *     `pybind11::class_`, such as base-class handles.
 * @param module Native module receiving the class.
 * @param name Complete native Python class name.
 * @param description Python class docstring.
 * @param extra Additional arguments forwarded to `pybind11::class_`.
 * @return The class binding, ready for `.def(...)` calls.
 */
template<typename Class, typename... Options, typename... Extra>
pybind11::class_<Class, Options...> bindInternalClass(pybind11::module_& module, std::string const& name, char const* description, Extra&&... extra) {
    pybind11::class_<Class, Options...> result(module, name.c_str(), description, std::forward<Extra>(extra)...);
    return result;
}

/**
 * Return the registration dictionary for a template family, creating it when
 * necessary.
 *
 * Registrations are stored on the native module as:
 *
 * @code{.py}
 * module._template_instantiations = {
 *     "DFT": {
 *         (float,): module._DFT_Double,
 *     },
 * }
 * @endcode
 *
 * `TemplateClass` reads this table when the Python package is initialized.
 *
 * @param module Native module owning the registrations.
 * @param family Public template-family name.
 * @return Borrowed family dictionary mapping parameter tuples to classes.
 */
inline pybind11::dict templateInstantiations(pybind11::module_& module, std::string_view family) {
    pybind11::dict families;
    if (pybind11::hasattr(module, "_template_instantiations")) {
        families = pybind11::reinterpret_borrow<pybind11::dict>(module.attr("_template_instantiations"));
    } else {
        families = pybind11::dict();
        module.attr("_template_instantiations") = families;
    }

    pybind11::str const familyName(family);
    if (!families.contains(familyName)) {
        families[familyName] = pybind11::dict();
    }
    return pybind11::reinterpret_borrow<pybind11::dict>(families[familyName]);
}

/**
 * Bind and register one concrete specialization of a template family.
 *
 * The class receives a stable descriptive native name and is inserted into the
 * module registration table under `index.key`. Registering the same family and
 * key twice is an error.
 *
 * @tparam Class Bound C++ specialization.
 * @tparam Options Additional `pybind11::class_` options, such as holder types.
 * @tparam Extra Types of additional constructor arguments forwarded to
 *     `pybind11::class_`, such as base-class handles.
 * @param module Native module receiving the class and registration.
 * @param family Public template-family name.
 * @param index Complete specialization lookup and naming index.
 * @param description Python class docstring.
 * @param extra Additional arguments forwarded to `pybind11::class_`.
 * @return The class binding, ready for `.def(...)` calls.
 * @throws std::runtime_error If the family already contains `index.key`.
 */
template<typename Class, typename... Options, typename... Extra>
pybind11::class_<Class, Options...> bindTemplateClass(pybind11::module_& module, std::string_view family, TemplateIndex const& index, char const* description,
                                                      Extra&&... extra) {
    pybind11::dict instantiations = templateInstantiations(module, family);
    if (instantiations.contains(index.key)) {
        throw std::runtime_error("Duplicate native template instantiation for " + std::string(family));
    }

    auto result = bindInternalClass<Class, Options...>(module, templateClassName(family, index), description, std::forward<Extra>(extra)...);
    instantiations[index.key] = result;
    return result;
}

}  // namespace stormpy::bindings

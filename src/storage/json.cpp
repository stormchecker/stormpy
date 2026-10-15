#include "json.h"

#include <storm/adapters/JsonAdapter.h>

#include "src/binding_type_index.h"
#include "src/helpers.h"

template<typename RationalValueType>
void define_json(py::module& m) {
    using Json = storm::json<RationalValueType>;
    auto jsoncont = stormpy::bindings::bindTemplateClass<Json>(m, "JsonContainer", stormpy::bindings::typeIndex<RationalValueType>(),
                                                               "Storm-internal container for JSON structures");
    jsoncont.def("__str__", [](Json const& container) { return container.dump(4); });
    jsoncont.def("__getitem__", [](Json const& container, std::string const& item) { return container[item]; });
    // Compare the JSON structures also with scalar values
    jsoncont.def(py::self == py::self);
    jsoncont.def("__eq__", [](Json const& container, bool value) { return container == Json(value); }, py::is_operator());
    jsoncont.def("__eq__", [](Json const& container, int64_t value) { return container == Json(value); }, py::is_operator());
    jsoncont.def("__eq__", [](Json const& container, RationalValueType const& value) { return container == Json(value); }, py::is_operator());
    jsoncont.def("__eq__", [](Json const& container, std::string const& value) { return container == Json(value); }, py::is_operator());
    jsoncont.def("__hash__", [](Json const& container) { return std::hash<Json>{}(container); });
}

template void define_json<double>(py::module& m);
template void define_json<storm::RationalNumber>(py::module& m);

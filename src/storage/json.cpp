#include "json.h"

#include <storm/adapters/JsonAdapter.h>

#include "src/binding_type_index.h"
#include "src/helpers.h"

template<typename RationalValueType>
void define_json(py::module& m) {
    auto jsoncont = stormpy::bindings::bindTemplateClass<storm::json<RationalValueType>>(m, "JsonContainer", stormpy::bindings::typeIndex<RationalValueType>(),
                                                                                         "Storm-internal container for JSON structures");
    jsoncont.def("__str__", [](storm::json<RationalValueType> const& container) { return container.dump(4); });
    jsoncont.def("__getitem__", [](storm::json<RationalValueType> const& container, std::string const& item) { return container[item]; });
}

template void define_json<double>(py::module& m);
template void define_json<storm::RationalNumber>(py::module& m);

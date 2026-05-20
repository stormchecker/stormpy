#include "json.h"
#include <storm/adapters/JsonAdapter.h>
#include "src/helpers.h"

template<typename RationalValueType>
void define_json(py::module& m, std::string const& vtSuffix) {
    py::class_<storm::json<RationalValueType>> jsoncont(m, ("JsonContainer" + vtSuffix).c_str(), "Storm-internal container for JSON structures");
    jsoncont.def("__str__", [](storm::json<RationalValueType> const& container) { return container.dump(4); });
    jsoncont.def("__getitem__", [](storm::json<RationalValueType> const& container, std::string const& item) { return container[item]; });
}

template void define_json<double>(py::module& m, std::string const& vtSuffix);
template void define_json<storm::RationalNumber>(py::module& m, std::string const& vtSuffix);
#pragma once

#include <boost/optional.hpp>

// `boost::optional` as an example -- can be any `std::optional`-like container
namespace pybind11 {
namespace detail {

template<typename T>
struct type_caster<boost::optional<T>> : optional_caster<boost::optional<T>> {};

template<>
struct type_caster<boost::none_t> : public void_caster<boost::none_t> {};

}  // namespace detail
}  // namespace pybind11

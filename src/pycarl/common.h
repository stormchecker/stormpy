#pragma once

#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>
#include <tuple>
#include <exception>


#include <boost/variant.hpp>

namespace py = pybind11;

#if PY_MAJOR_VERSION >= 3
#define PY_DIV "__truediv__"
#define PY_RDIV "__rtruediv__"
#else
#define PY_DIV "__div__"
#define PY_RDIV "__rdiv__"
#endif

struct NoPickling: public std::exception {
    virtual const char* what() const throw() {
        return "Pickling support not implemented!";
    }
};



// `boost::variant` as an example -- can be any `std::variant`-like container
namespace pybind11 {
    namespace detail {
        template <typename... Ts>
        struct type_caster<boost::variant<Ts...>> : variant_caster<boost::variant<Ts...>> {};

        // Specifies the function used to visit the variant -- `apply_visitor` instead of `visit`
        template <>
        struct visit_helper<boost::variant> {
            template <typename... Args>
            static auto call(Args &&...args)
            -> decltype(boost::apply_visitor(std::forward<Args>(args)...)) {
                return boost::apply_visitor(std::forward<Args>(args)...);
            }
        };
    }
} // namespace pybind11::detail
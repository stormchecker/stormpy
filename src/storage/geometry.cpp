#include "geometry.h"

#include <storm/storage/geometry/Halfspace.h>
#include <storm/storage/geometry/Polytope.h>

#include "src/binding_type_index.h"
#include "src/helpers.h"

template<typename ValueType>
void define_geometry(py::module& m) {
    auto const index = stormpy::bindings::typeIndex<ValueType>();

    typedef storm::storage::geometry::Halfspace<ValueType> Halfspace;
    stormpy::bindings::bindTemplateClass<Halfspace>(m, "Halfspace", index, "Halfspace given by normal_vector * x <= offset")
        .def(py::init<std::vector<ValueType> const&, ValueType const&>(), "Create halfspace", py::arg("normal_vector"), py::arg("offset"))
        .def_property_readonly("normal_vector", py::overload_cast<>(&Halfspace::normalVector, py::const_), "Normal vector")
        .def_property_readonly("offset", py::overload_cast<>(&Halfspace::offset, py::const_), "Offset")
        .def("contains", &Halfspace::contains, "Whether the point is contained in the halfspace", py::arg("point"))
        .def("distance", &Halfspace::distance, "Distance of the point from the halfspace, scaled by the 2-norm of the normal vector", py::arg("point"))
        .def("__str__", [](Halfspace const& halfspace) { return halfspace.toString(); });

    typedef storm::storage::geometry::Polytope<ValueType> Polytope;
    auto polytope = stormpy::bindings::bindTemplateClass<Polytope>(m, "Polytope", index, "Polytope");
    polytope.def_property_readonly("vertices", &Polytope::getVertices);
    polytope.def("downward_closure", &Polytope::downwardClosure);
    polytope.def("get_vertices_in_clockwise_order", &Polytope::getVerticesInClockwiseOrder);
    polytope.def_static("create_downward_closure", &Polytope::createDownwardClosure, "Create the downward closure of the convex hull of the points",
                        py::arg("points"));
    polytope.def_property_readonly("halfspaces", &Polytope::getHalfspaces, "Halfspaces whose intersection is the polytope");
    polytope.def("is_empty", &Polytope::isEmpty, "Whether the polytope is empty");
    polytope.def("is_universal", &Polytope::isUniversal, "Whether the polytope is universal, i.e., contains every point");
    polytope.def("contains", py::overload_cast<typename Polytope::Point const&>(&Polytope::contains, py::const_), "Whether the point is contained",
                 py::arg("point"));
    polytope.def("contains", py::overload_cast<std::shared_ptr<Polytope> const&>(&Polytope::contains, py::const_), "Whether the other polytope is contained",
                 py::arg("other"));
    polytope.def("optimize", &Polytope::optimize,
                 "Find a point maximizing the dot product with the direction. Returns the point and whether such a point exists "
                 "(it does not if the polytope is empty or unbounded in the direction)",
                 py::arg("direction"));
    polytope.def("__str__", [](Polytope const& p) { return p.toString(); });
}

template void define_geometry<double>(py::module&);
template void define_geometry<storm::RationalNumber>(py::module&);

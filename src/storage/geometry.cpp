#include "geometry.h"
#include <storm/storage/geometry/Polytope.h>
#include "src/helpers.h"

template<typename ValueType>
void define_geometry(py::module& m, std::string vt_suffix) {
    typedef storm::storage::geometry::Polytope<ValueType> Polytope;
    py::class_<Polytope, std::shared_ptr<Polytope>> polytope(m, ("Polytope" + vt_suffix).c_str());
    polytope.def_property_readonly("vertices", &Polytope::getVertices);
    polytope.def("create_downward_closure", &Polytope::downwardClosure);
    polytope.def("get_vertices_clockwise", &Polytope::getVerticesInClockwiseOrder);
}

template void define_geometry<double>(py::module&, std::string);
template void define_geometry<storm::RationalNumber>(py::module&, std::string);

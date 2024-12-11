#find_package(pybind11 ${PYBIND_VERSION} CONFIG QUIET)
#if(pybind11_FOUND)
#    message(STATUS "Stormpy - Using system version of pybind11 (version ${PYBIND_VERSION}).")
#else()
message(STATUS "Stormpy - Using shipped version of pybind11 (version ${PYBIND_VERSION}).")

include(FetchContent)
FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11
    GIT_TAG        "v${PYBIND_VERSION}"
    PATCH_COMMAND git apply ${CMAKE_CURRENT_SOURCE_DIR}/resources/pybind11_${PYBIND_VERSION}.patch || git apply ${CMAKE_CURRENT_SOURCE_DIR}/resources/pybind11_${PYBIND_VERSION}.patch --reverse --check
)

FetchContent_MakeAvailable(pybind11)
#endif()

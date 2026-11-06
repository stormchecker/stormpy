# Set variable to strings "True"/"False" according to condition
function(set_variable_string NAME CONDITION)
    if(CONDITION)
        set(${NAME} "True" PARENT_SCOPE)
    else()
        set(${NAME} "False" PARENT_SCOPE)
    endif()
endfunction(set_variable_string)

# Check whether Storm library is available
# Sets variable STORMPY_HAVE_STORM_XYZ
function(storm_with_lib NAME)
    string(TOLOWER ${NAME} NAME_LOWER)
    if(TARGET storm-${NAME_LOWER})
        set(STORMPY_HAVE_STORM_${NAME} TRUE PARENT_SCOPE)
    else()
        set(STORMPY_HAVE_STORM_${NAME} FALSE PARENT_SCOPE)
    endif()
endfunction(storm_with_lib)

# Note that the following functions cannot simply call set_variable_string because the scope would change.
# Using 'macro' instead of 'function' is also not viable because arguments are then not handled as variables any more.

# Set variable for Storm dependencies
# which can be checked with STORMPY_STORM_HAVE_XYZ
# Sets variable STORMPY_STORM_WITH_XYZ_BOOL
function(set_dependency_var NAME)
    if (STORM_HAVE_${NAME})
        set(STORMPY_STORM_WITH_${NAME}_BOOL "True" PARENT_SCOPE)
    else()
        set(STORMPY_STORM_WITH_${NAME}_BOOL "False" PARENT_SCOPE)
    endif()
endfunction(set_dependency_var)

# Set variable for optional Storm libraries (if used)
# which can be checked with STORMPY_HAVE_STORM_XYZ and option STORMPY_USE_STORM_XYZ
# Sets variable STORMPY_STORM_WITH_XYZ_BOOL
function(set_optional_lib_var NAME)
    if ((STORMPY_USE_STORM_${NAME}) AND (STORMPY_HAVE_STORM_${NAME}))
        set(STORMPY_STORM_WITH_${NAME}_BOOL "True" PARENT_SCOPE)
    else()
        set(STORMPY_STORM_WITH_${NAME}_BOOL "False" PARENT_SCOPE)
    endif()
endfunction(set_optional_lib_var)

# Set STORM_VERSION_FULL to the full Storm version x.y.z.N for development versions (N > 0) and x.y.z for releases.
# STORM_VERSION_FULL_DEV is only exported by Storm >= 2.0.0.2, otherwise fall back to STORM_VERSION (x.y.z).
# Sets STORMPY_STORM_HAS_VERSION_TWEAK if Storm provides StormVersion::versionTweak.
macro(set_storm_version_full)
    if (DEFINED STORM_VERSION_FULL_DEV)
        if (STORM_VERSION_DEV GREATER 0)
            set(STORM_VERSION_FULL ${STORM_VERSION_FULL_DEV})
        else()
            set(STORM_VERSION_FULL ${STORM_VERSION})
        endif()
        set(STORMPY_STORM_HAS_VERSION_TWEAK ON)
    else()
        set(STORM_VERSION_FULL ${STORM_VERSION})
        set(STORMPY_STORM_HAS_VERSION_TWEAK OFF)
    endif()
endmacro(set_storm_version_full)

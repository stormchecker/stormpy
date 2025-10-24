# Set variable to strings "True"/"False" according to condition
function(set_variable_string NAME CONDITION)
    if(CONDITION)
        set(${NAME} "True" PARENT_SCOPE)
    else()
        set(${NAME} "False" PARENT_SCOPE)
    endif()
endfunction(set_variable_string)

# Check whether Storm library is available
# Sets variable HAVE_STORM_XYZ
function(storm_with_lib NAME)
    string(TOLOWER ${NAME} NAME_LOWER)
    if(TARGET storm-${NAME_LOWER})
        set(HAVE_STORM_${NAME} TRUE PARENT_SCOPE)
    else()
        set(HAVE_STORM_${NAME} FALSE PARENT_SCOPE)
    endif()
endfunction(storm_with_lib)

# Note that the following functions cannot simply call set_variable_string because the scope would change.
# Using 'macro' instead of 'function' is also not viable because arguments are then not handled as variables any more.

# Set variable for Storm dependencies
# which can be checked with STORM_HAVE_XYZ
# Sets variable STORM_WITH_XYZ_BOOL
function(set_dependency_var NAME)
    if (STORM_HAVE_${NAME})
        set(STORM_WITH_${NAME}_BOOL "True" PARENT_SCOPE)
    else()
        set(STORM_WITH_${NAME}_BOOL "False" PARENT_SCOPE)
    endif()
endfunction(set_dependency_var)

# Set variable for optional Storm libraries (if used)
# which can be checked with HAVE_STORM_XYZ and optiona USE_STORM_XYZ
# Sets variable STORM_WITH_XYZ_BOOL
function(set_optional_lib_var NAME)
    if ((USE_STORM_${NAME}) AND (HAVE_STORM_${NAME}))
        set(STORM_WITH_${NAME}_BOOL "True" PARENT_SCOPE)
    else()
        set(STORM_WITH_${NAME}_BOOL "False" PARENT_SCOPE)
    endif()
endfunction(set_optional_lib_var)

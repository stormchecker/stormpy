#pragma once

#include <sstream>
#include <string>

/**
 * Helper function to get a string out of the stream operator.
 * Used for __str__ functions.
 */
template<typename T>
std::string streamToString(T const & t) {
    std::stringstream ss;
    ss << t;
    return ss.str();
}

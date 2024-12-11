#include "parser.h"

ParserResultWrapper<Polynomial> from_string(const std::string& input) {
    ParserResultWrapper<Polynomial> res;
    res._content = carlparser::deserialize<Polynomial>(input);
    return res;
}
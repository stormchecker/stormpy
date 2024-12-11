#pragma once

#include "src/pycarl/common.h"
#include "src/pycarl/types.h"
#include <string>
#include <carl/core/MultivariatePolynomial.h>
#include <carl-parser/Parser.h>

template<typename Pol>
struct ParserResultWrapper {
    carlparser::parser_types<Pol> _content;

    carlparser::ParserReturnType getType() const {
        return carlparser::check_type(_content);
    }

    typename Pol::CoeffType asRational() const {
        return boost::get<typename Pol::CoeffType>(_content);
    }

    carl::Monomial::Arg asMonomial() const {
        return boost::get<carl::Monomial::Arg>(_content);
    }

    carl::Variable asVariable() const {
        return boost::get<carl::Variable>(_content);
    }

    carl::Term<typename Pol::CoeffType> asTerm() const {
        return boost::get<carl::Term<typename Pol::CoeffType>>(_content);
    }

    Pol asPolynomial() const {
        return boost::get<Pol>(_content);
    }

    carl::RationalFunction<Pol, true> asRationalFunction() const {
        auto rf = boost::get<carl::RationalFunction<Pol>>(_content);
        return carl::RationalFunction<Pol, true>(rf.nominatorAsPolynomial(), rf.denominatorAsPolynomial());
    }

    carl::Constraint<Pol> asConstraint() const {
        return boost::get<carl::Constraint<Pol>>(_content);
    }

    carl::Formula<Pol> asFormula() const {
        return boost::get<carl::Formula<Pol>>(_content);
    }
};

ParserResultWrapper<Polynomial> from_string(const std::string& input);

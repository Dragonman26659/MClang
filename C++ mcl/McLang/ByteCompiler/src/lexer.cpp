#include "compiler.h"
#include <iostream>
#include <string>
#include <vector>
#include <regex>

std::vector<Token> lex(const std::string& source_code) {
    std::vector<Token> tokens;
    std::regex token_regex(R"(\b(var|funct|out|true|false|byteFunct|while|delete)\b|\b[a-zA-Z_][a-zA-Z0-9_]*\b|\b\d+\b|(\+\+|--|=|\+|-|\(|\)|\{|\}|\,|\[|\]|\#StartByte|\#EndByte|\#Define|\#include|\;|\:|\,|\"|\')|(\s+))");
    std::sregex_iterator it(source_code.begin(), source_code.end(), token_regex);
    std::sregex_iterator end;
    while (it != end) {
        std::smatch match = *it;
        std::string value = match.str();
        if (value.empty()) {
            tokens.push_back({ TokenType::END_OF_FILE, "" });
        }
        else if (std::regex_match(value, std::regex(R"(\s+)"))) {
            tokens.push_back({ TokenType::WHITESPACE, value });
        }
        else if (std::regex_match(value, std::regex(R"(\b(var|funct|out|true|false|byteFunct|while|delete)\b)"))) {
            tokens.push_back({ TokenType::KEYWORD, value });
        }
        else if (std::regex_match(value, std::regex(R"(\b[a-zA-Z_][a-zA-Z0-9_]*\b)"))) {
            tokens.push_back({ TokenType::IDENTIFIER, value });
        }
        else if (std::regex_match(value, std::regex(R"(\b\d+\b)"))) {
            tokens.push_back({ TokenType::NUMBER, value });
        }
        else if (std::regex_match(value, std::regex(R"(\+\+|--|=|\+|-|\(|\)|\{|\}|\,|\[|\]|\#StartByte|\#EndByte|\#Define|\#include|\;|\:|\,|\"|\')"))) {
            tokens.push_back({ TokenType::OPERATOR, value });
        }
        else if (std::regex_match(value, std::regex(R"(\(|\)|\{|\}|\,|\[|\]|\#StartByte|\#EndByte|\#Define|\#include|\;|\:|\,|\"|\')"))) {
            tokens.push_back({ TokenType::PUNCTUATION, value });
        }
        ++it;
    }
    return tokens;
}
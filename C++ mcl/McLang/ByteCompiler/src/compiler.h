#ifndef BYTECOMPILER_H
#define BYTECOMPILER_H

#include <vector>
#include <string>
#include <memory>

// TokenType enum declaration
enum class TokenType {
    KEYWORD,
    IDENTIFIER,
    NUMBER,
    OPERATOR,
    PUNCTUATION,
    WHITESPACE,
    END_OF_FILE
};

// Token structure declaration
struct Token {
    TokenType type;
    std::string value;
};

// Node structure declaration for AST
struct Node {
    std::string value;
    std::vector<std::unique_ptr<Node>> children;
};

// Function declarations
std::vector<Token> lex(const std::string& source_code);
Node* parse(const std::vector<Token>& tokens);
void generate_bytecode(Node* root);

#endif // BYTECOMPILER_H
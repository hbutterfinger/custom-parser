# Custom Language Parser

A compact Python parser for a small Ada-style imperative language. It reads source code, validates the syntax, builds an Abstract Syntax Tree (AST), and prints a formatted textual representation of that tree.

## Overview

This project implements a parser for a custom imperative language with familiar control-flow and expression syntax. It is designed to:

- recognize valid source programs in the language,
- build an AST that reflects the program structure,
- preserve operator precedence and associativity in expressions,
- provide a clean textual AST output for downstream tooling or testing.

The language supports assignments, output statements, conditional blocks, and both `while` and `for` loops.

## Language Features

### Statements
- Assignment
- `Put(...)` output statement
- `if ... then ... else ... end if`
- `while ... loop ... end loop`
- `for ... in ... .. ... loop ... end loop`

### Expressions
- Integer literals
- Boolean literals: `True`, `False`
- Identifiers
- Parenthesized expressions
- Arithmetic operators: `+`, `-`, `*`, `/`, `mod`
- Comparison operators: `=`, `/=`, `<`, `>`, `<=`, `>=`
- Logical operators: `and`, `or`

## Grammar Summary

```ebnf
program      ::= block-stmt
block-stmt   ::= stmt*
stmt         ::= assign-stmt
               | put-stmt
               | if-stmt
               | loop-stmt

assign-stmt  ::= id ":=" expr ";"
put-stmt     ::= "Put" "(" expr ")" ";"
if-stmt      ::= "if" expr "then" block-stmt ("else" block-stmt)? "end" "if" ";"
loop-stmt    ::= while-loop | for-loop
while-loop   ::= "while" expr "loop" block-stmt "end" "loop" ";"
for-loop     ::= "for" id "in" expr ".." expr "loop" block-stmt "end" "loop" ";"

expr         ::= conjunction ("or" conjunction)*
conjunction   ::= comparison ("and" comparison)*
comparison    ::= term (( "=" | "/=" | "<" | ">" | "<=" | ">=" ) term)?
term          ::= factor (( "+" | "-" ) factor)*
factor        ::= primary (( "*" | "/" | "mod" ) primary)*
primary       ::= integer | bool | id | "(" expr ")"
```

## Output

For valid input, the parser prints the formatted AST as text. The exact node layout and formatting follow the project’s AST node definitions, so the output can be used for testing and verification.

## Compatibility

- Python 3
- Compatible with Python 3.10 or lower
- Standard library only

No external packages are required.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/hbutterfinger/custom-parser.git
cd custom-parser
```

### 2. Run the parser

If your entry point is `Parser.py`, run:

```bash
python Parser.py < input.txt
```

If your project uses a different driver script, replace `Parser.py` with the correct file name.

### 3. View the AST output

The parser writes the AST to standard output. You can redirect it to a file if needed:

```bash
python Parser.py < input.txt > ast_output.txt
```

## Example

### Input

```text
x := 3;
y := x + 4 * 2;
if y > 5 then
    Put(y);
else
    Put(0);
end if;
```

### Output

The program prints the AST representation for the full block, including the assignment nodes, the conditional node, and the nested expressions.


##  Notes

- Keep the parser compatible with the provided AST node definitions.
- Preserve operator precedence when parsing expressions.
- Make sure nested blocks and optional `else` branches are handled correctly.
- Avoid third-party dependencies to keep the project portable.


## Acknowledgments

This project is a documentations and extension from Project 1 - CMPSC 461 @ Penn State


## Contributing

 If you extend the language, consider updating:

- the grammar summary,
- example programs,
- AST output documentation,
- any parser tests or fixtures.

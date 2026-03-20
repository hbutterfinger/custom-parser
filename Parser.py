from ASTNodeDefs import *
from typing import List, Tuple, Union, Set
import re

"""
This is the skeleton code for the Parser with a Lexer
Feel free to modify anything in this file as needed
To run tests, use Verify.py
"""


class Lexer:
    """
    The Lexer (also known as a tokenizer or scanner) is responsible for breaking
    the raw source code string into a stream of meaningful tokens.
    """

    def __init__(self, code: str):
        self.code = code
        self.tokens: List[Tuple[str, str]] = []  # List of (token_type, token_value)
        self.token_specs = [
            ("ASSIGN", r":="),
            ("SEMICOLON", r";"),
            ("COMMENT", r"--[^\n]*"),
            ("SKIP", r"[\s]+"),
            ("DOTDOT", r"\.\."),
            ("LE", r"<="),
            ("GE", r">="),
            ("NE", r"/="),
            ("EQ", r"="),
            ("LT", r"<"),
            ("GT", r">"),
            ("PLUS", r"\+"),
            ("MINUS", r"-"),
            ("STAR", r"\*"),
            ("SLASH", r"/"),
            ("LPAREN", r"\("),
            ("RPAREN", r"\)"),
            ("INTEGER", r"[0-9]+"),
            ("ID", r"[A-Za-z_][A-Za-z0-9_]*"),
            ("MISMATCH", r"."),
            # Fill in more token specifications here if needed
        ]
        self.token_regex = re.compile(
            "|".join(f"(?P<{pair[0]}>{pair[1]})" for pair in self.token_specs)
        )

    def tokenize(self) -> List[Tuple[str, str]]:
        """
        Tokenizes the input code into a list of tokens.
        Each token is represented as a tuple (token_type, token_value).
        """

        for mo in self.token_regex.finditer(self.code):
            if mo is None:
                raise RuntimeError(f"Unexpected character") #checks for empty mo
            kind = mo.lastgroup
            value = mo.group()
            if kind == "SKIP" or kind =="COMMENT":
                continue
            elif kind == "MISMATCH":
                raise RuntimeError(f"Unexpected character: {value}")
            elif kind == "ID": # keyword case
                reserved = { 
                    "if": "IF",
                    "then": "THEN",
                    "else": "ELSE",
                    "end": "END",
                    "loop": "LOOP",
                    "while": "WHILE",
                    "for": "FOR",
                    "in": "IN",
                    "Put": "PUT",
                    "and": "AND",
                    "or": "OR",
                    "mod": "MOD",
                    "True": "BOOLEAN",
                    "False": "BOOLEAN",
                } # dict for reserved keywords
                token_type = reserved.get(value, "ID")
                self.tokens.append((token_type, value)) # token for keywords 
            else: # other identifiers
                self.tokens.append((kind, value))
        self.tokens.append(("EOF", ""))  # End-of-file token
        return self.tokens


class Parser:
    def __init__(self, tokens: List[Tuple[str, str]]):
        self.tokens = tokens
        self.pos = 0  # Current position in the token list

    def current_token(self) -> Tuple[str, str]:
        # Returns the current token without consuming it
        return self.tokens[self.pos]

    def advance(self) -> None:
        # Advances to the next token unless at end of list
        if self.pos < len(self.tokens) - 1:
            self.pos += 1

    def expect(self, token_type: str) -> Tuple[str, str]:
        # Consumes the current token if it matches the expected type and returns it
        current_type, current_value = self.current_token()
        if current_type == token_type:
            self.advance()
            return (current_type, current_value)
        else:
            raise RuntimeError(
                f"Expected token type {token_type}, got type {current_type}"
            )

    def parse(self) -> ASTNode:
        block = self.parse_block()
        self.expect("EOF")
        return block

    def parse_block(self, terminators: List[str] | None = None) -> Block:
        statements: List[ASTNode] = []

        while True:
            token_type, _ = self.current_token()

            if token_type == "EOF":
                break
            if terminators is not None and token_type in terminators:
                break
            statements.append(self.parse_statement()) # only continues when both conditions are met 
        
        # wrap the statement list in a Block AST node
        return Block(statements)

    def parse_statement(self) -> Union[Assign, Put, If, WhileLoop, ForLoop]:
        # chooses how to parse based on token type
        token_type, _ = self.current_token()
        if token_type == "ID":
            return self.parse_assign_statement()
        if token_type == "PUT":
            return self.parse_put_statement()
        if token_type == "IF":
            return self.parse_if_statement()
        if token_type == "WHILE":
            return self.parse_while_loop()
        if token_type == "FOR":
            return self.parse_for_loop()
        # other types are invalid
        raise RuntimeError(f"Unexpected token type {token_type} in statement")

    def parse_assign_statement(self) -> Assign: 
        # <ID> := <expr>;
        _, name = self.expect("ID")
        self.expect("ASSIGN")
        expr = self.parse_expr()
        self.expect("SEMICOLON")

        # build the AST assignment node using an ID on the lhs
        return Assign(Identifier(name), expr)
    
    def parse_put_statement(self) -> Put:
        # Put(<expr>);
        self.expect("PUT")
        self.expect("LPAREN")
        expr = self.parse_expr()
        self.expect("RPAREN")
        self.expect("SEMICOLON")

        # return the print/output AST node
        return Put(expr)

    def parse_if_statement(self) -> If:
        # if <expr> then <block-stmt> (else<block-stmt>)? end if;
        # if statement with optional else
        self.expect("IF")
        condition = self.parse_expr()
        self.expect("THEN")

        then_block = self.parse_block({"ELSE", "END"}) # parse the "then" branch until we hit either ELSE or END

        else_block = None
        if self.current_token()[0] == "ELSE":
            self.advance()
            else_block = self.parse_block({"END"})

        self.expect("END")
        self.expect("IF")
        self.expect("SEMICOLON")

        # return the conditional AST node
        return If(condition, then_block, else_block)

    def parse_while_loop(self) -> WhileLoop:
        # while <expr> loop <block-stmt> end loop;
        self.expect("WHILE")
        condition = self.parse_expr()
        self.expect("LOOP")

        body = self.parse_block({"END"}) # parse loop body until END.
        
        self.expect("END")
        self.expect("LOOP")
        self.expect("SEMICOLON")

        # build the while loop AST node
        return WhileLoop(condition, body)

    def parse_for_loop(self) -> ForLoop:
        # for <id> in <expr> . . <expr> loop <block-stmt> end loop;
        self.expect("FOR")
        _, iterator_name = self.expect("ID") # loop var
        self.expect("IN")

        #start end of for loop
        start_expr = self.parse_expr()
        self.expect("DOTDOT")
        end_expr = self.parse_expr()

        #parse block statement until END
        self.expect("LOOP")
        body = self.parse_block({"END"})
        self.expect("END")
        self.expect("LOOP")
        self.expect("SEMICOLON")

        # return the for loop AST node
        return ForLoop(Identifier(iterator_name), start_expr, end_expr, body)

    def parse_expr(self) -> ASTNode:
        # <conjunction> (or <conjunction>)*
        # multiple conjunctions or'd together
        conjunctions = [self.parse_conjunction()]
        while self.current_token()[0] == "OR": # looks for OR
            self.advance()
            conjunctions.append(self.parse_conjunction())

        if len(conjunctions) > 1: # for multiple conjunctions
            result = Or(conjunctions)
        else: # for only one conjunction
            result = conjunctions[0]
        return result

    def parse_conjunction(self) -> ASTNode:
        # <comparison> (and <comparison>)*
        # multiple comparisons and'd together
        comparisons = [self.parse_comparison()]
        while self.current_token()[0] == "AND": # looks for AND
            self.advance()
            comparisons.append(self.parse_comparison())

        if len(comparisons) > 1: # for multiple comparisons
            result = And(comparisons)
        else: # for only one comparison
            result = comparisons[0]
        return result

    def parse_comparison(self) -> ASTNode:
        # <term> (( = | /= | < | > | <= | >= ) <term>)?
        # either a single term or two terms separated by comparison sign
        # checks left side for term first
        left = self.parse_term()
        token_type, token_value = self.current_token()
        # check for any comparisons
        if token_type in {"EQ", "NE", "LT", "GT", "LE", "GE"}:
            self.advance()
            right = self.parse_term()
            return Comparison(left, token_value, right) # if has comparisons
        
        return left # if no comparisons

    def parse_term(self) -> ASTNode:
        # <factor> (( + | - ) <factor>)*
        # each term can be multiple factors separated by addition/subtraction
        factors = [self.parse_factor()]
        operators: List[str] = []

        while self.current_token()[0] in {"PLUS", "MINUS"}: # keeps collecting factors if + or -
            operators.append(self.current_token()[1])
            self.advance()
            factors.append(self.parse_factor())
        
        if operators: # for multiple factors
            result = Term(factors, operators)
        else: # for one factor
            result = factors[0]
        return result

    def parse_factor(self) -> ASTNode:
        #  <primary> (( * | / | mod) <primary>)*
        # each factor can be multiple primaries separated by *, /, or mod
        primaries = [self.parse_primary()]
        operators: List[str] = []

        while self.current_token()[0] in {"STAR", "SLASH", "MOD"}: # keeps collecting primaries if *, /, or mod
            operators.append(self.current_token()[1])
            self.advance()
            primaries.append(self.parse_primary())
        
        if operators: # for multiple primaries
            result = Factor(primaries, operators)
        else: # for one primary
            result = primaries[0]
        return result

    def parse_primary(self) -> ASTNode:
        # <integer> | <boolean> | <id> | (<expr>)
        # primaries can only be integer ([0-9]+), booleans (True | False), ids ([a-zA-Z_][a-zA-Z0-9_]*), or expressions in parenthesis
        token_type, token_value = self.current_token()
        if token_type == "INTEGER":
            self.advance()
            return Integer(token_value)
        if token_type == "BOOLEAN":
            self.advance()
            return Boolean(token_value)
        if token_type == "ID":
            self.advance()
            return Identifier(token_value)
        if token_type == "LPAREN":
            self.advance()
            expr = self.parse_expr()
            self.expect("RPAREN")
            return expr
        
        # everything else is invalid
        raise RuntimeError(f"Unexpected token type {token_type} in primary")
    
        # More parsing methods can be added as needed
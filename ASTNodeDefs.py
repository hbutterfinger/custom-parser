from typing import List


# Base class for all AST nodes
class ASTNode:
    def to_string(self):
        """Method to provide compact string representation without newlines."""
        return repr(self)


# Class for block-stmt
class Block(ASTNode):
    def __init__(self, statements: List[ASTNode]):
        self.statements = statements

    def to_string(self):
        statement_strs = ", ".join(stmt.to_string() for stmt in self.statements)
        return f"Block([{statement_strs}])"


# Class for assign-stmt
class Assign(ASTNode):
    def __init__(self, identifier: ASTNode, expression: ASTNode):
        self.identifier = identifier
        self.expression = expression

    def to_string(self):
        return f"Assign({self.identifier.to_string()}, {self.expression.to_string()})"


# Class for put-stmt
class Put(ASTNode):
    def __init__(self, expression: ASTNode):
        self.expression = expression

    def to_string(self):
        return f"Put({self.expression.to_string()})"


# Class for if-stmt
class If(ASTNode):
    def __init__(
        self, condition: ASTNode, then_block: ASTNode, else_block: ASTNode = None
    ):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block

    def to_string(self):
        condition_str = self.condition.to_string()
        then_str = self.then_block.to_string()
        else_str = (
            self.else_block.to_string() if self.else_block is not None else "None"
        )
        return f"If({condition_str}, {then_str}, {else_str})"


# Class for while-loop
class WhileLoop(ASTNode):
    def __init__(self, condition: ASTNode, body: ASTNode):
        self.condition = condition
        self.body = body

    def to_string(self):
        condition_str = self.condition.to_string()
        body_str = self.body.to_string()
        return f"WhileLoop({condition_str}, {body_str})"


# Class for for-loop
class ForLoop(ASTNode):
    def __init__(
        self, iterator: ASTNode, start_expr: ASTNode, end_expr: ASTNode, body: ASTNode
    ):
        self.iterator = iterator
        self.start_expr = start_expr
        self.end_expr = end_expr
        self.body = body

    def to_string(self):
        iterator_str = self.iterator.to_string()
        start_str = self.start_expr.to_string()
        end_str = self.end_expr.to_string()
        body_str = self.body.to_string()
        return f"ForLoop({iterator_str}, {start_str}, {end_str}, {body_str})"


# Class for expr with 'or' operators
class Or(ASTNode):
    def __init__(self, conjunctions: List[ASTNode]):
        self.conjunctions = conjunctions

    def to_string(self):
        conj_strs = ", ".join(conj.to_string() for conj in self.conjunctions)
        return f"Or([{conj_strs}])"


# Class for conjunction with 'and' operators
class And(ASTNode):
    def __init__(self, comparisons: List[ASTNode]):
        self.comparisons = comparisons

    def to_string(self):
        comp_strs = ", ".join(comp.to_string() for comp in self.comparisons)
        return f"And([{comp_strs}])"


# Class for comparison
class Comparison(ASTNode):
    def __init__(self, left: ASTNode, operator: str, right: ASTNode):
        self.left = left
        self.operator = operator
        self.right = right

    def to_string(self):
        left_str = self.left.to_string()
        right_str = self.right.to_string()
        return f"Comparison({left_str}, {self.operator}, {right_str})"


# Class for term
class Term(ASTNode):
    def __init__(self, factors: List[ASTNode], operators: List[str]):
        assert (
            len(factors) == len(operators) + 1
        ), "Number of operators must be one less than number of factors"
        self.factors = factors
        self.operators = operators

    def to_string(self):
        # use comma to connect factors and operators
        factor_strs = [factor.to_string() for factor in self.factors]
        combined = []
        for i in range(len(self.operators)):
            combined.append(factor_strs[i])
            combined.append(self.operators[i])
        combined.append(factor_strs[-1])
        combined_str = ", ".join(combined)
        return f"Term([{combined_str}])"


# Class for factor
class Factor(ASTNode):
    def __init__(self, primaries: List[ASTNode], operators: List[str]):
        assert (
            len(primaries) == len(operators) + 1
        ), "Number of operators must be one less than number of primaries"
        self.primaries = primaries
        self.operators = operators

    def to_string(self):
        # use comma to connect primaries and operators
        primary_strs = [primary.to_string() for primary in self.primaries]
        combined = []
        for i in range(len(self.operators)):
            combined.append(primary_strs[i])
            combined.append(self.operators[i])
        combined.append(primary_strs[-1])
        combined_str = ", ".join(combined)
        return f"Factor([{combined_str}])"


# Class for Integer
class Integer(ASTNode):
    def __init__(self, value: str):
        self.value = value

    def to_string(self):
        return f"Integer({self.value})"


# Class for Boolean
class Boolean(ASTNode):
    def __init__(self, value: str):
        self.value = value

    def to_string(self):
        return f"Boolean({self.value})"


# Class for Identifier
class Identifier(ASTNode):
    def __init__(self, name: str):
        self.name = name

    def to_string(self):
        return f"Identifier({self.name})"


# Class for decl-stmt (only for Project 2)
class Decl(ASTNode):
    def __init__(
        self, identifier: ASTNode, var_type: ASTNode, initial_value: ASTNode = None
    ):
        self.identifier = identifier
        self.var_type = var_type
        self.initial_value = initial_value

    def to_string(self):
        id_str = self.identifier.to_string()
        type_str = self.var_type.to_string()
        init_str = self.initial_value.to_string() if self.initial_value else "None"
        return f"Decl({id_str}, {type_str}, {init_str})"


# Class for type (only for Project 2)
class Type(ASTNode):
    def __init__(self, type_name: str):
        self.type_name = type_name

    def to_string(self):
        return f"Type({self.type_name})"


# Class for error (only for Project 2 when violating rules)
class Error(ASTNode):
    def __init__(self):
        pass

    def to_string(self):
        return "Invalid"

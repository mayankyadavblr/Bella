class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __eq__(self, other):
        if isinstance(other, Token):
            return self.type == other.type and self.value == other.value
        return False

    def __repr__(self):
        return f'Token({self.type}, {self.value})'


class Lexer:
    def __init__(self, input):
        self.input = input
        self.position = 0

    def tokenize(self):
        pass // You need to write code here

class Node:
    def __init__(self, type, value=None, children=None):
        self.type = type
        self.value = value
        self.children = children if children is not None else []

    def __str__(self, level=0):
        ret = "\t" * level + f'{self.type}: {self.value}\n'
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def consume(self, expected_type=None):
        pass // You need to write code here

    def peek(self):
        pass // You need to write code here

    def parse(self):
        pass // You need to write code here

    def parse_statement(self):
        pass // You need to write code here

    def parse_assignment(self):
        pass // You need to write code here

    def parse_expression(self):
        pass // You need to write code here

    def parse_term(self):
        pass // You need to write code here


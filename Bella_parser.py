from temp_lexer import Lexer, Token

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
    
    def consumeValue(self, tokenValue):
        print(self.tokens[self.position].value)
        if self.tokens[self.position].value == tokenValue:
            self.position += 1
            return self.tokens[self.position - 1]
        else:
            raise SyntaxError(f'Expected {tokenValue} but found {self.tokens[self.position].value}')
        
    def consumeType(self, tokenType):
        if self.tokens[self.position].type == tokenType:
            self.position += 1
            return self.tokens[self.position - 1]
        else:
            return SyntaxError(f'Expected {tokenType} but found {self.tokens[self.position].type}')
    def peek(self):
        return self.tokens[self.position + 1]

    def parse(self):
        return self.parseProgram()

    def parseProgram(self):
        root = Node("Program")
        while self.position < len(self.tokens):
            if self.tokens[self.position].value == '{':
                root.children += [self.parseBlock()]
            else:
                root.children += [self.parseStatement()]

    def parseBlock(self):
        root = Node("Block")
        while self.position < len(self.tokens):
            if self.tokens[self.position].value == '}':
                self.consumeValue('}')
                return
            else:
                root.children += [self.parseStatement()]

    def parseStatement(self):
        if self.tokens[self.position].value == 'let':
            return self.parseDeclaration()
        
        elif self.tokens[self.position].value == 'function':
            return self.parseFunction()
        
        elif self.tokens[self.position].value == 'print':
            return self.parsePrint()
        
        elif self.tokens[self.position].type == 'VARIABLE':
            return self.parseAssignment()

        elif self.tokens[self.position].value == 'while':
            return self.parseWhile()

    def parseExpression(self):
        
        left = self.parseTerm()
        return left
        if self.tokens[self.position].value in ['-', '!']:
            return [self.parseUnary()]
        
        if self.tokens[self.position].value in ['+', '-', '*', '/', '%', '**', '<', '<=', '==', '!=', '>=', '>', '&&', '||']:
            return [self.parseBinary()]
        else:
            return left
        

    def parseBinary(self, left): 
        root = Node("Binary")
        root.children += [self.parseExpression()]
        root.children += [self.consumeValue(self.tokens[self.position].value)]
        root.children += [self.parseExpression()]

        return root

    def parseUnary(self):
        root = Node("Unary")
        root.children += [self.consumeValue(self.tokens[self.position].value)]
        root.children += [self.parseExpression()]
        return root

    def parseDeclaration(self):
        root = Node("Assignment")
        self.consumeValue('let')
        root.children += [self.parseVariable()]
        self.consumeValue('=')
        root.children += [self.parseExpression()]
        self.consumeValue(';')
        return root
    
    def parseFunction(self):
        root = Node("Function")
        self.consumeValue('function')
        root.children += [self.parseVariable()]
        self.consumeValue('(')
        params = Node("Parameters")
        while self.tokens[self.position].value != ')':
            params.children += [self.parseVariable()]
        self.consumeValue(')')
        root.children += [params]
        root.children += [self.parseBlock()]
        return root
    
    def parsePrint(self):
        root = Node("Print")
        self.consumeValue('print')
        root.children += [self.parseExpression()]
        self.consumeValue(';')
        return root
    
    def parseAssignment(self):
        root = Node("Assignment")
        root.children += [self.parseVariable()]
        self.consumeValue('=')
        root.children += [self.parseExpression()]
        self.consumeValue(';')
        return root

    def parseWhile(self):
        root = Node("While")
        self.consumeValue('while')
        root.children += [self.parseExpression()]
        root.children += [self.parseBlock()]
        return root

    def parseInteger(self):
        root = Node("INTEGER", self.consumeType("INTEGER").value)
        return root

    def parseVariable(self):
        root = Node("ID", self.consumeType("ID").value)
        return root
    
    def parseTerm(self):
        if self.tokens[self.position].type == 'INTEGER':
            return self.parseInteger()
        elif self.tokens[self.position].type == 'ID':
            return self.parseVariable()

    

print(Parser(Lexer('let x = 5;').lexer()).parse())

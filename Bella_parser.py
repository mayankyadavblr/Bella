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
        #print(self.tokens[self.position].value)
        if self.tokens[self.position].value == tokenValue:
            self.position += 1
            return self.tokens[self.position - 1]
        else:
            raise SyntaxError(f'Expected {tokenValue} but found {self.tokens[self.position].value}')
    
    def at(self):
        return self.tokens[self.position]

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
        while self.at().type != 'EOF': 
            print(self.at().value)
            if self.tokens[self.position].value == '{':
                self.consumeValue('{')
                root.children += [self.parseBlock()]
            else:
                root.children += [self.parseStatement()]
        return root

    def parseBlock(self):
        root = Node("Block")
        while self.at().type != 'RBRACE':
            if self.at().value == '{':
                self.consumeValue('{')
                root.children += [self.parseBlock()]
            else:
                root.children += [self.parseStatement()]
        self.consumeValue('}')
        return root

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
        
        
        return self.parseComparison()

        
    def parseComparison(self):
        left = self.parseAdditive()

        while self.at().value in ['<', '<=', '==', '!=', '>=', '>']:
            op = self.consumeValue(self.at().value)
            right = self.parseAdditive()
            left = Node("BINOP", op.value, children=[left, right])

        return left
        
    def parseAdditive(self):
        left = self.parseMultiplicative()

        while self.at().value in ['+', '-']:
            op = self.consumeValue(self.at().value)
            right = self.parseMultiplicative()
            left = Node("BINOP", op.value, children=[left, right])
        
        return left

    def parseMultiplicative(self):
        left = self.parseFundamental()

        while self.at().value in ['*', '/', '%', '**']:
            op = self.consumeValue(self.at().value)
            right = self.parseFundamental()
            left = Node("BINOP", op.value, children=[left, right])
        
        return left
    
    def parseUnary(self):

        if self.at().value in ['-', '!']:
            op = self.consumeValue(self.at().value)
            right = self.parseFundamental()
            return Node(op.value, children=[right])
        else:
            return self.parsePrimary()

    def parseDeclaration(self):
        root = Node("Assignment")
        self.consumeValue('let')
        root.children += [self.parseFundamental()]
        self.consumeValue('=')
        root.children += [self.parseExpression()]
        self.consumeValue(';')
        return root
    
    def parseFunction(self):
        root = Node("Function")
        self.consumeValue('function')
        root.children += [self.parseFundamental()]
        self.consumeValue('(')
        params = Node("Parameters")
        while self.tokens[self.position].value != ')':
            params.children += [self.parseFundamental()]
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
        root.children += [self.parseFundamental()]
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

    def parseFundamental(self):
        tk = self.at()
        self.position += 1

        if tk.type == 'NUMBER':
            return Node(tk.type, tk.value)
        elif tk.type == 'ID':
            return Node(tk.type, tk.value)
        elif tk.type == 'LPAREN':
            self.consumeType('LPAREN')
            root = self.parseExpression()
            self.consumeType('RPAREN')
            return root

    
tokens = Lexer('let x = 5 * (y - 10); {let y = x;{let z = 1 * 2; let mayank = god;}}').lexer()
print(tokens)
print(Parser(tokens).parse())

from temp_lexer import Lexer, Token
from SymbolTable import *

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
        self.symbol_table = SymbolTable()
    
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
        root = self.parseProgram()
        if self.symbol_table.valid_mem_stack():
            return root
        else:
            raise Exception("Memory not freed segmentation fault")

    def parseProgram(self):
        root = Node("Program")
        while self.at().type != 'EOF': 
            print(self.at().value)
            if self.tokens[self.position].value == '{':
                self.consumeValue('{')
                root.children += [self.parseBlock(self.symbol_table)]
            else:
                root.children += [self.parseStatement(self.symbol_table)]
        return root

    def parseBlock(self, table):
        root = Node("Block")
        while self.at().type != 'RBRACE':
            if self.at().value == '{':
                self.consumeValue('{')
                root.children += [self.parseBlock()]
            else:
                root.children += [self.parseStatement(table)]
        self.consumeValue('}')
        return root

    def parseStatement(self, table):
        if self.tokens[self.position].value == 'let':
            return self.parseDeclaration(table)
        
        elif self.tokens[self.position].value == 'function':
            return self.parseFunction()
        
        elif self.tokens[self.position].value == 'print':
            return self.parsePrint()
        
        elif self.tokens[self.position].type == 'ID':
            return self.parseAssignment(table)

        elif self.tokens[self.position].value == 'while':
            return self.parseWhile(table)
        
        elif self.at().type == 'LBRACE':
            return self.parseBlock()
        
        elif self.at().type == 'FREE':
            return self.parseFree(table)
    
    def parseFree(self, table):
        root = Node("FREE")

        self.consumeType("FREE")
        self.consumeValue("(")
        
        tk = self.consumeType("ID")
        if tk.value in table.mem_stack:
            table.mem_stack.remove(tk.value)
        else:
            raise Exception(f"Variable not allocated: {tk.value}")
        root.children += [Node(tk.type, tk.value)]
        self.consumeValue(")")
        self.consumeValue(";")
        return root

    def parseExpression(self, table):

        return self.parseLogical(table)
    
    def parseTernary(self, left, table):
        root = Node("TriOp")
        root.children += [left]
        self.consumeValue('?')
        root.children += [self.parseLogical(table)]
        self.consumeValue(':')
        root.children += [self.parseExpression(table)]
        #root.children += [self.parseExpression()]
        return root

    def parseLogical(self, table):
        left = self.parseComparison(table)

        if self.at().value == '?':
            return self.parseTernary(left, table)

        while self.at().value in ['&&', '||']:
            op = self.consumeValue(self.at().value)
            right = self.parseComparison(table)
            left = Node("BINOP", op.value, children=[left, right])
        
        return left
        
    def parseComparison(self, table):
        left = self.parseAdditive(table)

        while self.at().value in ['<', '<=', '==', '!=', '>=', '>']:
            op = self.consumeValue(self.at().value)
            right = self.parseAdditive(table)
            left = Node("BINOP", op.value, children=[left, right])

        return left
        
    def parseAdditive(self, table):
        left = self.parseMultiplicative(table)

        while self.at().value in ['+', '-']:
            op = self.consumeValue(self.at().value)
            right = self.parseMultiplicative(table)
            left = Node("BINOP", op.value, children=[left, right])
        
        return left

    def parseMultiplicative(self, table):
        left = self.parseFundamental(table)

        while self.at().value in ['*', '/', '%', '**']:
            op = self.consumeValue(self.at().value)
            right = self.parseFundamental(table)
            left = Node("BINOP", op.value, children=[left, right])
        
        return left
    
    def parseUnary(self):

        if self.at().value in ['-', '!']:
            op = self.consumeValue(self.at().value)
            right = self.parseFundamental()
            return Node(op.value, children=[right])
        else:
            return self.parsePrimary()

    def parseDeclaration(self, table):
        root = Node("Declaration")
        self.consumeValue('let')
        tk = self.consumeType("ID")

        root.children += [Node(tk.type, tk.value)]

        if tk.value not in table.table:
            table.add(tk.value, "NUMBER")
        else:
            raise Exception(f"Variable already declared: {root.children[0].value}")

        self.consumeValue('=')

        if self.at().type == "ALLOC":
            self.consumeValue('alloc')
            self.consumeType("LPAREN")
            self.consumeType("RPAREN")
            self.consumeValue(";")
            root.children += [Node("MEMORY")]
            if tk.value in table.mem_stack:
                raise Exception(f"Variable already allocated: {tk.value}")
            else:
                table.mem_stack += [tk.value]
            return root

        root.children += [self.parseExpression(self.symbol_table)]
        self.consumeValue(';')
        return root
    
    def parseFunction(self):
        root = Node("Function")
        self.consumeValue('function')
        tk = self.consumeType('ID')
        root.children += [Node(tk.type, tk.value)]
        self.consumeValue('(')
        self.symbol_table.add(tk.value, "FUNCTION")

        params = Node("Parameters")
        
        function_table = SymbolTable()
        
        tk = self.consumeType("ID")
        params.children += [Node(tk.type, tk.value)]
        while self.at().value != ')':
            self.consumeValue(',')
            tk = self.consumeType("ID")
            params.children += [Node(tk.type, tk.value)]
        self.consumeValue(')')
        self.consumeValue('=')
        root.children += [params]


        for child in params.children:
            function_table.add(child.value, "NUMBER")
        
        function_table.parent = self.symbol_table
        self.symbol_table.children += [function_table]

        root.children += [self.parseExpression(function_table)]
        self.consumeValue(';')
        return root
    
    def parsePrint(self):
        root = Node("Print")
        self.consumeValue('print')
        root.children += [self.parseExpression()]
        self.consumeValue(';')
        return root
    
    def parseAssignment(self, table):
        root = Node("Assignment")
        root.children += [self.parseFundamental(self.symbol_table)]

        if self.symbol_table.lookup(root.children[0].value) == None:
            raise Exception(f"Variable not declared: assignment {root.children[0].value}")

        self.consumeValue('=')
        root.children += [self.parseExpression(table)]
        self.consumeValue(';')
        return root

    def parseWhile(self, table):
        root = Node("While")
        self.consumeValue('while')
        root.children += [self.parseExpression(table)]
        self.consumeValue('{')

        while_table = SymbolTable()
        while_table.parent = table
        table.children += [while_table]

        root.children += [self.parseBlock(while_table)]
        return root

    def parseFundamental(self, table):
        tk = self.at()
        self.position += 1

        if tk.type == "ID":
            tk_type = table.lookup(tk.value)
            if tk_type == None:
                print(f"Variable not delcared fundamental: {tk.value}")
                exit()
                raise Exception(f"Variable not declared: {tk.value}")
            else:
                table.update(tk.value, tk_type)
                

        if tk.type == 'NUMBER':
            return Node(tk.type, tk.value)
        elif tk.type == 'ID':
            if self.at().value == '(':
                return self.parseFunctionCall(tk, table)
            return Node(tk.type, tk.value)
        elif tk.type == 'LPAREN':
            self.consumeType('LPAREN')
            root = self.parseExpression(table)
            self.consumeType('RPAREN')
            return root
    
    def parseFunctionCall(self, tk, table):
        root = Node("FunctionCall")
        root.children += [Node("ID", tk.value)]
        self.consumeValue('(')
        root.children += [self.parseExpression(table)]
        while self.at().value != ')':
            self.consumeValue(',')
            root.children += [self.parseExpression(table)]
        self.consumeValue(')')
        return root


tokens = Lexer('''
                let x = alloc();
                free(x);
                let dozen = 12; 
                function gcd(x, y) = y == 0 ? x : gcd(dozen, x % y) ; 
                while dozen >= 3 || (gcd(1, 10) != 5) { 
                    let triple = 5;
                    let y = alloc();
                    free(y);
                    dozen = dozen - 2.75E+19 ** 1 ** 3;
               }
               ''').lexer()
print(tokens)
parser = Parser(tokens)
print(parser.parse())
print(parser.symbol_table)
print(parser.symbol_table.mem_stack)

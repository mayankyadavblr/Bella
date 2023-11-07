from temp_lexer import Lexer, Token, TokenType

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return AST.Integer(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node

    def term(self):
        node = self.factor()

        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            token = self.current_token
            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif token.type == TokenType.DIV:
                self.eat(TokenType.DIV)

            node = AST.BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        node = self.term()

        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)

            node = AST.BinOp(left=node, op=token, right=self.term())

        return node

class AST:
    class BinOp:
        def __init__(self, left, op, right):
            self.left = left
            self.token = self.op = op
            self.right = right

    class Integer:
        def __init__(self, token):
            self.token = token
            self.value = token.value

    def __str__(self):
        return str(self.__dict__)

def main():
    lexer = Lexer('2 + 3 * 4')
    parser = Parser(lexer)
    tree = parser.expr()
    print(tree)

if __name__ == '__main__':
    main()

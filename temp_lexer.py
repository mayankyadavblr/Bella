import re

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
class Lexer():
    tokenFormats = {
        "WHILE": r'\bwhile\b',
        "LET": r'\blet\b',
        "FUNCTION": r'\bfunction\b',
        "TRUE": r'\btrue\b',
        "FALSE": r'\bfalse\b',
        "IF": r'\bif\b',
        "ELSE": r'\belse\b',
        "PRINT": r'\bprint\b',
        "ID": r'[a-zA-Z_][a-zA-Z0-9_]*',
        #"NUMBER": r'[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)',
        "NUMBER": r'[+\-]?(?:0|[1-9]\d*)(?:\.\d+)?(?:[eE][+\-]?\d+)?',
        "PLUS": r'\+',
        "MINUS": r'-',
        "TIMES": r'\*[^\*]',
        "EXPONENT": r'\*\*',
        "DIVIDE": r'/',
        "MODULO": r'%',
        "EQUALS": r'[^=^>^<^!]=[^=^>^<^!]',
        "LPAREN": r'\(',
        "RPAREN": r'\)',
        "LBRACE": r'{',
        "RBRACE": r'}',
        "SEMICOLON": r';',
        "COMMA": r',',
        "AND": r'&&',
        "OR": r'\|\|',
        "NOT": r'![^=]',
        "LT": r'<[^=]',
        "LE": r'<=',
        "EQ": r'==',
        "NE": r'!=',
        "GE": r'>=',
        "GT": r'>[^=]',
        "QUESTION": r'\?',
        "COLON": r':',
        "IGNORE": r'\t|\n|\s'
    }
    
    def __init__(self, input):
        self.input = input

    def lexer(self):
        input = self.input
        pos = 0
        tokens = []
        while pos < len(input):
            match = None
            for tokenFormat in Lexer.tokenFormats:
                pattern, tag = Lexer.tokenFormats[tokenFormat], tokenFormat
                regex = re.compile(pattern)
                match = regex.match(input, pos) #Essentially Build Lexeme
                #print(pattern, tag, match)
                find = False
                if match is not None:
                    lexeme = match.group(0)
                    find = True

                    #attr = checkForAttribute(lexeme,tag)
                    if not tag == "IGNORE":
                        token = Token(tag, lexeme.strip()) #removed attr from here
                        tokens.append(token)
                        break

            if not find:
                print(f'Illegal or unknown character: {input[pos]}, {pos}')
                pos = pos + 1
            else:
                pos = match.end(0)
        return tokens 

test_input = '''
let x = 5;
'''
tokens = Lexer(test_input).lexer()
print(tokens)
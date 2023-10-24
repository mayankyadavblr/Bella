import re
import sys

tokens = {
    "WHILE": r'\bwhile\b',
    "LET": r'\blet\b',
    "FUNCTION": r'\bfunction\b',
    "TRUE": r'\btrue\b',
    "FALSE": r'\bfalse\b',
    "IF": r'\bif\b',
    "ELSE": r'\belse\b',
    "PRINT": r'\bprint\b',
    "ID": r'[a-zA-Z_][a-zA-Z0-9_]*',
    "NUMBER": r'\d+',
    "PLUS": r'\+',
    "MINUS": r'-',
    "TIMES": r'\*[^\*]',
    "EXPONENT": r'\*\*',
    "DIVIDE": r'/',
    "MODULO": r'%',
    "EQUALS": r'[^=^>^<^!]=[^=^>^<^!]',
    "LPAREN": r'\(',
    "RPAREN": r'\)',
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
    "IGNORE": r' \t'
}

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*[^\*]'
t_EXPO = r'\*\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_SEMICOLON = r';'
t_COMMA = r','
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_LT = r'<^='
t_LE = r'<='
t_EQ = r'=='
t_NE = r'!='
t_GE = r'>='
t_GT = r'>^='
t_QUESTION = r'\?'
t_COLON = r':'
t_EQUALS = r'='
t_WHILE = r'\bwhile\b'
t_LET = r'\blet\b'
t_FUNCTION = r'\bfunction\b'
t_TRUE = r'\btrue\b'
t_FALSE = r'\bfalse\b'
t_IF = r'\bif\b'
t_ELSE = r'\belse\b'
t_PRINT = r'\bprint\b'
t_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_NUMBER = r'\d+'
t_ignore  = ' \t|\n|\s'


def lexer(input, tokenFormats):
    pos = 0
    tokens = []
    while pos < len(input):
        match = None
        for tokenFormat in tokenFormats:
            pattern, tag = tokenFormats[tokenFormat], tokenFormat
            regex = re.compile(pattern)
            match = regex.match(input,pos) #Essentially Build Lexeme
            #print(pattern, tag, match)
            find = False
            if match is not None:
                lexeme = match.group(0)

                #attr = checkForAttribute(lexeme,tag)
                if not tag == "IGNORE":
                    token = (lexeme, tag) #removed attr from here
                    tokens.append(token)
                    find = True
                    break

        if not find:
            print('Illegal or unknown character: %s' % pos)
            pos = pos + 1
        else:
            pos = match.end(0)
    return tokens 

test_input = '''
let dozen = 12;
print dozen % 3 ** 1; 
'''
tokens = lexer(test_input, tokens)
print(tokens)
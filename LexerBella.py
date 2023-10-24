import re
import sys

TOKENS = {
    "WHILE",
    "LET",
    "FUNCTION",
    "TRUE",
    "FALSE",
    "IF",
    "ELSE",
    "PRINT",
    "ID",
    "NUMBER",
    "PLUS",
    "MINUS",
    "TIMES",
    "EXPONENT",
    "DIVIDE",
    "EQUALS",
    "LPAREN",
    "RPAREN",
    "SEMICOLON",
    "COMMA",
    "AND",
    "OR",
    "NOT",
    "LT",
    "LE",
    "EQ",
    "NE",
    "GE",
    "GT",
    "QUESTION",
    "COLON"
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
t_LT = r'<'
t_LE = r'<='
t_EQ = r'=='
t_NE = r'!='
t_GE = r'>='
t_GT = r'>'
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
# t_ignore  = ' \t'


def lexer(input, tokenFormats):
    pos = 0
    tokens = []
    while pos < len(input):
        match = None
        for tokenFormat in tokenFormats:
            pattern, tag = tokenFormat
            regex = re.compile(pattern)
            match = regex.match(input,pos) #Essentially Build Lexeme
            if match:
                lexeme = match.group(0)
                if tag:
                    #attr = checkForAttribute(lexeme,tag)
                    token = (lexeme, tag) #removed attr from here
                    tokens.append(token)
                    break
                else:
                    break
        if not match:
            sys.stderr.write('Illegal or unknown character: %s\n' % input[pos])
            pos = pos + 1
        else:
            pos = match.end(0)
    return tokens

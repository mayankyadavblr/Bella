import re

def tokenizer_WHILE(txt): 
    output = []
    for match in re.finditer(r'>[^=]', txt):
        output += [(match.group(), match.span())]
    return output

print(tokenizer_WHILE(" > >= >= >"))
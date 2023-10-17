import re

def tokenizer_WHILE(txt): 
    output = []
    for match in re.finditer(r'\bwhile\b', txt):
        output += [(match.group(), match.span())]
    return output

print(tokenizer_WHILE(" while blah blah while+while"))
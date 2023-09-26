import re

regex_dict = {
    'program': re.compile(r'Program = (?P<statement>+)'),
    'statement': re.compile(r'''Statement = (?P<let>)\s(?P<id>)\s?=\s?(?P<exp>)\s?;
                            |(?P<function>)\s(?P<id>)\s?(?P<params>)\s?=\s?(?P<exp>)\s?;
                            |(?)<exp7_id>\s?=\s?(?P<exp>)\s?;
                            |print\s(?P<exp>)\s?;
                            |while\s(?P<exp>)\s(?P<block>)
                            '''),   
     'params': re.compile(r"\(\s?(?P<id>)(,(?P<id>))*\)"),
     'block': re.compile(r"\{(?P<statement>)*\}"),
     'exp': re.compile(r"(-|!)(?P<exp7>)|(?P<exp1>)|(?P<exp1>)\?(?P<exp1>)\:(?P<exp>)"),
     'exp1': re.compile(r"(?P<exp1>)\|\|(?P<exp2>)|(?P<exp2>)"),
     'exp2': re.compile(r"(?P<exp2>)&&(?P<exp3>)|(?P<exp3>)"),
     'exp3': re.compile(r"(?P<exp4>)("<="|"<"|"=="|"!="|">="|">")(?P<exp4>)"),
     'exp4': re.compile(r"(?P<exp4>)(\+|\-)(?P<exp5>)|(?P<exp5>)"),
}


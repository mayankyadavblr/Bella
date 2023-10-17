import re

regex_dict = {
    'program': re.compile(r'(<statement>)+'),
    'statement': re.compile(r'''(<let>)\s(<id>)\s?=\s?(<exp>)\s?\;
                            |(<function>)\s(<id>)\s?(<params>)\s?=\s?(<exp>)\s?;
                            |(<exp7_id>)\s?=\s?(<exp>)\s?;
                            |print\s(<exp>)\s?;
                            |while\s(<exp>)\s(<block>)
                            '''),   
    'params': re.compile(r"\(\s?(<id>)(,(<id>))*\)"),
    'block': re.compile(r"\{(<statement>)*\}"),
    'exp': re.compile(r"(-|!)(<exp7>)|(<exp1>)|(<exp1>)\?(<exp1>)\:(<exp>)"),
    'exp1': re.compile(r"(<exp1>)\|\|(<exp2>)|(<exp2>)"),
    'exp2': re.compile(r"(<exp2>)&&(<exp3>)|(<exp3>)"),
    'exp4': re.compile(r"(<exp4>)(\+|\-)(<exp5>)|(<exp5>)"),
    'exp3': re.compile(r'''(<exp4>)("<="|"<"|"=="|"!="|">="|">")(<exp4>)'''),
    'exp5': re.compile(r"(<exp5>)(\*|\/|\%)(<exp6>)|(<exp6>)"),
    'exp6': re.compile(r"(<exp6>)(\*\*)(<exp7>)|(<exp7>)"),
    'exp7': re.compile(r"(<num>)|true|false|(<call>)|(<id>)|\((<exp>)\)"),

    'call': re.compile(r"(<id>)\((<exp>)(,(<exp>))*\)"),
    'let': re.compile(r"let"),
    'function': re.compile(r"function"),
    'while': re.compile(r"while"),
    'true': re.compile(r"true"),
    'false': re.compile(r"false"),
    'print': re.compile(r"print"),
    'keyword': re.compile(r"(<let>)|(<function>)|(<while>)|(<true>)|(<false>)|(<print>)"),
    'digit': re.compile(r"[0-9]"),
    'num': re.compile(r"(<digit>)+ (\.(<digit>)+)? ((E | e) (\+ | \-)? (<digit>)+)?"),
    'id': re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")

}

def _parse_line(line):
    """
    Do a regex search against all defined regexes and
    return the key and match result of the first matching regex

    """

    for key, rx in regex_dict.items():
        match = rx.search(line)
        if match:
            print(key, match)
    # if there are no matches
    return None, None

_parse_line("while")
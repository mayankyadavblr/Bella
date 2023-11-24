from Bella_parser import *

class SymbolTable:

    def __init__(self):
        self.table = {}
        self.parent = None
    
    def add(self, name, type_of_var):
        if name in self.table:
            raise ValueError(f'Variable {name} already defined in scope')
        self.table[name] = type_of_var

    def lookup(self, name):
        if name in self.table:
            return self.table[name]
        elif self.parent is not None:
            return self.parent.lookup(name)
        else:
            raise ValueError(f'Variable {name} not defined in scope')
    
output = {'number': ['+', '-', '*', '/', '%', '**'], 'boolean_out': ['==', '!=', '<', '<=', '>', '>='], 'boolean_in': ['&&', '||', '!']}
def walkExp(root, table):

    if root.value in output['number']:
        return walkExp(root.children[0], table) == 'number' and 'number' == walkExp(root.children[1], table)
    elif root.value in output['boolean_out']:
        return walkExp(root.children[0], table) == 'number' and 'number' == walkExp(root.children[1], table)
    elif root.value in output['boolean_in']:
        return walkExp(root.children[0], table) == walkExp(root.children[1], table)
    elif root.value == 'ID':
        return table.lookup(root.value)
    elif root.value == 'NUMBER':
        return 'number'
    

def buildSymbolTable(root):

    table = SymbolTable()

    for child in root.children:
        if child.value == 'Function':
            table.add(child.children[0].value, 'function')
            for param in child.children[1].children:
                table.add(param.value, 'void')
            
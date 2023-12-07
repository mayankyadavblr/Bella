class TypeChecker:

    @staticmethod
    def check_assignment(target_type, value_type):
        # Your task: Complete the function
        if target_type == value_type:
            return True
        elif target_type == 'FLOAT' and value_type == 'INTEGER':
            return True
        elif target_type == 'VOID':
            return True
        else:
            return False
    
    @staticmethod
    def result_type_of_op(left_type, op, right_type):
        """
        Determines the resulting type of a binary operation given the types of its operands.

        Args:
            left_type (str): The type of the left operand.
            op (str): The operator being applied.
            right_type (str): The type of the right operand.

        Returns:
            str: The resulting type of the operation.
        """
        valid_ops = ['+', '-', '*', '/'] #Hint
        # Your task: Complete the function
        if op not in valid_ops:
            raise Exception(f'Invalid operator {op}')
        elif left_type == 'CHAR' or right_type == 'CHAR':
            raise Exception(f'Invalid operand type {left_type} or {right_type}')
        elif left_type == 'FLOAT' or right_type == 'FLOAT':
            return 'FLOAT'
        elif left_type == 'VOID' or right_type == 'VOID':
            return 'FLOAT'
        else:
            return 'INTEGER'

    @staticmethod
    def check_op(left_type, op, right_type):
        # Your task: Complete the function
        valid_ops = ['+', '-', '*', '/']
        if op not in valid_ops:
            return False
        elif left_type == 'CHAR' or right_type == 'CHAR':
            return False
        else:
            return True
        
class SymbolTable:
    def __init__(self, parent=None):
        self.table = {}
        self.parent = parent
        self.children = []
        self.mem_stack = []
    
    def __str__(self, level=0):
        ret = "\t" * level + f'{self.table}\n'
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret

    def valid_mem_stack(self):
        if len(self.mem_stack) != 0:
            return False
        for child in self.children:
            if not child.valid_mem_stack():
                return False
        return True

    def add(self, identifier, type):
        # Your task: Complete the function
        if identifier in self.table:
            raise Exception(f'Variable {identifier} already declared')
        else:
            self.table[identifier] = type

    '''def is_initialized(self, identifier):
        # Your task: Complete the function
        return self.table[identifier][1]'''

    '''def set_initialized(self, identifier):
        # Your task: Complete the function
        if identifier in self.table:
            self.table[identifier] = (self.table[identifier][0], True)'''

    def lookup(self, identifier):
        # Your task: Complete the function
        if identifier not in self.table:
            if self.parent is not None:
                return self.parent.lookup(identifier)
            else:
                return None
        return self.table[identifier]
    
    def update(self, identifier, type):
        if identifier in self.table:
            pass
        else:
            self.table[identifier] = type

    '''def update(self, identifier, newType):
        # Your task: Complete the function
        if identifier in self.table:
            self.table[identifier] = (newType, self.table[identifier])
        else:
            raise Exception(f'Variable {identifier} not declared')'''
import re
import ply.lex as lex


class LexManager:

    def __init__(self):
        self.errors = []

    reserved = {
        'int': 'INT',
        'float': 'FLOAT',
        'string': 'STRING',
        'bool': 'BOOLEAN',
        'if': 'IF',
        'else': 'ELSE',
        'elif': 'ELIF',
        'while': 'WHILE',
        'print': 'PRINT',
        'read': 'READ',
        'do': 'DO',
        'for': 'FOR',
        'true': 'BOOLEAN_VALUE_T',
        'false': 'BOOLEAN_VALUE_F'
    }

    literals = ['=', '+', '-', '*', '/', '^',
                ">", "<", '(', ')', '{', '}', ';']

    tokens = [
        'EQUALS',
        'DIFFERENT',
        'GREAT_EQUAL',
        'LESS_EQUAL',
        'AND',
        'OR',
        'INT_VALUE',
        'FLOAT_VALUE',
        'STRING_VALUE',
        'ID'
    ] + list(reserved.values())

    # Regular expression rules for simple tokens

    t_EQUALS = r'=='
    t_DIFFERENT = r'!='
    t_GREAT_EQUAL = r'>='
    t_LESS_EQUAL = r'<='
    t_AND = r'&&'
    t_OR = r'\|\|'

    def t_ID(self, t):
        r'[a-zA-Z]+[a-zA-Z0-9]*'
        t.type = self.reserved.get(t.value, 'ID')
        return t

    def t_FLOAT_VALUE(self, t):
        r'[0-9]*\.[0-9]+'
        t.value = float(t.value)
        return t

    def t_INT_VALUE(self, t):
        r'[0-9]+'
        t.value = int(t.value)
        return t

    def t_STRING_VALUE(self, t):
        r'".*"'
        return t

    def t_newline(self, t):
        r'\n+|\r+|(\r\n)+'
        t.lexer.lineno += len(t.value)

    t_ignore = ' \t'

    def t_error(self, t):
        error = re.match(r'.+?[\s;]', t.value)
        if error is None:
            t.lexer.skip(len(t.value))
        else:
            t.value = t.value[error.span()[0]: error.span()[1]-1]
            t.lexer.skip(error.span()[1]-1)
        self.errors.append(
            "Token {} Not recognized at line {}".format(t.value, t.lineno))

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer

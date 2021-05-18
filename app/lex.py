import re
import ply.lex as lex

tokens = (
    'INT',
    'FLOAT',
    'STRING',
    'BOOLEAN',
    'ASSIGN',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'POW',
    'EQUALS',
    'DIFFERENT',
    'GREAT_THAN',
    'LESS_THAN',
    'GREAT_EQUAL',
    'LESS_EQUAL',
    'AND',
    'OR',
    'PRINT',
    'IF',
    'ELSE',
    'ELIF',
    'WHILE',
    'DO',
    'FOR',
    'LPAREN',
    'RPAREN',
    'LBRACK',
    'RBRACK',
    'INT_VALUE',
    'FLOAT_VALUE',
    'BOOLEAN_VALUE',
    'STRING_VALUE',
    'END_STATEMENT',
    'ID'
)

# Regular expression rules for simple tokens
t_INT = r'int'
t_FLOAT = r'float'
t_STRING = r'string'
t_BOOLEAN = r'bool'
t_ASSIGN = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_POW = r'\^'
t_EQUALS = r'=='
t_DIFFERENT = r'!='
t_GREAT_THAN = r'>'
t_LESS_THAN = r'<'
t_GREAT_EQUAL = r'>='
t_LESS_EQUAL = r'<='
t_AND = r'&&'
t_OR = r'\|\|'
t_PRINT = r'print'
t_IF = r'if'
t_ELSE = r'else'
t_ELIF = r'elif'
t_WHILE = r'while'
t_DO = r'do'
t_FOR = r'for'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACK = r'{'
t_RBRACK = r'}'
t_END_STATEMENT = r';'
t_ID = r'[a-zA-Z]+[a-zA-Z0-9]*'


def t_INT_VALUE(t):
    r'[+-]?[0-9]+'
    t.value = int(t.value)
    return t


def t_FLOAT_VALUE(t):
    r'[+-]?([0-9]*[.])?[0-9]+'
    t.value = float(t.value)
    return t


def t_BOOLEAN_VALUE(t):
    r'true|false'
    t.value = t.value == "true"
    return t


def t_STRING_VALUE(t):
    r'".*"'
    t.value = t.value[1:-1]
    return t


def t_newline(t):
    r'\n+|\r+|(\r\n)+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule


def t_error(t):
    error = re.match(r'(.+?)[\s;]', t.value)
    print("Illegal token '%s'" % t.value[error.span()[0]: error.span()[1]-1])
    t.lexer.skip(error.span()[1]-1)


# Build the lexer
lexer = lex.lex()

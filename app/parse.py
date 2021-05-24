import ply.yacc as yacc
from .lex import LexManager


class ParseManager:

    tokens = LexManager.tokens
    start = 'prog'
    precedence = (
        ('right', '='),
        ('left', 'AND', 'OR'),
        ('left', 'EQUALS', 'DIFFERENT'),
        ('nonassoc', '<', '>', 'GREAT_EQUAL', 'LESS_EQUAL'),
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('left', '^'),
        ('right', 'UMINUS'),
    )

    def __init__(self):
        self.errors = []
        self.lexer = LexManager().build()

    def p_prog(self, p):
        ''' prog : expression 
                 | prog expression '''

    def p_expression(self, p):
        ''' expression : closed_statement 
                       | selection_statement 
                       | iteration_statement '''

    def p_selection_statement(self, p):
        ''' selection_statement : IF special_statement
                                | IF special_statement ELSE blocked_content
                                | IF special_statement elif ELSE blocked_content '''

    def p_iteration_statement(self, p):
        ''' iteration_statement : WHILE special_statement
                                | DO blocked_content WHILE blocked_op ';'
                                | FOR '(' for_first for_second ')' blocked_content
                                | FOR '(' for_first for_second op_expression ')' blocked_content '''

    def p_elif(self, p):
        ''' elif : ELIF special_statement 
                 | elif ELIF special_statement '''

    def p_blocked_content(self, p):
        ''' blocked_content : '{' prog '}' '''

    def p_blocked_op(self, p):
        ''' blocked_op : '(' op_expression ')' '''

    def p_special_statement(self, p):
        ''' special_statement : blocked_op blocked_content'''

    def p_closed_statement(self, p):
        ''' closed_statement : ';' 
                             | statement ';' '''

    def p_for_first(self, p):
        ''' for_first : ';' 
                             | assign_op ';' 
                             | declaration ';' '''

    def p_for_second(self, p):
        ''' for_second : ';' 
                             | op_expression ';' '''

    def p_statement(self, p):
        ''' statement : print 
                      | read
                      | op_expression 
                      | declaration '''

    def p_print(self, p):
        ''' print : PRINT '(' op_expression ')' '''

    def p_read(self, p):
        ''' read : READ '(' op_expression ')' '''

    def p_declaration(self, p):
        ''' declaration : type ID 
                        | type assign_op '''

    def p_op_expression(self, p):
        ''' op_expression : val 
                          | assign_op 
                          | bin_op 
                          | '-' val %prec UMINUS'''

    def p_assign_op(self, p):
        ''' assign_op : ID '=' op_expression '''

    def p_bin_op(self, p):
        ''' bin_op : op_expression '+' op_expression 
                   | op_expression '-' op_expression
                   | op_expression '*' op_expression
                   | op_expression '/' op_expression
                   | op_expression '^' op_expression
                   | op_expression '>' op_expression
                   | op_expression '<' op_expression
                   | op_expression AND op_expression
                   | op_expression OR op_expression
                   | op_expression EQUALS op_expression
                   | op_expression DIFFERENT op_expression
                   | op_expression GREAT_EQUAL op_expression
                   | op_expression LESS_EQUAL op_expression '''

    def p_val(self, p):
        ''' val : ID 
                | lit_val '''

    def p_lit_val(self, p):
        ''' lit_val : INT_VALUE 
                    | FLOAT_VALUE 
                    | STRING_VALUE 
                    | BOOLEAN_VALUE_T 
                    | BOOLEAN_VALUE_F '''

    def p_type(self, p):
        ''' type : INT 
                 | FLOAT 
                 | STRING 
                 | BOOLEAN '''

    def p_error(self, p):
        print("Syntax error in input!")
        self.errors.append(p)

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser

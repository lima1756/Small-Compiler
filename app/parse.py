import ply.yacc as yacc
from .lex import LexManager


class Symbol:

    def __init__(self, name, type, declaration_pos, value=None, init_pos=None):
        self.name = name
        self.type = type
        self.declaration_pos = declaration_pos
        self.value = value
        self.init_pos = init_pos

    def initialized(self):
        return self.init_pos != None


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

    def symbol_exists(self, name):
        return name in self.symbol_table

    def __init__(self):
        self.errors = []
        self.lexer = LexManager().build()
        self.symbol_table = {}

    def p_prog(self, p):
        ''' prog : expression prog
                 | empty '''
        if len(p) == 3 and p[2][0] is not None:
            p[0] = (p[1],) + p[2]
            print('a')
        else:
            p[0] = (p[1],)
            print('a')

    def p_empty(self, p):
        'empty :'
        pass

    def p_expression(self, p):
        ''' expression : closed_statement 
                       | selection_statement 
                       | iteration_statement '''
        p[0] = p[1]

    def p_selection_statement(self, p):
        ''' selection_statement : IF special_statement
                                | IF special_statement ELSE blocked_content
                                | IF special_statement elif ELSE blocked_content '''
        if len(p) == 3:
            p[0] = (p[1], p[2])
        elif len(p) == 5:
            p[0] = (p[1], p[2], (p[3], p[4]))
        else:
            p[0] = (p[1], p[2], p[3], (p[4], p[5]))

    def p_iteration_statement(self, p):
        ''' iteration_statement : WHILE special_statement
                                | DO blocked_content WHILE blocked_op ';'
                                | FOR '(' for_first for_second ')' blocked_content
                                | FOR '(' for_first for_second op_expression ')' blocked_content '''
        if p[1] == "while":
            p[0] = (p[1], p[2])
        elif p[1] == "do":
            p[0] = (p[1], p[2], p[4])
        elif p[1] == "for" and p[5] == ')':
            p[0] = (p[1], p[3], p[4], p[6])
        elif p[1] == "for":
            p[0] = (p[1], p[3], p[4], p[5], p[7])

    def p_elif(self, p):
        ''' elif : ELIF special_statement 
                 | elif ELIF special_statement '''
        if p[1] == 'elif':
            p[0] = (p[1], p[2])
        else:
            p[0] = (p[1], (p[2], p[3]))

    def p_blocked_content(self, p):
        ''' blocked_content : '{' prog '}' '''
        p[0] = p[2]

    def p_blocked_op(self, p):
        ''' blocked_op : '(' op_expression ')' '''
        p[0] = p[2]

    def p_special_statement(self, p):
        ''' special_statement : blocked_op blocked_content'''
        p[0] = (p[1], p[2])

    def p_closed_statement(self, p):
        ''' closed_statement : ';' 
                             | statement ';' '''
        if p[1] != ";":
            p[0] = p[1]

    def p_for_first(self, p):
        ''' for_first : ';' 
                             | assign_op ';' 
                             | declaration ';' '''
        if p[1] != ";":
            p[0] = p[1]

    def p_for_second(self, p):
        ''' for_second : ';' 
                             | op_expression ';' '''
        if p[1] != ";":
            p[0] = p[1]

    def p_statement(self, p):
        ''' statement : print 
                      | read
                      | op_expression 
                      | declaration '''
        p[0] = p[1]

    def p_print(self, p):
        ''' print : PRINT '(' op_expression ')' '''
        p[0] = ('PRINT', p[3])

    def p_read(self, p):
        ''' read : READ '(' ID ')' '''
        if self.symbol_exists(p[3]):
            v = self.symbol_table[p[3]]
            v.value = None
            v.init_pos == p.lexer.lineno
            p[0] = ('READ', v.name)
        else:
            self.errors.append("Variable {} hasn't been defined, at line {}".format(
                p[3], p.lexer.lineno))
            raise SyntaxError()

    def p_declaration(self, p):
        ''' declaration : type ID 
                        | type ID '=' op_expression '''
        if p[2] in self.symbol_table:
            value = self.symbol_table[p[2]]
            self.errors.append("Variable {} already defined at line {}, and is redefined at {}".format(
                p[2], value.declaration_pos, p.lexer.lineno))
            raise SyntaxError()
        elif len(p) == 3:
            self.symbol_table[p[2]] = Symbol(
                p[2], p[1], p.lexer.lineno)
            p[0] = ('DECL', p[2], p[1])
        else:
            self.symbol_table[p[2]] = Symbol(p[2], p[1], p.lexer.lineno)
            p[0] = ('DECL', p[2], p[1], ('=', p[2], p[4]))

    def p_op_expression(self, p):
        ''' op_expression : val 
                          | assign_op 
                          | bin_op 
                          | '-' val %prec UMINUS
                          | '(' op_expression ')' '''
        if p[1] == '-':
            p[0] = ('-', p[2])
        elif p[1] == '(':
            p[0] = p[2]
        else:
            p[0] = p[1]

    def p_assign_op(self, p):
        ''' assign_op : ID '=' op_expression '''
        if not self.symbol_exists(p[1]):
            self.errors.append("Variable {} hasn't been declared and is being used, at line {}".format(
                p[1], p.lexer.lineno))
            raise SyntaxError()
        v1 = self.symbol_table[p[1]]
        p[0] = ('=', v1.name, p[3])

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
        p[0] = (p[2], p[1], p[3])

    def p_val(self, p):
        ''' val : ID 
                | lit_val '''
        if type(p[1]) == str:
            if not self.symbol_exists(p[1]):
                self.errors.append("Variable {} hasn't been defined, at line {}".format(
                    p[1], p.lexer.lineno))
                raise SyntaxError()
            else:
                p[0] = ('ID', p[1])

        else:
            p[0] = p[1]

    def p_lit_val(self, p):
        ''' lit_val : INT_VALUE 
                    | FLOAT_VALUE 
                    | STRING_VALUE 
                    | BOOLEAN_VALUE_T 
                    | BOOLEAN_VALUE_F '''
        if p[1] == 'true' or p[1] == 'false':
            p[0] = ('BOOLEAN', True) if p[1] == 'true' else ('BOOLEAN', False)
        elif type(p[1]) == int:
            p[0] = ('INT', p[1])
        elif type(p[1]) == float:
            p[0] = ('FLOAT', p[1])
        elif type(p[1]) == str:
            p[0] = ('STRING', p[1])

    def p_type(self, p):
        ''' type : INT 
                 | FLOAT 
                 | STRING 
                 | BOOLEAN '''
        p[0] = p[1]

    def p_error(self, p):
        print("Syntax error in input!")
        self.errors.append(
            "Unexpected symbol {}, at line {}".format(p.value, p.lineno))

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser

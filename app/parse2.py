import ply.yacc as yacc
from .lex import LexManager


class Symbol:

    def __init__(self, name, type, declaration_pos=None, value=None, init_pos=None):
        self.type = type
        self.name = name
        self.value = value
        self.declaration_pos = declaration_pos
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
                      | op_expression 
                      | declaration '''

    def p_print(self, p):
        ''' print : PRINT '(' op_expression ')' '''

    def p_declaration(self, p):
        ''' declaration : type ID 
                        | type ID '=' op_expression '''
        if p[2] in self.symbol_table:
            value = self.symbol_table[p[2]]
            self.errors.append("Variable %s already defined at line %d".format(
                p[2], value.declaration_pos))
        elif len(p) == 3:
            self.symbol_table[p[2]] = Symbol(
                p[1], None, p.lexer.lineno, None)
        elif len(p) > 3:
            self.symbol_table[p[2]] = Symbol(
                p[1], p[4], p.lexer.lineno, p.lexer.lineno)

    def p_op_expression(self, p):
        ''' op_expression : val 
                          | assign_op 
                          | bin_op 
                          | '-' val %prec UMINUS'''
        if len(p) == 2:
            p[0] = p[1]
        elif type(p[2]) == int or type(p[2]) == float:
            p[0] = -p[2]
        else:
            pass
            # TODO: if variable, check type, if not number then error if number idk
            # self.errors.append("Unary minus can't be used with a ")

    def p_assign_op(self, p):
        ''' assign_op : ID '=' op_expression '''
        if not self.symbol_exists(p[1]):
            self.errors.append("Variable %s hasn't been declared and is being used, at line %d".format(
                p[1], p.lexer.lineno))
            raise SyntaxError
        v1 = self.symbol_table[p[1]]
        if p[3][0] == 'ID':
            if not self.symbol_exists(p[3][1]):
                self.errors.append("Variable %s hasn't been declared and is being used, at line %d".format(
                    p[3][1], p.lexer.lineno))
                raise SyntaxError
            v2 = self.symbol_table[p[3][1]]
            if v1.type == v2.type and v2.value != None:
                v1.value = v2.value
                return ('=', v1.name, (v1.type, v2.value))
            elif v1.type == v2.type:
                return ('=', v1.name, ("ID", v2.name))
            else:
                self.errors.append("Variable %s is not the same type as %s, at line %d".format(
                    v1.name, v2.name, p.lexer.lineno))
                raise SyntaxError
        if p[3][0] == 'INT' and v1.type == 'INT':
            v1.value = p[3][1]
            return ('=', v1.name, ('INT', p[3][1]))
        elif p[3][0] == 'FLOAT' and v1.type == 'FLOAT':
            v1.value = p[3][1]
            return ('=', v1.name, ('FLOAT', p[3][1]))
        elif p[3][0] == 'STRING' and v1.type == 'STRING':
            v1.value = p[3][1]
            return ('=', v1.name, ('STRING', p[3][1]))
        elif p[3][0] == 'BOOLEAN' and v1.type == 'BOOLEAN':
            v1.value = p[3][1]
            return ('=', v1.name, ('BOOLEAN', p[3][1]))
        elif p[3][0] == '=':
            v1.value = p[3][1]
            return ('=', v1.name, ('BOOLEAN', p[3][1]))

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
        a = self.get_variable_or_p(p[1])
        b = self.get_variable_or_p(p[3])
        if a[0] == 'id' or b[0] == 'id':
            return (p[2], )
        if a[0] == 'int':
            if b[0] == 'int':
                return ('int', a[1]+b[1])
            if b[0] == 'float':
                return ('float', float(a[1])+b[1])
            if b[0] == 'float':
                return ('float', float(a[1])+b[1])
        elif a[0] == 'float':

        elif a[0] == 'bool':

        elif a[0] == 'string':

    def p_val(self, p):
        ''' val : ID 
                | lit_val '''
        if type(p[1]) == str:
            # TODO: check symbol table that id exists and has value
            p[0] = ('id', p[1])
        else:
            p[0] = p[1]

    def p_lit_val(self, p):
        ''' lit_val : INT_VALUE 
                    | FLOAT_VALUE 
                    | STRING_VALUE 
                    | BOOLEAN_VALUE_T 
                    | BOOLEAN_VALUE_F '''
        if p[1] == 'true' or p[2] == 'false':
            p[0] = ('bool', True) if p[1] == 'true' else ('bool', False)
        elif type(p[1]) == int:
            p[0] = ('int', p[1])
        elif type(p[1]) == float:
            p[0] = ('float', p[1])
        elif type(p[1]) == str:
            p[0] = ('string', p[1])

    def p_type(self, p):
        ''' type : INT 
                 | FLOAT 
                 | STRING 
                 | BOOLEAN '''
        p[0] = ('type', p[1])

    def p_error(self, p):
        print("Syntax error in input!")
        self.errors.append(p)

    def get_variable_or_p(self, p):
        if p[0] != 'id':
            return p
        type = ""
        val = None
        if p[0] == id and not self.symbol_table[p[1]].is_variable():
            type = self.symbol_table[p[1]].symbol_type
            val = self.symbol_table[p[1]].value
            return (type, val)
        return ('id', p[1])

    def process_sum(self, a, b):
        if a[0] == b[0] and a[0] == 'int':
            return ('int', a[0]+b[0])
        if a[0] == b[0] and a[0] == 'float' \
                or (a[0] == 'int' and b[0] == 'float' or a[0] == 'float' and b[0] == 'int') \
                or (a[0] == 'int' and b[0] == 'float' or a[0] == 'float' and b[0] == 'int'):
            return ('float', a[0]+b[0])
        if (a[0] == 'string' or b[0] == 'string') and (a[0] == 'bool' or b[0] == 'bool'):
            return ('string', str(a[0])+str(b[0]))
        self.errors.append("Types %s and %s are not compatible, at %d".format(
            a[0], a[1], p.lexer.lineno))
        raise SyntaxError

    def process_sub(self, a, b):
        if a[0] == b[0] and a[0] == 'int':
            return ('int', a[0]-b[0])
        if a[0] == b[0] and a[0] == 'float' \
                or (a[0] == 'int' and b[0] == 'float' or a[0] == 'float' and b[0] == 'int') \
                or (a[0] == 'int' and b[0] == 'float' or a[0] == 'float' and b[0] == 'int'):
            return ('float', a[0]-b[0])
        self.errors.append("Types %s and %s are not compatible, at %d".format(
            a[0], a[1], p.lexer.lineno))
        raise SyntaxError

    def process_times(self, a, b):
        if a[0] == b[0] and a[0] == 'int':
            return ('int', a[0]*b[0])
        if a[0] == b[0] and a[0] == 'float' \
                or (a[0] == 'int' and b[0] == 'float' or a[0] == 'float' and b[0] == 'int') \
                or (a[0] == 'int' and b[0] == 'float' or a[0] == 'float' and b[0] == 'int'):
            return ('float', a[0]*b[0])
        self.errors.append("Types %s and %s are not compatible, at %d".format(
            a[0], a[1], p.lexer.lineno))
        raise SyntaxError

    def process_division(self, a, b):
        if b[1] == 0:
            self.errors.append("Division by zero, at %d")
        if a[0] == b[0] and a[0] == 'int':
            return ('int', a[0]/b[0])
        if a[0] == b[0] and a[0] == 'float' \
                or (a[0] == 'int' and b[0] == 'float' or a[0] == 'float' and b[0] == 'int') \
                or (a[0] == 'int' and b[0] == 'float' or a[0] == 'float' and b[0] == 'int'):
            return ('float', a[0]/b[0])
        self.errors.append("Types %s and %s are not compatible, at %d".format(
            a[0], a[1], p.lexer.lineno))
        raise SyntaxError

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)
        return self.parser

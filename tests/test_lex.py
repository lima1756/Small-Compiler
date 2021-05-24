import os
from app.lex import LexManager


class TestLex:

    @classmethod
    def setup_class(cls):
        cls.dir = os.path.dirname(__file__)

    def setup_method(self):
        self.lexManager = LexManager()
        self.lexer = self.lexManager.build()

    def pass_tokens(self, data):
        self.lexer.input(data)
        tokens = []
        for t in self.lexer:
            tokens.append(t)
        return tokens

    def test_int(self):
        tokens = self.pass_tokens("int")
        assert len(tokens) == 1
        assert tokens[0].type == 'INT'
        assert len(self.lexManager.errors) == 0

    def test_float(self):
        tokens = self.pass_tokens("float")
        assert len(tokens) == 1
        assert tokens[0].type == 'FLOAT'
        assert len(self.lexManager.errors) == 0

    def test_string(self):
        tokens = self.pass_tokens("string")
        assert len(tokens) == 1
        assert tokens[0].type == 'STRING'
        assert len(self.lexManager.errors) == 0

    def test_bool(self):
        tokens = self.pass_tokens("bool")
        assert len(tokens) == 1
        assert tokens[0].type == 'BOOLEAN'
        assert len(self.lexManager.errors) == 0

    def test_if(self):
        tokens = self.pass_tokens("if")
        assert len(tokens) == 1
        assert tokens[0].type == 'IF'
        assert len(self.lexManager.errors) == 0

    def test_else(self):
        tokens = self.pass_tokens("else")
        assert len(tokens) == 1
        assert tokens[0].type == 'ELSE'
        assert len(self.lexManager.errors) == 0

    def test_elif(self):
        tokens = self.pass_tokens("elif")
        assert len(tokens) == 1
        assert tokens[0].type == 'ELIF'
        assert len(self.lexManager.errors) == 0

    def test_while(self):
        tokens = self.pass_tokens("while")
        assert len(tokens) == 1
        assert tokens[0].type == 'WHILE'
        assert len(self.lexManager.errors) == 0

    def test_print(self):
        tokens = self.pass_tokens("print")
        assert len(tokens) == 1
        assert tokens[0].type == 'PRINT'
        assert len(self.lexManager.errors) == 0

    def test_do(self):
        tokens = self.pass_tokens("do")
        assert len(tokens) == 1
        assert tokens[0].type == 'DO'
        assert len(self.lexManager.errors) == 0

    def test_for(self):
        tokens = self.pass_tokens("for")
        assert len(tokens) == 1
        assert tokens[0].type == 'FOR'
        assert len(self.lexManager.errors) == 0

    def test_true(self):
        tokens = self.pass_tokens("true")
        assert len(tokens) == 1
        assert tokens[0].type == 'BOOLEAN_VALUE_T'
        assert len(self.lexManager.errors) == 0

    def test_false(self):
        tokens = self.pass_tokens("false")
        assert len(tokens) == 1
        assert tokens[0].type == 'BOOLEAN_VALUE_F'
        assert len(self.lexManager.errors) == 0

    def test_assign(self):
        tokens = self.pass_tokens("=")
        assert len(tokens) == 1
        assert tokens[0].type == '='
        assert len(self.lexManager.errors) == 0

    def test_plus(self):
        tokens = self.pass_tokens("+")
        assert len(tokens) == 1
        assert tokens[0].type == '+'
        assert len(self.lexManager.errors) == 0

    def test_minus(self):
        tokens = self.pass_tokens("-")
        assert len(tokens) == 1
        assert tokens[0].type == '-'
        assert len(self.lexManager.errors) == 0

    def test_times(self):
        tokens = self.pass_tokens("*")
        assert len(tokens) == 1
        assert tokens[0].type == '*'
        assert len(self.lexManager.errors) == 0

    def test_divide(self):
        tokens = self.pass_tokens("/")
        assert len(tokens) == 1
        assert tokens[0].type == '/'
        assert len(self.lexManager.errors) == 0

    def test_pow(self):
        tokens = self.pass_tokens("^")
        assert len(tokens) == 1
        assert tokens[0].type == '^'
        assert len(self.lexManager.errors) == 0

    def test_less(self):
        tokens = self.pass_tokens("<")
        assert len(tokens) == 1
        assert tokens[0].type == '<'
        assert len(self.lexManager.errors) == 0

    def test_great(self):
        tokens = self.pass_tokens(">")
        assert len(tokens) == 1
        assert tokens[0].type == '>'
        assert len(self.lexManager.errors) == 0

    def test_start_parenthesis(self):
        tokens = self.pass_tokens("(")
        assert len(tokens) == 1
        assert tokens[0].type == '('
        assert len(self.lexManager.errors) == 0

    def test_end_parenthesis(self):
        tokens = self.pass_tokens(")")
        assert len(tokens) == 1
        assert tokens[0].type == ')'
        assert len(self.lexManager.errors) == 0

    def test_start_bracket(self):
        tokens = self.pass_tokens("{")
        assert len(tokens) == 1
        assert tokens[0].type == '{'
        assert len(self.lexManager.errors) == 0

    def test_end_bracket(self):
        tokens = self.pass_tokens("}")
        assert len(tokens) == 1
        assert tokens[0].type == '}'
        assert len(self.lexManager.errors) == 0

    def test_semicolon(self):
        tokens = self.pass_tokens(";")
        assert len(tokens) == 1
        assert tokens[0].type == ';'
        assert len(self.lexManager.errors) == 0

    def test_equals(self):
        tokens = self.pass_tokens("==")
        assert len(tokens) == 1
        assert tokens[0].type == 'EQUALS'
        assert len(self.lexManager.errors) == 0

    def test_different(self):
        tokens = self.pass_tokens("!=")
        assert len(tokens) == 1
        assert tokens[0].type == 'DIFFERENT'
        assert len(self.lexManager.errors) == 0

    def test_grat_equal(self):
        tokens = self.pass_tokens(">=")
        assert len(tokens) == 1
        assert tokens[0].type == 'GREAT_EQUAL'
        assert len(self.lexManager.errors) == 0

    def test_less_equal(self):
        tokens = self.pass_tokens("<=")
        assert len(tokens) == 1
        assert tokens[0].type == 'LESS_EQUAL'
        assert len(self.lexManager.errors) == 0

    def test_and(self):
        tokens = self.pass_tokens("&&")
        assert len(tokens) == 1
        assert tokens[0].type == 'AND'
        assert len(self.lexManager.errors) == 0

    def test_or(self):
        tokens = self.pass_tokens("||")
        assert len(tokens) == 1
        assert tokens[0].type == 'OR'
        assert len(self.lexManager.errors) == 0

    def test_int_value(self):
        tokens = self.pass_tokens("1583")
        assert len(tokens) == 1
        assert tokens[0].type == 'INT_VALUE'
        assert len(self.lexManager.errors) == 0

    def test_float_value(self):
        tokens = self.pass_tokens("12.05")
        assert len(tokens) == 1
        assert tokens[0].type == 'FLOAT_VALUE'
        tokens = self.pass_tokens(".05")
        assert len(tokens) == 1
        assert tokens[0].type == 'FLOAT_VALUE'
        tokens = self.pass_tokens("0.05")
        assert len(tokens) == 1
        assert tokens[0].type == 'FLOAT_VALUE'
        assert len(self.lexManager.errors) == 0

    def test_string_value(self):
        tokens = self.pass_tokens("\"asdf\"")
        assert len(tokens) == 1
        assert tokens[0].type == 'STRING_VALUE'
        assert len(self.lexManager.errors) == 0

    def test_id(self):
        tokens = self.pass_tokens("notReserved123")
        assert len(tokens) == 1
        assert tokens[0].type == 'ID'
        assert len(self.lexManager.errors) == 0

    def test_read(self):
        tokens = self.pass_tokens("read")
        assert len(tokens) == 1
        assert tokens[0].type == 'READ'
        assert len(self.lexManager.errors) == 0

    def test_error(self):
        self.pass_tokens("%%_asf")
        assert len(self.lexManager.errors) == 1

    def test_empty(self):
        tokens = self.pass_tokens("")
        assert len(tokens) == 0
        assert len(self.lexManager.errors) == 0

    def test_correct_input(self):
        with open(os.path.join(TestLex.dir, "./input_tests/ok1.txt")) as f:
            tokens = self.pass_tokens(f.read())
            assert len(tokens) == 198
            assert len(self.lexManager.errors) == 0

    def test_incorrect_input(self):
        with open(os.path.join(self.dir, "./input_tests/lexical_fail1.txt")) as f:
            tokens = self.pass_tokens(f.read())
            assert len(tokens) == 15
            assert len(self.lexManager.errors) == 3

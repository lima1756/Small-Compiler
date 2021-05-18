import os
from app.lex import lexer


class TestLex:

    dir = os.path.dirname(__file__)

    def test_correct_input(self):
        with open(os.path.join(self.dir, "./input_tests/ok1.txt")) as f:
            lexer.input(f.read())
            for t in lexer:
                print(t)

    def test_incorrect_input(self):
        with open(os.path.join(self.dir, "./input_tests/syntax_fail1.txt")) as f:
            lexer.input(f.read())
            for t in lexer:
                print(t)

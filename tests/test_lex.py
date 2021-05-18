import os
from pytest import fixture
from app.lex import LexManager


@fixture()
def prepare():
    lexer = Lexer()
    lexer.build()
    print('pre')
    yield lexer
    print("post")


class TestLex:

    def setup_method(self, method):
        self.lexManager = LexManager()
        self.lexer = self.lexManager.build()

    @classmethod
    def setup_class(cls):
        cls.dir = os.path.dirname(__file__)

    def test_correct_input(self):
        with open(os.path.join(TestLex.dir, "./input_tests/ok1.txt")) as f:
            self.lexer.input(f.read())
            for t in self.lexer:
                print(t)
            assert len(self.lexManager.errors) == 0

    def test_incorrect_input(self):
        with open(os.path.join(self.dir, "./input_tests/syntax_fail1.txt")) as f:
            self.lexer.input(f.read())
            for t in self.lexer:
                print(t)
            assert len(self.lexManager.errors) == 3

import os
from app.parse import ParseManager


class TestLex:

    @classmethod
    def setup_class(cls):
        cls.dir = os.path.dirname(__file__)

    def setup_method(self):
        self.parseManager = ParseManager()
        self.parser = self.parseManager.build()

    def test_correct_input(self):
        with open(os.path.join(TestLex.dir, "./input_tests/ok2.txt")) as f:
            self.parser.parse(f.read())
        raise Exception("t")

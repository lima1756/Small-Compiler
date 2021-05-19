import os
from app.parse import ParseManager


class TestLex:
    dir = os.path.dirname(__file__)

    def setup_method(self):
        self.parseManager = ParseManager()
        self.parser = self.parseManager.build()

    def test_correct_input1(self):
        with open(os.path.join(TestLex.dir, "./input_tests/ok1.txt")) as f:
            self.parser.parse(f.read())
            assert len(self.parseManager.errors) == 0

    def test_correct_input2(self):
        with open(os.path.join(TestLex.dir, "./input_tests/ok2.txt")) as f:
            self.parser.parse(f.read())
            assert len(self.parseManager.errors) == 0

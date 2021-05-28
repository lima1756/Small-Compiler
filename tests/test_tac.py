import os
from app.parse import ParseManager
from app.tac import TACGenerator


class TestTAC:
    dir = os.path.dirname(__file__)

    def setup_method(self):
        self.parser = ParseManager().build()

    def test_correct_input1(self):
        with open(os.path.join(TestTAC.dir, "./input_tests/ok1.txt")) as f:
            tree = self.parser.parse(f.read())
            output = TACGenerator(tree).generate()
            print(output)

    def test_correct_input2(self):
        with open(os.path.join(TestTAC.dir, "./input_tests/ok2.txt")) as f:
            tree = self.parser.parse(f.read())
            output = TACGenerator(tree).generate()
            print(output)

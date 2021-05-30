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
            expected_output = open(os.path.join(
                TestTAC.dir, "./output_tests/ok1.out")).read()
            assert output == expected_output

    def test_correct_input2(self):
        with open(os.path.join(TestTAC.dir, "./input_tests/ok2.txt")) as f:
            tree = self.parser.parse(f.read())
            output = TACGenerator(tree).generate()
            expected_output = open(os.path.join(
                TestTAC.dir, "./output_tests/ok2.out")).read()
            assert output == expected_output

    def test_correct_input3(self):
        with open(os.path.join(TestTAC.dir, "./input_tests/ok3.txt")) as f:
            tree = self.parser.parse(f.read())
            output = TACGenerator(tree).generate()
            expected_output = open(os.path.join(
                TestTAC.dir, "./output_tests/ok3.out")).read()
            assert output == expected_output

    def test_correct_input4(self):
        with open(os.path.join(TestTAC.dir, "./input_tests/ok4.txt")) as f:
            tree = self.parser.parse(f.read())
            output = TACGenerator(tree).generate()
            expected_output = open(os.path.join(
                TestTAC.dir, "./output_tests/ok4.out")).read()
            assert output == expected_output

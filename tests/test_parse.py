import os
from app.parse import ParseManager


class TestLex:
    dir = os.path.dirname(__file__)

    def setup_method(self):
        self.parseManager = ParseManager()
        self.parser = self.parseManager.build()

    def test_correct_input1(self):
        with open(os.path.join(TestLex.dir, "./input_tests/ok1.txt")) as f:
            tree = self.parser.parse(f.read())
            ok_tree = open(os.path.join(
                TestLex.dir, "./parse_trees/ok1_tree.txt")).read()
            assert len(self.parseManager.errors) == 0
            assert str(tree) == ok_tree

    def test_correct_input2(self):
        with open(os.path.join(TestLex.dir, "./input_tests/ok2.txt")) as f:
            tree = self.parser.parse(f.read())
            ok_tree = open(os.path.join(
                TestLex.dir, "./parse_trees/ok2_tree.txt")).read()
            assert len(self.parseManager.errors) == 0
            assert str(tree) == ok_tree

    def test_incorrect_input(self):
        with open(os.path.join(self.dir, "./input_tests/syntax_fail1.txt")) as f:
            self.parser.parse(f.read())
            assert len(self.parseManager.errors) == 4

import os
from app.parse import ParseManager


class TestLex:
    dir = os.path.dirname(__file__)

    def setup_method(self):
        self.parseManager = ParseManager()
        self.parser = self.parseManager.build()

    def print_errors(self, errors):
        for e in errors:
            print(e)

    def test_correct_input1(self):
        with open(os.path.join(TestLex.dir, "./input_tests/ok1.txt")) as f:
            tree = self.parser.parse(f.read())
            self.print_errors(self.parseManager.errors)
            ok_tree = open(os.path.join(
                TestLex.dir, "./parse_trees/ok1.tree")).read()
            assert len(self.parseManager.errors) == 0
            assert str(tree) == ok_tree

    def test_correct_input2(self):
        with open(os.path.join(TestLex.dir, "./input_tests/ok2.txt")) as f:
            tree = self.parser.parse(f.read())
            self.print_errors(self.parseManager.errors)
            ok_tree = open(os.path.join(
                TestLex.dir, "./parse_trees/ok2.tree")).read()
            assert len(self.parseManager.errors) == 0
            assert str(tree) == ok_tree

    def test_correct_input3(self):
        with open(os.path.join(TestLex.dir, "./input_tests/ok3.txt")) as f:
            tree = self.parser.parse(f.read())
            self.print_errors(self.parseManager.errors)
            ok_tree = open(os.path.join(
                TestLex.dir, "./parse_trees/ok3.tree")).read()
            assert len(self.parseManager.errors) == 0
            assert str(tree) == ok_tree

    def test_correct_input4(self):
        with open(os.path.join(TestLex.dir, "./input_tests/ok4.txt")) as f:
            tree = self.parser.parse(f.read())
            self.print_errors(self.parseManager.errors)
            ok_tree = open(os.path.join(
                TestLex.dir, "./parse_trees/ok4.tree")).read()
            assert len(self.parseManager.errors) == 0
            assert str(tree) == ok_tree

    def test_incorrect_input(self):
        with open(os.path.join(self.dir, "./input_tests/syntax_fail1.txt")) as f:
            self.parser.parse(f.read())
            assert len(self.parseManager.errors) == 4

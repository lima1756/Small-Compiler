

class TACGenerator():

    operators = ['+', '-', '*', '/', '^', '<', '=',
                 '>', '&&', '||', '==', '!=', '>=', '<=']

    def __init__(self, parse_tree):
        self.parse_tree = parse_tree
        self.t_counter = 0
        self.label_counter = 0

    def generate(self):
        output = ""
        for node in self.parse_tree:
            output += self.process_node(node)
        return output

    def process_node(self, node):
        if node[0] == "DECL":
            return self.decl(node)
        elif node[0] == "if":
            return self.if_node(node)
        elif node[0] == "for":
            return self.for_node(node)
        elif node[0] == "do":
            return self.do(node)
        elif node[0] == "while":
            return self.while_node(node)
        elif node[0] == "PRINT":
            return self.print_node(node)
        elif node[0] == "READ":
            return self.read(node)
        elif node[0] == "ID":
            return self.id(node)
        elif node[0] in TACGenerator.operators:
            return self.operator_node(node)
        else:
            return ""

    def for_node(self, node):
        return ""

    def do(self, node):
        return ""

    def while_node(self, node):
        return ""

    def if_node(self, node):
        output = ""
        pre, val = self.possible_operator(node[1][0])
        out = "L"+self.label_counter
        self.label_counter += 1
        l1 = "L"+self.label_counter
        self.label_counter += 1
        output += "{}if not {} goto {}\n".format(pre, val, l1)
        for n in node[1][1]:
            output += self.process_node(n)
        output += "goto {}\n".format(out)
        output += "label {}\n".format(l1)
        for i in range(2, len(node)):
            if node[i][0] == "elif":
                pre2, val2 = self.possible_operator(node[i][1][0])
                ln = "L"+self.label_counter
                self.label_counter += 1
                output += "{}if not {} goto {}\n".format(pre2, val2, ln)
                for n in node[i][1][1]:
                    output += self.process_node(n)
                output += "goto {}\n".format(out)
                output += "label {}\n".format(ln)
            if node[i][0] == "else":
                for n in node[i][1][0]:
                    output += self.process_node(n)
        output += "label {}\n".format(out)
        return output

    def operator_node(self, node):
        if node[0] == "=":
            pre, val = self.possible_operator(node[3])
            self.t_counter = 0
            return "{}{} = {}\n".format(pre, node[2][2], val)
        else:
            t = "t"+str(self.t_counter)
            self.t_counter += 1
            pre1, first = self.possible_operator(node[2])
            pre2, second = self.possible_operator(node[3])
            return "{}{}{} = {} {} {}\n".format(pre1, pre2, t, first, node[0], second)

    def possible_operator(self, node):
        if node[0] == "ID":
            return ("", self.id(node))
        elif node[0] == "val":
            return ("", self.val(node))
        else:
            t = "t"+str(self.t_counter)
            self.t_counter += 1
            pre1, first = self.possible_operator(node[2])
            pre2, second = self.possible_operator(node[3])
            return ("{}{}{} = {} {} {}\n".format(pre1, pre2, t, first, node[0], second), t)

    def decl(self, node):
        if len(node) == 3:
            return "{} {}\n".format(node[2], node[1])
        else:
            pre, val = self.possible_operator(node[3][3])
            self.t_counter = 0
            return "{}{} {}\n{} = {}\n".format(pre, node[2], node[1], node[1], val)

    def read(self, node):
        return "read {}\n".format(node[1])

    def print_node(self, node):
        pre, val = self.possible_operator(node[1])
        self.t_counter = 0
        return "{}print {}\n".format(pre, val)

    def val(self, node):
        return str(node[2])

    def id(self, node):
        return node[2]

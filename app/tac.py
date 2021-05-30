

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
        if node is None:
            return ""
        node_types = {
            "DECL": self.decl,
            "if": self.if_node,
            "for": self.for_node,
            "do": self.do,
            "while": self.while_node,
            "PRINT": self.print_node,
            "READ": self.read,
            "ID": self.id
        }
        type = node[0]
        if type in node_types.keys():
            return node_types[type](node)
        elif node[0] in TACGenerator.operators:
            return self.operator_node(node)
        else:
            return ""

    def for_node(self, node):
        output = ""
        startLabel = "L"+str(self.label_counter)
        self.label_counter += 1
        endLabel = "L"+str(self.label_counter)
        self.label_counter += 1
        if node[1] is not None and node[1][0] == "DECL":
            output += self.decl(node[1])
        elif node[1] is not None:
            output += self.operator_node(node[1])

        output += "label {}\n".format(startLabel)
        if node[2] is not None:
            pre, val = self.possible_operator(node[2])
            output += "{}if not {} goto {}\n".format(pre, val, endLabel)

        for n in node[4]:
            output += self.process_node(n)

        if node[3] is not None:
            output += self.operator_node(node[3])
        output += "goto {}\n".format(startLabel)
        output += "label {}\n".format(endLabel)
        return output

    def do(self, node):
        output = ""
        startLabel = "L"+str(self.label_counter)
        self.label_counter += 1

        output += "label {}\n".format(startLabel)

        for n in node[1]:
            output += self.process_node(n)

        pre, val = self.possible_operator(node[2])
        output += "{}if {} goto {}\n".format(pre, val, startLabel)

        return output

    def while_node(self, node):
        output = ""
        startLabel = "L"+str(self.label_counter)
        self.label_counter += 1
        endLabel = "L"+str(self.label_counter)
        self.label_counter += 1

        output += "label {}\n".format(startLabel)
        pre, val = self.possible_operator(node[1][0])
        output += "{}if not {} goto {}\n".format(pre, val, endLabel)

        for n in node[1][1]:
            output += self.process_node(n)

        output += "goto {}\n".format(startLabel)
        output += "label {}\n".format(endLabel)
        return output

    def if_node(self, node):
        output = ""
        pre, val = self.possible_operator(node[1][0])
        out = "L"+str(self.label_counter)
        self.label_counter += 1
        l1 = "L"+str(self.label_counter)
        self.label_counter += 1
        output += "{}if not {} goto {}\n".format(pre, val, l1)
        for n in node[1][1]:
            output += self.process_node(n)
        output += "goto {}\n".format(out)
        output += "label {}\n".format(l1)
        for i in range(len(node[2]) if node[2] is not None else 0):
            pre2, val2 = self.possible_operator(node[2][i][1])
            ln = "L"+str(self.label_counter)
            self.label_counter += 1
            output += "{}if not {} goto {}\n".format(pre2, val2, ln)
            for n in node[2][i][2]:
                output += self.process_node(n)
            output += "goto {}\n".format(out)
            output += "label {}\n".format(ln)
        if node[3] is not None:
            for n in node[3][1]:
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

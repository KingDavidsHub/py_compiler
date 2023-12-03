import sys
class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.currentPosition = -1
        self.currentToken = None
        self.advance()

    def advance(self):
        self.currentPosition += 1
        if self.currentPosition < len(self.tokens):
            self.currentToken = self.tokens[self.currentPosition]

    def runParse(self):
        statements = []

        while self.currentToken.type != "TT_EOF":

            if self.currentToken.type == "TT_NWL":
                self.advance()
                continue

            statement = self.isStatement()
            if statement:
                statements.append(statement)
            else:
                sys.exit("Add your statement function and change me")

            if self.tokens[self.currentPosition].type != "TT_NWL":
                sys.exit("Parsing Error: expected newline")


        return statements
    
    def isStatement(self):
        # return self.expression()
        if self.currentToken.type == "TT_IDENT":  # assignment statement
            identifier = self.currentToken
            self.advance()
            if self.currentToken.type == "TT_EQ":
                self.advance()
                expression = self.expression()
                return Assign(identifier, expression)

        elif self.currentToken.type == "TT_KEYW" and self.currentToken.value == "print":  # print statement
            self.advance()
            if self.currentToken.type == "TT_LPAREN":
                self.advance()
                expression = self.expression()

                if self.currentToken.type == "TT_RPAREN":
                    self.advance()
                    return Print(expression)
                else:
                    sys.exit("Parsing Error: expected ')' ")
            else:
                sys.exit("Parsing Error: expected '(' ")
    def expression(self):
        return  self.BiOptn(self.term, ["TT_PLUS", "TT_MINUS"])

    def term(self):
        return  self.BiOptn(self.exponent, ["TT_MULT", "TT_DIV"])

    def exponent(self):
        return self.BiOptn(self.factor, ["TT_POW"])

    def factor(self):
        tok = self.currentToken

        if self.currentToken.type == "TT_NUMBER":
            self.advance()
            return Node(tok)
        elif self.currentToken.type == "TT_IDENT":
            self.advance()
            return Node(tok)
        elif self.currentToken.type == "TT_LPAREN":
            self.advance()
            expr = self.expression()
            if self.currentToken.type == "TT_RPAREN":
                self.advance()
                return expr
            else:
                sys.exit("Parsing Error: Expected a )")
        elif self.currentToken.type == "TT_EOF":
            return Node(tok)
        else:
            sys.exit(f"Parsing Error: Expected a number, but got {self.currentToken.value}")


    def BiOptn(self, func, opts):

        left = func()

        while self.currentToken.type in opts:
            optn = self.currentToken
            self.advance()
            right = func()
            left = BiNode(left, optn, right)

        return left

class Node:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f'{self.tok.value}'

    def read(self, obj):
        return self.tok.read(obj)

class BiNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node} {self.op_tok.value} {self.right_node})'

    def read(self, obj):

        if self.op_tok.type == "TT_PLUS":
            return self.left_node.read(obj) + self.right_node.read(obj)
        if self.op_tok.type == "TT_MINUS":
            return self.left_node.read(obj) - self.right_node.read(obj)
        if self.op_tok.type == "TT_DIV":
            return self.left_node.read(obj) / self.right_node.read(obj)
        if self.op_tok.type == "TT_MULT":
            return self.left_node.read(obj) * self.right_node.read(obj)
        if self.op_tok.type == "TT_POW":
            return self.left_node.read(obj) ** self.right_node.read(obj)


class Assign:

    def __init__(self, ident, value):
        self.variable = ident.value
        self.value = value

    def __repr__(self):
        return f"{self.variable} = {self.value}"

    def read(self, obj):
        obj.storage[self.variable] = self.value.read(obj)


class Print:

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"print({self.value})"

    def read(self, obj):
         print(self.value.read(obj))

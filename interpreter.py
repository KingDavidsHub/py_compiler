class Interpreter:

    def __init__(self, asts):
        # Constructor initializes the Interpreter with a list of Abstract Syntax Trees (ASTs) and an empty storage dictionary
        self.asts = asts
        self.storage = {}

    def execute(self):
        # Execute method iterates through each AST and calls its read method with the current Interpreter instance
        for ast in self.asts:
            ast.read(self)
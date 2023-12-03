class Interpreter:

    def __init__(self, asts):
        self.asts = asts
        self.storage = {}

    def execute(self):
        for ast in self.asts:
            ast.read(self)

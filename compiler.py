from lexer import *
from parser_1 import *
from interpreter import *
import sys

def main():
    source = sys.argv[1]
    new_lexer = Lexer(source)

    tokens = new_lexer.getTokens()

    # for i in tokens:
    #     print(i)

    new_parser = Parser(tokens)
    asts = new_parser.runParse()

    new_interpreter = Interpreter(asts)
    new_interpreter.execute()

main()
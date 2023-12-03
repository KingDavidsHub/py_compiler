from lexer import *
from parser_1 import *
from interpreter import *
import sys

def main():
    # Get the source code file path from command line arguments
    source = sys.argv[1]

    # Create a new lexer instance with the provided source code
    new_lexer = Lexer(source)

    # Get tokens from the lexer
    tokens = new_lexer.getTokens()

    # Uncomment the following lines to print tokens
    # for i in tokens:
    #     print(i)

    # Create a new parser instance with the obtained tokens
    new_parser = Parser(tokens)

    # Generate Abstract Syntax Trees (ASTs) using the parser
    asts = new_parser.runParse()

    # Create a new interpreter instance with the generated ASTs
    new_interpreter = Interpreter(asts)

    # Execute the interpreter to interpret and run the program
    new_interpreter.execute()

# Call the main function when the script is executed
main()
from lexer import *
from parser_1 import *
from interpreter import *
from debugger import Debugger
from validator import parse_code  # Import the parse_code function
import sys

def main():
    # Get the source code file path from command line arguments
    source = sys.argv[1]

    # Validate the source code
    if not parse_code(source):
        print("Validation failed. Exiting.")
        return

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

    # Create a new debugger instance
    debugger = Debugger()

    # Load the script into the debugger
    script_lines = debugger.load_script(source)

    # Run the debugger script
    debugger.run_debugger_script(script_lines)

    # Execute the interpreter to interpret and run the program
    new_interpreter.execute()

    # Enter the user command loop of the debugger
    debugger.user_command_loop()

# Call the main function when the script is executed
if __name__ == "__main__":
    main()

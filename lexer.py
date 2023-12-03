import sys

# Define a Lexer class for tokenizing input.
class Lexer:
    def __init__(self, input):
        # Initialize Lexer with input, current character, position, token list, and error state.
        self.source = input
        self.curChar = ''
        self.curPos = -1
        self.tokenList = []
        self.error = None
        self.nextChar()

    # Move to the next character in the input.
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = '\0'
        else:
            self.curChar = self.source[self.curPos]

    # Peek at the next character without moving the position.
    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curPos + 1]

    # Abort lexing with an error message.
    def abort(self, message):
        sys.exit("Lexing error. " + message)

    # Skip whitespaces and carriage return characters.
    def skipWhitespace(self):
        while self.curChar == ' ' or self.curChar == '\r':
            self.nextChar()

    # Skip comments starting with '#'.
    def skipComment(self):
        if self.curChar == '#':
            while self.curChar != '\n':
                self.nextChar()

    # Get tokens from the input source.
    def getTokens(self):
        while self.curChar != '\0':
            self.skipWhitespace()
            self.skipComment()
            token = None

            # Check for various token types and create corresponding Token objects.
            if self.curChar == '+':
                token = Token("TT_PLUS", self.curChar, self.curPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == '-':
                # Similar logic for other operators and symbols...
                token = Token("TT_MINUS", self.curChar, self.curPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar.isalpha():
                # Handle identifiers and keywords...
                token = Token("TT_IDENTIFIER", self.curChar, self.curPos, self.curPos)
                self.tokenList.append(token)
            else:
                self.abort("Unknown token: " + self.curChar)

            self.nextChar()

        # Append end-of-file token and return the token list.
        self.tokenList.append(Token("TT_EOF"))
        return self.tokenList


# Define a Token class to represent different token types.
class Token:
    def __init__(self, type_, value=None, start=None, end=None):
        self.type = type_
        self.value = value
        self.start = start
        self.end = end

    def __repr__(self):
        if self.value:
            return f'{self.type}:\"{self.value}\"'
        return f'{self.type}'

    def read(self, obj):
        if self.value:
            if self.type == "TT_NUMBER":
                self.value = float(self.value)
            return self.value
        else:
            return None

# Define a specialized IdentToken class for identifiers.
class IdentToken(Token):
    def __init__(self, type_, value=None, start=None, end=None):
        super().__init__(type_, value, start, end)

    def __repr__(self):
        if self.value:
            return f'{self.type}:\"{self.value}\"'
        return f'{self.type}'

    def read(self, obj):
        try:
            if obj.storage[self.value]:
                return obj.storage[self.value]
        except:
            sys.exit(f"'{self.value}' doesn't exist")
        return None

# Function to check if a given token is a keyword.
def isKeyWord(token):
    keywords = ["print"]
    if token in keywords:
        return True
    return False
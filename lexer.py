import sys


class Lexer:
    def __init__(self, input):
        self.source = input
        self.curChar = ''
        self.curPos = -1
        self.tokenList = []
        self.error = None
        self.nextChar()


    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = '\0'
        else:
            self.curChar = self.source[self.curPos]


    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curPos+1]


    def abort(self, message):
        sys.exit("Lexing error. " + message)

    def skipWhitespace(self):
        while self.curChar == ' '  or self.curChar == '\r':
            self.nextChar()


    def skipComment(self):
        if self.curChar == '#':
            while self.curChar != '\n':
                self.nextChar()


    def getTokens(self):

        while self.curChar != '\0':

            self.skipWhitespace()
            self.skipComment()
            token = None

            if self.curChar == '+':
                token = Token("TT_PLUS", self.curChar, self.curPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == '-':
                token = Token("TT_MINUS", self.curChar, self.curPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == '*':
                if self.peek() == '*':
                    lastChar = self.curChar
                    self.nextChar()
                    token = Token("TT_POW", lastChar + self.curChar, self.curPos - 1, self.curPos)
                else:
                    token = Token("TT_MULT", self.curChar, self.curPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == '/':
                token = Token("TT_DIV", self.curChar, self.curPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == '=':
                if self.peek() == '=':
                    lastChar = self.curChar
                    self.nextChar()
                    token = Token("TT_EQEQ", lastChar + self.curChar, self.curPos-1, self.curPos)
                else:
                    token = Token("TT_EQ", self.curChar, self.curPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == '>':
                if self.peek() == '=':
                    lastChar = self.curChar
                    self.nextChar()
                    token = Token("TT_GTEQ", lastChar + self.curChar, self.curPos-1, self.curPos)
                else:
                    token = Token("TT_GT", self.curChar, self.curPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == '<':
                    if self.peek() == '=':
                        lastChar = self.curChar
                        self.nextChar()
                        token = Token("TT_LTEQ", lastChar + self.curChar, self.curPos-1, self.curPos)
                    else:
                        token = Token("TT_LT", self.curChar, self.curPos, self.curPos)
                    self.tokenList.append(token)
            elif self.curChar == '!':
                if self.peek() == '=':
                    lastChar = self.curChar
                    self.nextChar()
                    token = Token("TT_NTEQ", lastChar + self.curChar, self.curPos, self.curPos)
                else:
                    self.abort("Expected !=, got !" + self.peek())
                self.tokenList.append(token)
            elif self.curChar == '\"':
                self.nextChar()
                startPos = self.curPos

                while self.curChar != '\"':
                    if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                        self.abort("Illegal character in string.")
                    self.nextChar()

                tokText = self.source[startPos : self.curPos+1]
                token = Token("TT_STRING", tokText, startPos-1, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == "\'":
                self.nextChar()
                startPos = self.curPos

                while self.curChar != "\'":
                    if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                        self.abort("Illegal character in string.")
                    self.nextChar()

                tokText = self.source[startPos : self.curPos+1]
                token = Token("TT_STRING", tokText, startPos-1, self.curPos)
                self.tokenList.append(token)
            elif self.curChar.isdigit():
                startPos = self.curPos
                while self.peek().isdigit():
                    self.nextChar()
                if self.peek() == '.':
                    self.nextChar()

                    if not self.peek().isdigit():
                        self.abort("Illegal character in number.")
                    while self.peek().isdigit():
                        self.nextChar()

                tokText = self.source[startPos : self.curPos + 1]
                token = Token("TT_NUMBER", tokText, startPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar.isalpha():
                startPos = self.curPos
                while self.peek().isalnum():
                    self.nextChar()

                if self.source[startPos - 1].isdigit():
                    self.abort(f"Invalid Identifier: {self.source[startPos-1 : self.curPos +1]}")

                tokText = self.source[startPos : self.curPos + 1]
                keyword = isKeyWord(tokText)
                if not keyword:
                    token = IdentToken("TT_IDENT", tokText, startPos, self.curPos)
                else:
                    token = Token("TT_KEYW", tokText, startPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == '(':
                token = Token("TT_LPAREN", self.curChar, self.curPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == ')':
                token = Token("TT_RPAREN", self.curChar, self.curPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == '[':
                token = Token("TT_LSQPAREN", self.curChar, self.curPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == ']':
                token = Token("TT_RSQPAREN", self.curChar, self.curPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == ':':
                token = Token("TT_COLON", self.curChar, self.curPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == ',':
                token = Token("TT_COMMA", self.curChar, self.curPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == '\t':
                token = Token("TT_TAB", '',  self.curPos, self.curPos)
                self.tokenList.append(token)
            elif self.curChar == '\n':
                token = Token("TT_NWL", '', self.curPos, self.curPos)
                self.tokenList.append(token)
            else:
                self.abort("Unknown token: " + self.curChar)

            self.nextChar()

        self.tokenList.append(Token("TT_EOF"))
        return self.tokenList


class Token:
    def __init__(self, type_, value=None, start=None, end=None):
        self.type = type_
        self.value = value
        self.start = start
        self.end = end

    def __repr__(self):
        if self.value: return f'{self.type}:\"{self.value}\"'
        return f'{self.type}'

    def read(self, obj):
        if(self.value):
            if self.type == "TT_NUMBER":
                self.value = float(self.value)
            return self.value
        else:
            return None


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
            sys.exit(f"'{self.value}' doesn't exists")
        return None


def isKeyWord(token):
    keywords = ["print"]
    if token in keywords:
        return True
    return False
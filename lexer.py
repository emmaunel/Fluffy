from sly import Lexer


class BasicLexer(Lexer):
    tokens = {NAME, NUMBER, STRING, IF, ELSE, FOR, FUNC, EQEQ}
    ignore = '\t '

    literals = { '=', '+', '-', '/', '*', '(', ')', ',', ';'}
    # Define Tokens
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    IF = r'if'
    ELSE = r'else'
    FOR = r'for'
    FUNC = r'func'
    STRING = r'\".*?\"'

    EQEQ = r'=='

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'//.*')
    def COMMENT(self, t):
        pass

    @_(r'\n+')
    def newline(self, t):
        self.lineno = t.value.count('\n')


if __name__ == '__main__':
    lexer = BasicLexer()
    env = {}
    while True:
        try:
            text = input('fluffy > ')
        except EOFError:
            break
        if text:
            lex = lexer.tokenize(text)
            for token in lex:
                print(token)

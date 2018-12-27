from sly import Lexer


class Fluffy_Lexer(Lexer):
    tokens = {NAME, NUMBER, STRING, IF, THEN, ELSE, FOR, FUN, TO, ARROW, EQEQ, EXIT}
    ignore = '\t '

    literals = {'=', '+', '-', '/', '*', '(', ')', ',', ';'}

    # Define tokens
    IF = r'if'
    THEN = r'then'
    ELSE = r'else'
    FOR = r'for'
    FUN = r'fun'
    TO = r'to'
    EXIT = r'exit'
    ARROW = r'->'
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'\".*?\"'

    EQEQ = r'=='

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'#.*')
    def COMMENT(self, t):
        pass

    @_(r'\n+')
    def newline(self, t):
        self.lineno = t.value.count('\n')


if __name__ == '__main__':
    lexer = Lexer()
    env = {}
    while True:
        try:
            text = input('fluffy > ')
        except EOFError:
            break
        if text:
            lex = lexer.tokenize(text)
            # for token in lex:
            #     print(token)

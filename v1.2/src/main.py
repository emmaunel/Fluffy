import os
import sys
import lexer
import parser

def main():
    content = ""
    path = os.getcwd()

    try:
        fileName = sys.argv[1]
    except:
        print("[ERROR] Expected 1 Argument Containing File Name to be Run e.g 'fluffy main.f'")
        return

    if fileName[len(fileName) - 2:len(fileName)] != ".f":
        print("[ERROR] File extension not recognised please make sure extension is '.tn'")
        return # quit program

    try:
        print('[ERROR] Expected 1 argument found 2 (' + sys.argv[1] + ", " + sys.argv[2] + ')')
        return # quit programme
    except:
        pass

    try:
        with open(path + "/" + fileName, "r") as file:
            content = file.read()
    except:
        print('Cannot find "' + fileName + '"')


    print('|||||||||||||||||||||  LEXER LOG  ||||||||||||||||||||| \n')
    lex = lexer.Lexer()
    tokens = lex.tokenize(content)
    print(tokens)
    print('\n||||||||||||||||||||||||||||||||||||||||||||||||||||| \n')

    print('|||||||||||||||||||||  PARSER LOG  ||||||||||||||||||||| \n')
    Parser = parser.Parser(tokens)
    source_ast = Parser.parse(tokens)
    print(source_ast)
    print('\n|||||||||||||||||||||||||||||||||||||||||||||||||||||| \n')

main()

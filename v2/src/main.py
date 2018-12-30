import os
import sys
from v2.src import Lexer
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
        return  # quit program

    try:
        print('[ERROR] Expected 1 argument found 2 (' + sys.argv[1] + ", " + sys.argv[2] + ')')
        return  # quit program
    except:
        pass

    try:
        with open(path + "/" + fileName, "r") as file:
            content = file.read()
    except:
        print('Cannot find "' + fileName + '"')

    lex = Lexer.Lexer()
    tokens = lex.tokenize(content)
    print(tokens)


main()

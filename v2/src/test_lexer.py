import lexer

def main(file_name):
    with open(file_name) as inFile:
        line = inFile.read()
        print(line)


if __name__ == '__main__':
    file_name = input("Enter a file name: ")
    main(file_name)

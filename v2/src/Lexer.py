import constants
import re


class Lexer(object):
    def tokenize(self, source_code):
        """
        This method converts the content of a file(.f extention) and
        returns a list of the words putted into their respective tokens.
        E.g: str name = "Ayo" -> [["DATATYPE", str], ["IDENTIFIER", name],
                                ["OPERATOR", =], ["IDENTIFIER", "Ayo"]]
        :param source_code: each line of a file
        :return: a list of tokens
        """
        # List of all the tokens
        tokens = []

        # split each line to words and igonors the \n
        source_code = source_code.split()

        # Current word index
        source_index = 0

        while source_index < len(source_code):

            # Individual word from the source c0de
            word = source_code[source_index]

            # If there is a new line, ignore
            if word == "\n":
                pass

            # Check if the word is a BUILT-IN datatype
            elif word in constants.DATATYPE:
                tokens.append(["DATATYPE", word])

            # Check if the word is a BUILT-IN keywords
            elif word in constants.KEYWORDS:
                tokens.append(["IDENTIFIER", word])

            elif re.match("[a-zA-Z]", word):
                # If the last character is ;, it ignores that
                # and puts the rest of the word
                if word[len(word) - 1] != ";":
                    tokens.append(["IDENTIFIER", word])
                else:
                    tokens.append(["IDENTIFIER", word[0:len(word) - 1]])

            # You get the point right?
            elif word == "+=" or word == "-=" or word == "*=" or word == "/=":
                tokens.append(['INCREMENTAL_OPERATOR', word])

            # TODO: put them in the constants folder
            elif word in "*-/+%=":
                tokens.append(["OPERATOR", word])

            elif word == "&&" or word == "||":
                tokens.append(["BINARY_OPERATOR", word])

            # TODO: Change later to a better loop format
            elif word == "->":
                tokens.append(["SEPARATOR", word])

            elif word in "==" or word in "!=" or word in ">" or word in "<" or word in "<=" \
                    or word in ">=":
                tokens.append(["COMPARISON_OPERATOR", word])

            elif word in "{}":
                tokens.append(["SCOPE_DEFINER", word])

            elif word == "//":
                tokens.append(["COMMENT_DEFINER", word])

            elif re.match("[0-9]", word) or re.match("[-]?[0-9]", word):
                if word[len(word) - 1] == ";":
                    tokens.append(["INTEGER", word[:-1]])
                else:
                    tokens.append(["INTEGER", word])

            # Check if the there's a " in the word
            elif ('"') in word:
                matcherReturn = self.matcher('"', source_index, source_code)

                # If the the string was just a single word like "Hello"
                if matcherReturn[1] == '':
                    tokens.append(["STRING", matcherReturn[0]])
                else:
                    tokens.append(["STRING", matcherReturn[0]])
                    if ";" in matcherReturn[1]:
                        tokens.append(["STATEMENT_END", ";"])

                    # Skip all the already checked string items so there are no duplicates
                    source_index += matcherReturn[2]

                    # Skip every other check and loop again
                    pass

            # Checks for the end of a statement ';'
            if ';' in word[len(word) - 1]:
                tokens.append(["STATEMENT_END", ";"])
            source_index += 1

        return tokens

    def matcher(self, matcher, current_index, source_code):
        """
        This function basically extract the word that is between two quotes
        :param matcher:
        :param current_index:
        :param source_code:
        :return:
        """

        # Check if the quotes is the same in the source code
        if source_code[current_index].count('"') == 2:

            # This will partition the string and return a tuple like,
            # ('word', 'matcher(")', ';')
            word = source_code[current_index].partition('"')[-1].partition('"'[0])
            if word[2] != '':
                return ['"' + word[0] + '"', '', word[2]]
            else:
                return ['"' + word[0] + '"', '', '']
        else:
            source_code = source_code[current_index:len(source_code)]
            word = ""
            iter_count = 0
            for item in source_code:
                iter_count += 1
                word += item + " "
                if matcher in item and iter_count != 1:
                    return [
                        '"' + word.partition('"')[-1].partition('"'[0])[0] + '"',  # The string
                        word.partition('"')[-1].partition('"'[0])[2],              # The extra character
                        iter_count - 1                                                   # Number of iterations it took
                    ]

                    # break

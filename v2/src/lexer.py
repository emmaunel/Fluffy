import constants
import re

class Lexer(object):
    def tokenize(self, source_code):
        tokens = []
        source_code = source_code.split()
        source_index = 0
        while source_index < len(source_code):
            word = source_code[source_index]
            if word == "\n":
                pass
            elif word in constants.DATATYPE:
                tokens.append(["DATATYPE", word])
            elif word in constants.KEYWORDS:
                tokens.append(["IDENTIFIER", word])
            elif re.match("[a-zA-Z]", word):
                if word[len(word) - 1] != ";":
                    tokens.append(["IDENTIFIER", word])
                else:
                    tokens.append(["IDENTIFIER", word[0:len(word) - 1]])
            elif word == "+=" or word == "-=" or word == "*=" or word == "/=":
                tokens.append(['INCREMENTAL_OPERATOR', word])
            # TODO: put them in the constants folder
            elif word in "*-/+%=":
                tokens.append(["OPERATOR", word])
            elif word == "&&" or word == "||":
                tokens.append(["BINARY_OPERATOR"], word)
            # TODO: Change later to a better loop format
            elif word == "->":
                tokens.append(["SEPERATOR", word])
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

            elif ('"') in word:
                matcherReturn = self.matcher('"', source_index, source_code)
                if matcherReturn[1] == '':
                    tokens.append(["STRING", matcherReturn[0]])
                else:
                    tokens.append(["STRING", matcherReturn[0]])
                    if ';' in matcherReturn[1]:
                        tokens.append(["STATEMENT_END", ";"])
                    source_index += matcherReturn[2]
                    pass
            if ';' in word[len(word) - 1]:
                tokens.append(["STATEMENT_END", ";"])
            source_index += 1

        return tokens


    def matcher(self, matcher, current_index, source_code):
        if source_code[current_index].count('"') == 2:
            word = source_code[current_index].partition('"')[-1].partition('"'[0])
            if word[2] != '':
                return ['"' + word[0] + '"', '', word[2]]
            else:
                return ['"' + word[0] + '"', '', '']
        else:
            source_code = source_code[current_index:len(source_code)]
            word = ""
            iter = 0
            for item in source_code:
                iter_count += 1
                word += item + " "
                if matcher in item and iter != 1:
                    return [
                        '"' + word.partition('"')[-1].partition('"'[0])[0] + '"',
                        word.partition('"')[-1].partition('"'[0])[2],
                        iter - 1
                    ]

                    break

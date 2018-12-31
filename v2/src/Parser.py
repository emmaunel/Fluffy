"""
File: Parser.py
Language: Python 3
Author: Ayobami Emmanuel Adewale <aadewale123@gmail.com>
Purpose:
"""
import constants


class Parser(object):
    """docstring for Parser."""

    def __init__(self, token_stream):
        # Abstract Syntax tree
        self.source_ast = {'main_scope': []}
        # Symbol table for variable semantical analyses
        self.symbol_tree = []
        self.token_stream = token_stream
        self.token_index = 0

    def parse(self, token_stream):
        """
        Takes in a list of tokens and turn them into a tree(like binary tree but a syntax tree)
        :param token_stream: A list of tokens created by the lexer
        """
        while self.token_index < len(token_stream):
            token_type = token_stream[self.token_index][0]
            token_value = token_stream[self.token_index][1]

            print('------------------------------ ', token_type, token_value, ' ------------------------------')

            # This will find the token pattern for a variable deceleration
            if token_type == "DATATYPE":
                self.variable_deceleration_parsing(token_stream[self.token_index:len(token_stream)], False)

            # This will find the token pattern for an if statement
            # elif token_type == "IDENTIFIER" and token_value == "if":
            #     self.conditional_statement_parser(token_stream[self.token_index:len(token_stream)], False)
            #
            # # This will find the pattern started for a for loop
            elif token_type == "IDENTIFIER" and token_value == "for":
                print("FOR BEFORE: ", self.token_index)
                self.parse_for(token_stream[self.token_index:len(token_stream)], False)
                print("FOR AFTER: ", self.token_index)

            # # This will find the pattern for a built-in function call
            # elif token_type == "IDENTIFIER" and token_value in constants.BUILT_IN_FUNCTIONS:
            #     self.parse_built_in_function(token_stream[self.token_index:len(token_stream)], False)
            #
            # # This will find the pattern started for a comment
            # elif token_type == "COMMENT_DEFINER" and token_value == "(**":
            #     self.parse_comment(token_stream[self.token_index:len(token_stream)], False)
            #
            self.token_index += 1
        return self.source_ast

    # TODO: Create one function for all the loops(while, for, switch)
    def parse_for(self, token_stream, isInBody):
        """
        This function parse for loops
        :param token_stream: All the tokens from the lexer
        :param isInBody: Tells if the function has been checked or not
        :return:
        """

        ast = {'ForLoop': []}

        # Start the parsing at index 1 so it ignores the word 'for
        tokens_checked = 1

        # Indicates when it in the condition part(for int x = 0 -> < 10) and when it's in the incrementation part
        loopSection = 1
        while tokens_checked < len(token_stream):

            # When it gets to the opening bracket, break out of the loop
            if token_stream[tokens_checked][1] == '{':
                break

            if tokens_checked == 1:
                # Gets the tokens before the first separator ->
                var_decl_tokens = self.get_token_to_matcher("->", "{", token_stream[tokens_checked:len(token_stream)])

                # Perform error handling to see if the tokens could be fetched and the separator '::' was found
                if not var_decl_tokens:
                    self.send_error_message("Loop missing separator '->'", token_stream)

                # Manually append statement end to the end of the var deceleration so var parser behaves and doesnt
                # throw error
                var_decl_tokens[0].append(['STATEMENT_END', ';'])
                var_parsing = self.variable_deceleration_parsing(var_decl_tokens[0], True)

                # Append initialValueName property to the ForLoop AST
                # Call the variable parser with True so the var deceleration isn't added to source_ast
                ast['ForLoop'].append({'initialValueName': var_parsing[0]['VariableDeceleration'][1]['name']})
                # Append initialValue property to the ForLoop AST
                ast['ForLoop'].append({'initialValue': var_parsing[0]['VariableDeceleration'][2]['value']})
                # Increase tokens checked count and minus 1 because we manually add the STATEMENT_END token
                self.token_index -= var_decl_tokens[1]

            if token_stream[tokens_checked][1] == '->':

                # This will handle the parsing for loop section 1 which is the ConditionForLoop such as x < 10
                if loopSection == 1:
                    condition_tokens = self.get_token_to_matcher('->', '{',
                                                                 token_stream[tokens_checked + 1:len(token_stream)])

                    ast['ForLoop'].append({'comparison': condition_tokens[0][1][1]})
                    ast['ForLoop'].append({'endValue': condition_tokens[0][1][1]})
                    tokens_checked += condition_tokens[1]

                # This will handle the parsing for loop section 1 which is the IncrementForLoop such as x = x + 1
                if loopSection == 2:
                    increment_tokens = self.get_token_to_matcher('{', '}',
                                                                 token_stream[tokens_checked + 1:len(token_stream)])
                    ast['ForLoop'].append({'incrementer': self.assemble_token_values(increment_tokens[0])})
                    tokens_checked += increment_tokens[1]

                # Increase the loopSection by 1 so it can read next section differently
                loopSection += 1

            # Increase tokens checked count by 1 for each token being looped through so we can keep an accurate count
            tokens_checked += 1

        self.token_index += tokens_checked

        # Get the tokens from the body and the amount of tokens there is in the body
        # Add 1 as usual body tokens parsing and object generation or else indentation won't work properly
        get_body_tokens = self.get_statement_body(token_stream[tokens_checked + 1:len(token_stream)])

        # If parse not called from body parser method then append to source ast
        if not isInBody:
            self.parse_body(get_body_tokens[0], ast, 'ForLoop', False)
        else:
            self.parse_body(get_body_tokens[0], ast, 'ForLoop', True)

        # Add the amount tokens we checked in body
        tokens_checked += get_body_tokens[1]

        return [ast, tokens_checked]

    def assemble_token_values(self, tokens):
        attached_tokens = ""
        for token in tokens:
            attached_tokens += token[1] + ""
            return attached_tokens

    def get_token_to_matcher(self, matcher, terminating_matcher, token_stream):
        """ Get Token Matcher

        This will get all the tokens in a token stream until it find the token with the correct
        matcher
        args:
            matcher      (str)   : The string which contains matcher
            token_stream (list)  : The list of tokens matcher needs to be found in
            terminating_matcher (str) : The token value that when found will stop check regardless if there is more tokens or if the matcher was found
        returns:
            tokens (list) : A list of all the tokens found before the matcher"""

        tokens = []
        tokens_checked = 0

        for token in token_stream:
            tokens_checked += 1
            # If the terminating matcher is found then return False as it means scope we allow for the check is reached
            if token[1] == terminating_matcher:
                return False
            # If the token matcher is found then return all the tokens found before it or else append the tokens to var
            if token[1] == matcher:
                return [tokens, tokens_checked - 1]
            else:
                tokens.append(token)

        # Return False if the matcher nor the terminator_matcher is found
        return False

    def parse_comment(self, token_stream, isInBody):
        """ Parse Comment

        This will parse single/multi line comments
        args:
            token_stream (list) : The tokens produced by lexer
            isInBody     (bool) : This will hold True if this function is being run from body parsing
        returns:
            ast          (dict) : The condtion ast without the body
            tokens_checked (int): The count of tokens checked that made up the condition statement
        """
        ast = {'Comment': ""}
        tokens_checked = 0
        comment_string = ""

        for token in range(0, len(token_stream)):

            # When the closing comment definer is found then break out the loop
            if token_stream[token][0] == "COMMENT_DEFINER" and token != 0: break

            # Add the words up together to make full comment string and also skip the first token because its the comment_definer
            if token != 0: comment_string += str(token_stream[token][1]) + " "

            # Increment tokens checked count
            tokens_checked += 1

        # Append comment string to the comment AST
        ast['Comment'] = comment_string
        # If parse not called from body parser method then append to source ast
        if not isInBody: self.source_ast['main_scope'].append(ast)
        # Append the number of variables checked to the token index
        self.token_index += tokens_checked

        return [ast, tokens_checked]

    def parse_built_in_function(self, token_stream, isInBody):
        """ Parse Built-in Function

        This will parse built in methods and their parameters to form an AST
        args:
            token_stream (list) : The tokens produced by lexer
            isInBody     (bool) : This will hold True if this function is being run from body parsing
        returns:
            ast          (dict) : The condtion ast without the body
            tokens_checked (int): The count of tokens checked that made up the condition statement
        """
        ast = {'PrebuiltFunction': []}
        tokens_checked = 0

        for token in range(0, len(token_stream)):

            # Break out of loop whn statement end is found
            if token_stream[token][0] == "STATEMENT_END": break

            # This will get the builtin function name
            if token == 0:
                ast['PrebuiltFunction'].append({'type': token_stream[token][1]})

            # This will get the parameter
            if token == 1 and token_stream[token][0] in ['INTEGER', 'STRING', 'IDENTIFIER']:

                # If the argument passed is a variable (identifier) then try get value
                if token_stream[token][0] == 'IDENTIFIER':
                    # Get value and handle any errors
                    value = self.get_variable_value(token_stream[token][1])
                    if value != False:
                        ast['PrebuiltFunction'].append({'arguments': [value]})
                    else:
                        self.send_error_message("Variable '%s' does not exist" % token_stream[tokens_checked][1],
                                                token_stream[0:tokens_checked + 1])
                # TODO Allow for concatenation and equation parsing
                else:
                    if token_stream[token + 1][0] == 'STATEMENT_END':
                        ast['PrebuiltFunction'].append({'arguments': [token_stream[token][1]]})
                    else:
                        value_list_func_call = self.form_value_list(token_stream[tokens_checked:len(token_stream)])
                        print(value_list_func_call)

            # This will throw an error if argument passed in is not a permitted token type
            elif token == 1 and token_stream[token][0] not in ['INTEGER', 'STRING', 'IDENTIFIER']:
                self.send_error_message(
                    "Invalid argument type of %s expected string, identifier or primitive data type" %
                    token_stream[token][0],
                    token_stream[0:tokens_checked + 1])

            tokens_checked += 1  # Increment tokens checked

        # If it's being parsed within a body don't ass the ast to the source ast
        if not isInBody: self.source_ast['main_scope'].append(ast)
        # Increase token index to make up for tokens checked
        self.token_index += tokens_checked

        return [ast, tokens_checked]

    def variable_deceleration_parsing(self, token_stream, isInBody):
        """ Variable Deceleration Parsing
        This method will parse variable decelerations and add them to the source AST or
        return them if variable deceleration is being parsed for body of a statement
        Args:
            token_stream (list) : The token stream starting from where var decleration was found
        """

        ast = {'VariableDeceleration': []}  # The abstract syntax tree for var decl
        tokens_checked = 0  # Number of token checked that made up the var decl
        var_exists = True

        for x in range(0, len(token_stream)):

            # Create variables for identifying token type and value more easily
            token_type = token_stream[x][0]
            token_value = token_stream[x][1]
            # print(token_stream[1])
            # print(token_type)
            # print(token_value)
            # print(token_stream[2])

            # Skip the '=' operator in var decl
            if x == 2 and token_type == "OPERATOR" and token_value == "=":
                pass
            # This will handle error detection for making sure the '=' is found
            if x == 2 and token_type != "OPERATOR" and token_value != "=":
                self.send_error_message("Variable Deceleration Missing '='.",
                                        self.token_stream[self.token_index:self.token_index + tokens_checked + 2])

            # If a statement end is found then break out parsing
            if token_stream[x][0] == "STATEMENT_END":
                break

            # This will parse the first token which will be the var type
            if x == 0:
                ast['VariableDeceleration'].append({"type": token_value})

            # This will parse the second token which will be the name of the var
            if x == 1 and token_type == "IDENTIFIER":

                # Check if a variable has already been named the same and is so send an error
                if self.get_variable_value(token_value):
                    self.send_error_message("Variable '%s' already exists and cannot be defined again!" % token_value,
                                            self.token_stream[self.token_index:self.token_index + tokens_checked + 1])
                else:
                    # Set var exists to False so that it can be added
                    var_exists = False

                    # This will check if the variable is being declared but not initialised
                    # e.g int x;
                    if token_stream[x + 1][0] == "STATEMENT_END":
                        # Adds the default value of 'undefined' and breaks out of loop
                        ast['VariableDeceleration'].append({"name": token_value})
                        ast['VariableDeceleration'].append({"value": '"undefined"'})
                        tokens_checked += 1
                        break
                    else:
                        ast['VariableDeceleration'].append({"name": token_value})

            # Error handling for variable name to make sure the naming convention is acceptable
            if x == 1 and token_type != "IDENTIFIER":
                self.send_error_message("Invalid Variable Name '%s'" % token_value,
                                        self.token_stream[self.token_index:self.token_index + tokens_checked + 1])

            # This will parse the 3rd token which is the value of the variable
            if x == 3 and token_stream[x + 1][0] == "STATEMENT_END":

                # Check if the value matches the variable defined type
                if type(eval(token_value)) == eval(token_stream[0][1]):
                    # Add value as a number not a string if it is an int or else add it as a string
                    try:
                        ast['VariableDeceleration'].append({"value": int(token_value)})
                    except ValueError:
                        ast['VariableDeceleration'].append({"value": token_value})
                else:
                    self.send_error_message("Variable value does not match defined type!",
                                            self.token_stream[self.token_index:self.token_index + tokens_checked + 1])

            # This will parse any variable declerations which have concatenation or arithmetics
            elif x >= 3:

                # This will call the form_value_list method and it will return the concatenation value and tokens
                # checked
                value_list_func_call = self.form_value_list(token_stream[tokens_checked:len(token_stream)])
                value_list = value_list_func_call[0]
                tokens_checked += value_list_func_call[1]

                # Call the equation parser and append value returned or try concat parser if an error occurs
                try:
                    ast['VariableDeceleration'].append({"value": self.equation_parser(value_list)})
                except:
                    try:
                        ast['VariableDeceleration'].append({"value": self.concatenation_parser(value_list)})
                    except:
                        self.send_error_message("Invalid variable deceleration!",
                                                self.token_stream[self.token_index:self.token_index + tokens_checked])
                break  # Break out of the current var parsing loop since we just parsed everything

            tokens_checked += 1  # Indent within overall for loop

        # Last case error validation checking if all needed var decl elements are in the ast such as:
        # var type, name and value
        try:
            ast['VariableDeceleration'][0]
        except:
            self.send_error_message("Invalid variable deceleration could not set variable type!",
                                    self.token_stream[self.token_index:self.token_index + tokens_checked])
        try:
            ast['VariableDeceleration'][1]
        except:
            self.send_error_message("Invalid variable deceleration could not set variable name!",
                                    self.token_stream[self.token_index:self.token_index + tokens_checked])
        try:
            ast['VariableDeceleration'][2]
        except:
            self.send_error_message("Invalid variable deceleration could not set variable value!",
                                    self.token_stream[self.token_index:self.token_index + tokens_checked])

        # If this is being run to parse inside a body then there is no need to add it to the source ast
        # as it will be added to the body of statement being parsed
        if not isInBody:
            self.source_ast['main_scope'].append(ast)

        if not var_exists:
            self.symbol_tree.append([ast['VariableDeceleration'][1]['name'], ast['VariableDeceleration'][2]['value']])

        self.token_index += tokens_checked
        print(ast)
        return [ast, tokens_checked]  # Return is only used within body parsing to create body ast

    def conditional_statement_parser(self, token_stream, isNested):
        """ Conditional Statement Parser
        This will parse conditional statements like 'if else' and create an
        abstract sytax tree for it.
        args:
            token_stream (list) : tokens which make up the conditional statement
            isNested     (bool) : True the conditional statement is being parsed within another conditional statement
        return:
            ast          (dict)  : The condtion ast without the body
            tokens_checked (int) : The count of tokens checked that made up the condition statement
        """

        tokens_checked = 0
        ast = {'ConditionalStatement': []}

        # This loop will parse the condition e.g. if 12 < 11
        for x in range(0, len(token_stream)):

            tokens_checked += 1

            # Simplification variables that will improve readbility
            token_type = token_stream[x][0]
            token_value = token_stream[x][1]
            allowed_conditional_token_types = ['INTEGER', 'STRING', 'IDENTIFIER']

            # Break out of loop at the end of the condition
            if token_type == 'SCOPE_DEFINER' and token_value == '{': break

            # Pass if token is the 'if' identifier as it has already been checked
            if token_type == 'IDENTIFIER' and token_value == 'if':  pass

            # This will check for the first value and add it to the AST
            if x == 1 and token_type in allowed_conditional_token_types:
                # This will check for an identifier (var) and then check if it exists so it can add the value to it
                if self.get_variable_value(token_value) != False:
                    ast['ConditionalStatement'].append({'value1': self.get_variable_value(token_value)})
                else:
                    ast['ConditionalStatement'].append({'value1': token_value})

            # This will check for the comparison operator and add it to the AST
            if x == 2 and token_type == 'COMPARISON_OPERATOR':
                ast['ConditionalStatement'].append({'comparison_type': token_value})

            # This will check for the second value and add it to the AST
            if x == 3 and token_type in allowed_conditional_token_types:
                # This will check for an identifier (var) and then check if it exists so it can add the value to it
                if self.get_variable_value(token_value) != False:
                    ast['ConditionalStatement'].append({'value2': self.get_variable_value(token_value)})
                else:
                    ast['ConditionalStatement'].append({'value2': token_value})

        # Increment global token index for tokens checked in condition
        self.token_index += tokens_checked - 1

        # This will get the body tokens and the tokens checked that make up the body to skip them
        get_body_return = self.get_statement_body(token_stream[tokens_checked:len(token_stream)])

        print()
        print()
        print()
        print('---', get_body_return)
        print()
        print()
        print()

        # If it nested then call parse_body with nested parameter of true else false
        if isNested == True:
            self.parse_body(get_body_return[0], ast, 'ConditionalStatement', True)
        else:
            self.parse_body(get_body_return[0], ast, 'ConditionalStatement', False)

        # Add the amount tokens we checked in body
        tokens_checked += get_body_return[1]

        return [ast, tokens_checked]  # Return is only used within body parsing to create body ast

    def parse_body(self, token_stream, statement_ast, astName, isNested):
        """ Parse body
        This will parse the body of conditional, iteration, functions and more in order
        to return a body ast like this --> {'body': []}
        args:
            token_stream  (list) : tokens which make up the body
            statement_ast (dict) : The condition of the body being parsed
            isNested      (bool) : If the condition being parsed is nested
        returns:
            ast       (object) : Abstract Syntax Tree of the body
        """

        ast = {'body': []}
        tokens_checked = 0
        nesting_count = 0

        # Loop through each token to find a pattern to parse
        while tokens_checked < len(token_stream):

            # This will parse variable declerations within the body
            if token_stream[tokens_checked][0] == "DATATYPE":
                var_decl_parse = self.variable_decleration_parsing(token_stream[tokens_checked:len(token_stream)], True)
                ast['body'].append(var_decl_parse[0])
                tokens_checked += var_decl_parse[1]

            # This will parse nested conditional statements within the body
            elif token_stream[tokens_checked][0] == 'IDENTIFIER' and token_stream[tokens_checked][1] == 'if':
                condition_parsing = self.conditional_statement_parser(token_stream[tokens_checked:len(token_stream)],
                                                                      True)
                ast['body'].append(condition_parsing[0])
                tokens_checked += condition_parsing[1] - 1  # minus one to not skip extra token

            elif token_stream[tokens_checked][0] == "IDENTIFIER" and token_stream[tokens_checked][1] == "for":
                loop_parse = self.parse_for_loop(token_stream[tokens_checked:len(token_stream)], True)
                ast['body'].append(loop_parse[0])
                tokens_checked += loop_parse[1]

            # This will parse builtin functions within the body
            elif token_stream[tokens_checked][0] == 'IDENTIFIER' and token_stream[tokens_checked][
                1] in constants.BUILT_IN_FUNCTIONS:
                built_in_func_parse = self.parse_built_in_function(token_stream[tokens_checked:len(token_stream)], True)
                ast['body'].append(built_in_func_parse[0])
                tokens_checked += built_in_func_parse[1]

            # This will parse comments within the body
            elif token_stream[tokens_checked][0] == "COMMENT_DEFINER" and token_stream[tokens_checked][1] == "//":
                comment_parsing = self.parse_comment(token_stream[tokens_checked:len(token_stream)], True)
                ast['body'].append(comment_parsing[0])
                tokens_checked += comment_parsing[1]

            # This is needed to increase token index by 1 when a closing scope definer is found because it is skipped
            # so when it is found then add 1 or else this will lead to a logical bug in nesting
            if token_stream[tokens_checked][1] == '}':
                nesting_count += 1

            tokens_checked += 1

        # Increase token index by amount of closing scope definers found which is usually skipped and add 1 for the last
        #  one which is not passed in to this method
        self.token_index += nesting_count + 1
        # Form the full ast with the statement and body combined and then add it to the source ast
        statement_ast[astName].append(ast)
        # If the statments is not nested then add it or else don;t because parent will be added containing the child
        if not isNested: self.source_ast['main_scope'].append(statement_ast)

    def get_statement_body(self, token_stream):
        """ Get Statement Body

            This will get the tokens that make up the body of a statement and return
            the tokens

            args:
                token_stream (list): This will hold the tokens after the scope definer
            return:
                tokens_list  (list): Returns tokens that make up the body for statement
        """

        nesting_count = 1
        tokens_checked = 0
        body_tokens = []

        for token in token_stream:

            tokens_checked += 1

            # Simpliies & Increases readabilty of toke type and value
            token_value = token[1]
            token_type = token[0]

            # Keeps track of the opening and closing scope definers '}' and '{'
            if token_type == "SCOPE_DEFINER" and token_value == "{":
                nesting_count += 1
            elif token_type == "SCOPE_DEFINER" and token_value == "}":
                nesting_count -= 1

            # Checks whether the closing scope definer is found to finish creating body tokens
            if nesting_count == 0:
                body_tokens.append(token)
                break
            else:
                body_tokens.append(token)

        print('{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}}}', body_tokens)

        return [body_tokens, tokens_checked]

    def equation_parser(self, equation):
        """ Equation parsing
        This will parse equations such as 10 * 10 which is passed in as an array with
        numbers and operands.
        args:
            equation (list) : List of the ints and operands in order
        returns:
            value (int)     : The value of the equation
        """
        total = 0  # Holds equation value
        for item in range(0, len(equation)):
            # Add first value to total as a starting int to perform calculatios on
            if item == 0:
                total += equation[item]
                pass
            # This will check every operator and perform the right calculations based on total
            # and the number that is after the operator
            if item % 2 == 1:
                if equation[item] == "+":
                    total += equation[item + 1]
                elif equation[item] == "-":
                    total += equation[item + 1]
                elif equation[item] == "/":
                    total /= equation[item + 1]
                elif equation[item] == "*":
                    total *= equation[item + 1]
                elif equation[item] == "%":
                    total %= equation[item + 1]
                else:
                    self.send_error_message("Error parsing equation, check that you are using correct operand",
                                            equation)
            # Skip every number since we already check and use them
            elif item % 2 == 0:
                pass
        return total

    def concatenation_parser(self, concatenation_list):
        """ Concatenaion Parser
        This will parse concatenation of strings and variables with string values or integer
        values to concatenate arithmetics to strings together e.g. "Ryan " + last_name;
        args:
            concatenation_list (list) : Array with all items needed seperated to perform concatenation
        return:
            value (string)            : Full string after concatenation done
            error (list)              : Return False with an error message in a list
        """
        full_string = ""
        for item in range(0, len(concatenation_list)):
            current_value = concatenation_list[item]
            # Add the first item to the string
            if item == 0:
                # This checks if the value being checked is a string or a variable
                # If it is a string then just add it without the surrounding quotes
                if current_value[0] == '"':
                    full_string += current_value[1:len(current_value) - 1]
                # If it isn't a string then get the variable value and append it
                else:
                    var_value = self.get_variable_value(current_value)
                    if var_value != False:
                        full_string += var_value[1:len(var_value) - 1]
                    else:
                        self.send_error_message(
                            'Cannot find variable "%s" because it was never created' % concatenation_list[item + 1],
                            concatenation_list)
                pass
            # This will check for the concatenation operator
            if item % 2 == 1:
                if current_value == "+":
                    # This checks if the value being checked is a string or a variable
                    if concatenation_list[item + 1][0] != '"':
                        # This will get the variable value and check if it exists if so then it adds it to the full string
                        var_value = self.get_variable_value(concatenation_list[item + 1])
                        if var_value != False:
                            full_string += var_value[1:len(var_value) - 1]
                        else:
                            self.send_error_message(
                                'Cannot find variable "%s" because it was never created' % concatenation_list[item + 1],
                                concatenation_list)
                    else:
                        full_string += concatenation_list[item + 1][1:len(concatenation_list[item + 1]) - 1]
                elif current_value == ",":
                    full_string += " " + concatenation_list[item + 1]
                else:
                    self.send_error_messages("Error parsing equation, check that you are using correct operand",
                                             concatenation_list)
            # This will skip value as it is already being added and dealt with when getting the operand
            if item % 2 == 0: pass
        return '"' + full_string + '"'

    def get_variable_value(self, name):
        """ Get Variable Value
        This will get the value of a variable from the symbol tree and return the value
        if the variable exists or an error if it doesn't
        args:
            name (string)  : The name which we will search for in symbol tree
        returns:
            value (string) : The value of the variable if it is found
            error (bool)   : Sends back False if it was not found
        """

        for var in self.symbol_tree:
            if var[0] == name:
                return var[1]
        return False

    def form_value_list(self, tokens):
        value_list = []
        tokens_checked = 0
        for token in tokens:
            if token[0] == "STATEMENT_END":
                break
            try:
                value_list.append(int(token[1]))
            except:
                value_list.append(token[1])
            tokens_checked += 1

        return [value_list, tokens_checked]

    def send_error_message(self, msg, error_list):
        """ Send Error Messages
        This will simply send all the found error messages within the source code
        and return a list of error messages and tokens of which part of the source code
        caused that error
        args:
            error_list (list) : List with error message and tokens
        """

        print("------------------------ ERROR FOUND ----------------------------")
        print(" " + msg)
        print('\033[91m', "".join(str(r) for v in error_list for r in (v[1] + " ")), '\033[0m')
        print("-----------------------------------------------------------------")
        quit()

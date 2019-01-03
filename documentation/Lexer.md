# Lexical Analyzer

Lexical Analyzer is the first phase of a compilier. It takes the modified source
written in the form of sentences and breaks them down into tokens.

# Tokens

| Type          | Token                       | Reference                       |
|---------------|-----------------------------|---------------------------------|
| identifier    | ["IDENTIFIER", "if"]        | [Identifiers](#Identifiers)     |
| string        | ["STRING". '"Emmanuel"'] | [Strings](#strings)             |
| datatype      | ["DATATYPE", "str"]         | [Data Types](#Data-Types)       |
| operator      | ["OPERATOR", "+"]           | [Operators](#Operators)         |
| integer       | ["INTEGER", "12"]           | [Integers](#Integers)           |
| statement_end | ["STATEMENT_END", ";"]      | [End Statement](#end-statements)|
| comparison_operator | ["COMPARISON_OPERATOR", "=="] | [Comparison Operators](#comparison-operators) |
| scope_definer | ["SCOPE_DEFINER", "{"]      | [Scope Definer](#scope-definer) |

# Data Types
The current state of Fluffy is in its growing stage. It has simple data types, like string and integer.
But as I continue to learn, I am hoping to add more data types like list and arrays.

    DATATYPE = ['bool', 'str', 'int'] <--- current
    DATATYPE = ['bool', 'int', 'str', 'arr', 'list', 'float', and more] <-- Goal

The way the tokens are created is that first it reads from the file and uses the split the file to 
one line using python's command `string.split()`. With that each word is on one line and it is easy 
to put them in their respective datatype which ends up like this:
    
    ['DATATYPE', 'int']
   
There is a list of availble datatype located at [constants.py](https://github.com/emmaunel/Fluffy_Language/blob/master/v2/src/constants.py)  And what I do is loop through that list and if 
a string in the source file is in that list, it creates the tokens as showed above.

    if word in constants.DATATYPE:
        tokens.append(['DATATYPE', word])
        
# Identifiers

There are few keywords at the moment. It will hopefully become more robust in the future

    KEYWORDS = ["fun", "class", "if", "else", "for", "true", "false", "null", "print", "bool", "int", "str", "exit"]

It works the same way the data types tokens are made.

    if word in constants.KEYWORD:
        tokens.append(["IDENTIFIER", word])
    
    ["IDENTIFIER", 'for']
    
# Operators

Similar technique used in Identifiers and Data type were implemented but I didn't use a list of 
operators like I did before. I created a string which contains the operations `*-/+%` to manage memory 
use. When it checks if a word is a operator, it returns

    ['OPERATOR', '+']
    
The current operators:

- `*` multiplication
- `-` subtractions
- `/` division
- `+` addition
- `%` modulus

The token generator code is shown below:

    if word in '*-/+%':
        tokens.append(['OPERATOR', word])
        
# Comparison & Binary Operators

> TO BE UPDATED

# Integer

I used regex expression which made finding tokens with integers easy. However, it sometimes return two type
of integer like `43` and `43;` which required me to check if the last index of the number has `;`. This was how
it was done:

    elif re.match("[0-9]", word):
        if word[len(word) - 1] == ';': 
            tokens.append(["INTEGER", word[:-1]])
        else: 
            tokens.append(["INTEGER", word])  

    
This if statement dosn't ignore the `;` totally. Later in the loop, there is a check of `;` which is added 
as a `STATEMENT_END` token. So at the end, if a number like `21;`, it will return this:

    ["INTEGER", 21], ["STATEMENT_END", ';'], 

    
# Scope Definer

The scope definer are `{` and `}` just like in java. They are used to identify function, conditionals and loops.
The token generated is:

    ['SCOPE_DEFINER', '{']
    
It is done like this:

    if word in "{}":
        tokens.append(['SCOPE_DEFINER', word])
        

# Strings

### Implementation of string token analysis

The following code snippet is a call to the getMatcher method to get the string and return it but what this snippet does extra is check the return to see how to behave.

      # Identify any strings which are surrounded in  ""
      elif ('"') in word: 

          # Call the getMatcher() method to get the full string
          matcherReturn = self.getMatcher('"', source_index, source_code)

          # If the string was in one source code item then we can just append it
          if matcherReturn[1] == '': tokens.append("[STRING " + matcherReturn[0] + "]")

          # If the string was spread out across multiple source code item
          else:

              # Append the string token
              tokens.append("[STRING " + matcherReturn[0] + "]")
                    
              # Check for a semicolon at the end of thee string and if there is one then add end statament
              if ';' in matcherReturn[1]: tokens.append("[STATEMENT_END ;]")

              # Skip all the already checked string items so there are no duplicates
              source_index += matcherReturn[2]

              # Skip every other check and loop again
              pass


Strings however are a bit more difficult to parse as in some cases you will need to look through multiple source code items to find a whole string, for example:

`['"Ryan'], ['is'], ['coding'], ['something"']`

`--^---------------------------------------^--`

This shows where the string begins and then ends and illustrates that the closing quote will not be in the same item so a simple regular expression wouldn't be able to find the string. Therefore, I created a new function `getMatcher()` which is shown below.

----
> ### GetMatcher(matcher, current_index, source_code)
What this function will do is loop from current source code index where the first quote was found and iterate through the rest of the source code until it finds the closing quote.

**`Arguments`** the arguments are:
- `matcher` this is the quote we found or in other cases a `(` or `{`.
- `current_index` is the index at which we found the character we need to find a matcher for.
- `source_code` is the source code we are looping through to find matcher.

**`return`** this will return:
- The full string
- Number of indexes at which second matcher was found at. This is used to skip all the checked indexes and not have to rechecks them.
- The symbol at the end of string

**`Source code`**:

    def getMatcher(self, matcher, current_index, source_code):

        # Check if matcher is in the same source_code item
        if source_code[current_index].count('"') == 2:

            # this will partition the string and return a tuple like this
            # ('word', '"', ';')
            word = source_code[current_index].partition('"')[-1].partition('"'[0])

            # This will return the string and any extra characters such as end statement
            if word[2] != '': return [ '"' + word[0] + '"', '', word[2] ]

            # This will return just the string and empty fields that represent `undefined` or `nil`
            else:  return [ '"' + word[0] + '"', '', '' ]
        
        else:

            # Cut off the parts of the source code behind the matcher
            source_code = source_code[current_index:len(source_code)]

            # This will keep track of the string as it is being built up
            word = ""

            # This will keep count of the interations
            iter_count = 0

            # This will loop through the source code to find each part of the string and matcher
            for item in source_code:

                # Increment the iteration count every iteration
                iter_count += 1

                # Append the word that has been found to the string
                word += item + " "

                # If the word has the matcher in it and it is not the first matcher
                if matcher in item and iter_count != 1: 

                    # return the whole string, iteration count and extra characters like a statement end
                    return [
                        '"' + word.partition('"')[-1].partition('"'[0])[0] + '"', # The string
                        word.partition('"')[-1].partition('"'[0])[2], # The extra character
                        iter_count - 1
                    ]

                    # Break out the loop as the whole string was found
                    break
                  
**`Things to fix`**:
This is not perfect and still has improvements that need to be done and some bugs are:

- In order to work quote has to be at the begining of the item like this `"Ryan` and not like this `("Ryan` or else it won't work.

- There can only be one character at the end of the matching quote item or else it will output invalid tokens for example:

  - `buzz"` would also be valid
  - `fizz";` would be a valid
  - `fizzbuzz";)` would be invalid

# End Statement

Creating a token for the semicolon was quite easy. For words like `"fizz";`, all I had to do was check if the last
index of that word has `;` at the end. I did like this:

# Checks for the end of a statement ';'
    if ";" in word[len(word) - 1]: 

        # Will hold the value of the last token which may have the end statemnt ';' still in it
        last_token = tokens[source_index - 1][1]

        # If there is an end statement still in that token then ...
        if last_token[len(last_token) - 1] == ';':

            # ... We remove the end_statement ';' from the token ...
            new = last_token[:len(last_token) - 1] + '' + last_token[len(last_token):]

            # ... and then we simply add the new made token to the place of the old one which had the end_statement ';'
            tokens[len(tokens) - 1][1] = new
                
        # Append the statement end token as a end stataemtn was found
        tokens.append(["STATEMENT_END", ";"])
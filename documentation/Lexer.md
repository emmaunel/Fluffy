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

    
> TO BE CONTINUED

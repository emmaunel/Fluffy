# **Parser**

---

## Class Parser

The parser will handle all the syntactic and semantical
analysis of the the parsing for the code. It will also
raise errors when syntax errors are found.

### Parser class initializer:

- `source_ast`
    
    This will initially hold a dictionary with keys
    of `main_scopte` with the value of an empty array 
    where all the source code AST structures will
    be appended to. This will be used in order to be 
    interpreted and compiled.
    The variable will look like this: 
    `{'main_scope': []}`.
    
- `symbol_tree`

    This will be used in order to store variables with 
    their name and value in the following format
    `['name', 'value']` so that I can perform 
    semantic analysis and perform checks to see
    if a variable exists or not.
    
-  `token_stream`

    This will be hold the tokens that have just
    been produced by the lexical analyser which
    the parser will use to turn into an Abstract
    Syntax Tree(AST) and Symbol Trees so that syntactic
    and semantic analysis can be performed.
    
- `error_messages`
    
    This will hold all the error messages that happened
    during the parsing and print them all out
    at the end of the source code parsing if there 
    are any.
    
- `token_index`
    
    This holds the index of the tokens which we 
    have checked globally so that we can keep track
    of the tokens we have checked.
    
---

## `parse()`

This will parse the tokens given as argument and turn
the sequence of tokens into abstract syntax trees.

**Arguments**

- `token_stream (list)`
    - The tokens produced by lexer.
    
**Returns**

- `source_ast (dict)`
    - This will return the full source code ast
    
This method tries to idntify a patter of tokens that
 make up a pasre tree for example a variable would
 be recognixed if the parse method stumbled across
 a datatype toke (`['DATATYPE', 'str']`),
    
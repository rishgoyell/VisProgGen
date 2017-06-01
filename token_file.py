'''
This file contains the definitions of tokens required
to tokenize the program
'''
import ply.lex as lex
def build_lexer(debug_mode=True, optimize_mode=False):

    tokens = [
        'IDENTIFIER',
        'UNION',
        'INTERSECTION',
        'DIFFERENCE',
        'INTEGER'
    ]

    literals = "(),"

    # t_token = value
    def t_UNION(t):
        r'\+'
        return t

    def t_INTERSECTION(t):
        r'\*'
        return t

    def t_DIFFERENCE(t):
        r'-'
        return t

    def t_IDENTIFIER(t):
        r'c|t|s'
        return t

    def t_INTEGER(t):
        r'[0-9](_?[0-9]+)*([Ee](\+)?[0-9](_?[0-9]+)*)?'
        t.value = int(float(t.value.replace("_","")))
        return t

    '''
    The following rule are taken form ply tutorial for easier debugging.
    source : http://www.dabeaz.com/ply/ply.html#ply_nn4
    '''
    # Define a rule so we can track line numbers
    def t_newline(t):
        r'\n'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'
    t_ignore_COMMENT = r'%.*'
    # Error handling rule
    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    if debug_mode:
        return [tokens, lex.lex(debug=1)]
    elif optimize_mode:
        return [tokens, lex.lex(optimize=1)]    # disables error checking
    else:
        return [tokens, lex.lex()]

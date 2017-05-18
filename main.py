#i!/usr/bin/env python

import ply.yacc as yacc
import ply.lex as lex
from grammar import Rules

#pydot_error_chars = ',#:@'

class Ada_Parser(Rules):
    def __init__(self):
        from token_file import build_lexer
        self.tokens, self.lexer = build_lexer(debug_mode=False)
        self.parser = yacc.yacc(module=self)

        self.successful = True

    def process(self, filename):
        assert type(filename) is str
        try:
            with open(filename, 'rb') as fp:
                data = fp.read()
                print(str(data)[2:-1])
                self.parser.parse(str(data)[2:-1])
                if self.successful:
                    print('Parsing successful for file ' + filename)
                else:
                    print('Could not parse ' + filename + ' successfully')
        except IOError:
            print("Unable to find " + filename)

if __name__ == '__main__':
    import sys
    p1 = Ada_Parser()
    assert len(sys.argv) > 1
    for i in range(1, len(sys.argv)):
        p1.successful = True
        p1.process(sys.argv[i])

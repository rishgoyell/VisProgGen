#i!/usr/bin/env python

import ply.yacc as yacc
import os
import ply.lex as lex
from grammar import Rules
import genexp

#pydot_error_chars = ',#:@'

numexs = 50
numops = 1

class Parser(Rules):
    global numexs
    def __init__(self):
        from token_file import build_lexer
        self.tokens, self.lexer = build_lexer(debug_mode=False)
        self.parser = yacc.yacc(module=self)
        self.successful = True  #set to True as long as parsing is proceeding correctly

    def processFile(self, filename):
        assert type(filename) is str
        try:
            with open(filename, 'rb') as fp:
                exp = fp.read()
                print(str(exp)[2:-1])
                Rules.random = 0
                Rules.exp = str(exp)[2:-1]  #some feature of python 3.6, introduces b in front of string for some reason
                self.parser.parse(Rules.exp)
                os.remove("expressions.txt") #remove empty expressions file
                if self.successful:
                    print('Parsing successful for file' + filename + ': Output stored in genImage.png')
                else:
                    print('Could not parse ' + filename + ' successfully')
        except IOError:
            print("Unable to find " + filename)

    def processExp(self, exp):
        if Parser.numgen == numexs:
            Rules.filename.close()
            return 0
        else:
            Rules.exp = exp
            self.parser.parse(exp)
            if not self.successful:
                print('Could not parse' + exp + 'successfully')
            return 1



if __name__ == '__main__':
    import sys
    p1 = Parser()
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            p1.successful = True
            p1.processFile(sys.argv[i])
    else:
        flag = 1
        while flag:
            p1.successful = True
            exp = genexp.fixedSizeExp(numops)
            flag = p1.processExp(exp)
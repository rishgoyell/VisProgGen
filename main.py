#i!/usr/bin/env python

import ply.yacc as yacc
import os, re
import ply.lex as lex
from grammar import Rules
import genexp
import pydot
from canvasops import canvas

#pydot_error_chars = ',#:@'

numexs = 50000
numops = 1
opcolor = {'+': 'yellow', '-': 'red', '*':'blue'}

class Parser(Rules):
    global numexs
    def __init__(self):
        from token_file import build_lexer
        self.tokens, self.lexer = build_lexer(debug_mode=False)
        self.parser = yacc.yacc(module=self)
        self.successful = True  #set to True as long as parsing is proceeding correctly
        self.graph = pydot.Dot(graph_type='digraph', bgcolor='#1e5e68')
        self.nnodes = 0
        self.numdraws = 0


    def processFile(self, filename):
        assert type(filename) is str
        try:
            with open(filename, 'rb') as fp:
                exp = fp.read()
                print(str(exp)[2:-1])
                Rules.random = 0
                Rules.exp = str(exp)[2:-1]  #some feature of python 3.6, introduces b in front of string for some reason
                self.parser.parse(Rules.exp)
                if self.successful:
                    print('Parsing successful for file ' + filename)
                    if Rules.visualize:
                        self.plot_parse_tree(filename)      #save the visualization graph
                        #remove unwanted intermediate canvases
                        for f in os.listdir(Rules.path):
                            if re.search(r'temp[0-9]+', f):
                                os.remove(os.path.join(Rules.path, f))

                else:
                    print('Could not parse ' + filename + ' successfully')
        except IOError:
            print("Unable to find " + filename)

    def processExp(self, exp):
        #end if num of generated samples equals num of required samples
        if Parser.numgen == numexs:
            Rules.filename.close()
            return 0
        else:
            self.numdraws = 0   #keeps track of number of operations, including draws
            Rules.exp = exp
            self.parser.parse(exp)
            if not self.successful:
                print('Could not parse' + exp + 'successfully')
            elif Rules.visualize:
                self.plot_parse_tree('visual'+str(Rules.numgen)+'.png')
            return 1


    def makenode(self, p):
        global numdraws
        global opcolor
        '''
        p : stack
        returns root node
        '''
        parent_id = self.get_unique_id()

        tempimage = Rules.path + 'temp' + str(self.numdraws)
        p[0].save(tempimage, 0)
        self.numdraws = self.numdraws+1

        if len(p) == 4:
            parent = pydot.Node(parent_id, style="filled", fillcolor=opcolor[p[3]], shape='square', image=tempimage+'.png', fontcolor='transparent')
            self.graph.add_node(parent)
            self.graph.add_edge(pydot.Edge(parent_id, p[1].nodeID, fontcolor=opcolor[p[3]], label=p[3]))
            self.graph.add_edge(pydot.Edge(parent_id, p[2].nodeID))
        else:
            parent = pydot.Node(parent_id, style="filled", fontcolor='transparent', shape='square', image=tempimage+'.png')
            self.graph.add_node(parent)
        p[0].nodeID = parent_id


    def plot_parse_tree(self, filename):
        # self.graph.write_dot(filename + '.dot')
        self.graph.write_ps(filename + '.ps')

    def get_unique_id(self):
        self.nnodes += 1
        return 'NODE' + str(self.nnodes)



if __name__ == '__main__':
    import sys
    p1 = Parser()
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            p1.successful = True
            p1.processFile(sys.argv[i])
    else:
        flag = 1
        Rules.visualize = False
        while flag:
            p1.successful = True
            exp = genexp.fixedSizeExp(numops)
            flag = p1.processExp(exp)
